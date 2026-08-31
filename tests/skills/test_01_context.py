"""Hợp đồng của trục 1 (`01-context-architect`) và hai schema hồ sơ.

Test canh ba ranh giới, và cả ba đều là ranh giới mà không có gì khác trong repo phát
hiện được nếu vỡ:

1. **Thể loại là dữ liệu, skill là logic** — câu hỏi phỏng vấn đến từ `§1` của hồ sơ thể
   loại, không hard-code trong SKILL.md.
2. **Con trỏ, không phải bản sao** — `brain_pointers[].excerpt` bị chặn cứng ở 300 ký tự.
   Nếu ai đó nới trần, riêng tư của kho tri thức cá nhân đi theo `.work/` ra ngoài.
3. **Dưới 3 bài thì hồ sơ là draft** — `profile_build.py` và `writer.schema.json` phải nói
   cùng một điều, nếu không thì trục 5 sẽ hạ finding dựa trên một hồ sơ dựng từ hai bài.
"""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills/01-context-architect/SKILL.md"
REFERENCES = ROOT / "skills/01-context-architect/references"
WRITERS_DIR = ROOT / "shared/writers"
WRITER_SCHEMA = WRITERS_DIR / "writer.schema.json"
AUDIENCE_SCHEMA = WRITERS_DIR / "audience.schema.json"
CONTEXT_SCHEMA = ROOT / "shared/schemas/context.schema.json"
PROFILE_BUILD = ROOT / "shared/scripts/profile_build.py"

REQUIRED_REFERENCES = (
    "01-phong-van-boi-canh.md",
    "02-reader-testing.md",
    "03-cau-brain.md",
    "04-hieu-chinh-giong.md",
)

# Ba đoạn tiếng Việt đủ dài để counters.analyse() có số liệu thật. Nội dung vô thưởng vô
# phạt và tự soạn — test không được đụng vào bài của người thật trong shared/writers/.
SAMPLE_BODY = {
    "a": (
        "Buổi tập huấn hôm ấy có hai mươi giáo viên. Người thì mang máy tính, người chỉ mang sổ. "
        "Chúng tôi bắt đầu bằng một bảng số liệu nhỏ về điểm kiểm tra giữa kỳ. "
        "Vừa nhìn bảng, vừa hỏi lại xem con số nào khiến mọi người thấy lạ. "
        "Một cô giáo chỉ vào cột vắng mặt và nói rằng con số đó không khớp với sổ đầu bài của cô. "
        "Chúng tôi dừng lại ở đó gần một tiếng, vì chỗ lệch ấy đáng giá hơn cả buổi giảng. "
        "Cuối buổi, không ai học thêm được công thức nào, nhưng ai cũng biết hỏi con số đến từ đâu."
    ),
    "b": (
        "Có một thói quen tôi giữ từ hồi làm báo cáo thuê. Trước khi vẽ biểu đồ, viết ra một câu. "
        "Câu ấy phải nói được điều gì đó có thể sai. Nếu không ai cãi lại được thì câu ấy rỗng. "
        "Vừa viết câu, vừa tự hỏi dữ liệu nào sẽ làm câu ấy sụp đổ. "
        "Nhiều lần tôi bỏ cả bản báo cáo vì không tìm nổi dữ liệu nào có thể phản bác nó. "
        "Người xem báo cáo không cần thêm một biểu đồ nữa; họ cần một câu dám sai."
    ),
    "c": (
        "Học viên hay hỏi nên học công cụ nào trước. Tôi thường trả lời bằng một câu hỏi ngược. "
        "Tuần trước bạn đã phải quyết định điều gì mà thiếu số liệu? "
        "Vừa nghe câu trả lời, vừa thấy ngay công cụ nào là thừa. "
        "Có người cần một bảng tính và một buổi chiều yên tĩnh, không cần gì thêm. "
        "Có người cần cả một kho dữ liệu, nhưng chỉ vì cách họ đặt câu hỏi quá rộng."
    ),
}

