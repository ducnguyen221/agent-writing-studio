#!/usr/bin/env python3
"""Render a Vietnamese forensic review report from evidence JSON.

The renderer does not detect AI writing. It only presents evidence already
created by the agent-led reading workflow.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError as error:  # pragma: no cover - depends on optional script environment
    raise RuntimeError(
        "report.py cần jsonschema; cài requirements-dev.txt trước khi dùng renderer tùy chọn."
    ) from error


BANDS = [
    (60, "🔴 ƯU TIÊN KIỂM TRA"),
    (30, "🟡 NÊN XEM TRONG NGỮ CẢNH"),
    (0, "⚪ ÍT DẤU HIỆU"),
]
SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
REQUIRED_VERDICT_FIELDS = {
    "review_priority",
    "review_priority_range",
    "ai_signal_coverage",
    "label",
    "confidence",
    "limitations",
}
REQUIRED_FINDING_FIELDS = {
    "id",
    "rule_id",
    "group",
    "tier",
    "stability",
    "location",
    "quoted_text",
    "severity",
    "evidence",
    "counterevidence",
    "suggested_fix",
    "verification_question",
    "genre_basis",
}
REQUIRED_LOCATION_FIELDS = {"section", "paragraph_index", "sentence_id", "quote_anchor"}


def band(score: float) -> str:
    for lower_bound, label in BANDS:
        if score >= lower_bound:
            return label
    return BANDS[-1][1]


def _escape_markdown(value: Any) -> str:
    text = str(value)
    text = text.replace("\\", "\\\\")
    for character in ("`", "*", "_", "[", "]", "(", ")", "<", ">", "#", "!", "|"):
        text = text.replace(character, "\\" + character)
    return text


def _inline(value: Any) -> str:
    return re.sub(r"\s+", " ", _escape_markdown(value)).strip()


def _blockquote(value: Any) -> str:
    lines = str(value).splitlines() or [""]
    return "\n".join("> " + _escape_markdown(line) for line in lines)


def _range_text(value_range: dict[str, Any] | None) -> str:
    if not value_range:
        return "chưa cung cấp khoảng"
    status = "đã hiệu chỉnh" if value_range.get("calibrated") else "chưa hiệu chỉnh"
    return (
        f"{_inline(value_range.get('low', '?'))}–{_inline(value_range.get('high', '?'))}, "
        f"{_inline(status)}"
    )


RESULT_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "assets" / "result.schema.json"
RESULT_SCHEMA = json.loads(RESULT_SCHEMA_PATH.read_text(encoding="utf-8"))
RESULT_VALIDATOR = Draft202012Validator(RESULT_SCHEMA)


def _validate_render_contract(evidence: dict[str, Any]) -> None:
    verdict = evidence.get("verdict") or {}
    if verdict.get("label") == "insufficient_evidence" and evidence.get("findings"):
        raise SystemExit("TỪ CHỐI RENDER: insufficient_evidence không được đi kèm findings.")
    schema_errors = sorted(
        RESULT_VALIDATOR.iter_errors(evidence),
        key=lambda error: [str(part) for part in error.absolute_path],
    )
    if schema_errors:
        error = schema_errors[0]
        path = ".".join(str(part) for part in error.absolute_path) or "$"
        raise SystemExit(f"TỪ CHỐI RENDER: schema lỗi tại {path}: {error.message}")
    missing_verdict = sorted(REQUIRED_VERDICT_FIELDS - verdict.keys())
    if missing_verdict:
        raise SystemExit(
            "TỪ CHỐI RENDER: thiếu verdict fields: " + ", ".join(missing_verdict)
        )
    if not verdict.get("limitations"):
        raise SystemExit(
            "TỪ CHỐI RENDER: verdict.limitations rỗng. "
            "Báo cáo không nêu giới hạn là báo cáo gây hiểu nhầm."
        )
    for index, finding in enumerate(evidence.get("findings") or [], start=1):
        missing = sorted(REQUIRED_FINDING_FIELDS - finding.keys())
        if missing:
            raise SystemExit(
                f"TỪ CHỐI RENDER: finding {index} thiếu fields: " + ", ".join(missing)
            )
        empty = [
            field
            for field in REQUIRED_FINDING_FIELDS - {"location"}
            if finding.get(field) in (None, "")
        ]
        if empty:
            raise SystemExit(
                f"TỪ CHỐI RENDER: finding {index} có field rỗng: " + ", ".join(sorted(empty))
            )
        location = finding.get("location") or {}
        missing_location = sorted(REQUIRED_LOCATION_FIELDS - location.keys())
        if missing_location:
            raise SystemExit(
                f"TỪ CHỐI RENDER: finding {index} thiếu location fields: "
                + ", ".join(missing_location)
            )


def _render_finding(lines: list[str], finding: dict[str, Any]) -> None:
    location = finding.get("location", {})
    section = location.get("section", "?")
    paragraph = location.get("paragraph_index", "?")
    lines.append(
        f"### {_inline(finding.get('id', '?'))} · §{_inline(section)} · đoạn {_inline(paragraph)} · "
        f"{_inline(finding.get('group', '?'))} · `{_inline(finding.get('severity', '?'))}`\n"
    )
    lines.append(_blockquote(finding.get("quoted_text", "")) + "\n")
    lines.append(f"- **Dấu hiệu:** {_inline(finding.get('evidence', ''))}")
    lines.append(f"- **Phản chứng:** {_inline(finding.get('counterevidence', ''))}")
    lines.append(f"- **Cách sửa:** {_inline(finding.get('suggested_fix', ''))}")
    lines.append(f"- **Câu hỏi xác minh:** {_inline(finding.get('verification_question', ''))}")
    lines.append(
        f"- **Cơ sở thể loại:** `{_inline(finding.get('genre_basis', '?'))}` · "
        f"rule `{_inline(finding.get('rule_id', '?'))}` · {_inline(finding.get('tier', '?'))}/"
        f"{_inline(finding.get('stability', '?'))}\n"
    )


def render(evidence: dict[str, Any]) -> str:
    _validate_render_contract(evidence)
    verdict = evidence["verdict"]
    limitations = verdict.get("limitations")

    document = evidence["document"]
    lines: list[str] = []
    add = lines.append
    score = verdict["review_priority"]

    add("# Báo cáo rà soát dấu hiệu AI trong văn bản\n")
    add(
        "> **Đây không phải kết luận về tác giả và không phải xác suất AI.** "
        "Các chỉ số chỉ giúp xếp thứ tự phần cần đọc lại, hỏi nguồn hoặc vấn đáp.\n"
    )
    add(
        f"- **Tài liệu:** `{_inline(str(document.get('sha256', '?'))[:16])}…` · "
        f"thể loại `{_inline(document.get('genre', '?'))}` · "
        f"ngôn ngữ `{_inline(document.get('language', '?'))}`"
        + (" · ⚠️ OCR" if document.get("ocr") else "")
    )
    add(f"- **S — điểm dấu hiệu:** **{_inline(score)}/100** — {_inline(band(score))}")
    add(f"- **Khoảng S:** {_range_text(verdict.get('review_priority_range'))}")

    coverage = verdict.get("ai_signal_coverage") or {}
    if coverage:
        add(
            f"- **C — độ phủ dấu hiệu:** **{_inline(coverage.get('percent', '?'))}%** "
            f"(khoảng {_inline(coverage.get('low', '?'))}–"
            f"{_inline(coverage.get('high', '?'))}%)"
        )
        add(
            f"- **Phép đếm C:** {_inline(coverage.get('flag_count', '?'))} FLAG + "
            f"0,4 × {_inline(coverage.get('note_count', '?'))} NOTE / "
            f"{_inline(coverage.get('eligible_sentence_count', '?'))} câu hợp lệ"
        )
    add(
        f"- **Nhãn:** `{_inline(verdict.get('label', '?'))}` · "
        f"**độ tin cậy:** `{_inline(verdict.get('confidence', '?'))}`\n"
    )

    if verdict.get("label") == "insufficient_evidence":
        add("## Dừng đánh giá\n")
        add("Không đủ cơ sở để tạo nhận định. Xem lý do ở mục Giới hạn.\n")
        add("## Giới hạn của báo cáo\n")
        for limitation in limitations:
            add(f"- {_inline(limitation)}")
        return "\n".join(lines)

    group_scores = verdict.get("group_scores") or {}
    if group_scores:
        add("## Điểm theo nhóm\n")
        add("| Nhóm | Điểm sau trần |")
        add("|---|---:|")
        for group, group_score in group_scores.items():
            add(f"| {_inline(group)} | {_inline(group_score)} |")
        add("")

    findings = sorted(
        evidence.get("findings") or [],
        key=lambda item: (
            SEVERITY_ORDER.get(item.get("severity"), 9),
            item.get("location", {}).get("paragraph_index", 10**9),
        ),
    )
    add(f"## Findings cần xem lại ({len(findings)})\n")
    if not findings:
        add("_Không có finding đủ hợp đồng bằng chứng._\n")
    for finding in findings:
        _render_finding(lines, finding)

    if findings:
        add("## Dấu hiệu ngược lại cần giữ trong quyết định\n")
        for finding in findings:
            add(
                f"- `{_inline(finding.get('id', '?'))}`: "
                f"{_inline(finding.get('counterevidence', ''))}"
            )
        add("")

        questions = [item.get("verification_question") for item in findings]
        questions = [question for question in questions if question][:5]
        add("## Câu hỏi trao đổi với tác giả\n")
        for question in questions:
            add(f"- {_inline(question)}")
        add("")

    if evidence.get("unsourced_numbers"):
        add("## Con số chưa có nguồn\n")
        add("Đề nghị tác giả trưng nguồn; đây là bước xác minh, không phải cáo buộc.\n")
        for item in evidence["unsourced_numbers"][:25]:
            add(
                f"- `{_inline(item.get('value', ''))}` tại "
                f"`{_inline(item.get('sentence_id', ''))}`: {_inline(item.get('context', ''))}"
            )
        add("")

    add("## Giới hạn của báo cáo\n")
    for limitation in limitations:
        add(f"- {_inline(limitation)}")
    add("\n---\n")
    add(
        "*Không dùng báo cáo này làm căn cứ kỷ luật độc lập. Bước tiếp theo phù hợp là "
        "đọc lại trong ngữ cảnh, xin nguồn/bản nháp và trao đổi với tác giả.*"
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence")
    parser.add_argument("--out", default="-")
    args = parser.parse_args()
    path = Path(args.evidence)
    if path.is_dir():
        path = path / "evidence.json"
    evidence = json.loads(path.read_text(encoding="utf-8"))
    markdown = render(evidence)
    if args.out == "-":
        sys.stdout.reconfigure(encoding="utf-8")
        print(markdown)
    else:
        Path(args.out).write_text(markdown, encoding="utf-8")
        print(f"-> {args.out}")


if __name__ == "__main__":
    main()
