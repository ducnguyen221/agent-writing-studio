import re
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class MarkdownLinkTests(unittest.TestCase):
    def test_local_markdown_links_resolve(self):
        broken = []
        for document in ROOT.rglob("*.md"):
            content = document.read_text(encoding="utf-8")
            for raw_target in LINK.findall(content):
                target = raw_target.strip().strip("<>").split("#", maxsplit=1)[0]
                if not target or "://" in target or target.startswith(("mailto:", "skill:")):
                    continue
                target = unquote(target)
                resolved = (document.parent / target).resolve()
                if not resolved.exists():
                    broken.append(f"{document.relative_to(ROOT)} -> {raw_target}")
        self.assertEqual(broken, [], "Liên kết nội bộ bị gãy:\n" + "\n".join(broken))


if __name__ == "__main__":
    unittest.main()
