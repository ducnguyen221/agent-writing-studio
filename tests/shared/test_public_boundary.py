"""Ranh giới public: repo không mang dấu hệ thống riêng của máy người dựng.

Ba luật, đều quét **mọi file đang track** (kể cả test, schema, HTML):

1. **Biến kho tri thức là `WRITING_STUDIO_KNOWLEDGE`.** Tên cũ chỉ còn đúng ở chỗ phải có nó: luật
   phân giải trong cầu kho tri thức (đường lùi cho máy dựng trước 0.3.0) và CHANGELOG (lịch sử).
2. **Không mặc định đoán một thư mục kho tri thức trong home** — không đặt biến là không có kho.
3. **Không đường home tuyệt đối có tên thật** (`C:\\Users\\<tên>`, `/Users/<tên>`, `/home/<tên>`);
   chỗ giữ chỗ kiểu `C:\\Users\\...` hay `<tên>` thì được.

Danh sách cho phép viết cứng ở đây: thêm một chỗ nhắc tên cũ là phải sửa test — tức là phải nghĩ.
"""

import re
import unittest
from pathlib import Path

from tests.shared.test_repo_gates import HAS_GIT, tracked_files


ROOT = Path(__file__).resolve().parents[2]
THIS = "tests/shared/test_public_boundary.py"

NEW_VAR = "WRITING_STUDIO_KNOWLEDGE"
LEGACY_PATTERN = re.compile(r"opcos", re.IGNORECASE)
# Chỗ được phép nhắc tên cũ / tên hệ riêng, kèm lý do.
LEGACY_ALLOWED = {
    "skills/01-context-architect/references/03-brain-bridge.md": "đường lùi tên biến cũ tới 0.4",
    "CHANGELOG.md": "lịch sử phát hành",
    "index.html": "chờ quyết định P-1 (liên kết trang giới thiệu)",
    THIS: "chính test này",
}
HOME_DEFAULT = re.compile(r"~/Brain\b")
REAL_HOME = re.compile(r"[A-Za-z]:\\Users\\(?![.<])[A-Za-z]|/Users/(?![.<])[A-Za-z]|/home/(?![.<])[a-z]")
TEXT_SUFFIXES = {".md", ".json", ".py", ".html", ".yml", ".yaml", ".cff", ".txt", ".svg", ""}


def text_files():
    for rel in tracked_files():
        path = ROOT / rel
        if path.suffix.lower() in TEXT_SUFFIXES and path.is_file():
            yield rel, path.read_text(encoding="utf-8", errors="replace")


@unittest.skipUnless(HAS_GIT, "không có git hoặc không phải bản checkout git")
class PublicBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = dict(text_files())

    def test_legacy_names_only_where_allowed(self):
        hits = sorted(rel for rel, text in self.files.items()
                      if LEGACY_PATTERN.search(text) and rel not in LEGACY_ALLOWED)
        self.assertEqual(hits, [], "tên hệ riêng/biến cũ lọt ra ngoài danh sách cho phép")

    def test_knowledge_variable_is_documented_where_the_resolution_rule_lives(self):
        for rel in ("skills/01-context-architect/references/03-brain-bridge.md", "README.md",
                    "shared/schemas/context.schema.json"):
            with self.subTest(file=rel):
                self.assertIn(NEW_VAR, self.files[rel])

    def test_no_guessed_home_default_for_the_knowledge_root(self):
        hits = sorted(rel for rel, text in self.files.items()
                      if HOME_DEFAULT.search(text) and rel not in (THIS, "CHANGELOG.md"))
        self.assertEqual(hits, [])

    def test_no_real_home_path(self):
        hits = sorted(rel for rel, text in self.files.items()
                      if REAL_HOME.search(text) and rel != THIS)
        self.assertEqual(hits, [], "đường home tuyệt đối có tên thật")

    def test_detectors_catch_what_they_target(self):
        """Đột biến: ba bộ bắt phải bắt đúng, và tha chỗ giữ chỗ."""
        self.assertTrue(REAL_HOME.search(r"C:\Users\somebody\Code"))
        self.assertTrue(REAL_HOME.search("/Users/somebody/Code"))
        self.assertFalse(REAL_HOME.search(r"C:\Users\...\Code"))
        self.assertFalse(REAL_HOME.search(r"C:\Users\<tên>\..."))
        self.assertTrue(HOME_DEFAULT.search("mặc định ~/Brain"))
        self.assertTrue(LEGACY_PATTERN.search("OPCOS_BRAIN_PATH"))


if __name__ == "__main__":
    unittest.main()
