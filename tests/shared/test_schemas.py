"""Năm hợp đồng dữ liệu của studio — context · draft · critique · polish · provenance.

Test giữ hai thứ: (a) schema là Draft 2020-12 hợp lệ; (b) ví dụ mẫu vừa khít schema.
Quan trọng nhất là các phép thử ĐỎ: ví dụ vi phạm phải fail. Một schema chỉ nói "có"
mà không bao giờ nói "không" thì không bảo vệ được gì.
"""

import json
import unittest
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "shared/schemas"
# Bốn cái đầu sống trong `.work/<case>/`. `provenance` là cái duy nhất ĐI RA KHỎI thư mục ca: nó đi
# kèm bản giao, vì phép thử cột B cho thấy sau trục 4 văn bản không mang dấu nào cho biết nó đã qua
# biên tập máy (docs/results/self-audit-cot-B.md mục 4).
NAMES = ("context", "draft", "critique", "polish", "provenance")


def load(name):
    return json.loads((SCHEMA_DIR / f"{name}.schema.json").read_text(encoding="utf-8"))


CONTEXT_SAMPLE = {
    "schema_version": "1.0",
    "created_at": "2026-08-30T09:00:00+07:00",
    "genre": "essay",
    "intent": {
        "task": "Bàn về vai trò của kỹ năng đọc dữ liệu với sinh viên kinh tế, tối đa 1200 chữ.",
        "thesis_one_sentence": (
            "Sinh viên kinh tế nên học đọc báo cáo dữ liệu trước khi học dựng báo cáo, "
            "vì phần lớn sai lầm nghề nghiệp nằm ở khâu đọc chứ không ở khâu dựng."
        ),
        "answers": [
            {
                "question": "Luận đề viết lại thành một câu có thể bị phản bác là gì?",
                "answer": "Ưu tiên dạy đọc trước dạy dựng; người phản đối sẽ nói phải dựng mới hiểu được cách đọc.",
                "source": "user",
            }
        ],
        "unresolved": [],
    },
    "writer_profile_ref": None,
    "audience": {
        "vai_tro": "giảng viên chấm bài cuối kỳ",
        "tieu_chi_cham": "barem khoa, nặng về lập luận và dẫn chứng",
        "muc_do_quen_chu_de": "cao",
    },
    "brain_pointers": [
        {
            "path": "Brain/57-hoc-tap/doc-hieu-du-lieu.md",
            "excerpt": "Ba lỗi đọc biểu đồ hay gặp: nhầm trục, nhầm mẫu, nhầm chiều nhân quả.",
            "why": "Cung cấp ba ví dụ cụ thể cho luận điểm thứ hai.",
        }
    ],
    "constraints": [
        {"id": "gioi_han_tu", "statement": "Không quá 1200 chữ.", "hard": True}
    ],
}

DRAFT_SAMPLE = {
    "schema_version": "1.0",
    "created_at": "2026-08-30T10:00:00+07:00",
    "context_ref": ".work/case-01/context.json",
    "genre": "essay",
    "structure_id": "mo_than_ket",
    "outline_approved": True,
    "outline_depth_reached": 3,
    "machine_written_spans": [
        {"sentence_id": "s0004", "origin": "machine"},
        {
            "sentence_id": "s0011",
            "origin": "machine_edited_by_human",
            "note": "Người viết đổi ví dụ sang lớp của mình.",
        },
    ],
    "model": {"name": "claude-opus", "version": "5"},
    "profile_used": None,
    "self_checks": [
        {"name": "counters.py", "passed": True, "detail": "Không có khuôn G1 lặp quá 2 lần."}
    ],
}

