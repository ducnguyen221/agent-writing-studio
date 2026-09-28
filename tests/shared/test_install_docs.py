"""Tài liệu cài đặt: một đường cài có thật, prompt dán ngắn, host nào cũng có hướng dẫn.

Hỏng kiểu này thì hỏng im lặng: README quay lại dạy chép thư mục `skills/` bằng tay (hai bản trôi khỏi
nhau), prompt dán dài tới mức người dùng cắt mất nửa, hay `CLAUDE.md` tự mọc luật riêng lệch
`AGENTS.md`. Test đọc đúng những chỗ đó.
"""

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


class ReadmeInstallTests(unittest.TestCase):
    def test_install_section_does_not_copy_skills_by_hand(self):
        install = section(read("README.md"), "### Cài")
        for banned in ("cp -r", "Copy-Item", "~/.claude/skills", "~/.codex/skills"):
            with self.subTest(banned=banned):
                self.assertNotIn(banned, install)

    def test_install_section_names_the_plugin_path_and_the_clone_path(self):
        install = section(read("README.md"), "### Cài")
        self.assertIn("claude plugin install agent-writing-studio@agent-writing-studio", install)
        self.assertIn("git clone", install)
        self.assertIn("studio.py", install)

    def test_station_is_optional_and_shown_for_both_systems(self):
        readme = read("README.md")
        self.assertIn("workspace mặc định", readme)
        self.assertIn("setx WRITING_STUDIO_DATA", readme)
        self.assertIn("export WRITING_STUDIO_DATA", readme)


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


if __name__ == "__main__":
    unittest.main()