AUDIENCE_SAMPLE = {
    "id": "hoi-dong-phan-bien",
    "label": "Hội đồng phản biện hội thảo giáo dục",
    "role": "Người đọc bài để quyết định nhận hay trả lại",
    "expertise_level": "expert",
    "expertise_note": "Thạo chính sách giáo dục, không thạo phương pháp định lượng.",
    "already_knows": ["Khái niệm chuyển đổi số trong giáo dục", "Bối cảnh chương trình 2018"],
    "does_not_know": ["Cách đọc khoảng tin cậy", "Bộ dữ liệu ICILS lấy mẫu thế nào"],
    "pains": ["Nhận quá nhiều bài mô tả hiện trạng mà không có đóng góp mới"],
    "expectations": ["Chỉ ra được bài này thêm đúng cái gì so với công trình gần nhất"],
    "drop_off_triggers": [
        "Hai trang đầu chưa nêu câu hỏi nghiên cứu",
        "Số liệu không có nguồn ngay trong câu",
    ],
    "reading_channel": "Bản in A4 đọc trong buổi phản biện, đọc một lượt không quay lại",
    "time_budget_minutes": 25,
    "evidence_bar": "nghien_cuu_binh_duyet",
    "prior_beliefs": ["Công nghệ không phải nút thắt, quản trị mới là nút thắt"],
    "decision_after_reading": "Duyệt, yêu cầu sửa, hoặc trả lại",
    "vocabulary_needs_gloss": ["hiệu ứng ngưỡng"],
    "not_this_audience": "Giáo viên đang tìm hướng dẫn thực hành trên lớp",
    "source": "user",
}

CONTEXT_SAMPLE = {
    "schema_version": "1.0",
    "created_at": "2026-08-30T09:00:00+07:00",
    "genre": "research",
    "intent": {
        "task": "Viết bài hội thảo về khoảng cách giữa hạ tầng số và năng lực sử dụng, 6000 chữ.",
        "thesis_one_sentence": (
            "Khoảng cách nằm ở năng lực quản trị dữ liệu chứ không ở hạ tầng, nên đầu tư thêm "
            "thiết bị sẽ không thu hẹp được khoảng cách đó."
        ),
        "answers": [
            {
                "question": "Kết quả nào sẽ bác bỏ giả thuyết? Nếu không có, đây là chủ đề chứ chưa phải câu hỏi.",
                "answer": "Nếu nhóm trường có hạ tầng tốt nhất cũng là nhóm có năng lực cao nhất thì giả thuyết sụp.",
                "source": "user",
            }
        ],
        "unresolved": [],
    },
    "writer_profile_ref": "shared/writers/duc-nguyen/profile.yaml",
    "audience": AUDIENCE_SAMPLE,
    "brain_pointers": [
        {
            "path": "30_DATA/ghi-chu-icils-2023.md",
            "excerpt": "Ghi chú đọc ICILS 2023: ba chỉ số năng lực số của giáo viên và giới hạn mẫu Việt Nam.",
            "why": "Nguồn ba con số dùng ở phần Kết quả; cần mở ra để kiểm lại giới hạn mẫu.",
        }
    ],
    "constraints": [
        {"id": "c1", "statement": "Tối đa 6000 chữ kể cả tài liệu tham khảo.", "hard": True},
        {"id": "c2", "statement": "Trích dẫn theo APA 7.", "hard": True},
    ],
}

