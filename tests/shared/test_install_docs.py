"""Tài liệu cài đặt: một đường cài có thật, prompt dán ngắn, host nào cũng có hướng dẫn.

Hỏng kiểu này thì hỏng im lặng: README quay lại dạy chép thư mục `skills/` bằng tay (hai bản trôi khỏi
nhau), prompt dán dài tới mức người dùng cắt mất nửa, hay `CLAUDE.md` tự mọc luật riêng lệch
`AGENTS.md`. Test đọc đúng những chỗ đó.
"""

import html
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOSTS = ("claude", "codex", "antigravity", "claude-desktop")
SUBCOMMANDS = ("doctor", "install", "update", "uninstall")
FENCE = re.compile(r"(?ms)^```text\r?\n(.*?)^```")


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def section(text, heading):
    start = text.index(heading)
    rest = text[start + len(heading):]
    end = re.search(r"(?m)^#{2,3} ", rest)
    return rest[: end.start()] if end else rest


# README tiếng Anh (README.md) và tiếng Việt (README.vi.md) — mỗi bản có mục cài của riêng nó.
README_INSTALL = (("README.md", "## 2. Install", "default workspace"),
                  ("README.vi.md", "### Cài", "workspace mặc định"))


class ReadmeInstallTests(unittest.TestCase):
    def test_install_section_does_not_copy_skills_by_hand(self):
        for rel, heading, _ in README_INSTALL:
            install = section(read(rel), heading)
            for banned in ("cp -r", "Copy-Item", "~/.claude/skills", "~/.codex/skills"):
                with self.subTest(file=rel, banned=banned):
                    self.assertNotIn(banned, install)

    def test_skills_readme_does_not_copy_skills_by_hand(self):
        """`skills/README.md` từng dạy chép sang `~/.claude/skills/` — trái `hosts/README.md`."""
        text = read("skills/README.md")
        for banned in ("cp -r", "Copy-Item", "~/.claude/skills", "~/.codex/skills"):
            with self.subTest(banned=banned):
                self.assertNotIn(banned, text)
        self.assertIn("hosts/README.md", text, "trỏ về hướng dẫn cài theo host")

    def test_install_section_names_the_plugin_path_and_the_clone_path(self):
        for rel, heading, _ in README_INSTALL:
            install = section(read(rel), heading)
            with self.subTest(file=rel):
                self.assertIn("claude plugin install agent-writing-studio@agent-writing-studio", install)
                self.assertIn("git clone", install)
                self.assertIn("studio.py", install)
                self.assertIn("python3.12", install, "macOS gọi Python bằng tên có số phiên bản")

    def test_station_is_optional_and_shown_for_both_systems(self):
        for rel, _, default_phrase in README_INSTALL:
            readme = read(rel)
            with self.subTest(file=rel):
                self.assertIn(default_phrase, readme)
                self.assertIn("setx WRITING_STUDIO_DATA", readme)
                self.assertIn("export WRITING_STUDIO_DATA", readme)

    def test_both_readmes_explain_the_workspace_migration(self):
        for rel, _, _ in README_INSTALL:
            readme = read(rel)
            with self.subTest(file=rel):
                for needle in ("studio.py migrate", "migrate --yes", "migrate --undo --yes", ".work/"):
                    self.assertIn(needle, readme)


class InstallGuideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = read("INSTALL.md")

    def test_prompts_exist_in_two_languages_and_stay_short(self):
        prompts = section(self.text, "## Prompt copy-dán")
        blocks = FENCE.findall(prompts)
        self.assertEqual(len(blocks), 2, "cần đúng hai prompt: tiếng Việt và tiếng Anh")
        for block in blocks:
            with self.subTest(prompt=block[:30]):
                lines = [line for line in block.splitlines() if line.strip()]
                self.assertLessEqual(len(lines), 12)
                self.assertIn("INSTALL.md", block)
                self.assertIn("studio.py doctor", block)

    def test_every_lifecycle_command_is_documented(self):
        for command in SUBCOMMANDS:
            with self.subTest(command=command):
                self.assertIn(f"studio.py {command}", self.text)

    def test_both_operating_systems_are_covered(self):
        for word in ("Windows", "macOS", "winget", "brew"):
            with self.subTest(word=word):
                self.assertIn(word, self.text)

    def test_macos_gaps_are_closed(self):
        """Ba chỗ hổng macOS: tên Python có số phiên bản, kiểm biến qua login shell, plugin vẫn cần clone."""
        self.assertIn("python3.12", self.text)
        self.assertIn("zsh -lic", self.text)
        plugin = section(self.text, "### 3a.")
        self.assertIn("3b", plugin, "đường plugin phải nói cách có studio.py cho bước doctor")
        self.assertIn("doctor", plugin)

    def test_error_table_lives_in_troubleshooting(self):
        self.assertIn("docs/troubleshooting.md", section(self.text, "## Lỗi hay gặp"))
        self.assertNotIn("| Triệu chứng |", self.text, "bảng lỗi đã dời sang docs/troubleshooting.md")
        self.assertIn("| Triệu chứng |", read("docs/troubleshooting.md"))

    def test_every_documented_flag_exists_in_studio(self):
        source = read("studio.py")
        for flag in set(re.findall(r"studio\.py \w+[^\n`]*?(--[a-z-]+)", self.text)):
            with self.subTest(flag=flag):
                self.assertIn(f'"{flag}"', source)


