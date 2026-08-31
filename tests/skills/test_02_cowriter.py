"""Hợp đồng của trục 2 (`02-cowriter`).

Trục 2 là trục duy nhất SINH ra văn bản, nên ba ranh giới dưới đây không có gì khác trong repo
phát hiện được nếu chúng vỡ:

1. **Không có `context.json` thì không viết.** Bỏ luật này là bỏ luôn trục 1: skill sẽ tự phỏng
   vấn qua loa rồi viết, và bài ra đời từ một bối cảnh không ai duyệt.
2. **`draft.meta.json` với `machine_written_spans[]` là bắt buộc** (`ARCHITECTURE_v2.md` §2.5).
   Đây là bản tự khai của chính studio, và là ground truth duy nhất để đo trục 5. Mất nó thì
   repo mất tư cách nói về liêm chính.
3. **Chống khuôn áp NGAY KHI SINH.** `anti_llm_defaults[]` của §2 phải có mặt đủ trong
   `references/04-chong-khuon-llm.md`; thiếu một mục là một khuôn lọt xuống tận trục 4, nơi gỡ
   nó đồng nghĩa với viết lại cả đoạn.
"""

import json
import re
import unittest
from copy import deepcopy
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills/02-cowriter/SKILL.md"
REFERENCES = ROOT / "skills/02-cowriter/references"
DRAFT_SCHEMA = ROOT / "shared/schemas/draft.schema.json"
GENRES_DIR = ROOT / "shared/genres"
TELLS = ROOT / "shared/rules/vi-ai-tells.json"

REQUIRED_REFERENCES = (
    "01-outline-ba-tang.md",
    "02-vong-sua-danh-gia-giu.md",
    "03-tu-khai-nguon-goc.md",
    "04-chong-khuon-llm.md",
)

# Bốn họ tell mô tả CHỖ ĐẶT của một câu chứ không phải cách dùng từ, nên phải chặn lúc sinh.
ALWAYS_ON_TELLS = ("T25", "T27", "T28", "T32")

HEADING = re.compile(r"(?m)^##\s+(\d)\.\s")
YAML_BLOCK = re.compile(r"(?ms)^```yaml\r?\n(.*?)^```")

# draft.meta.json mẫu — hình dạng mà trục 2 phải xuất ra sau mỗi lần viết.
DRAFT_META_SAMPLE = {
    "schema_version": "1.0",
    "created_at": "2026-08-30",
    "context_ref": ".work/cot-b-ai-baitap/context.json",
    "genre": "essay",
    "structure_id": "luan_de_phan_de",
    "outline_approved": True,
    "outline_depth_reached": 3,
    "machine_written_spans": [
        {
            "sentence_id": "s0004",
            "origin": "machine",
            "note": "Câu chuyển đoạn, viết theo quan hệ đối lập đã khai ở tầng hai outline",
        },
        {
            "sentence_id": "s0011",
            "origin": "machine_edited_by_human",
            "note": "Tác giả đổi hai từ và thêm mốc thời gian",
        },
        {"sentence_id": "s0019", "origin": "human_edited_by_machine"},
    ],
    "model": {"name": "claude-opus", "version": "5"},
    "profile_used": "duc-nguyen",
    "self_checks": [
        {"name": "counters.py", "passed": True, "detail": "NOMINAL 6,8/1000; không cột nào bất thường"},
        {"name": "lens:task_response", "passed": True, "detail": "Bốn đoạn thân đều ánh xạ về luận đề"},
    ],
}


def skill_text():
    return SKILL.read_text(encoding="utf-8")


def reference_text(name):
    return (REFERENCES / name).read_text(encoding="utf-8")


def normalise(text):
    """Bỏ khác biệt xuống dòng: chuỗi dài trong file bị wrap, trong YAML thì không."""
    return " ".join(text.split())


def genre_section_yaml(genre, number):
    text = (GENRES_DIR / f"{genre}.md").read_text(encoding="utf-8")
    heads = list(HEADING.finditer(text))
    for index, head in enumerate(heads):
        if head.group(1) != str(number):
            continue
        end = heads[index + 1].start() if index + 1 < len(heads) else len(text)
        block = YAML_BLOCK.search(text[head.end():end])
        assert block, f"{genre}.md §{number} không có khối yaml"
        return yaml.safe_load(block.group(1))
    raise AssertionError(f"{genre}.md không có mục §{number}")


