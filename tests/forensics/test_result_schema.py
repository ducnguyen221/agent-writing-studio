import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]


class ResultSchemaTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(
            (ROOT / "skills/05-forensics/assets/result.schema.json").read_text(encoding="utf-8")
        )
        self.validator = Draft202012Validator(self.schema["$defs"]["finding"])
        self.bundle_validator = Draft202012Validator(self.schema)

    def valid_finding(self):
        return {
            "id": "F01",
            "rule_id": "G2-EMPTY-CLAIM",
            "group": "G2",
            "tier": "agent",
            "stability": "unstable",
            "location": {
                "section": "2.1",
                "paragraph_index": 4,
                "sentence_id": "s0042",
                "quote_anchor": "Trong bối cảnh chuyển đổi số",
            },
            "quoted_text": "Trong bối cảnh chuyển đổi số, AI đóng vai trò quan trọng.",
            "severity": "medium",
            "evidence": "Câu thiếu chủ thể và không có dữ kiện kiểm chứng.",
            "counterevidence": "Có thể là câu mở đoạn theo văn nghị luận.",
            "suggested_fix": "Nêu đơn vị, hành động và kết quả cụ thể.",
            "verification_question": "Đơn vị nào đã làm việc gì và đo kết quả ra sao?",
            "genre_basis": "essay",
        }

    def test_complete_finding_is_valid(self):
        self.assertEqual(list(self.validator.iter_errors(self.valid_finding())), [])

    def test_missing_counterevidence_is_invalid(self):
        finding = self.valid_finding()
        finding.pop("counterevidence")
        self.assertTrue(list(self.validator.iter_errors(finding)))

    def test_high_agent_finding_requires_verification_question(self):
        finding = self.valid_finding()
        finding["severity"] = "high"
        finding["verification_question"] = ""
        self.assertTrue(list(self.validator.iter_errors(finding)))

    def valid_bundle(self):
        return {
            "schema_version": "2.0",
            "run": {
                "created_at": "2026-08-30T10:00:00+07:00",
                "skill_version": "2.0",
                "measurement_mode": "agent_read",
                "branches": {
                    "blind_agent": {"model": "agent", "sealed_before_counters": True},
                    "deterministic": {},
                },
            },
            "document": {"sha256": "a" * 64, "language": "vi", "genre": "essay"},
            "verdict": {
                "review_priority": 64,
                "review_priority_range": {"low": 39, "high": 89, "calibrated": False},
                "ai_signal_coverage": {
                    "percent": 13,
                    "low": 3,
                    "high": 23,
                    "flag_count": 4,
                    "note_count": 5,
                    "eligible_sentence_count": 46,
                    "formula": "100 * (FLAG + 0.4 * NOTE) / eligible_sentences",
                },
                "label": "priority_check",
                "confidence": "low",
                "limitations": ["Chưa hiệu chỉnh cùng thể loại."],
            },
            "findings": [self.valid_finding()],
            "sentences": [],
        }

    def test_complete_bundle_is_valid(self):
        self.assertEqual(list(self.bundle_validator.iter_errors(self.valid_bundle())), [])

    def test_insufficient_evidence_bundle_allows_zero_eligible_sentences(self):
        bundle = self.valid_bundle()
        bundle["verdict"]["label"] = "insufficient_evidence"
        bundle["verdict"]["ai_signal_coverage"].update(
            {"percent": 0, "low": 0, "high": 0, "flag_count": 0, "note_count": 0,
             "eligible_sentence_count": 0}
        )
        bundle["findings"] = []
        self.assertEqual(list(self.bundle_validator.iter_errors(bundle)), [])

    def test_insufficient_evidence_rejects_findings(self):
        bundle = self.valid_bundle()
        bundle["verdict"]["label"] = "insufficient_evidence"
        self.assertTrue(list(self.bundle_validator.iter_errors(bundle)))

    def test_bundle_requires_score_range(self):
        bundle = self.valid_bundle()
        bundle["verdict"].pop("review_priority_range")
        self.assertTrue(list(self.bundle_validator.iter_errors(bundle)))

    def test_group_scores_use_canonical_keys_and_caps(self):
        bundle = self.valid_bundle()
        bundle["verdict"]["group_scores"] = {"G1": 30, "G2": 20, "G3": 25, "G4": 25}
        self.assertEqual(list(self.bundle_validator.iter_errors(bundle)), [])
        bundle["verdict"]["group_scores"]["G1"] = 31
        self.assertTrue(list(self.bundle_validator.iter_errors(bundle)))

    def test_verified_fabrication_requires_human_check(self):
        bundle = self.valid_bundle()
        bundle["citations"] = [{"raw": "Nguồn X", "status": "verified_fabrication"}]
        self.assertTrue(list(self.bundle_validator.iter_errors(bundle)))
        bundle["citations"][0]["checked_by_human"] = True
        self.assertEqual(list(self.bundle_validator.iter_errors(bundle)), [])


if __name__ == "__main__":
    unittest.main()
