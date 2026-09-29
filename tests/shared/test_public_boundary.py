"""Ranh giới public (cổng chống rò): repo không mang dấu hệ thống riêng của máy người dựng.

Quét **mọi file đang track + file mới chưa bị ignore** (bắt được trước khi `git add`), kể cả test,
schema, HTML. Năm luật:

1. **Biến kho tri thức là `WRITING_STUDIO_KNOWLEDGE`.** Tên biến cũ (tiền tố của hệ điều phối riêng)
   đã bỏ ở 0.4.0; chỉ còn được nhắc trong CHANGELOG (ghi chú bỏ) và test chứng minh nó không còn được đọc.
2. **Không mặc định đoán một thư mục kho tri thức trong home** — không đặt biến là không có kho.
3. **Không đường home tuyệt đối có tên thật** (`C:\\Users\\<tên>`, `/Users/<tên>`, `/home/<tên>`);
   chỗ giữ chỗ kiểu `C:\\Users\\...` hay `<tên>` thì được.
4. **Không tên riêng của kho tri thức cá nhân của tác giả** (một từ viết hoa) — repo nói "kho tri thức".
5. **Danh sách cấm riêng sống NGOÀI repo.** Tên ca thật, tên người, đường máy cụ thể… không được viết
   vào repo public — kể cả viết vào chính cổng này. Đặt biến `WRITING_STUDIO_LEAK_DENYLIST` trỏ một file
   văn bản (mỗi dòng một cụm, `#` là chú thích, không phân biệt hoa thường) thì cổng quét thêm các cụm
   đó; không đặt thì bỏ qua **kèm lời nhắn**, không xanh câm. Báo lỗi chỉ ghi file, dòng và SỐ THỨ TỰ
   cụm — không in lại cụm, để log CI không thành chỗ rò.

Chuỗi cấm ở luật 1, 2, 4 dựng bằng `chr()` để chính file này không mang chúng. Danh sách cho phép viết
cứng ở đây: thêm một chỗ nhắc tên cũ là phải sửa test — tức là phải nghĩ.
"""

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.shared.test_repo_gates import HAS_GIT, tracked_files


ROOT = Path(__file__).resolve().parents[2]
THIS = "tests/shared/test_public_boundary.py"
DENYLIST_ENV = "WRITING_STUDIO_LEAK_DENYLIST"


def s(*codes):
    return "".join(map(chr, codes))


NEW_VAR = "WRITING_STUDIO_KNOWLEDGE"
LEGACY_PATTERN = re.compile(s(111, 112, 99, 111, 115), re.IGNORECASE)            # tên hệ điều phối riêng
VAULT_NAME = s(66, 114, 97, 105, 110)                                              # tên kho riêng (viết hoa)
VAULT_PATTERN = re.compile(r"\b" + VAULT_NAME + r"\b")                             # KHÔNG bỏ qua hoa thường
HOME_DEFAULT = re.compile(r"~/" + VAULT_NAME + r"\b")
# Chỗ được phép nhắc tên biến cũ, kèm lý do.
LEGACY_ALLOWED = {
    "CHANGELOG.md": "ghi chú bỏ tên biến cũ ở 0.4.0 — người nâng cấp cần đọc thấy",
    "tests/shared/test_studio_lifecycle.py": "test chứng minh tên biến cũ không còn được đọc",
}
REAL_HOME = re.compile(r"[A-Za-z]:\\Users\\(?![.<])[A-Za-z]|/Users/(?![.<])[A-Za-z]|/home/(?![.<])[a-z]")
TEXT_SUFFIXES = {".md", ".json", ".py", ".html", ".yml", ".yaml", ".cff", ".txt", ".svg", ".toml",
                 ".cfg", ".ini", ".sh", ".ps1", ".css", ".js", ".example", ""}


def candidate_files():
    """File track + file mới chưa bị ignore (`--others --exclude-standard`)."""
    result = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--cached", "--others",
                             "--exclude-standard", "-z"], capture_output=True, text=True,
                            encoding="utf-8")
    listed = {p for p in result.stdout.split("\0") if p} or set(tracked_files())
    return sorted(listed)


def text_files():
    for rel in candidate_files():
        path = ROOT / rel
        if rel == THIS or not path.is_file():
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name.startswith("."):
            try:
                yield rel, path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue


def load_denylist(path: Path) -> list:
    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        term = line.strip()
        if term and not term.startswith("#"):
            terms.append(term)
    return terms


def denylist_hits(files: dict, terms: list) -> list:
    """`file:dòng [cụm #N]` — không bao giờ in lại chính cụm."""
    hits = []
    lowered = [t.lower() for t in terms]
    for rel, text in sorted(files.items()):
        for number, line in enumerate(text.splitlines(), 1):
            low = line.lower()
            hits += [f"{rel}:{number} [cụm #{i + 1}]" for i, term in enumerate(lowered) if term in low]
    return hits