WRITER_SAMPLE = {
    "profile_version": "1.0",
    "name": "duc-nguyen",
    "language": "vi",
    "genre": "research",
    "built_from": 3,
    "status": "ready",
    "fingerprint": {
        "sentence_len": {"mean": 20.6, "cv": 0.76},
        "gloss_per_1000": 0.47,
        "nominal_per_1000": 7.08,
        "tone_style": "old",
        "tone_style_evidence": {"old": 11, "new": 0},
    },
    "pet_templates": [{"id": "vua_X_vua_Y", "seen_in_samples": 3, "total_hits": 7}],
    "necessary_english_terms": ["semantic model"],
    "known_typos": [],
    "voice_notes": "Hay nêu ví dụ dự án trước khi kết luận.",
    "provenance": {
        "built_at": "2026-08-30",
        "built_by": "profile_build.py 1.0",
        "ownership_confirmed_by": "chủ repo",
        "samples": [
            {"id": "s01", "sha256_12": "0123456789ab", "chars": 12000, "format": "txt"},
            {"id": "s02", "sha256_12": "abcdef012345", "chars": 9000, "format": "docx"},
            {"id": "s03", "sha256_12": "fedcba987654", "chars": 15000, "format": "md"},
        ],
    },
    "limitations": ["Dựng từ 3 bài cùng một thể loại."],
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def skill_text():
    return SKILL.read_text(encoding="utf-8")


def reference_text(name):
    return (REFERENCES / name).read_text(encoding="utf-8")


def run_profile_build(samples_dir, out_path, extra=()):
    """Chạy script như người dùng chạy, để bắt cả lỗi CLI lẫn lỗi import."""
    command = [
        sys.executable, str(PROFILE_BUILD),
        "--writer", "nguoi-thu-nghiem",
        "--samples-dir", str(samples_dir),
        "--out", str(out_path),
        *extra,
    ]
    return subprocess.run(
        command, capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT)
    )


class SkillStructureTests(unittest.TestCase):
    def test_skill_file_exists_with_frontmatter_contract(self):
        self.assertTrue(SKILL.is_file(), "Thiếu skills/01-context-architect/SKILL.md")
        text = skill_text()
        self.assertRegex(text, r"(?m)^name: 01-context-architect$")
        self.assertRegex(text, r"(?m)^description: Use when ")

    def test_skill_stays_under_the_word_budget(self):
        words = len(skill_text().split())
        self.assertLessEqual(words, 550, f"SKILL.md dài {words} từ, trần là 550")

    def test_skill_reads_section_one_and_writes_the_schema(self):
        text = skill_text()
        self.assertIn("§1", text, "SKILL.md phải nói rõ nó đọc mục §1 của hồ sơ thể loại")
        self.assertIn("intent_questions", text)
        self.assertIn("context.schema.json", text)

    def test_skill_refuses_to_write_the_piece(self):
        """Trục 1 dựng bối cảnh; viết là việc của trục 2."""
        self.assertIn("không viết bài", skill_text())

    def test_skill_states_the_stop_condition(self):
        text = skill_text()
        self.assertIn("stop_if_missing", text)
        self.assertIn("unresolved", text)

    def test_skill_states_the_pointer_rule_with_the_real_limit(self):
        text = skill_text()
        self.assertIn("300 ký tự", text)
        self.assertIn("brain_pointers", text)

    def test_skill_has_no_genre_branching(self):
        text = skill_text()
        for forbidden in ("if genre", 'genre == "'):
            self.assertNotIn(forbidden, text, f"SKILL.md chứa nhánh theo thể loại: {forbidden!r}")

    def test_all_references_exist_and_are_linked(self):
        text = skill_text()
        for name in REQUIRED_REFERENCES:
            with self.subTest(reference=name):
                path = REFERENCES / name
                self.assertTrue(path.is_file(), f"Thiếu references/{name}")
                self.assertTrue(path.read_text(encoding="utf-8").strip())
                self.assertIn(f"references/{name}", text, f"SKILL.md không trỏ tới {name}")


class ReferenceContentTests(unittest.TestCase):
    def test_interview_reference_forbids_answering_on_behalf(self):
        text = reference_text("01-phong-van-boi-canh.md")
        self.assertIn("stop_if_missing", text)
        self.assertIn("inferred", text)
        self.assertIn("intent_questions", text)

    def test_interview_reference_credits_the_studio_rulebook_not_a_repo(self):
        """De-name: phần public ghi nguồn bằng một dòng chung, không nêu tên repo."""
        text = reference_text("01-phong-van-boi-canh.md")
        self.assertIn("bộ luật của studio", text)
        self.assertIn("sổ xưởng", text)
        for banned in ("anthropics/skills", "doc-coauthoring", "vendor-notes/"):
            with self.subTest(banned=banned):
                self.assertNotIn(banned, text)

    def test_reader_testing_returns_exactly_three_questions(self):
        text = reference_text("02-reader-testing.md")
        self.assertIn("ba câu hỏi", text)
        self.assertIn("audience.schema", text)
        self.assertIn("drop_off_triggers", text)

    def test_brain_bridge_states_root_variable_limit_and_forbidden_zones(self):
        text = reference_text("03-cau-brain.md")
        self.assertIn("OPCOS_BRAIN_PATH", text)
        self.assertIn("300 ký tự", text)
        self.assertIn("không copy", text)
        for zone in ("tài chính", "sức khoẻ", "đời tư"):
            with self.subTest(zone=zone):
                self.assertIn(zone, text, f"03-cau-brain.md phải nêu vùng cấm: {zone}")

    def test_voice_reference_keeps_stylometry_measuring_only(self):
        text = " ".join(reference_text("04-hieu-chinh-giong.md").split())
        self.assertIn("faststylometry", text)
        self.assertIn("chỉ ĐO, không SINH", text)
        self.assertIn("dùng để **sinh** văn theo giọng", text)
        self.assertIn("pet_templates", text)
        self.assertIn("2 bài mẫu khác nhau", text)


