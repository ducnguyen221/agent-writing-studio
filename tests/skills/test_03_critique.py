"""Hợp đồng cấu trúc của trục 3 (`03-critique`).

Test này canh đúng một ranh giới: **thể loại là dữ liệu, skill là logic**. Nếu kiến thức
thể loại rò vào SKILL.md, hoặc một hồ sơ thể loại tự bịa ra lăng kính mới, ranh giới đó vỡ
và không có gì khác trong repo phát hiện được.
"""

import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills/03-critique/SKILL.md"
REFERENCES = ROOT / "skills/03-critique/references"
LENS_DOC = REFERENCES / "01-lang-kinh.md"
GENRES_DIR = ROOT / "shared/genres"
SCENARIO = ROOT / "tests/skills/scenarios/03-essay-tron-tru.md"

REQUIRED_REFERENCES = (
    "01-lang-kinh.md",
    "02-nguy-bien-13-loai-vi.md",
    "03-blind-referee.md",
    "04-barem-mau.md",
    "05-tich-hop-project-feedback.md",
)

# Danh mục lăng kính hợp lệ. Nguồn sự thật là 01-lang-kinh.md; danh sách này chỉ để bắt
# trường hợp file reference bị cắt cụt hoặc bị đổi tên lăng kính mà không ai để ý.
KNOWN_LENSES = {
    "fallacy_scan",
    "claim_check",
    "task_response",
    "source_reliability",
    "source_independence",
    "balance_check",
    "method_rigor",
    "plot_consistency",
    "character_consistency",
    "pacing_curve",
    "three_chapter_selfcheck",
    "value_density",
    "retention",
}

HEADING = re.compile(r"(?m)^##\s+(\d)\.\s+(.+?)\s*$")
YAML_BLOCK = re.compile(r"(?ms)^```yaml\r?\n(.*?)^```\s*$")


def skill_text():
    return SKILL.read_text(encoding="utf-8")


def documented_lenses():
    """Lăng kính mà 01-lang-kinh.md thật sự định nghĩa (có tiêu đề riêng)."""
    text = LENS_DOC.read_text(encoding="utf-8")
    headings = re.findall(r"(?m)^##\s+\d+\.\s+`([a-z][a-z0-9_]+)`", text)
    return set(headings)


def lens_section(name):
    """Thân của mục lăng kính trong 01-lang-kinh.md, tới tiêu đề `##` kế tiếp."""
    text = LENS_DOC.read_text(encoding="utf-8")
    heads = list(re.finditer(r"(?m)^##\s+\d+\.\s+`([a-z][a-z0-9_]+)`", text))
    for index, head in enumerate(heads):
        if head.group(1) != name:
            continue
        end = heads[index + 1].start() if index + 1 < len(heads) else len(text)
        return text[head.start(): end]
    raise AssertionError(f"01-lang-kinh.md không có mục lăng kính `{name}`")


def genre_lenses():
    """{tên file: [lăng kính khai ở §3]} cho mọi hồ sơ thể loại có §3."""
    result = {}
    for path in sorted(GENRES_DIR.glob("*.md")):
        if path.name == "_schema.md":
            continue
        text = path.read_text(encoding="utf-8")
        matches = list(HEADING.finditer(text))
        for index, match in enumerate(matches):
            if match.group(1) != "3":
                continue
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            blocks = YAML_BLOCK.findall(text[match.end(): end])
            if blocks:
                data = yaml.safe_load(blocks[0])
                result[path.name] = list(data.get("lenses", []))
    return result


class SkillStructureTests(unittest.TestCase):
    def test_skill_file_exists_with_frontmatter_contract(self):
        self.assertTrue(SKILL.is_file(), "Thiếu skills/03-critique/SKILL.md")
        text = skill_text()
        self.assertRegex(text, r"(?m)^name: 03-critique$")
        self.assertRegex(text, r"(?m)^description: Use when ")

    def test_skill_stays_under_the_word_budget(self):
        words = len(skill_text().split())
        self.assertLessEqual(words, 550, f"SKILL.md dài {words} từ, trần là 550")

    def test_skill_reads_section_three_and_writes_the_schema(self):
        text = skill_text()
        self.assertIn("§3", text, "SKILL.md phải nói rõ nó đọc mục §3 của hồ sơ thể loại")
        self.assertIn(
            "critique.schema.json",
            text,
            "SKILL.md phải nêu schema mà critique.json phải hợp lệ theo",
        )

    def test_skill_states_the_smooth_prose_rule(self):
        """Luật số một: văn trơn tru không phải lập luận tốt."""
        self.assertIn("trơn tru", skill_text())

    def test_skill_has_no_genre_branching(self):
        """Kiến thức thể loại nằm ở shared/genres/, không nằm trong skill."""
        text = skill_text()
        for forbidden in ("if genre", "if genre ==", 'genre == "'):
            self.assertNotIn(
                forbidden,
                text,
                f"SKILL.md chứa nhánh theo thể loại: {forbidden!r}",
            )

    def test_all_references_exist_and_are_linked(self):
        text = skill_text()
        for name in REQUIRED_REFERENCES:
            with self.subTest(reference=name):
                path = REFERENCES / name
                self.assertTrue(path.is_file(), f"Thiếu references/{name}")
                self.assertTrue(path.read_text(encoding="utf-8").strip())
        # Bốn reference quy trình phải được SKILL.md trỏ tới; file tích hợp được nhắc ở
        # mục bàn giao.
        for name in REQUIRED_REFERENCES:
            with self.subTest(linked=name):
                self.assertIn(f"references/{name}", text, f"SKILL.md không trỏ tới {name}")