CRITIQUE_SAMPLE = {
    "schema_version": "1.0",
    "genre": "essay",
    "rubric_source": "Barem khoa Kinh tế, học kỳ 2026-1",
    "blind_referee": True,
    "criteria_scores": [
        {
            "id": "task_response",
            "score": 72,
            "evidence": "Luận đề rõ; đoạn 4 và 5 nói về công cụ, không phục vụ luận đề.",
            "question": "Đoạn nào không phục vụ luận đề? Bỏ đoạn 4 thì bài không yếu đi.",
            "confidence": "medium",
        },
        {
            "id": "evidence",
            "score": 48,
            "evidence": "Bốn khẳng định thực chứng, một có nguồn.",
            "question": "Khẳng định nào quan trọng nhất mà không có gì đỡ? Câu ở s0019.",
        },
    ],
    "lenses_run": ["task_response", "claim_check"],
    "findings": [
        {
            "id": "F1",
            "criterion_id": "evidence",
            "lens": "claim_check",
            "location": {"section": "Thân bài 2", "paragraph_index": 4, "sentence_id": "s0019"},
            "quoted_text": "Phần lớn sinh viên ra trường không đọc nổi một biểu đồ cột.",
            "severity": "high",
            "evidence": "Khẳng định về tỷ lệ, không có khảo sát hay nguồn nào đi kèm.",
            "counterevidence": "Có thể là quan sát nghề nghiệp của chính tác giả; nếu vậy chỉ cần đổi thành câu kể có phạm vi.",
            "suggested_fix": "Ghi rõ phạm vi quan sát, hoặc dẫn một khảo sát cụ thể.",
            "verification_question": "Con số 'phần lớn' đến từ đâu, và áp cho nhóm sinh viên nào?",
        }
    ],
    "must_fix": [
        {
            "finding_id": "F1",
            "why_it_matters": "Đây là câu đỡ cho toàn bộ luận điểm hai; mất nó thì luận điểm rỗng.",
            "blocking": True,
        }
    ],
    "limitations": [
        "Người chấm không có bản gốc dữ liệu tác giả nhắc tới, nên không kiểm được số liệu ở đoạn 3.",
    ],
}

POLISH_SAMPLE = {
    "schema_version": "1.0",
    "genre": "essay",
    "source_declared": {"how": "draft_meta", "draft_meta_ref": ".work/case-01/draft.meta.json"},
    "profile_used": None,
    "edits": [
        {
            "location": {"section": "Mở bài", "paragraph_index": 0, "sentence_id": "s0002"},
            "tell_id": "T13",
            "before": "Việc nâng cao năng lực đọc dữ liệu là một yêu cầu cấp thiết hiện nay.",
            "after": "Sinh viên kinh tế cần đọc được dữ liệu trước khi ra trường.",
            "reason": "Câu gốc không nói ai phải làm gì; bản sau nêu chủ thể và hành động.",
            "move": "Đổi danh từ hoá thành động từ có chủ thể",
        },
        {
            "location": {"sentence_id": "s0007"},
            "tell_id": None,
            "before": "Tuy nhiên, bên cạnh đó, cũng cần phải nói thêm rằng dữ liệu không phải tất cả.",
            "after": "Dữ liệu cũng không trả lời được câu hỏi nên làm gì tiếp theo.",
            "reason": "Ba từ nối chồng nhau ở đầu câu làm mất quan hệ logic thật.",
        },
    ],
    "facts_added": [],
    "facts_removed": [],
    "counters_before": {"G1_khuon_hinh_thuc": {"sentence_len": {"cv": 0.41}}},
    "counters_after": {"G1_khuon_hinh_thuc": {"sentence_len": {"cv": 0.44}}},
    "warnings": [],
    "metadata": {"stylometric_polish": True, "tool": "04-humanizer", "forensics_score_seen": False},
}

PROVENANCE_SAMPLE = {
    "schema_version": "1.0",
    "generated_at": "2026-08-30T11:00:00+07:00",
    "document": {"file": "polished.md"},
    "genre": "essay",
    "origin": {
        "sentences_total": 47,
        "machine_pct": 95.7,
        "machine_edited_pct": 0.0,
        "human_pct": 4.3,
        "counted_from": "sentences.json",
        "undeclared_sentences": 2,
    },
    "model": {"name": "claude-fable", "version": "5", "role": "viết (trục 2) và biên tập (trục 4)"},
    "stylometric_polish": True,
    "forensics_score_seen": False,
    "draft_meta_sha256": "0" * 64,
    "notes": ["Cùng một mô hình vừa viết vừa tự chấm; xem limitations của critique.json."],
}

SAMPLES = {
    "context": CONTEXT_SAMPLE,
    "draft": DRAFT_SAMPLE,
    "critique": CRITIQUE_SAMPLE,
    "polish": POLISH_SAMPLE,
    "provenance": PROVENANCE_SAMPLE,
}


