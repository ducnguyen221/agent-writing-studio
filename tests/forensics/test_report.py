import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = ROOT / "skills/05-forensics/scripts/report.py"


def load_report_module():
    spec = importlib.util.spec_from_file_location("forensics_report", REPORT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_report_module()

    def evidence(self):
        return {
            "schema_version": "2.0",
            "run": {
                "created_at": "2026-08-30T00:00:00+07:00",
                "skill_version": "2.0",
                "measurement_mode": "agent_read",
                "branches": {
                    "blind_agent": {"model": "test", "sealed_before_counters": True},
                    "deterministic": {},
                },
            },
            "document": {"sha256": "a" * 64, "genre": "essay", "language": "vi"},
            "verdict": {
                "review_priority": 64,
                "review_priority_range": {"low": 39, "high": 89, "calibrated": False},
                "ai_signal_coverage": {
                    "percent": 13.0,
                    "low": 3.0,
                    "high": 23.0,
                    "flag_count": 4,
                    "note_count": 5,
                    "eligible_sentence_count": 46,
                },
                "label": "priority_check",
                "confidence": "low",
                "limitations": ["Chưa có corpus mốc cùng thể loại."],
            },
            "findings": [
                {
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
                    "evidence": "Câu thiếu chủ thể và dữ kiện kiểm chứng.",
                    "counterevidence": "Có thể là câu mở đoạn theo văn nghị luận.",
                    "suggested_fix": "Nêu đơn vị, hành động và kết quả cụ thể.",
                    "verification_question": "Đơn vị nào đã làm gì và đo kết quả ra sao?",
                    "genre_basis": "essay",
                }
            ],
            "sentences": [],
        }

    def test_renders_score_coverage_range_and_interpretation(self):
        rendered = self.module.render(self.evidence())
        self.assertIn("64/100", rendered)
        self.assertIn("39–89", rendered)
        self.assertIn("13.0%", rendered)
        self.assertIn("không phải xác suất", rendered.lower())

    def test_renders_located_finding_counterevidence_fix_and_question(self):
        rendered = self.module.render(self.evidence())
        self.assertIn("§2.1 · đoạn 4", rendered)
        self.assertIn("Phản chứng", rendered)
        self.assertIn("Có thể là câu mở đoạn", rendered)
        self.assertIn("Cách sửa", rendered)
        self.assertIn("Câu hỏi xác minh", rendered)

    def test_refuses_empty_limitations(self):
        evidence = self.evidence()
        evidence["verdict"]["limitations"] = []
        with self.assertRaises(SystemExit):
            self.module.render(evidence)

    def test_refuses_incomplete_finding(self):
        evidence = self.evidence()
        evidence["findings"][0].pop("counterevidence")
        with self.assertRaisesRegex(SystemExit, "counterevidence"):
            self.module.render(evidence)

    def test_refuses_score_without_range(self):
        evidence = self.evidence()
        evidence["verdict"].pop("review_priority_range")
        with self.assertRaisesRegex(SystemExit, "review_priority_range"):
            self.module.render(evidence)

    def test_refuses_findings_when_evidence_is_insufficient(self):
        evidence = self.evidence()
        evidence["verdict"]["label"] = "insufficient_evidence"
        with self.assertRaisesRegex(SystemExit, "insufficient_evidence"):
            self.module.render(evidence)

    def test_escapes_untrusted_markdown_in_report_fields(self):
        evidence = self.evidence()
        evidence["findings"][0]["quoted_text"] = "Câu đầu.\n# Tiêu đề giả\n![ảnh](https://invalid.example/x.png)"
        evidence["findings"][0]["evidence"] = "[Bấm vào đây](https://invalid.example)"
        rendered = self.module.render(evidence)
        self.assertNotIn("\n# Tiêu đề giả", rendered)
        self.assertNotIn("![ảnh]", rendered)
        self.assertIn("> \\# Tiêu đề giả", rendered)

    def test_refuses_schema_invalid_missing_confidence(self):
        evidence = self.evidence()
        evidence["verdict"].pop("confidence")
        with self.assertRaisesRegex(SystemExit, "confidence"):
            self.module.render(evidence)

    def test_refuses_verdict_markdown_injection_before_render(self):
        evidence = self.evidence()
        evidence["verdict"]["ai_signal_coverage"]["percent"] = "12\n# injected"
        with self.assertRaisesRegex(SystemExit, "percent"):
            self.module.render(evidence)


if __name__ == "__main__":
    unittest.main()
