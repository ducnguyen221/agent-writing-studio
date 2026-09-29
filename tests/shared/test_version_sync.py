"""Một số phiên bản cho mọi chỗ khai phiên bản.

Repo không có gói Python, nên nguồn phiên bản là **bốn chỗ khai** phải đổi cùng lúc khi bump:
`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (mục plugin), `.codex-plugin/plugin.json`
và `CITATION.cff`. Lệch một chỗ thì marketplace của Claude, plugin của Codex và nút "Cite this
repository" nói ba phiên bản khác nhau — và không gì báo, trừ con mắt người đọc.

Test cũng khoá **tên**: bốn chỗ cùng một tên plugin, vì lệnh `/agent-writing-studio:<lệnh>` ăn theo nó.
"""

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ".claude-plugin/plugin.json"
MARKETPLACE = ".claude-plugin/marketplace.json"
CODEX = ".codex-plugin/plugin.json"
CITATION = "CITATION.cff"
NAME = "agent-writing-studio"


def versions(root=ROOT):
    """Mọi chỗ khai phiên bản -> {nơi: số}. `root` đổi được để test đột biến trên bản chép."""
    def read(rel):
        return (root / rel).read_text(encoding="utf-8")

    found = {
        PLUGIN: json.loads(read(PLUGIN)).get("version"),
        CODEX: json.loads(read(CODEX)).get("version"),
    }
    market = json.loads(read(MARKETPLACE))
    for plugin in market.get("plugins") or []:
        found[f"{MARKETPLACE}#{plugin.get('name')}"] = plugin.get("version")
    match = re.search(r"(?m)^version:\s*\"?([^\"\s]+)\"?\s*$", read(CITATION))
    found[CITATION] = match.group(1) if match else None
    return found


class VersionSyncTests(unittest.TestCase):
    def test_every_declaration_shares_one_semver(self):
        found = versions()
        self.assertEqual(len(found), 4, f"phải đúng bốn chỗ khai: {sorted(found)}")
        self.assertNotIn(None, found.values(), f"thiếu trường version: {found}")
        self.assertEqual(len(set(found.values())), 1, f"version lệch: {found}")
        self.assertRegex(next(iter(found.values())), r"^\d+\.\d+\.\d+$")

    def test_every_manifest_names_the_same_plugin(self):
        names = {json.loads((ROOT / rel).read_text(encoding="utf-8"))["name"] for rel in (PLUGIN, CODEX)}
        market = json.loads((ROOT / MARKETPLACE).read_text(encoding="utf-8"))
        names |= {market["name"]} | {plugin["name"] for plugin in market["plugins"]}
        self.assertEqual(names, {NAME})

    def test_codex_manifest_points_at_the_repo_skills(self):
        codex = json.loads((ROOT / CODEX).read_text(encoding="utf-8"))
        self.assertEqual(codex.get("skills"), "./skills/")
        self.assertTrue((ROOT / "skills").is_dir())

    def test_a_single_bump_is_caught(self):
        """Đột biến: bump một chỗ trên bản chép thì bộ đọc phải thấy lệch."""
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp)
            for rel in (PLUGIN, MARKETPLACE, CODEX, CITATION):
                (copy / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, copy / rel)
            codex = json.loads((copy / CODEX).read_text(encoding="utf-8"))
            codex["version"] = "99.0.0"
            (copy / CODEX).write_text(json.dumps(codex), encoding="utf-8")
            self.assertGreater(len(set(versions(copy).values())), 1)


if __name__ == "__main__":
    unittest.main()