class SchemaTests(unittest.TestCase):
    def test_every_schema_exists_and_is_draft_2020_12(self):
        for name in NAMES:
            with self.subTest(schema=name):
                path = SCHEMA_DIR / f"{name}.schema.json"
                self.assertTrue(path.is_file(), f"Thiếu {path.name}")
                Draft202012Validator.check_schema(load(name))

    def test_samples_validate(self):
        for name in NAMES:
            with self.subTest(schema=name):
                errors = sorted(
                    Draft202012Validator(load(name)).iter_errors(SAMPLES[name]),
                    key=lambda e: list(e.path),
                )
                self.assertEqual(
                    [],
                    [f"{list(e.path)}: {e.message}" for e in errors],
                    f"Ví dụ mẫu {name} không hợp lệ",
                )

    # --- phép thử ĐỎ: schema phải biết nói KHÔNG ---

    def test_polish_rejects_added_facts(self):
        sample = deepcopy(POLISH_SAMPLE)
        sample["facts_added"] = ["Thêm số liệu 63% không có trong bản gốc"]
        errors = list(Draft202012Validator(load("polish")).iter_errors(sample))
        self.assertTrue(errors, "facts_added khác rỗng PHẢI bị từ chối")

    def test_polish_rejects_removed_facts(self):
        sample = deepcopy(POLISH_SAMPLE)
        sample["facts_removed"] = ["Xoá trích dẫn Nguyễn Văn A (2024)"]
        errors = list(Draft202012Validator(load("polish")).iter_errors(sample))
        self.assertTrue(errors, "facts_removed khác rỗng PHẢI bị từ chối")

    def test_polish_requires_stylometric_polish_flag(self):
        sample = deepcopy(POLISH_SAMPLE)
        sample["metadata"]["stylometric_polish"] = False
        errors = list(Draft202012Validator(load("polish")).iter_errors(sample))
        self.assertTrue(errors, "metadata.stylometric_polish=false PHẢI bị từ chối")

    def test_polish_rejects_seeing_forensics_score(self):
        sample = deepcopy(POLISH_SAMPLE)
        sample["metadata"]["forensics_score_seen"] = True
        errors = list(Draft202012Validator(load("polish")).iter_errors(sample))
        self.assertTrue(errors, "Trục 4 xem điểm trục 5 PHẢI bị từ chối")

    def test_provenance_requires_the_stylometric_polish_flag(self):
        """Bản giao đi ra mà khai `false` thì sidecar thành tấm bình phong, tệ hơn là không có."""
        sample = deepcopy(PROVENANCE_SAMPLE)
        sample["stylometric_polish"] = False
        errors = list(Draft202012Validator(load("provenance")).iter_errors(sample))
        self.assertTrue(errors, "stylometric_polish=false PHẢI bị từ chối")

    def test_provenance_requires_a_hash_back_to_the_per_sentence_declaration(self):
        """Không có hash thì con số tổng ở sidecar không nối được với bản tự khai từng câu."""
        sample = deepcopy(PROVENANCE_SAMPLE)
        del sample["draft_meta_sha256"]
        errors = list(Draft202012Validator(load("provenance")).iter_errors(sample))
        self.assertTrue(errors, "Thiếu draft_meta_sha256 PHẢI bị từ chối")
        sample = deepcopy(PROVENANCE_SAMPLE)
        sample["draft_meta_sha256"] = "khong-phai-hash"
        errors = list(Draft202012Validator(load("provenance")).iter_errors(sample))
        self.assertTrue(errors, "Hash sai dạng PHẢI bị từ chối")

    def test_provenance_requires_the_three_origin_percentages(self):
        for field in ("machine_pct", "machine_edited_pct", "human_pct"):
            with self.subTest(field=field):
                sample = deepcopy(PROVENANCE_SAMPLE)
                del sample["origin"][field]
                errors = list(Draft202012Validator(load("provenance")).iter_errors(sample))
                self.assertTrue(errors, f"Thiếu origin.{field} PHẢI bị từ chối")

    def test_critique_must_fix_can_route_work_to_the_writing_axis(self):
        """P0-3: việc đòi đổi mức mạnh khẳng định là việc của trục 2, phải khai được owner."""
        sample = deepcopy(CRITIQUE_SAMPLE)
        sample["must_fix"][0]["owner"] = "02-cowriter"
        errors = list(Draft202012Validator(load("critique")).iter_errors(sample))
        self.assertEqual([], errors, "must_fix phải nhận owner: 02-cowriter")
        sample["must_fix"][0]["owner"] = "05-forensics"
        errors = list(Draft202012Validator(load("critique")).iter_errors(sample))
        self.assertTrue(errors, "owner ngoài danh sách PHẢI bị từ chối")

    def test_polish_warning_can_carry_a_route_instead_of_a_silent_edit(self):
        """Trục 4 không sửa mức mạnh khẳng định; nó ghi cảnh báo có địa chỉ trục phải làm."""
        sample = deepcopy(POLISH_SAMPLE)
        sample["warnings"] = [
            "CV độ dài câu tăng bất thường.",
            {
                "message": "must_fix F2 đòi hạ mức khẳng định ở s0032 — việc của vòng viết lại.",
                "route_to": "02-cowriter:round2",
                "sentence_id": "s0032",
                "must_fix_ref": "F2",
            },
        ]
        errors = list(Draft202012Validator(load("polish")).iter_errors(sample))
        self.assertEqual([], errors, "warnings phải nhận cả chuỗi lẫn object có route_to")
        sample["warnings"][1]["route_to"] = "04-humanizer"
        errors = list(Draft202012Validator(load("polish")).iter_errors(sample))
        self.assertTrue(errors, "route_to trỏ về chính trục 4 PHẢI bị từ chối")

    def test_polish_accepts_an_ad_hoc_profile_declaration(self):
        """Chưa có hồ sơ người viết mà người dùng đưa 1–2 bài mẫu ngay trong lượt.

        Bài mẫu đó vẫn được dùng, nhưng sổ ghi phải nói rõ nó chưa xác nhận chính chủ —
        `null` là sai sự thật (đã dùng bài mẫu), một slug là sai (chưa có hồ sơ nào).
        """
        sample = deepcopy(POLISH_SAMPLE)
        sample["profile_used"] = "ad-hoc (2 bài, chưa xác nhận chính chủ)"
        errors = list(Draft202012Validator(load("polish")).iter_errors(sample))
        self.assertEqual([], errors, "profile_used phải nhận khai báo ad-hoc")
        description = load("polish")["properties"]["profile_used"].get("description", "")
        self.assertIn("ad-hoc", description, "schema phải nói rõ dạng khai ad-hoc")
        self.assertIn("chưa xác nhận chính chủ", description)

    def test_context_rejects_long_brain_excerpt(self):
        sample = deepcopy(CONTEXT_SAMPLE)
        sample["brain_pointers"][0]["excerpt"] = "x" * 301
        errors = list(Draft202012Validator(load("context")).iter_errors(sample))
        self.assertTrue(errors, "Trích Brain dài hơn 300 ký tự PHẢI bị từ chối")

    def test_draft_requires_machine_written_spans_key(self):
        sample = deepcopy(DRAFT_SAMPLE)
        del sample["machine_written_spans"]
        errors = list(Draft202012Validator(load("draft")).iter_errors(sample))
        self.assertTrue(errors, "Thiếu machine_written_spans PHẢI bị từ chối")

    def test_draft_allows_empty_machine_written_spans(self):
        sample = deepcopy(DRAFT_SAMPLE)
        sample["machine_written_spans"] = []
        errors = list(Draft202012Validator(load("draft")).iter_errors(sample))
        self.assertEqual([], errors, "Mảng rỗng là khẳng định hợp lệ 'không câu nào do máy viết'")

    def test_critique_requires_counterevidence_in_every_finding(self):
        sample = deepcopy(CRITIQUE_SAMPLE)
        del sample["findings"][0]["counterevidence"]
        errors = list(Draft202012Validator(load("critique")).iter_errors(sample))
        self.assertTrue(errors, "Finding không có phản chứng PHẢI bị từ chối")

    def test_critique_requires_non_empty_limitations(self):
        sample = deepcopy(CRITIQUE_SAMPLE)
        sample["limitations"] = []
        errors = list(Draft202012Validator(load("critique")).iter_errors(sample))
        self.assertTrue(errors, "limitations rỗng PHẢI bị từ chối")

    def test_critique_has_no_total_score_field(self):
        schema = load("critique")
        self.assertNotIn("total_score", schema["properties"])
        self.assertIs(schema["additionalProperties"], False)

    # --- gắn kết với hồ sơ thể loại ---

    def test_critique_sample_criteria_exist_in_essay_profile(self):
        essay = (ROOT / "shared/genres/essay.md").read_text(encoding="utf-8")
        for row in CRITIQUE_SAMPLE["criteria_scores"]:
            self.assertIn(
                f"id: {row['id']}",
                essay,
                f"Tiêu chí {row['id']} không có trong §3 của essay.md",
            )

    def test_draft_sample_structure_exists_in_essay_profile(self):
        essay = (ROOT / "shared/genres/essay.md").read_text(encoding="utf-8")
        self.assertIn(f"id: {DRAFT_SAMPLE['structure_id']}", essay)


if __name__ == "__main__":
    unittest.main()
