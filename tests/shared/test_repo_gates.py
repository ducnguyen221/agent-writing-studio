"""Cổng ranh giới dữ liệu: `.gitignore` chặn đúng họ file, và **Git index** không chứa thứ bị cấm.

`.gitignore` không bảo vệ file đã track hay `git add -f`. Nên có hai tầng kiểm:

1. `git check-ignore` — đường dữ liệu mẫu (workspace `workspace/` và tên cũ `.work/`, bí mật, bài học
   viên, hồ sơ giọng)
   phải bị bỏ qua, còn file công khai cùng thư mục (README, schema, `.env.example`) thì không;
2. `git ls-files` — cây đang track không có file nào dưới vùng dữ liệu, và không có file bí mật.

Hai tầng chỉ chạy được trong một bản checkout git thật (CI checkout, máy dev); bản tải zip không có
`.git` thì bỏ qua kèm lý do — không xanh câm.
"""

import fnmatch
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HAS_GIT = bool(shutil.which("git")) and (ROOT / ".git").exists()

# (đường, có bị bỏ qua không)
IGNORE_CASES = (
    ("workspace/bai-x/draft.md", True),
    ("workspace/.studio-migrate.json", True),
    (".work/bai-x/draft.md", True),          # tên cũ trước 0.4.0 — vẫn chặn
    (".work/bai-x/context.json", True),
    # Neo ở gốc: thư mục trùng tên nằm sâu trong cây là source, không bị chặn.
    ("skills/02-cowriter/workspace/README.md", False),
    ("shared/.work/README.md", False),
    (".venv/Lib/site.py", True),
    ("docs/plans/2026-09-29/plan.md", True),
    ("docs/results/do-lan-1.json", True),
    (".env", True),
    (".env.local", True),
    (".envrc", True),
    (".env.example", False),
    ("auth.json", True),
    ("secrets/ca.pem", True),
    ("fixtures/bai-hoc-vien.md", True),
    ("fixtures/README.md", False),
    ("fixtures/manifest.schema.json", False),
    ("shared/writers/nguoi-a/profile.yaml", True),
    ("shared/writers/nguoi-a/samples/bai-1.md", True),
    ("shared/writers/README.md", False),
    ("shared/writers/writer.schema.json", False),
    ("ban-giao.docx", True),
    ("skills/02-cowriter/SKILL.md", False),
)

# Mẫu cấm có mặt trong cây đang track (trừ ngoại lệ công khai ghi rõ).
FORBIDDEN_TRACKED = ("workspace/*", ".work/*", ".venv/*", "docs/plans/*", "docs/results/*",
                     ".env", ".env.*", "*.pem", "*.key", "auth.json",
                     "*.credentials.json", "oauth_creds.json", "*.docx", "*.pdf")
ALLOWED_TRACKED = {".env.example"}
DATA_ROOTS = {
    "fixtures/": {"fixtures/README.md", "fixtures/manifest.schema.json", "fixtures/.gitkeep"},
    "shared/writers/": {
        "shared/writers/README.md",
        "shared/writers/.gitkeep",
        "shared/writers/writer.schema.json",
        "shared/writers/audience.schema.json",
    },
}


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True,
                          encoding="utf-8")


def tracked_files():
    result = git("ls-files", "-z")
    return [path for path in result.stdout.split("\0") if path]


@unittest.skipUnless(HAS_GIT, "không có git hoặc không phải bản checkout git")
class GitIgnoreTests(unittest.TestCase):
    def test_git_really_ignores_the_data_and_not_the_public_files(self):
        for path, ignored in IGNORE_CASES:
            with self.subTest(path=path):
                result = git("check-ignore", "-q", "--no-index", path)
                self.assertEqual(result.returncode == 0, ignored, path)


@unittest.skipUnless(HAS_GIT, "không có git hoặc không phải bản checkout git")
class GitIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = tracked_files()

    def test_index_is_readable(self):
        self.assertIn("README.md", self.files)

    def test_no_forbidden_file_is_tracked(self):
        bad = [
            path for path in self.files
            if path not in ALLOWED_TRACKED
            and any(fnmatch.fnmatch(Path(path).name, pattern) or fnmatch.fnmatch(path, pattern)
                    for pattern in FORBIDDEN_TRACKED)
        ]
        self.assertEqual(bad, [], "file bị cấm đang nằm trong Git index")

    def test_data_folders_only_track_their_public_files(self):
        for prefix, allowed in DATA_ROOTS.items():
            with self.subTest(folder=prefix):
                extra = [p for p in self.files if p.startswith(prefix) and p not in allowed]
                self.assertEqual(extra, [], f"{prefix} chỉ được track README/schema")

    def test_detector_catches_a_forced_add(self):
        """Đột biến: một danh sách giả có file force-add phải bị bắt."""
        fake = ["README.md", "workspace/bai-x/draft.md", ".work/bai-x/draft.md",
                "skills/x/workspace/README.md", "shared/writers/nguoi-a/profile.yaml", ".env"]
        caught = [p for p in fake if any(fnmatch.fnmatch(p, pat) for pat in FORBIDDEN_TRACKED)]
        self.assertEqual(caught, ["workspace/bai-x/draft.md", ".work/bai-x/draft.md", ".env"])
        leaked = [p for p in fake if p.startswith("shared/writers/")
                  and p not in DATA_ROOTS["shared/writers/"]]
        self.assertEqual(leaked, ["shared/writers/nguoi-a/profile.yaml"])


if __name__ == "__main__":
    unittest.main()
