"""Luật chung cho MỌI `skills/*/SKILL.md`, không riêng bộ forensics.

`tests/forensics/test_structure.py` giữ phần định tuyến riêng của bộ `05*` (router gọi đúng
sub-skill, đọc mù trước khi chạy script). File này giữ phần mà cả chín skill cùng chịu:

1. `name:` khớp đúng tên thư mục — sai một chữ là skill không nạp được;
2. `description: Use when …` — câu quyết định skill có được gọi hay không;
3. **≤550 từ** — kiến thức dài phải nằm ở `references/`, không nằm trong SKILL.md;
4. thư mục skill nào có mặt trên đĩa cũng phải nằm trong danh sách dưới. Thêm skill mà quên
   thêm vào đây thì nó không bao giờ bị kiểm ba luật trên.
"""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"

WORD_BUDGET = 550

# Bốn trục viết của đợt này + năm skill của bộ forensics đã có từ trước.
EXPECTED_SKILLS = {
    "01-context-architect",
    "02-cowriter",
    "03-critique",
    "04-humanizer",
    "05-forensics",
    "05a-reading",
    "05b-scoring",
    "05c-reporting",
    "05d-calibration",
}

# Bốn trục viết: cái nào cũng phải trỏ vào ít nhất một file references/.
WRITING_SKILLS = ("01-context-architect", "02-cowriter", "03-critique", "04-humanizer")


def skills_on_disk():
    return {
        path.parent.name
        for path in SKILLS_DIR.glob("*/SKILL.md")
        if path.is_file()
    }


class SkillInventoryTests(unittest.TestCase):
    def test_every_skill_on_disk_is_declared_here(self):
        self.assertEqual(skills_on_disk(), EXPECTED_SKILLS)

    def test_the_four_writing_skills_all_exist(self):
        """Tiêu chí nghiệm thu spec §4: `ls skills/0{1,2,3,4}-*/SKILL.md` đủ bốn."""
        for name in WRITING_SKILLS:
            with self.subTest(skill=name):
                self.assertTrue((SKILLS_DIR / name / "SKILL.md").is_file(), name)


class SkillFrontmatterTests(unittest.TestCase):
    def test_name_matches_the_folder(self):
        for name in sorted(EXPECTED_SKILLS):
            with self.subTest(skill=name):
                text = (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertRegex(text, rf"(?m)^name: {re.escape(name)}$")

    def test_description_starts_with_use_when(self):
        for name in sorted(EXPECTED_SKILLS):
            with self.subTest(skill=name):
                text = (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertRegex(text, r"(?m)^description: Use when ")

    def test_every_skill_stays_under_the_word_budget(self):
        for name in sorted(EXPECTED_SKILLS):
            with self.subTest(skill=name):
                text = (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")
                words = len(text.split())
                self.assertLessEqual(
                    words, WORD_BUDGET, f"{name}/SKILL.md dài {words} từ, trần là {WORD_BUDGET}"
                )


class WritingSkillReferenceTests(unittest.TestCase):
    def test_each_writing_skill_links_at_least_one_reference(self):
        for name in WRITING_SKILLS:
            with self.subTest(skill=name):
                folder = SKILLS_DIR / name
                references = sorted((folder / "references").glob("*.md"))
                self.assertTrue(references, f"{name} không có references/")
                text = (folder / "SKILL.md").read_text(encoding="utf-8")
                linked = [
                    path for path in references if f"references/{path.name}" in text
                ]
                self.assertTrue(
                    linked, f"{name}/SKILL.md không trỏ tới file references/ nào"
                )

    def test_no_writing_skill_branches_on_genre(self):
        """Thể loại là dữ liệu, skill là logic — plan §2.1."""
        for name in WRITING_SKILLS:
            text = (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")
            for forbidden in ("if genre", 'genre == "'):
                with self.subTest(skill=name, forbidden=forbidden):
                    self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
