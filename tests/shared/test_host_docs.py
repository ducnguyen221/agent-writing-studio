"""Tài liệu theo host: bốn trang có thật, và mọi lệnh chúng dạy đều có thật trong repo.

Hỏng kiểu này thì hỏng im lặng: một trang host dạy `studio.py <lệnh>` đã bị bỏ, `--host <tên>` không
có trong `studio.py`, hay `/agent-writing-studio:<lệnh>` đã đổi tên — người đọc chỉ thấy lỗi khi gõ.
Test đọc mã (`studio.py` qua parser của chính nó, `commands/` trên đĩa) rồi đối chiếu với chữ.
"""

import importlib.util
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOSTS = ("claude", "codex", "antigravity", "claude-desktop")
HOST_PAGES = ["hosts/README.md"] + [f"hosts/{h}/README.md" for h in HOSTS]
# Tài liệu dạy lệnh cho người dùng hoặc agent. AGENTS.md có trong đây: nó là nguồn hướng dẫn chuẩn.
TEACHING_DOCS = HOST_PAGES + ["AGENTS.md", "INSTALL.md", "START-HERE.md", "README.md", "README.vi.md",
                              "GUIDE.md", "GUIDE.vi.md", "docs/troubleshooting.md"]
PLUGIN_REF = "agent-writing-studio@agent-writing-studio"


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def studio():
    spec = importlib.util.spec_from_file_location("studio_for_host_docs", ROOT / "studio.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def subcommands(module):
    parser = module.build_parser()
    action = next(a for a in parser._actions if a.__class__.__name__ == "_SubParsersAction")
    return set(action.choices)


class HostPageTests(unittest.TestCase):
    def test_every_host_page_exists_and_names_doctor(self):
        for rel in HOST_PAGES:
            with self.subTest(page=rel):
                self.assertTrue((ROOT / rel).is_file())
                self.assertIn("studio.py doctor", read(rel), f"{rel} không chỉ tới `studio.py doctor`")

    def test_host_index_lists_every_host_page(self):
        index = read("hosts/README.md")
        for host in HOSTS:
            with self.subTest(host=host):
                self.assertIn(f"{host}/README.md", index)

    def test_host_list_matches_studio(self):
        self.assertEqual(set(studio().HOSTS), set(HOSTS))

    def test_host_pages_do_not_teach_copying_skills(self):
        for rel in HOST_PAGES:
            text = read(rel)
            for banned in ("cp -r", "Copy-Item", "~/.claude/skills", "~/.codex/skills"):
                with self.subTest(page=rel, banned=banned):
                    self.assertNotIn(banned, text)


class CommandsAreRealTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = studio()
        cls.subs = subcommands(cls.module)
        cls.commands = {p.stem for p in (ROOT / "commands").glob("*.md") if p.name != "README.md"}

    def test_parser_knows_the_documented_lifecycle(self):
        self.assertEqual(self.subs, {"doctor", "install", "update", "uninstall", "migrate"})

    def test_every_studio_subcommand_taught_exists(self):
        for rel in TEACHING_DOCS:
            named = set(re.findall(r"studio\.py ([a-z][a-z-]+)", read(rel)))
            with self.subTest(doc=rel):
                self.assertEqual(named - self.subs, set(), f"{rel} dạy lệnh studio.py không có")

    def test_every_host_flag_value_is_a_real_host(self):
        for rel in TEACHING_DOCS:
            values = set(re.findall(r"--host ([a-z][a-z-]*)", read(rel)))
            with self.subTest(doc=rel):
                self.assertEqual(values - set(HOSTS), set(), f"{rel} dùng --host không có")

    def test_every_slash_command_taught_exists(self):
        # Bảng lỗi ở troubleshooting nhắc CỐ Ý một tên lệnh đã bỏ (triệu chứng của plugin cũ).
        for rel in [d for d in TEACHING_DOCS if d != "docs/troubleshooting.md"]:
            named = set(re.findall(r"/agent-writing-studio:([a-z0-9][a-z0-9-]*)", read(rel)))
            with self.subTest(doc=rel):
                self.assertEqual(named - self.commands, set(), f"{rel} dạy lệnh / không có trong commands/")

    def test_plugin_install_lines_use_the_real_plugin_ref(self):
        for rel in HOST_PAGES + ["INSTALL.md", "README.md", "README.vi.md"]:
            for ref in re.findall(r"claude plugin (?:install|update|uninstall) (\S+)", read(rel)):
                with self.subTest(doc=rel, ref=ref):
                    self.assertEqual(ref.strip("`.,;"), PLUGIN_REF)

    def test_detector_catches_an_invented_subcommand(self):
        """Đột biến: một lệnh bịa phải bị bắt."""
        named = set(re.findall(r"studio\.py ([a-z][a-z-]+)", "chạy `python studio.py repair`"))
        self.assertEqual(named - self.subs, {"repair"})


if __name__ == "__main__":
    unittest.main()