class LensCatalogueTests(unittest.TestCase):
    def test_catalogue_documents_every_known_lens_with_four_parts(self):
        text = LENS_DOC.read_text(encoding="utf-8")
        documented = documented_lenses()
        missing = KNOWN_LENSES - documented
        self.assertFalse(missing, f"01-lang-kinh.md chưa định nghĩa lăng kính: {sorted(missing)}")
        unknown = documented - KNOWN_LENSES
        self.assertFalse(unknown, f"01-lang-kinh.md định nghĩa lăng kính lạ: {sorted(unknown)}")
        for part in ("**Đầu vào:**", "**Câu hỏi:**", "**Bằng chứng cần:**", "**Đầu ra:**"):
            self.assertIn(part, text, f"01-lang-kinh.md thiếu phần {part}")

    def test_every_genre_lens_is_in_the_catalogue(self):
        documented = documented_lenses()
        by_genre = genre_lenses()
        self.assertTrue(by_genre, "Không đọc được lenses[] của hồ sơ thể loại nào")
        for name, lenses in by_genre.items():
            with self.subTest(genre=name):
                unknown = set(lenses) - documented
                self.assertFalse(
                    unknown,
                    f"{name} §3 bật lăng kính không có trong 01-lang-kinh.md: {sorted(unknown)}",
                )

    def test_retention_stays_advisory_and_never_reaches_must_fix(self):
        """Quyết định cổng Phase 2 (30/08): `retention` là lăng kính tư vấn.

        Nó chủ quan nhất trong danh mục — hai trong bốn lý do bỏ đọc không có neo văn
        bản. Nếu ai đó viết lại mục này mà bỏ mất câu chốt, `retention` sẽ lặng lẽ đẩy
        được cảm giác chủ quan vào danh sách bắt buộc sửa. Test này khoá câu chốt đó.
        """
        section = " ".join(lens_section("retention").split())
        self.assertIn("không được vào `must_fix[]`", section)
        self.assertIn("không được đổi `criteria_scores[]`", section)
        self.assertIn("tư vấn", section)

    def test_value_density_lists_at_least_four_protected_zones(self):
        """Quyết định cổng Phase 2 (30/08): carve-out của `value_density` là 4 vùng.

        Bản đầu chỉ chừa "tóm tắt/kết luận bài học thuật" nên bỏ sót câu Link của PEEL
        (T31) và `genre_baseline`. Đây là chỗ trục 3 dễ đề nghị xoá oan nhất, và trục 4
        sẽ thi hành đề nghị đó.
        """
        section = " ".join(lens_section("value_density").split())
        self.assertIn("T31", section, "carve-out phải nêu đích danh T31 (câu Link của PEEL)")
        self.assertIn("genre_baseline", section)
        zones = re.findall(r"\((\d)\)", section)
        self.assertGreaterEqual(
            len(zones),
            4,
            f"value_density phải liệt kê ít nhất 4 vùng không được chạm, đang có {len(zones)}",
        )
        self.assertEqual(zones[:4], ["1", "2", "3", "4"], "4 vùng phải được đánh số liên tục")
        self.assertIn("đoạn thân", section, "chỉ được đề nghị xoá đoạn thân")

    def test_catalogue_states_the_no_evidence_no_finding_rule(self):
        text = LENS_DOC.read_text(encoding="utf-8")
        self.assertIn("phản chứng", text)
        self.assertIn("không có finding", text)


