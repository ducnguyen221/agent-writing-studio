"""Cổng cho `.github/workflows/tests.yml`.

CI chỉ chạy thật sau khi repo được push, nên lỗi kiểu thiếu một hệ điều hành, action trôi theo tag
hay chỉ chạy một trong hai runner **không lộ ra ở máy** — nó lộ ra lúc mở pull request, tức sau khi
mọi thứ đã rời tay. Bộ test này kiểm tại chỗ đúng những thứ hỏng theo kiểu đó.

Viết bằng `unittest` để `python -m unittest discover` và `pytest` cùng đếm được nó.
"""

import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "tests.yml"
MIN_PYTHON = "3.10"


def load_workflow():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def triggers(workflow):
    # `on:` bị YAML 1.1 đọc thành boolean True — chấp nhận cả hai cách viết.
    return workflow.get("on", workflow.get(True))


class WorkflowShapeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not WORKFLOW.is_file():
            raise AssertionError("repo phải có .github/workflows/tests.yml")
        cls.wf = load_workflow()
        cls.job = cls.wf["jobs"]["test"]

    def test_permissions_are_read_only(self):
        self.assertEqual(self.wf.get("permissions"), {"contents": "read"})

    def test_push_runs_on_every_branch_and_on_pull_requests(self):
        on = triggers(self.wf)
        self.assertIn("push", on, "workflow phải chạy khi push")
        self.assertFalse((on["push"] or {}).get("branches"), "push không được lọc nhánh")
        self.assertIn("pull_request", on)

    def test_matrix_covers_windows_and_macos(self):
        oses = self.job["strategy"]["matrix"]["os"]
        self.assertTrue(any(o.startswith("windows") for o in oses), "thiếu Windows")
        self.assertTrue(any(o.startswith("macos") for o in oses), "thiếu macOS")
        self.assertIs(
            self.job["strategy"]["fail-fast"], False,
            "fail-fast=true giấu mất lỗi của OS còn lại",
        )

    def test_matrix_covers_the_python_range(self):
        versions = [str(v) for v in self.job["strategy"]["matrix"]["python-version"]]
        self.assertIn(MIN_PYTHON, versions, f"ma trận thiếu bản thấp nhất {MIN_PYTHON}")
        self.assertGreaterEqual(len(versions), 3)
        self.assertNotIn("3.1", versions, "viết '3.10' trong nháy, không thì YAML đọc thành 3.1")

    def test_both_runners_are_run(self):
        runs = " ".join(step.get("run", "") for step in self.job["steps"])
        self.assertIn("pytest", runs)
        self.assertIn("unittest discover -s tests -t .", runs)
        self.assertIn("requirements-dev.txt", runs)

    def test_ci_does_not_install_optional_heavy_libraries(self):
        """Test phải xanh trên máy trần; CI cài thư viện tuỳ chọn là tự bỏ phép thử đó."""
        runs = " ".join(step.get("run", "") for step in self.job["steps"]).lower()
        for optional in ("underthesea", "python-docx", "torch"):
            self.assertNotIn(optional, runs)

    def test_every_action_is_pinned_to_a_commit_sha(self):
        loose = []
        for name, job in self.wf["jobs"].items():
            for step in job.get("steps", []):
                uses = step.get("uses")
                if uses and not re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", uses):
                    loose.append(f"{name}: {uses}")
        self.assertEqual(loose, [], "action chưa ghim SHA")

    def test_checkout_does_not_persist_credentials(self):
        for name, job in self.wf["jobs"].items():
            for step in job.get("steps", []):
                if step.get("uses", "").startswith("actions/checkout@"):
                    self.assertIs((step.get("with") or {}).get("persist-credentials"), False, name)


class DeclaredPythonTests(unittest.TestCase):
    def test_readme_and_tests_readme_state_the_same_minimum(self):
        """Hứa 3.10 ở tài liệu mà CI không đo 3.10 (hay ngược lại) là hứa suông."""
        for rel in ("README.md", "tests/README.md"):
            with self.subTest(file=rel):
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertIn(f"Python {MIN_PYTHON}", text)

    def test_requirements_dev_lists_pytest(self):
        text = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8").lower()
        for package in ("jsonschema", "pyyaml", "pytest"):
            with self.subTest(package=package):
                self.assertIn(package, text)


if __name__ == "__main__":
    unittest.main()