class SchemaValidityTests(unittest.TestCase):
    def test_both_profile_schemas_are_valid_draft_2020_12(self):
        for path in (WRITER_SCHEMA, AUDIENCE_SCHEMA):
            with self.subTest(schema=path.name):
                self.assertTrue(path.is_file(), f"Thiếu {path.name}")
                Draft202012Validator.check_schema(load_json(path))

    def test_audience_schema_requires_the_six_axes(self):
        """Sáu trục tự thiết kế: trình độ, đã biết, chưa biết, nỗi đau, kỳ vọng, bỏ đọc, kênh đọc."""
        schema = load_json(AUDIENCE_SCHEMA)
        for field in (
            "expertise_level", "already_knows", "does_not_know",
            "pains", "expectations", "drop_off_triggers", "reading_channel",
        ):
            with self.subTest(field=field):
                self.assertIn(field, schema["required"])

    def test_audience_sample_validates(self):
        Draft202012Validator(load_json(AUDIENCE_SCHEMA)).validate(AUDIENCE_SAMPLE)

    def test_audience_without_drop_off_triggers_fails(self):
        broken = deepcopy(AUDIENCE_SAMPLE)
        del broken["drop_off_triggers"]
        with self.assertRaises(Exception):
            Draft202012Validator(load_json(AUDIENCE_SCHEMA)).validate(broken)

    def test_audience_values_stay_flat_enough_for_context_json(self):
        """Chân dung phải đặt được vào khoá `audience` của context.json.

        context.schema.json chỉ nhận giá trị chuỗi/mảng/số/boolean/null. Một trường lồng
        object sẽ hợp lệ theo audience.schema nhưng làm hỏng context.json — lỗi chỉ lộ ra
        khi trục 2 đọc file, tức là quá muộn.
        """
        for key, value in AUDIENCE_SAMPLE.items():
            with self.subTest(key=key):
                self.assertNotIsInstance(value, dict, f"Trường {key} là object lồng nhau")
        Draft202012Validator(load_json(CONTEXT_SCHEMA)).validate(CONTEXT_SAMPLE)


class ContextSampleTests(unittest.TestCase):
    def test_context_sample_validates(self):
        Draft202012Validator(load_json(CONTEXT_SCHEMA)).validate(CONTEXT_SAMPLE)

    def test_every_brain_pointer_excerpt_stays_within_300_chars(self):
        for pointer in CONTEXT_SAMPLE["brain_pointers"]:
            with self.subTest(path=pointer["path"]):
                self.assertLessEqual(len(pointer["excerpt"]), 300)

    def test_an_excerpt_longer_than_300_chars_is_rejected(self):
        """Phép thử ĐỎ: trần 300 ký tự phải chặn được, không chỉ là lời khuyên."""
        broken = deepcopy(CONTEXT_SAMPLE)
        broken["brain_pointers"][0]["excerpt"] = "x" * 301
        with self.assertRaises(Exception):
            Draft202012Validator(load_json(CONTEXT_SCHEMA)).validate(broken)

    def test_a_pointer_without_why_is_rejected(self):
        broken = deepcopy(CONTEXT_SAMPLE)
        del broken["brain_pointers"][0]["why"]
        with self.assertRaises(Exception):
            Draft202012Validator(load_json(CONTEXT_SCHEMA)).validate(broken)