class SkillStructureTests(unittest.TestCase):
    def test_skill_file_exists_with_frontmatter_contract(self):
        self.assertTrue(SKILL.is_file(), "Thiếu skills/02-cowriter/SKILL.md")
        text = skill_text()
        self.assertRegex(text, r"(?m)^name: 02-cowriter$")
        self.assertRegex(text, r"(?m)^description: Use when ")

    def test_skill_stays_under_the_word_budget(self):
        words = len(skill_text().split())
        self.assertLessEqual(words, 550, f"SKILL.md dài {words} từ, trần là 550")

    def test_all_references_exist_and_are_linked(self):
        text = skill_text()
        for name in REQUIRED_REFERENCES:
            with self.subTest(reference=name):
                path = REFERENCES / name
                self.assertTrue(path.is_file(), f"Thiếu references/{name}")
                self.assertTrue(path.read_text(encoding="utf-8").strip())
                self.assertIn(f"references/{name}", text, f"SKILL.md không trỏ tới {name}")

    def test_skill_has_no_genre_branching(self):
        text = skill_text()
        for forbidden in ("if genre", 'genre == "'):
            self.assertNotIn(forbidden, text, f"SKILL.md chứa nhánh theo thể loại: {forbidden!r}")


class RefusalTests(unittest.TestCase):
    """Không có bối cảnh thì không viết — luật đầu tiên của trục này."""

    def test_skill_refuses_to_write_without_a_context_file(self):
        text = skill_text()
        self.assertIn("context.json", text)
        self.assertIn("từ chối", text)

    def test_skill_names_the_axis_one_skill_to_call_instead(self):
        self.assertIn("01-context-architect", skill_text())

    def test_skill_stops_on_unresolved_context(self):
        self.assertIn("unresolved", skill_text())

    def test_skill_refuses_the_exploratory_paragraph_loophole(self):
        """"Viết thử một đoạn cho dễ hình dung" là cách thông dụng nhất để lách cổng duyệt."""
        text = skill_text()
        self.assertIn("Không viết thử một đoạn", text)


class ReadingContractTests(unittest.TestCase):
    def test_skill_reads_section_two_of_the_genre_profile(self):
        text = skill_text()
        self.assertIn("§2", text)
        for key in ("structures", "default_structure", "anti_llm_defaults", "outline_depth"):
            with self.subTest(key=key):
                self.assertIn(key, text)

    def test_skill_reads_the_writer_profile_including_a_draft_one(self):
        text = skill_text()
        self.assertIn("writer_profile_ref", text)
        self.assertIn("status: draft", text, "Hồ sơ dưới ba bài vẫn dùng được, phải nói rõ dùng thế nào")

    def test_skill_walks_outline_then_waits_then_writes(self):
        text = skill_text()
        order = [text.find("outline"), text.find("chờ duyệt"), text.find("Viết prose")]
        self.assertNotIn(-1, order, "SKILL.md thiếu một trong ba bước outline → duyệt → prose")
        self.assertEqual(order, sorted(order), "Ba bước phải đúng thứ tự trong SKILL.md")

    def test_skill_self_checks_before_handing_over(self):
        text = skill_text()
        self.assertIn("counters.py", text)
        self.assertIn("lăng kính", text)

    def test_skill_writes_both_output_files(self):
        text = skill_text()
        self.assertIn("draft.md", text)
        self.assertIn("draft.meta.json", text)
        self.assertIn("draft.schema.json", text)


class DraftMetaContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(DRAFT_SCHEMA.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)

    def test_sample_draft_meta_validates(self):
        self.assertEqual(sorted(self.validator.iter_errors(DRAFT_META_SAMPLE), key=str), [])

    def test_machine_written_spans_is_required_even_when_nothing_is_machine_written(self):
        empty = deepcopy(DRAFT_META_SAMPLE)
        empty["machine_written_spans"] = []
        self.assertEqual(sorted(self.validator.iter_errors(empty), key=str), [])

        missing = deepcopy(DRAFT_META_SAMPLE)
        del missing["machine_written_spans"]
        self.assertTrue(
            list(self.validator.iter_errors(missing)),
            "Bỏ hẳn machine_written_spans phải là file KHÔNG hợp lệ — rỗng khác với vắng mặt",
        )

    def test_approved_outline_must_declare_the_depth_it_reached(self):
        broken = deepcopy(DRAFT_META_SAMPLE)
        del broken["outline_depth_reached"]
        self.assertTrue(list(self.validator.iter_errors(broken)))

    def test_origin_values_are_closed(self):
        broken = deepcopy(DRAFT_META_SAMPLE)
        broken["machine_written_spans"][0]["origin"] = "co-written"
        self.assertTrue(list(self.validator.iter_errors(broken)))

    def test_structure_id_of_the_sample_exists_in_the_genre_profile(self):
        structures = genre_section_yaml(DRAFT_META_SAMPLE["genre"], 2)["structures"]
        self.assertIn(
            DRAFT_META_SAMPLE["structure_id"], [item["id"] for item in structures]
        )


class OutlineReferenceTests(unittest.TestCase):
    def test_outline_depth_comes_from_the_genre_not_from_the_reference(self):
        text = reference_text("01-outline-ba-tang.md")
        self.assertIn("outline_depth", text)
        self.assertIn("§2", text)

    def test_reference_names_all_three_layers(self):
        text = reference_text("01-outline-ba-tang.md")
        for layer in ("Tầng 1", "Tầng 2", "Tầng 3"):
            with self.subTest(layer=layer):
                self.assertIn(layer, text)
        self.assertIn("bằng chứng", text)

    def test_reference_gates_prose_behind_an_approved_outline(self):
        text = normalise(reference_text("01-outline-ba-tang.md"))
        self.assertIn("outline_approved", text)
        self.assertIn("không được nộp", text)

    def test_reference_forbids_filling_an_empty_evidence_slot_with_prose(self):
        text = normalise(reference_text("01-outline-ba-tang.md"))
        self.assertIn("Chỗ trống ở tầng ba là chỗ trống thật", text)
        self.assertIn("T05", text, "Nguồn mơ hồ là tell phải gọi tên, không nói chung chung")

    def test_research_outline_carries_its_citations_from_the_start(self):
        text = normalise(reference_text("01-outline-ba-tang.md"))
        self.assertIn("nguồn phải gắn ngay tại đây", text)
        self.assertIn("research.md", text)


class ModifyEvaluateKeepTests(unittest.TestCase):
    def test_reference_credits_the_studio_rulebook_not_a_repo(self):
        """De-name: sơ đồ ba bước là kiến thức chung, nguồn ghi ở sổ xưởng."""
        text = normalise(reference_text("02-vong-sua-danh-gia-giu.md"))
        self.assertIn("kiến thức chung của ngành", text)
        self.assertIn("bộ luật của studio", text)
        self.assertIn("sổ xưởng", text)
        for banned in ("autonovel", "vendor-notes/"):
            with self.subTest(banned=banned):
                self.assertNotIn(banned, text)

    def test_reference_runs_counters_plus_one_or_two_lenses(self):
        text = normalise(reference_text("02-vong-sua-danh-gia-giu.md"))
        self.assertIn("counters.py", text)
        self.assertIn("lăng kính", text)
        self.assertIn("01-lang-kinh.md", text, "Danh mục lăng kính là của trục 3, phải trỏ sang")

    def test_reference_keeps_the_old_version_when_the_new_one_does_not_win(self):
        text = normalise(reference_text("02-vong-sua-danh-gia-giu.md"))
        self.assertIn("giữ bản cũ", text.lower())

    def test_reference_states_the_anti_goodhart_rule(self):
        text = normalise(reference_text("02-vong-sua-danh-gia-giu.md"))
        self.assertIn("Goodhart", text)
        self.assertIn("Không sửa để con số đẹp lên", text)
        self.assertIn("genre_baseline", text)

    def test_reference_describes_the_three_chapter_self_check_as_active(self):
        """`novel.md` đã có từ Phase 1b: mục 5 phải là luật đang chạy, không phải mô tả."""
        text = normalise(reference_text("02-vong-sua-danh-gia-giu.md"))
        self.assertIn("ba chương", text)
        self.assertIn("novel.md", text)
        self.assertIn("luật đang chạy", text)
        self.assertNotIn("Chưa dùng được", text)
        self.assertNotIn("chưa tồn tại", text)
        for lens in ("character_consistency", "plot_consistency", "pacing_curve",
                     "three_chapter_selfcheck"):
            with self.subTest(lens=lens):
                self.assertIn(lens, text)