class HostAndPointerTests(unittest.TestCase):
    def test_every_host_has_a_readme(self):
        for host in HOSTS:
            with self.subTest(host=host):
                self.assertTrue((ROOT / "hosts" / host / "README.md").is_file())
        index = read("hosts/README.md")
        for host in HOSTS:
            self.assertIn(f"{host}/README.md", index)

    def test_claude_and_gemini_files_only_point_to_agents(self):
        for name in ("CLAUDE.md", "GEMINI.md"):
            with self.subTest(file=name):
                text = read(name)
                self.assertIn("AGENTS.md", text)
                self.assertLess(len(text.split()), 80, f"{name} là con trỏ, không chứa luật riêng")

    def test_agents_routes_every_axis_to_its_skill_file(self):
        text = read("AGENTS.md")
        for axis in ("01-context-architect", "02-cowriter", "03-critique", "04-humanizer", "05-forensics"):
            with self.subTest(axis=axis):
                self.assertIn(f"skills/{axis}/SKILL.md", text)


class WebInstallTests(unittest.TestCase):
    """Trang giới thiệu và trang `/install/` nói cùng một đường cài với INSTALL.md."""

    def test_landing_page_does_not_teach_copying_skills(self):
        page = read("index.html")
        for banned in ("cp -r", "Copy-Item"):
            with self.subTest(banned=banned):
                self.assertNotIn(banned, page)
        self.assertIn('href="install/"', page)

    def test_install_page_carries_the_same_prompts_as_install_md(self):
        page = html.unescape(read("install/index.html"))
        page_text = " ".join(re.sub(r"<[^>]+>", "", page).split())
        for block in FENCE.findall(section(read("INSTALL.md"), "## Prompt copy-dán")):
            with self.subTest(prompt=block[:30]):
                self.assertIn(" ".join(block.split()), page_text)

    def test_install_page_is_static(self):
        page = read("install/index.html")
        self.assertNotIn("<script", page)
        self.assertIn("prefers-color-scheme:dark", page)


# Trang người dùng mở ra rồi gõ lệnh theo. Mac: `python` thường không có, `python3` của hệ thống có thể
# là 3.9 (studio.py cần 3.10+) — trang nào dạy `python studio.py` phải nói tên macOS là `python3.12`.
ENTRY_PAGES = ("README.md", "README.vi.md", "GUIDE.md", "GUIDE.vi.md", "INSTALL.md", "START-HERE.md",
               "index.html", "install/index.html", "docs/troubleshooting.md", "hosts/README.md",
               *[f"hosts/{host}/README.md" for host in HOSTS])
BARE_PYTHON3 = re.compile(r"\bpython3\b(?![.\d])")


def plain(rel):
    return " ".join(re.sub(r"<[^>]+>", " ", html.unescape(read(rel))).split())


class MacPythonTests(unittest.TestCase):
    def test_every_page_teaching_studio_py_names_python312_for_macos(self):
        for rel in ENTRY_PAGES:
            text = plain(rel)
            if "python studio.py" not in text:
                continue
            with self.subTest(page=rel):
                self.assertIn("python3.12", text, "trang dạy `python studio.py` mà không nói tên lệnh trên macOS")

    def test_bare_python3_is_only_named_as_too_old(self):
        """`python3` trơn chỉ được nhắc để cảnh báo nó có thể là 3.9 — không bao giờ là lời khuyên gọi nó."""
        for rel in ENTRY_PAGES:
            for line in read(rel).splitlines():
                if BARE_PYTHON3.search(line):
                    with self.subTest(page=rel, line=line.strip()[:60]):
                        self.assertIn("3.9", line)

    def test_detector_catches_the_old_install_page_advice(self):
        """Đột biến: đúng câu `install/index.html` từng ghi trước 0.4.1."""
        line = "python studio.py install --host codex     # hoặc antigravity; macOS có thể là python3"
        self.assertTrue(BARE_PYTHON3.search(line))
        self.assertNotIn("3.9", line)
        self.assertFalse(BARE_PYTHON3.search("macOS: python3.12 studio.py doctor"))


if __name__ == "__main__":
    unittest.main()
