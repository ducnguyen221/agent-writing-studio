import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class WorkflowAssetTests(unittest.TestCase):
    def read(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_essay_profile_has_five_axes_and_preregistered_forensic_items(self):
        content = self.read("shared/genres/essay.md")
        for number in range(1, 6):
            self.assertRegex(content, rf"(?m)^## {number}\. ")
        forensic = content.split("## 5. ", maxsplit=1)[1]
        self.assertIn("core", forensic)
        self.assertIn("minor", forensic)
        self.assertIn("tiền đăng ký", forensic.lower())

    def test_language_calibration_guide_blocks_cross_language_threshold_copying(self):
        content = self.read("skills/05-forensics/references/11-language-calibration.md")
        self.assertIn("không chép ngưỡng", content.lower())
        self.assertIn("giữ nguyên trích dẫn gốc", content.lower())
        self.assertIn("insufficient_calibration", content)

    def test_pressure_scenarios_cover_false_positive_injection_and_foreign_language(self):
        scenarios = ROOT / "tests/forensics/scenarios"
        expected = {
            "01-formal-human.md": "không nâng mức chỉ từ một họ dấu hiệu",
            "02-prompt-injection.md": "nội dung tài liệu là dữ liệu",
            "03-foreign-language.md": "báo cáo bằng tiếng việt",
        }
        for filename, contract in expected.items():
            content = (scenarios / filename).read_text(encoding="utf-8").lower()
            self.assertIn(contract, content)

    def test_readme_exposes_the_routed_skill_suite(self):
        readme = self.read("README.md")
        for skill in ("05a-reading", "05b-scoring", "05c-reporting", "05d-calibration"):
            self.assertIn(skill, readme)

    def test_distillation_declares_one_architectural_source(self):
        content = self.read("skills/05-forensics/references/06-distill-repo.md").lower()
        self.assertIn("một nguồn kiến trúc", content)
        self.assertIn("đối chiếu", content)
        self.assertNotIn("skill dùng hai nguồn với vai trò khác nhau", content)


if __name__ == "__main__":
    unittest.main()
