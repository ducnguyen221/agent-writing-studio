"""Deterministic support for sealed, agent-authored forensic readings.

This module never creates findings or classifies prose. It only applies the
published arithmetic after an agent has completed and sealed a blind reading.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any


def _clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def _label_for(score: int, bands: list[Mapping[str, Any]]) -> str:
    for band in bands:
        if band["minimum"] <= score <= band["maximum"]:
            return str(band["label"])
    raise ValueError(f"Không có dải nhãn cho điểm {score}.")


def score_evidence(
    reading: Mapping[str, Any],
    *,
    genre: str,
    rules: Mapping[str, Any],
    counters: Mapping[str, Any] | None = None,
    calibration: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Convert a sealed agent reading into S, C, ranges, and conflict checks.

    ``counters`` is reserved for optional deterministic observations. It is not
    allowed to alter sentence labels or create a finding.
    """

    if reading.get("sealed_before_counters") is not True:
        raise ValueError("Phải khóa bản đọc mù trước khi tính điểm hoặc xem số đếm.")
    if not genre:
        raise ValueError("Thể loại là đầu vào bắt buộc.")

    caps = rules["group_caps"]
    supplied_scores = reading.get("group_scores", {})
    group_scores: dict[str, float] = {}
    for group in ("G1", "G2", "G3", "G4"):
        value = supplied_scores.get(group, 0)
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"Điểm {group} phải là số không âm.")
        numeric_value = float(value)
        if not math.isfinite(numeric_value):
            raise ValueError(f"Điểm {group} phải là số hữu hạn.")
        if numeric_value < 0:
            raise ValueError(f"Điểm {group} phải là số không âm.")
        group_scores[group] = min(numeric_value, float(caps[group]))

    raw_score = sum(group_scores.values())
    if group_scores["G3"] == 0 and group_scores["G4"] == 0:
        raw_score *= float(rules["form_vocabulary_only_multiplier"])
    review_priority = int(round(_clamp(raw_score)))

    weights = rules["sentence_weights"]
    eligible_labels: list[str] = []
    for sentence in reading.get("sentences", []):
        label = sentence.get("label")
        if label == "SKIP":
            continue
        if label not in weights:
            raise ValueError(f"Nhãn câu không hợp lệ: {label!r}.")
        eligible_labels.append(label)

    flag_count = eligible_labels.count("FLAG")
    note_count = eligible_labels.count("NOTE")
    eligible_count = len(eligible_labels)

    limitations = list(reading.get("limitations", []))
    if not limitations:
        limitations.append("Chưa ghi giới hạn của lượt đánh giá.")

    if eligible_count == 0:
        return {
            "genre": genre,
            "review_priority": review_priority,
            "label": "insufficient_evidence",
            "group_scores": group_scores,
            "ai_signal_coverage": {
                "percent": 0.0,
                "low": 0.0,
                "high": 0.0,
                "flag_count": 0,
                "note_count": 0,
                "eligible_sentence_count": 0,
            },
            "review_priority_range": {
                "low": 0,
                "high": 100,
                "calibrated": False,
            },
            "conflict_checks": ["no_eligible_sentences"],
            "limitations": limitations + ["Không có câu hợp lệ để tính độ phủ."],
        }

    weighted_count = sum(float(weights[label]) for label in eligible_labels)
    coverage = round(100 * weighted_count / eligible_count, 1)

    if calibration is not None and not isinstance(calibration.get("calibrated"), bool):
        raise ValueError("calibration.calibrated phải là boolean.")
    calibrated = calibration is not None and calibration.get("calibrated") is True
    if calibrated:
        try:
            s_margin = float(calibration["review_priority_margin"])
            c_margin = float(calibration["coverage_margin"])
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Calibration đã bật phải có hai margin dạng số.") from error
        if not math.isfinite(s_margin) or not math.isfinite(c_margin):
            raise ValueError("Calibration margins phải là số hữu hạn.")
        if s_margin < 0 or c_margin < 0:
            raise ValueError("Calibration margins phải không âm.")
    else:
        margins = rules["uncalibrated_margin"]
        s_margin = float(margins["review_priority"])
        c_margin = float(margins["coverage_percent"])

    label = _label_for(review_priority, rules["label_bands"])
    thresholds = rules["conflict_thresholds"]
    conflict_checks: list[str] = []
    marked_ratio = (flag_count + note_count) / eligible_count
    if marked_ratio > thresholds["marked_sentence_ratio"]:
        conflict_checks.append("rubric_may_be_too_sensitive")
    if (
        review_priority >= thresholds["document_level_score"]
        and coverage < thresholds["document_level_coverage"]
    ):
        conflict_checks.append("document_level_signal")
    if (
        coverage >= thresholds["weak_distributed_coverage"]
        and review_priority < thresholds["weak_distributed_score"]
    ):
        conflict_checks.append("weak_distributed_signal")
        label = "low_signal"

    result = {
        "genre": genre,
        "review_priority": review_priority,
        "label": label,
        "group_scores": group_scores,
        "review_priority_range": {
            "low": int(_clamp(review_priority - s_margin)),
            "high": int(_clamp(review_priority + s_margin)),
            "calibrated": calibrated,
        },
        "ai_signal_coverage": {
            "percent": coverage,
            "low": round(_clamp(coverage - c_margin), 1),
            "high": round(_clamp(coverage + c_margin), 1),
            "flag_count": flag_count,
            "note_count": note_count,
            "eligible_sentence_count": eligible_count,
        },
        "conflict_checks": conflict_checks,
        "limitations": limitations,
    }
    if counters is not None:
        result["optional_counters_used"] = True
    return result