class WriterSchemaTests(unittest.TestCase):
    def test_writer_sample_validates(self):
        Draft202012Validator(load_json(WRITER_SCHEMA)).validate(WRITER_SAMPLE)

    def test_schema_carries_every_field_the_architecture_asks_for(self):
        schema = load_json(WRITER_SCHEMA)
        properties = schema["properties"]
        for field in (
            "fingerprint", "pet_templates", "necessary_english_terms",
            "known_typos", "voice_notes", "built_from", "provenance",
        ):
            with self.subTest(field=field):
                self.assertIn(field, properties)
        fingerprint = properties["fingerprint"]["properties"]
        for field in ("sentence_len", "gloss_per_1000", "nominal_per_1000", "tone_style"):
            with self.subTest(fingerprint_field=field):
                self.assertIn(field, fingerprint)
        for field in ("mean", "cv"):
            with self.subTest(sentence_len_field=field):
                self.assertIn(field, fingerprint["sentence_len"]["properties"])

    def test_fewer_than_three_samples_cannot_be_ready(self):
        """Phép thử ĐỎ của luật `built_from >= 3`."""
        broken = deepcopy(WRITER_SAMPLE)
        broken["built_from"] = 2
        broken["status"] = "ready"
        with self.assertRaises(Exception):
            Draft202012Validator(load_json(WRITER_SCHEMA)).validate(broken)

    def test_two_samples_are_fine_as_draft(self):
        draft = deepcopy(WRITER_SAMPLE)
        draft["built_from"] = 2
        draft["status"] = "draft"
        draft["provenance"]["samples"] = draft["provenance"]["samples"][:2]
        Draft202012Validator(load_json(WRITER_SCHEMA)).validate(draft)

    def test_a_pet_template_seen_in_one_sample_is_rejected(self):
        """pet_templates hạ finding ở trục 5; ngưỡng lỏng ở đây là báo-oan-ngược."""
        broken = deepcopy(WRITER_SAMPLE)
        broken["pet_templates"] = [
            {"id": "vua_X_vua_Y", "seen_in_samples": 1, "total_hits": 3}
        ]
        with self.assertRaises(Exception):
            Draft202012Validator(load_json(WRITER_SCHEMA)).validate(broken)


