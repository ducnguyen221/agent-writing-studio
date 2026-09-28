"""`studio.py` — doctor · install · update · uninstall, chạy như người dùng chạy (tiến trình con).

Mọi ca chạy với **HOME giả** (`HOME` + `USERPROFILE` trỏ thư mục tạm) và **không** có biến trạm/kho
tri thức thật, nên test không đọc cấu hình host hay dữ liệu của máy đang chạy test. Station giả có
**file canary**: install, uninstall chạy xong mà canary đổi hay mất là đỏ — bộ vòng đời không bao giờ
được đụng dữ liệu người dùng.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STUDIO = ROOT / "studio.py"
VARS = ("WRITING_STUDIO_DATA", "WRITING_STUDIO_KNOWLEDGE", "OPCOS_BRAIN_PATH")
STATUSES = {"PASS", "WARN", "FAIL", "NOT_CHECKED"}


def manifest_version():
    return json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))["version"]


class StudioCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.env = {k: v for k, v in os.environ.items() if k not in VARS}
        self.env.update({"HOME": str(self.home), "USERPROFILE": str(self.home),
                         "PYTHONIOENCODING": "utf-8"})

    def tearDown(self):
        self._tmp.cleanup()

    def run_studio(self, *args, env=None, script=STUDIO):
        return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True,
                              encoding="utf-8", env=env or self.env, cwd=str(self.tmp))

    def doctor(self, env=None):
        result = self.run_studio("doctor", "--json", env=env)
        rows = {row["check"]: row for row in json.loads(result.stdout)}
        return result.returncode, rows


class DoctorTests(StudioCase):
    def test_doctor_on_a_bare_machine_has_no_fail(self):
        code, rows = self.doctor()
        self.assertEqual(code, 0, [r for r in rows.values() if r["status"] == "FAIL"])
        self.assertTrue(set(r["status"] for r in rows.values()) <= STATUSES)
        for check in ("python", "repo", "manifest", "genres", "samples", "data", "knowledge"):
            self.assertIn(check, rows)

    def test_no_hidden_home_default_for_data_or_knowledge(self):
        """HOME giả có sẵn `.writing` và một kho tri thức, nhưng không biến nào đặt ⇒ không đoán."""
        (self.home / ".writing" / "work").mkdir(parents=True)
        (self.home / "Brain").mkdir()
        _, rows = self.doctor()
        self.assertIn("workspace", rows["data"]["detail"])
        self.assertNotIn(".writing", rows["data"]["detail"])
        self.assertEqual(rows["knowledge"]["status"], "NOT_CHECKED")

    def test_station_env_is_used_and_a_missing_station_is_a_warning(self):
        env = dict(self.env, WRITING_STUDIO_DATA=str(self.tmp / "khong-co"))
        code, rows = self.doctor(env)
        self.assertEqual(rows["data"]["status"], "WARN")
        self.assertEqual(code, 0)

    def test_knowledge_variable_new_name_passes_legacy_name_warns(self):
        vault = self.tmp / "kho"
        vault.mkdir()
        _, rows = self.doctor(dict(self.env, WRITING_STUDIO_KNOWLEDGE=str(vault)))
        self.assertEqual(rows["knowledge"]["status"], "PASS")
        _, rows = self.doctor(dict(self.env, OPCOS_BRAIN_PATH=str(vault)))
        self.assertEqual(rows["knowledge"]["status"], "WARN")
        self.assertNotIn(str(vault), rows["knowledge"]["detail"], "doctor không in đường kho tri thức")

    def test_claude_plugin_ledger_is_read_not_guessed(self):
        _, rows = self.doctor()
        self.assertEqual(rows["host:claude"]["status"], "NOT_CHECKED")
        ledger = self.home / ".claude" / "plugins" / "installed_plugins.json"
        ledger.parent.mkdir(parents=True)
        key = "agent-writing-studio@agent-writing-studio"
        ledger.write_text(json.dumps({"version": 2, "plugins": {key: [{"version": "0.1.2"}]}}),
                          encoding="utf-8")
        _, rows = self.doctor()
        self.assertEqual(rows["host:claude"]["status"], "WARN")
        ledger.write_text(json.dumps({"version": 2, "plugins": {key: [{"version": manifest_version()}]}}),
                          encoding="utf-8")
        _, rows = self.doctor()
        self.assertEqual(rows["host:claude"]["status"], "PASS")

    def test_plain_output_is_one_line_per_check(self):
        result = self.run_studio("doctor")
        lines = [line for line in result.stdout.splitlines() if line.strip()]
        self.assertTrue(lines)
        for line in lines:
            self.assertIn(line.split()[0], STATUSES)


class InstallUninstallTests(StudioCase):
    def make_station(self):
        station = self.tmp / "station"
        (station / "work" / "ca-cu").mkdir(parents=True)
        canary = station / "work" / "ca-cu" / "draft.md"
        canary.write_text("bản nháp của người dùng", encoding="utf-8")
        return station, canary

    def test_install_creates_the_station_folders_and_keeps_existing_data(self):
        station, canary = self.make_station()
        result = self.run_studio("install", "--station", str(station))
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ("work", "out", "corpus"):
            self.assertTrue((station / name).is_dir(), name)
        self.assertEqual(canary.read_text(encoding="utf-8"), "bản nháp của người dùng")
        again = self.run_studio("install", "--station", str(station))
        self.assertEqual(again.returncode, 0)
        self.assertIn("giữ nguyên", again.stdout)
        self.assertIn("claude plugin install", again.stdout)

    def test_install_uses_the_station_variable(self):
        station, _ = self.make_station()
        result = self.run_studio("install", env=dict(self.env, WRITING_STUDIO_DATA=str(station)))
        self.assertEqual(result.returncode, 0)
        self.assertTrue((station / "corpus").is_dir())

    def test_dry_run_creates_nothing(self):
        station = self.tmp / "moi"
        result = self.run_studio("install", "--station", str(station), "--dry-run")
        self.assertEqual(result.returncode, 0)
        self.assertIn("sẽ tạo", result.stdout)
        self.assertFalse(station.exists())

    def test_workspace_mode_targets_the_repo_dot_work(self):
        result = self.run_studio("install", "--dry-run")
        self.assertEqual(result.returncode, 0)
        self.assertIn(str(ROOT / ".work"), result.stdout)

    def test_install_refuses_a_station_inside_the_source_tree(self):
        target = ROOT / "skills" / "khong-duoc-tao"
        result = self.run_studio("install", "--station", str(target))
        self.assertEqual(result.returncode, 2)
        self.assertFalse(target.exists())

    def test_install_never_edits_host_configuration(self):
        station, _ = self.make_station()
        self.run_studio("install", "--station", str(station), "--host", "claude")
        self.assertEqual(list(self.home.iterdir()), [], "install không được ghi gì vào HOME")

    def test_uninstall_prints_host_steps_and_leaves_data_alone(self):
        station, canary = self.make_station()
        result = self.run_studio("uninstall", env=dict(self.env, WRITING_STUDIO_DATA=str(station)))
        self.assertEqual(result.returncode, 0)
        self.assertIn("claude plugin uninstall", result.stdout)
        self.assertIn("KHÔNG bị đụng", result.stdout)
        self.assertEqual(canary.read_text(encoding="utf-8"), "bản nháp của người dùng")

    def test_every_host_has_install_and_uninstall_guidance(self):
        for host in ("claude", "codex", "antigravity", "claude-desktop"):
            with self.subTest(host=host):
                self.assertEqual(self.run_studio("install", "--dry-run", "--host", host).returncode, 0)
                self.assertEqual(self.run_studio("uninstall", "--host", host).returncode, 0)

    def test_unknown_arguments_are_refused(self):
        self.assertEqual(self.run_studio("install", "--host", "khong-co").returncode, 2)
        self.assertEqual(self.run_studio("khong-co-lenh").returncode, 2)


@unittest.skipUnless(shutil.which("git"), "cần git")
class UpdateTests(StudioCase):
    """`update` chạy trên một repo git tạm có bản chép `studio.py` — không bao giờ đụng repo thật."""

    def make_checkout(self):
        checkout = self.tmp / "checkout"
        checkout.mkdir()
        shutil.copyfile(STUDIO, checkout / "studio.py")
        (checkout / "README.md").write_text("bản đầu\n", encoding="utf-8")
        ident = ["-c", "user.name=test", "-c", "user.email=test@example.invalid"]
        for argv in (["init", "-q"], ["add", "-A"], [*ident, "commit", "-q", "-m", "init"]):
            subprocess.run(["git", "-C", str(checkout), *argv], check=True, capture_output=True)
        return checkout

    def test_update_refuses_a_dirty_checkout(self):
        checkout = self.make_checkout()
        (checkout / "README.md").write_text("sửa dở\n", encoding="utf-8")
        result = self.run_studio("update", "--yes", script=checkout / "studio.py")
        self.assertEqual(result.returncode, 2)
        self.assertEqual((checkout / "README.md").read_text(encoding="utf-8"), "sửa dở\n")

    def test_update_without_yes_only_prints_the_plan(self):
        checkout = self.make_checkout()
        result = self.run_studio("update", script=checkout / "studio.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("git pull --ff-only", result.stdout)


if __name__ == "__main__":
    unittest.main()
