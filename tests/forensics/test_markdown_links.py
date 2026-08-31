import re
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

# `docs/plans` và `docs/results` là nhật ký làm việc nội bộ: chúng nằm trên máy tác giả,
# KHÔNG đi theo repo. Chúng vẫn nằm trên đĩa nên rglob vẫn thấy — loại ra ở đây để một liên
# kết trong nhật ký cũ không làm đỏ cây public, và để test đo đúng thứ người clone nhận được.
EXCLUDED_PREFIXES = ("docs/plans/", "docs/results/")


class MarkdownLinkTests(unittest.TestCase):
    def test_local_markdown_links_resolve(self):
        broken = []
        for document in ROOT.rglob("*.md"):
            if document.relative_to(ROOT).as_posix().startswith(EXCLUDED_PREFIXES):
                continue
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
