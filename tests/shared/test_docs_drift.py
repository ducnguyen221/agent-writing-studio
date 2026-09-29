"""Cổng chống trôi tài liệu: chữ nói đúng thứ mã và manifest đang làm.

Tài liệu là thứ người ngoài đọc TRƯỚC lệnh đầu tiên. Mã đổi mà chữ không đổi thì người đọc không thấy
lỗi — họ chỉ thấy một phiên bản cũ, một lệnh thiếu, hay một con số test đã sai từ ba bản trước.

Khoá bốn thứ:
1. **Phiên bản:** mục đầu của CHANGELOG = phiên bản trong manifest; ngày mục đó = `date-released` của
   CITATION. Không tài liệu nào ghi cứng số test.
2. **Lệnh:** mọi lệnh con của `studio.py` được kể trong cả hai README và INSTALL; GUIDE kể đủ sáu lệnh
   của chuỗi viết.
3. **Cặp ngôn ngữ:** README và GUIDE mỗi bản trỏ sang bản ngôn ngữ kia.
4. **Tên workspace:** trang chỉ đường (lệnh, host, START-HERE, GUIDE, web) nói `workspace/`, không còn
   `.work/`. Tên cũ chỉ được nhắc ở chỗ giải thích việc dời (README, INSTALL, troubleshooting).

Liên kết tương đối trong mọi file `.md` đã có `tests/forensics/test_markdown_links.py` canh.
"""

import importlib.util
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
READMES = ("README.md", "README.vi.md")
GUIDES = ("GUIDE.md", "GUIDE.vi.md")
CHAIN = ("01-context", "02-draft", "03-critique", "04-humanize", "05-audit", "deliver-docx")
NO_LEGACY_WORKSPACE = ["START-HERE.md", *GUIDES, "index.html", "install/index.html",
                       "hosts/README.md", *[str(p.relative_to(ROOT).as_posix())
                                            for p in sorted((ROOT / "hosts").glob("*/README.md"))],
                       *[str(p.relative_to(ROOT).as_posix()) for p in sorted((ROOT / "commands").glob("*.md"))]]
PUBLIC_DOCS = [*READMES, *GUIDES, "INSTALL.md", "START-HERE.md", "index.html", "install/index.html",
               "docs/troubleshooting.md", "tests/README.md"]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def manifest_version():
    return json.loads(read(".claude-plugin/plugin.json"))["version"]


def studio_subcommands():
    spec = importlib.util.spec_from_file_location("studio_for_drift", ROOT / "studio.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    action = next(a for a in module.build_parser()._actions
                  if a.__class__.__name__ == "_SubParsersAction")
    return sorted(action.choices)


def changelog_head():
    match = re.search(r"(?m)^## \[(\d+\.\d+\.\d+)\] — (\d{4}-\d{2}-\d{2})", read("CHANGELOG.md"))
    return match.groups() if match else (None, None)


class VersionDriftTests(unittest.TestCase):
    def test_changelog_head_matches_the_manifest(self):
        self.assertEqual(changelog_head()[0], manifest_version(),
                         "phát hành bản mới thì mục đầu CHANGELOG phải là bản đó")

    def test_changelog_date_matches_citation(self):
        released = re.search(r'(?m)^date-released:\s*"?([\d-]+)"?', read("CITATION.cff")).group(1)
        self.assertEqual(changelog_head()[1], released)

    def test_no_document_hardcodes_a_test_count(self):
        for rel in PUBLIC_DOCS:
            text = re.sub(r"<[^>]+>", " ", read(rel))
            with self.subTest(doc=rel):
                self.assertEqual(re.findall(r"\b\d{2,}\s+(?:passed|test)\b", text), [],
                                 "số test đổi theo từng commit — đừng ghi cứng")


class CommandDriftTests(unittest.TestCase):
    def test_every_studio_subcommand_is_documented(self):
        for rel in (*READMES, "INSTALL.md"):
            text = read(rel)
            for sub in studio_subcommands():
                with self.subTest(doc=rel, command=sub):
                    self.assertIn(sub, text)

    def test_guides_walk_the_whole_chain(self):
        for rel in GUIDES:
            text = read(rel)
            for command in CHAIN:
                with self.subTest(doc=rel, command=command):
                    self.assertIn(f"`{command}`", text)
                    self.assertTrue((ROOT / "commands" / f"{command}.md").is_file())


class LanguagePairTests(unittest.TestCase):
    def test_pairs_link_to_each_other(self):
        for first, second in (READMES, GUIDES):
            with self.subTest(pair=first):
                self.assertIn(f"]({second})", read(first))
                self.assertIn(f"]({first})", read(second))


class WorkspaceNameDriftTests(unittest.TestCase):
    def test_route_pages_use_the_new_workspace_name(self):
        for rel in NO_LEGACY_WORKSPACE:
            with self.subTest(doc=rel):
                self.assertNotIn(".work/", read(rel), f"{rel} còn chỉ tới workspace tên cũ")

    def test_migration_is_explained_where_the_old_name_appears(self):
        for rel in (*READMES, "INSTALL.md", "docs/troubleshooting.md"):
            text = read(rel)
            with self.subTest(doc=rel):
                self.assertIn("workspace/", text)
                if ".work/" in text:
                    self.assertIn("studio.py migrate", text)

    def test_detector_catches_a_stale_count(self):
        """Đột biến: con số test ghi cứng phải bị bắt."""
        self.assertTrue(re.findall(r"\b\d{2,}\s+(?:passed|test)\b", "bản này: 438 passed"))


if __name__ == "__main__":
    unittest.main()