class FallacyReferenceTests(unittest.TestCase):
    def test_thirteen_fallacies_each_have_example_and_counterexample(self):
        text = (REFERENCES / "02-nguy-bien-13-loai-vi.md").read_text(encoding="utf-8")
        entries = re.findall(r"(?m)^##\s+(\d+)\.\s+(.+)$", text)
        self.assertEqual(
            len(entries), 13, f"Phải đúng 13 loại ngụy biện, đang có {len(entries)}"
        )
        self.assertEqual(
            [number for number, _ in entries],
            [str(index) for index in range(1, 14)],
            "13 loại phải đánh số liên tục từ 1 đến 13",
        )
        self.assertEqual(
            text.count("- **Ví dụ:**"), 13, "Mỗi loại phải có đúng một ví dụ tiếng Việt"
        )
        self.assertEqual(
            text.count("- **Phản chứng:**"), 13, "Mỗi loại phải có đúng một phản chứng tiếng Việt"
        )

    def test_fallacy_reference_separates_fallacy_from_language_error(self):
        text = (REFERENCES / "02-nguy-bien-13-loai-vi.md").read_text(encoding="utf-8")
        self.assertIn("Ngụy biện không phải lỗi ngôn ngữ", text)

    def test_fallacy_reference_takes_names_only_and_names_no_source_repo(self):
        """Chỉ mượn TÊN loại; định nghĩa và ví dụ tự biên, và không nêu tên repo nguồn."""
        text = (REFERENCES / "02-nguy-bien-13-loai-vi.md").read_text(encoding="utf-8")
        self.assertIn("tự biên", text)
        self.assertIn("bộ luật của studio", text)
        self.assertIn("sổ xưởng", text)
        # Tên nguồn cụ thể do hàng rào chung tests/shared/test_de_name.py canh.
        for banned in ("vendor-notes/",):
            with self.subTest(banned=banned):
                self.assertNotIn(banned, text)


class BlindRefereeTests(unittest.TestCase):
    def test_skill_and_reference_forbid_reading_draft_meta_early(self):
        skill = skill_text()
        reference = (REFERENCES / "03-blind-referee.md").read_text(encoding="utf-8")
        self.assertIn("draft.meta.json", skill)
        self.assertIn("draft.meta.json", reference)
        self.assertIn("câu hỏi mớm", skill)
        lowered = reference.lower()
        for step in ("đọc trôi", "lăng kính", "must_fix"):
            self.assertIn(step, lowered, f"03-blind-referee.md thiếu bước {step}")


class RubricReferenceTests(unittest.TestCase):
    def test_rubric_reference_names_its_three_real_sources(self):
        text = (REFERENCES / "04-barem-mau.md").read_text(encoding="utf-8")
        for source in ("IELTS", "nghị luận xã hội", "23/2021/TT-BGDĐT"):
            self.assertIn(source, text, f"04-barem-mau.md thiếu nguồn barem thật: {source}")

    def test_rubric_reference_states_task_rubric_wins(self):
        text = (REFERENCES / "04-barem-mau.md").read_text(encoding="utf-8")
        self.assertIn("barem của nhiệm vụ thắng", text)

    def test_rubric_reference_records_what_was_not_verified(self):
        text = (REFERENCES / "04-barem-mau.md").read_text(encoding="utf-8")
        self.assertIn("Chưa xác minh", text)


class IntegrationReferenceTests(unittest.TestCase):
    def test_integration_reference_covers_the_five_axes_of_project_feedback(self):
        text = (REFERENCES / "05-tich-hop-project-feedback.md").read_text(encoding="utf-8")
        for axis in (
            "Đáp ứng yêu cầu",
            "Năng lực kỹ thuật",
            "Tư duy phân tích",
            "Trình bày",
            "Hoàn thiện",
        ):
            self.assertIn(axis, text, f"Thiếu trục '{axis}' của project-feedback")

    def test_integration_is_a_file_contract_not_an_import(self):
        text = (REFERENCES / "05-tich-hop-project-feedback.md").read_text(encoding="utf-8")
        self.assertIn("không import", text)
        self.assertIn("critique.json", text)


class ScenarioTests(unittest.TestCase):
    def test_smooth_essay_scenario_expects_split_scores(self):
        self.assertTrue(SCENARIO.is_file(), "Thiếu kịch bản 03-essay-tron-tru.md")
        text = SCENARIO.read_text(encoding="utf-8")
        for token in ("`logic`", "`evidence`", "`language`"):
            self.assertIn(token, text, f"Kịch bản phải nói tới tiêu chí {token}")
        self.assertIn("blind_referee", text, "Kịch bản phải xử lý câu hỏi mớm")
        self.assertIn("must_fix", text)

    def test_scenario_refuses_to_infer_authorship(self):
        text = SCENARIO.read_text(encoding="utf-8")
        self.assertIn("không phải bằng chứng bài do máy viết", text)


if __name__ == "__main__":
    unittest.main()