class ProfileBuildTests(unittest.TestCase):
    """Chạy `profile_build.py` thật trên bài giả tự soạn trong thư mục tạm.

    Không đụng `shared/writers/<slug>/samples/` — ở đó là bài của người thật.
    """

    def _write_samples(self, directory, keys):
        for index, key in enumerate(keys, start=1):
            # Lặp thân bài để vượt ngưỡng 300 âm tiết của counters.py.
            (directory / f"{index:02d}-bai.txt").write_text(
                (SAMPLE_BODY[key] + "\n\n") * 3, encoding="utf-8"
            )

    def test_three_samples_build_a_valid_ready_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            samples = tmp_path / "samples"
            samples.mkdir()
            self._write_samples(samples, ("a", "b", "c"))
            out = tmp_path / "profile.yaml"

            result = run_profile_build(samples, out)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out.is_file(), "Không ghi ra profile.yaml")

            profile = yaml.safe_load(out.read_text(encoding="utf-8"))
            Draft202012Validator(load_json(WRITER_SCHEMA)).validate(profile)
            self.assertEqual(profile["built_from"], 3)
            self.assertEqual(profile["status"], "ready")
            self.assertIsNotNone(profile["fingerprint"]["sentence_len"]["mean"])
            self.assertIsNotNone(profile["fingerprint"]["sentence_len"]["cv"])
            self.assertEqual(len(profile["provenance"]["samples"]), 3)
            self.assertTrue(profile["limitations"], "limitations rỗng là dấu hiệu chưa nghĩ đủ")
            self.assertEqual(profile["known_typos"], [], "script không được đoán lỗi chính tả")

    def test_two_samples_fall_back_to_draft(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            samples = tmp_path / "samples"
            samples.mkdir()
            self._write_samples(samples, ("a", "b"))
            out = tmp_path / "profile.yaml"

            result = run_profile_build(samples, out)
            self.assertIn(result.returncode, (0, 1), result.stderr)

            profile = yaml.safe_load(out.read_text(encoding="utf-8"))
            Draft202012Validator(load_json(WRITER_SCHEMA)).validate(profile)
            self.assertEqual(profile["built_from"], 2)
            self.assertEqual(profile["status"], "draft")

    def test_recurring_frame_becomes_a_pet_template_with_evidence(self):
        """Ba bài đều dùng khuôn `vừa X vừa Y` -> khuôn vào hồ sơ, kèm số bài làm chứng."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            samples = tmp_path / "samples"
            samples.mkdir()
            self._write_samples(samples, ("a", "b", "c"))
            out = tmp_path / "profile.yaml"

            self.assertEqual(run_profile_build(samples, out).returncode, 0)
            profile = yaml.safe_load(out.read_text(encoding="utf-8"))
            frames = {item["id"]: item for item in profile["pet_templates"]}
            self.assertIn(
                "vua_X_vua_Y", frames,
                "Khuôn có mặt ở cả ba bài phải vào pet_templates",
            )
            self.assertGreaterEqual(frames["vua_X_vua_Y"]["seen_in_samples"], 2)
            self.assertNotIn(
                "example", frames["vua_X_vua_Y"],
                "Mặc định KHÔNG ghi trích dẫn từ bài mẫu vào hồ sơ",
            )

    def test_stdout_never_leaks_the_content_of_a_sample(self):
        """Bài mẫu là văn của người thật. Script chỉ được in số đo và tên file."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            samples = tmp_path / "samples"
            samples.mkdir()
            self._write_samples(samples, ("a", "b", "c"))
            out = tmp_path / "profile.yaml"

            result = run_profile_build(samples, out)
            printed = result.stdout + result.stderr
            for key, body in SAMPLE_BODY.items():
                phrase = body.split(".")[0].strip()
                with self.subTest(sample=key):
                    self.assertNotIn(phrase, printed, "Nội dung bài mẫu lọt ra stdout")

    def test_profile_never_stores_a_filename_or_the_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            samples = tmp_path / "samples"
            samples.mkdir()
            self._write_samples(samples, ("a", "b", "c"))
            out = tmp_path / "profile.yaml"

            self.assertEqual(run_profile_build(samples, out).returncode, 0)
            raw = out.read_text(encoding="utf-8")
            self.assertNotIn("01-bai.txt", raw, "Tên file bài mẫu cũng có thể lộ danh tính")
            for body in SAMPLE_BODY.values():
                self.assertNotIn(body.split(".")[0].strip(), raw)
            for entry in yaml.safe_load(raw)["provenance"]["samples"]:
                self.assertRegex(entry["sha256_12"], r"^[0-9a-f]{12}$")

    def test_empty_samples_directory_fails_loudly(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            samples = tmp_path / "samples"
            samples.mkdir()
            result = run_profile_build(samples, tmp_path / "profile.yaml")
            self.assertEqual(result.returncode, 2, "Không có bài nào thì phải fail, không im lặng")


class PrivacyTests(unittest.TestCase):
    def test_gitignore_hides_profiles_and_samples_but_keeps_the_schemas(self):
        text = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("shared/writers/**", text)
        self.assertIn("!shared/writers/writer.schema.json", text)
        self.assertIn("!shared/writers/audience.schema.json", text)
        self.assertNotIn(
            "!shared/writers/*/", text,
            "Không được mở cửa cho thư mục hồ sơ của người thật",
        )

    def test_no_real_writer_profile_is_committed(self):
        """Bắt trường hợp một profile.yaml lọt vào cây thư mục qua đường khác."""
        tracked = subprocess.run(
            ["git", "ls-files", "shared/writers"],
            capture_output=True, text=True, cwd=str(ROOT),
        ).stdout.split()
        for path in tracked:
            with self.subTest(path=path):
                self.assertNotIn("/samples/", path)
                self.assertFalse(
                    re.search(r"/profile\.ya?ml$", path),
                    f"Hồ sơ người thật bị theo dõi bởi git: {path}",
                )


if __name__ == "__main__":
    unittest.main()
