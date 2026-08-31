"""Luật chung cho MỌI `skills/*/SKILL.md`, không riêng bộ forensics.

`tests/forensics/test_structure.py` giữ phần định tuyến riêng của bộ `05*` (router gọi đúng
sub-skill, đọc mù trước khi chạy script). File này giữ phần mà cả chín skill cùng chịu:

1. `name:` khớp đúng tên thư mục — sai một chữ là skill không nạp được;
2. `description: Use when …` — câu quyết định skill có được gọi hay không;
3. **≤550 từ** — kiến thức dài phải nằm ở `references/`, không nằm trong SKILL.md;
4. thư mục skill nào có mặt trên đĩa cũng phải nằm trong bảng dưới. Thêm skill mà quên
   thêm vào đây thì nó không bao giờ bị kiểm ba luật trên.

Từ v0.1.1 bốn sub-skill của trục 5 nằm **trong** `skills/05-forensics/` để cây `skills/` còn đúng
năm thư mục — một thư mục một trục. Chúng vẫn là skill thật, nên bộ quét ở đây quét cả hai tầng
(`skills/*/SKILL.md` **và** `skills/05-forensics/05*/SKILL.md`): dời chỗ không phải là được miễn
trần 550 từ hay luật đặt tên.
"""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"

WORD_BUDGET = 550

# Bốn trục viết của đợt này + năm skill của bộ forensics đã có từ trước.
# Giá trị = đường tương đối từ `skills/`, vì bốn sub-skill của trục 5 nằm lồng một tầng.
EXPECTED_SKILLS = {
    "01-context-architect": "01-context-architect",
    "02-cowriter": "02-cowriter",
    "03-critique": "03-critique",
    "04-humanizer": "04-humanizer",
    "05-forensics": "05-forensics",
    "05a-reading": "05-forensics/05a-reading",
    "05b-scoring": "05-forensics/05b-scoring",
    "05c-reporting": "05-forensics/05c-reporting",
    "05d-calibration": "05-forensics/05d-calibration",
}

# Cây `skills/` phải còn đúng năm thư mục — trục 5 gom lại từ v0.1.1.
EXPECTED_TOP_LEVEL = {
    "01-context-architect",
    "02-cowriter",
    "03-critique",
    "04-humanizer",
    "05-forensics",
}

# Bốn trục viết: cái nào cũng phải trỏ vào ít nhất một file references/.
WRITING_SKILLS = ("01-context-architect", "02-cowriter", "03-critique", "04-humanizer")


def skills_on_disk():
    found = set()
    for pattern in ("*/SKILL.md", "05-forensics/05*/SKILL.md"):
        found |= {path.parent.name for path in SKILLS_DIR.glob(pattern) if path.is_file()}
    return found


def skill_text(name):
    return (SKILLS_DIR / EXPECTED_SKILLS[name] / "SKILL.md").read_text(encoding="utf-8")


class SkillInventoryTests(unittest.TestCase):
    def test_every_skill_on_disk_is_declared_here(self):
        self.assertEqual(skills_on_disk(), set(EXPECTED_SKILLS))

    def test_skills_tree_has_exactly_five_folders(self):
        """`ls skills/` = 5 — một thư mục một trục; sub-skill trục 5 nằm bên trong 05-forensics."""
        top = {path.name for path in SKILLS_DIR.iterdir() if path.is_dir()}
        self.assertEqual(top, EXPECTED_TOP_LEVEL)

    def test_the_four_writing_skills_all_exist(self):
        """Tiêu chí nghiệm thu spec §4: `ls skills/0{1,2,3,4}-*/SKILL.md` đủ bốn."""
        for name in WRITING_SKILLS:
            with self.subTest(skill=name):
                self.assertTrue((SKILLS_DIR / name / "SKILL.md").is_file(), name)


class SkillFrontmatterTests(unittest.TestCase):
    def test_name_matches_the_folder(self):
        for name in sorted(EXPECTED_SKILLS):
            with self.subTest(skill=name):
                text = skill_text(name)
                self.assertRegex(text, rf"(?m)^name: {re.escape(name)}$")

    def test_description_starts_with_use_when(self):
        for name in sorted(EXPECTED_SKILLS):
            with self.subTest(skill=name):
                text = skill_text(name)
                self.assertRegex(text, r"(?m)^description: Use when ")

    def test_every_skill_stays_under_the_word_budget(self):
        for name in sorted(EXPECTED_SKILLS):
            with self.subTest(skill=name):
                text = skill_text(name)
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
            text = skill_text(name)
            for forbidden in ("if genre", 'genre == "'):
                with self.subTest(skill=name, forbidden=forbidden):
                    self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
