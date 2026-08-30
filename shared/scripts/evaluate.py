"""Aggregate-only evaluation for the forensic skill suite.

Input records contain labels, rule IDs, and optional numeric spans. Source text
is intentionally rejected so evaluation artifacts can be stored without leaking
documents used as fixtures.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any


FORBIDDEN_SOURCE_FIELDS = {
    "text",
    "content",
    "quote",
    "quoted_text",
    "raw_text",
    "source_text",
    "context",
}
ALLOWED_RECORD_FIELDS = {
    "fixture_id",
    "language",
    "genre",
    "truth",
    "label",
    "predicted_rule_ids",
    "supported_rule_ids",
    "expected_spans",
    "predicted_spans",
    "abstained",
}
RULE_REGISTRY_PATH = Path(__file__).resolve().parents[1] / "rules/forensic-rule-registry.json"
ALLOWED_RULE_IDS = frozenset(
    json.loads(RULE_REGISTRY_PATH.read_text(encoding="utf-8"))["rule_ids"]
)
ALLOWED_LABELS = {
    "low_signal",
    "worth_reviewing",
    "priority_check",
    "insufficient_evidence",
    "verified_fabrication",
}


def _reject_source_text(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_SOURCE_FIELDS:
                raise ValueError(f"Không nhận văn bản nguồn trong trường {key!r}.")
            _reject_source_text(child)
    elif isinstance(value, list):
        for child in value:
            _reject_source_text(child)


def _wilson(errors: int, total: int, z: float = 1.959963984540054) -> list[float] | None:
    if total == 0:
        return None
    proportion = errors / total
    z_squared = z * z
    denominator = 1 + z_squared / total
    center = (proportion + z_squared / (2 * total)) / denominator
    margin = (
        z
        * math.sqrt(
            proportion * (1 - proportion) / total + z_squared / (4 * total * total)
        )
        / denominator
    )
    return [round(max(0, center - margin), 4), round(min(1, center + margin), 4)]


def _merge_spans(spans: Iterable[Iterable[int]]) -> list[tuple[int, int]]:
    normalized = sorted((int(start), int(end)) for start, end in spans if int(end) > int(start))
    merged: list[tuple[int, int]] = []
    for start, end in normalized:
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
        else:
            old_start, old_end = merged[-1]
            merged[-1] = (old_start, max(old_end, end))
    return merged


def _span_iou(expected: Iterable[Iterable[int]], predicted: Iterable[Iterable[int]]) -> float:
    expected_ranges = _merge_spans(expected)
    predicted_ranges = _merge_spans(predicted)
    expected_size = sum(end - start for start, end in expected_ranges)
    predicted_size = sum(end - start for start, end in predicted_ranges)
    intersection = 0
    for expected_start, expected_end in expected_ranges:
        for predicted_start, predicted_end in predicted_ranges:
            intersection += max(
                0, min(expected_end, predicted_end) - max(expected_start, predicted_start)
            )
    union = expected_size + predicted_size - intersection
    return intersection / union if union else 1.0


def _rate(hits: int, total: int) -> float | None:
    return round(hits / total, 4) if total else None


def _validate_spans(value: Any, field: str, record_index: int) -> None:
    if not isinstance(value, list):
        raise ValueError(f"Record {record_index}: {field} phải là danh sách [start, end].")
    for span_index, span in enumerate(value, start=1):
        valid_shape = isinstance(span, list) and len(span) == 2
        if not valid_shape:
            raise ValueError(
                f"Record {record_index}: {field}[{span_index}] phải có đúng start/end."
            )
        start, end = span
        if (
            not isinstance(start, int)
            or isinstance(start, bool)
            or not isinstance(end, int)
            or isinstance(end, bool)
            or start < 0
            or end <= start
        ):
            raise ValueError(
                f"Record {record_index}: {field}[{span_index}] phải là hai số nguyên "
                "không âm với end > start."
            )


def evaluate(records: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Return aggregate metrics without fixture IDs or document text."""

    rows = [dict(record) for record in records]
    _reject_source_text(rows)
    if not rows:
        raise ValueError("evaluate cần ít nhất một record thuộc một cohort language × genre.")

    allowed_truth = {"human", "ai", "mixed", "adversarial"}
    cohorts = set()
    for index, row in enumerate(rows, start=1):
        unknown_fields = sorted(set(row) - ALLOWED_RECORD_FIELDS)
        if unknown_fields:
            raise ValueError(f"Record {index} có fields không hỗ trợ: {', '.join(unknown_fields)}")
        language = row.get("language")
        genre = row.get("genre")
        if not isinstance(language, str) or not re.fullmatch(r"[a-z]{2,3}", language):
            raise ValueError(f"Record {index} thiếu language hợp lệ.")
        if not isinstance(genre, str) or not re.fullmatch(r"[a-z0-9_-]{1,40}", genre):
            raise ValueError(f"Record {index} thiếu genre hợp lệ.")
        cohorts.add((language, genre))
        if row.get("truth") not in allowed_truth:
            raise ValueError(f"truth không hợp lệ: {row.get('truth')!r}.")
        if row.get("label") not in ALLOWED_LABELS:
            raise ValueError(f"Record {index}: label không hợp lệ: {row.get('label')!r}.")
        if "abstained" in row and not isinstance(row["abstained"], bool):
            raise ValueError(f"Record {index}: abstained phải là boolean.")
        for field in ("predicted_rule_ids", "supported_rule_ids"):
            rule_ids = row.get(field, [])
            if not isinstance(rule_ids, list) or not all(isinstance(item, str) for item in rule_ids):
                raise ValueError(f"{field} phải là danh sách rule_id.")
            unknown_rule_ids = sorted(set(rule_ids) - ALLOWED_RULE_IDS)
            if unknown_rule_ids:
                raise ValueError(f"rule_id chưa đăng ký: {', '.join(unknown_rule_ids)}")
        for field in ("expected_spans", "predicted_spans"):
            if field in row:
                _validate_spans(row[field], field, index)
    if len(cohorts) > 1:
        raise ValueError("Mỗi lượt evaluate chỉ được chứa một cohort language × genre.")
    language, genre = next(iter(cohorts))

    human = [row for row in rows if row["truth"] == "human"]
    human_errors = sum(row.get("label") == "priority_check" for row in human)
    ai = [row for row in rows if row["truth"] == "ai"]
    ai_hits = sum(row.get("label") == "priority_check" for row in ai)

    predicted_by_rule: dict[str, int] = defaultdict(int)
    supported_by_rule: dict[str, int] = defaultdict(int)
    for row in rows:
        supported = set(row.get("supported_rule_ids", []))
        for rule_id in set(row.get("predicted_rule_ids", [])):
            predicted_by_rule[rule_id] += 1
            if rule_id in supported:
                supported_by_rule[rule_id] += 1

    rule_precision = {}
    for rule_id in sorted(predicted_by_rule):
        predicted = predicted_by_rule[rule_id]
        supported = supported_by_rule[rule_id]
        rule_precision[rule_id] = {
            "supported": supported,
            "predicted": predicted,
            "rate": _rate(supported, predicted),
        }

    mixed_ious = [
        _span_iou(row.get("expected_spans", []), row.get("predicted_spans", []))
        for row in rows
        if row["truth"] == "mixed" and "expected_spans" in row
    ]
    abstentions = sum(
        bool(row.get("abstained")) or row.get("label") == "insufficient_evidence"
        for row in rows
    )

    return {
        "cohort": {"language": language, "genre": genre},
        "human_priority_check_fpr": {
            "errors": human_errors,
            "total": len(human),
            "rate": _rate(human_errors, len(human)),
            "wilson_95": _wilson(human_errors, len(human)),
        },
        "ai_priority_check_recall": {
            "hits": ai_hits,
            "total": len(ai),
            "rate": _rate(ai_hits, len(ai)),
        },
        "rule_precision": rule_precision,
        "mixed_span_iou": {
            "samples": len(mixed_ious),
            "mean": round(sum(mixed_ious) / len(mixed_ious), 4) if mixed_ious else None,
        },
        "abstention": {
            "count": abstentions,
            "total": len(rows),
            "rate": _rate(abstentions, len(rows)),
        },
        "slices": {
            truth: sum(row["truth"] == truth for row in rows)
            for truth in ("human", "ai", "mixed", "adversarial")
        },
    }


def main() -> None:
    # FIX 30/08: JSON đầu ra chứa tiếng Việt → console cp1252 crash. Ép UTF-8 trong code, không nhờ env.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser()
    parser.add_argument("records", help="JSON array or JSONL without source text")
    parser.add_argument("--out", default="-")
    args = parser.parse_args()
    path = Path(args.records)
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        records = [json.loads(line) for line in raw.splitlines() if line.strip()]
    else:
        records = json.loads(raw)
    output = json.dumps(evaluate(records), ensure_ascii=False, indent=2, sort_keys=True)
    if args.out == "-":
        print(output)
    else:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"-> {args.out}")


if __name__ == "__main__":
    main()