@unittest.skipUnless(HAS_GIT, "không có git hoặc không phải bản checkout git")
class PublicBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = dict(text_files())

    def test_scans_something(self):
        self.assertGreater(len(self.files), 100, "cổng quét quá ít file — vô nghĩa")
        self.assertIn("README.md", self.files)

    def test_legacy_names_only_where_allowed(self):
        hits = sorted(rel for rel, text in self.files.items()
                      if LEGACY_PATTERN.search(text) and rel not in LEGACY_ALLOWED)
        self.assertEqual(hits, [], "tên hệ riêng/biến cũ lọt ra ngoài danh sách cho phép")

    def test_allowlist_is_not_stale(self):
        """Mục cho phép không còn khớp gì thì phải gỡ — cửa mở sẵn là cửa sẽ bị lợi dụng."""
        stale = [rel for rel in LEGACY_ALLOWED
                 if rel in self.files and not LEGACY_PATTERN.search(self.files[rel])]
        self.assertEqual(stale, [])

    def test_knowledge_variable_is_documented_where_the_resolution_rule_lives(self):
        for rel in ("skills/01-context-architect/references/03-knowledge-bridge.md", "README.md",
                    "shared/schemas/context.schema.json"):
            with self.subTest(file=rel):
                self.assertIn(NEW_VAR, self.files[rel])

    def test_no_guessed_home_default_for_the_knowledge_root(self):
        self.assertEqual(sorted(rel for rel, text in self.files.items() if HOME_DEFAULT.search(text)), [])

    def test_private_vault_name_is_not_used(self):
        hits = sorted(rel for rel, text in self.files.items() if VAULT_PATTERN.search(text))
        self.assertEqual(hits, [], "tên riêng của kho tri thức cá nhân — dùng 'kho tri thức'")

    def test_no_real_home_path(self):
        hits = sorted(rel for rel, text in self.files.items() if REAL_HOME.search(text))
        self.assertEqual(hits, [], "đường home tuyệt đối có tên thật")

    def test_detectors_catch_what_they_target(self):
        """Đột biến: các bộ bắt phải bắt đúng, và tha chỗ giữ chỗ."""
        self.assertTrue(REAL_HOME.search(r"C:\Users\somebody\Code"))
        self.assertTrue(REAL_HOME.search("/Users/somebody/Code"))
        self.assertFalse(REAL_HOME.search(r"C:\Users\...\Code"))
        self.assertFalse(REAL_HOME.search(r"C:\Users\<tên>\..."))
        self.assertTrue(HOME_DEFAULT.search("mặc định ~/" + VAULT_NAME))
        self.assertTrue(LEGACY_PATTERN.search(s(79, 80, 67, 79, 83) + "_X"))
        self.assertTrue(VAULT_PATTERN.search("ghi vào " + VAULT_NAME + "/"))
        self.assertFalse(VAULT_PATTERN.search("JetBrains Mono"), "tên font không phải tên kho")
        self.assertFalse(VAULT_PATTERN.search("brain_pointers"), "tên trường schema viết thường được phép")


@unittest.skipUnless(HAS_GIT, "không có git hoặc không phải bản checkout git")
class ExternalDenylistTests(unittest.TestCase):
    def test_external_denylist(self):
        value = (os.environ.get(DENYLIST_ENV) or "").strip()
        if not value:
            self.skipTest(f"chưa đặt {DENYLIST_ENV} — danh sách cấm riêng (ngoài repo) KHÔNG được quét "
                          "trong lượt này; máy tác giả nên đặt biến trước khi phát hành")
        path = Path(value).expanduser()
        self.assertTrue(path.is_file(), f"{DENYLIST_ENV} trỏ tới file không tồn tại — cấu hình sai, không bỏ qua")
        terms = load_denylist(path)
        self.assertTrue(terms, f"{DENYLIST_ENV}: file rỗng — cổng không quét gì")
        hits = denylist_hits(dict(text_files()), terms)
        self.assertEqual(hits, [], "cụm trong danh sách cấm riêng xuất hiện trong repo:\n" + "\n".join(hits))

    def test_matcher_reports_location_but_never_the_term(self):
        """Đột biến: một cụm cấm giả phải bị bắt, và báo cáo không in lại cụm đó."""
        with tempfile.TemporaryDirectory() as tmp:
            denylist = Path(tmp) / "deny.txt"
            denylist.write_text("# chú thích\n\nCa-Gia-Lap-XYZ\n", encoding="utf-8")
            terms = load_denylist(denylist)
        self.assertEqual(terms, ["Ca-Gia-Lap-XYZ"])
        hits = denylist_hits({"a.md": "dòng 1\nthấy ca-gia-lap-xyz ở đây\n", "b.md": "sạch"}, terms)
        self.assertEqual(hits, ["a.md:2 [cụm #1]"])
        self.assertNotIn("xyz", " ".join(hits).lower())


if __name__ == "__main__":
    unittest.main()