class SelfDeclarationReferenceTests(unittest.TestCase):
    def test_reference_cites_the_conflict_of_interest_rule(self):
        text = normalise(reference_text("03-tu-khai-nguon-goc.md"))
        self.assertIn("§2.5", text)
        self.assertIn("mất tư cách nói về liêm chính", text)

    def test_reference_explains_why_an_empty_array_is_a_claim(self):
        text = normalise(reference_text("03-tu-khai-nguon-goc.md"))
        self.assertIn("một khẳng định, không phải một chỗ trống", text)

    def test_reference_ties_spans_to_sentence_ids_from_extract(self):
        text = normalise(reference_text("03-tu-khai-nguon-goc.md"))
        self.assertIn("sentence_id", text)
        self.assertIn("sentences.json", text)
        self.assertIn("extract.py", text)

    def test_reference_covers_all_three_origin_values(self):
        text = reference_text("03-tu-khai-nguon-goc.md")
        schema = json.loads(DRAFT_SCHEMA.read_text(encoding="utf-8"))
        origins = schema["properties"]["machine_written_spans"]["items"]["properties"]["origin"]["enum"]
        for origin in origins:
            with self.subTest(origin=origin):
                self.assertIn(origin, text)

    def test_reference_warns_that_edits_shift_sentence_ids(self):
        text = normalise(reference_text("03-tu-khai-nguon-goc.md"))
        self.assertIn("dịch hết", text)
        self.assertIn("chạy lại extract", text)

    def test_reference_keeps_axis_three_and_five_blind(self):
        text = normalise(reference_text("03-tu-khai-nguon-goc.md"))
        self.assertIn("Trục 3 không xem `draft.meta.json` trước khi chấm xong", text)
        self.assertIn("Trục 5 chạy mù", text)


class AntiTemplateReferenceTests(unittest.TestCase):
    """`anti_llm_defaults[]` phải được gom đủ, không được rơi mục nào."""

    @classmethod
    def setUpClass(cls):
        cls.text = normalise(reference_text("04-chong-khuon-llm.md"))

    def test_every_anti_llm_default_of_every_genre_is_present(self):
        collected = 0
        for path in sorted(GENRES_DIR.glob("*.md")):
            if path.name == "_schema.md":
                continue
            text = path.read_text(encoding="utf-8")
            # Hồ sơ `partial` chỉ có §5 (4 thể loại VN đặc thù): trục 2 không đọc chúng,
            # nên chúng không khai anti_llm_defaults và không được tính vào phép gom này.
            if not re.search(r"(?m)^##\s+2\.\s", text):
                continue
            defaults = genre_section_yaml(path.stem, 2)["anti_llm_defaults"]
            for item in defaults:
                collected += 1
                with self.subTest(genre=path.stem, default=item[:40]):
                    self.assertIn(normalise(item), self.text)
        self.assertGreaterEqual(
            collected, 29, "Năm hồ sơ đầy đủ khai 29 khuôn; gom thiếu là lỗi"
        )

    def test_the_four_always_on_tell_families_are_listed_with_a_fix(self):
        entries = {
            item["id"]: item
            for item in json.loads(TELLS.read_text(encoding="utf-8"))["entries"]
        }
        for tell_id in ALWAYS_ON_TELLS:
            with self.subTest(tell=tell_id):
                self.assertIn(tell_id, self.text)
                self.assertIn(normalise(entries[tell_id]["label"]).lower(), self.text.lower())

    def test_reference_applies_at_generation_time_not_at_axis_four(self):
        self.assertIn("ngay khi sinh", self.text)
        self.assertIn("không đợi trục 4", self.text)

    def test_genre_baseline_and_writer_samples_beat_the_list(self):
        self.assertIn("genre_baseline", self.text)
        self.assertIn("thắng", self.text)
        self.assertIn("pet_templates", self.text)

    def test_reference_says_the_genre_profile_is_the_real_source(self):
        self.assertIn("nguồn thật vẫn là", self.text)


if __name__ == "__main__":
    unittest.main()
