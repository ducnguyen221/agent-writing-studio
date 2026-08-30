"""`shared/scripts/check_spans.py` — bản tự khai của trục 2 có còn trỏ đúng câu không?

Cổng Phase 5 cho thấy `draft.schema.json` một mình không đủ: nó kiểm hình dạng của
`machine_written_spans[]`, không kiểm `sentence_id` có tồn tại trong văn bản cuối. Ca
`.work/cot-b-ai-baitap` đi qua schema với 45 nhãn trên một văn bản 47 câu.

Test ở đây khoá bốn thứ:
1. Khớp thì exit 0, lệch id thì exit 1.
2. Câu chưa khai được LIỆT KÊ (không im lặng), nhưng mặc định không phải lỗi — bài viết chung tay
   có câu do người viết là chuyện thường.
3. `--strict` biến câu chưa khai thành lỗi, dùng cho bài khai 100 % do máy.
4. Dáng "khai đủ khúc đầu, hụt khúc cuối" bị gắn cờ NGHI INDEX CŨ — đó chính là dáng mà phép so
   tập ID không bắt được.
"""

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "shared/scripts/check_spans.py"

TEXT = (
    "Câu thứ nhất đủ dài để không ai nhầm nó với một mảnh cụt. "
    "Vì sao? "
    "Câu thứ ba trả lời câu hỏi vừa nêu và khép đoạn lại ở đây."
)


def load_module():
    spec = importlib.util.spec_from_file_location("shared_check_spans", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def meta_with(spans):
    return {
        "schema_version": "1.0",
        "genre": "essay",
        "structure_id": "luan_de_phan_de",
        "outline_approved": True,
        "outline_depth_reached": 3,
        "machine_written_spans": spans,
        "model": {"name": "test"},
        "profile_used": None,
    }


class CheckSpansTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.sentences = cls.module.load_extract().sentences(TEXT)

    def run_cli(self, spans, extra=()):
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            (tmpdir / "polished.md").write_text(TEXT, encoding="utf-8")
            (tmpdir / "draft.meta.json").write_text(
                json.dumps(meta_with(spans), ensure_ascii=False), encoding="utf-8"
            )
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = self.module.main(
                    [
                        "--meta", str(tmpdir / "draft.meta.json"),
                        "--text", str(tmpdir / "polished.md"),
                        *extra,
                    ]
                )
            return code, buffer.getvalue()

    def test_the_short_sentence_has_an_id_and_can_be_declared(self):
        """Nếu câu ngắn còn bị nuốt thì cả cổng này vô nghĩa: không có id để mà khai."""
        self.assertEqual(len(self.sentences), 3)
        self.assertEqual(self.sentences[1]["text"], "Vì sao?")
        self.assertTrue(self.sentences[1]["short"])

    def test_full_declaration_passes(self):
        spans = [{"sentence_id": item["id"], "origin": "machine"} for item in self.sentences]
        code, out = self.run_cli(spans)
        self.assertEqual(code, self.module.EXIT_OK)
        self.assertIn("Khớp", out)

    def test_unknown_sentence_id_is_drift(self):
        spans = [{"sentence_id": "s0099", "origin": "machine"}]
        code, out = self.run_cli(spans)
        self.assertEqual(code, self.module.EXIT_DRIFT)
        self.assertIn("s0099", out)
        self.assertIn("LỆCH", out)

    def test_duplicate_sentence_id_is_drift(self):
        spans = [
            {"sentence_id": "s0001", "origin": "machine"},
            {"sentence_id": "s0001", "origin": "machine"},
        ]
        code, out = self.run_cli(spans)
        self.assertEqual(code, self.module.EXIT_DRIFT)
        self.assertIn("khai hai lần", out)

    def test_undeclared_sentences_are_listed_but_not_an_error_by_default(self):
        spans = [{"sentence_id": "s0001", "origin": "machine"}]
        code, out = self.run_cli(spans)
        self.assertEqual(code, self.module.EXIT_OK)
        self.assertIn("CHƯA KHAI", out)
        self.assertIn("s0002", out)

    def test_strict_turns_undeclared_into_drift(self):
        spans = [{"sentence_id": "s0001", "origin": "machine"}]
        code, out = self.run_cli(spans, extra=["--strict"])
        self.assertEqual(code, self.module.EXIT_DRIFT)

    def test_a_declaration_that_stops_short_looks_like_a_stale_index(self):
        """Ca cot-b: 45 nhãn trên 47 câu, không id nào sai, mà mọi nhãn vẫn có thể trỏ lệch."""
        spans = [{"sentence_id": item["id"], "origin": "machine"} for item in self.sentences[:2]]
        code, out = self.run_cli(spans)
        self.assertEqual(code, self.module.EXIT_OK)
        self.assertIn("NGHI INDEX CŨ", out)

    def test_a_declared_quote_that_does_not_match_is_drift(self):
        """`quote` tuỳ chọn là cách duy nhất hiện có để bắt lệch khi số câu không đổi."""
        spans = [{"sentence_id": "s0001", "origin": "machine", "quote": "một câu không có thật"}]
        code, out = self.run_cli(spans)
        self.assertEqual(code, self.module.EXIT_DRIFT)
        self.assertIn("trích dẫn không có trong câu đó", out)

    def test_a_stale_disk_index_is_drift(self):
        problems = self.module.compare_disk_index(self.sentences, self.sentences[:2])
        self.assertTrue(problems)
        self.assertIn("index đã cũ", problems[0])

    def test_missing_spans_field_is_refused_not_treated_as_empty(self):
        with self.assertRaisesRegex(ValueError, "machine_written_spans"):
            self.module.declared_spans({"genre": "essay"})


if __name__ == "__main__":
    unittest.main()
