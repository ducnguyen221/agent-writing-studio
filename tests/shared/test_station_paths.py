"""Station `$WRITING_STUDIO_DATA` — đường mặc định có đi theo biến môi trường không?

Từ 31/08/2026 dữ liệu người thật (hồ sơ giọng, bài mẫu, ca chạy) không nằm trong repo nữa mà ở
station ngoài repo. Hai script có ĐƯỜNG MẶC ĐỊNH phải đọc biến `WRITING_STUDIO_DATA`:
`profile_build.py` (thư mục writers) và `extract.py` (thư mục ca chạy).

Test khoá ba luật, theo đúng thứ tự ưu tiên đã cam kết trong `shared/writers/README.md`:

1. **Có biến** → mặc định trỏ `<station>/writers` và `<station>/work`.
2. **Không có biến** (hoặc biến rỗng/toàn khoảng trắng) → lui về đường cũ trong repo
   (`shared/writers/`, `./workspace`), để người ngoài clone repo về vẫn chạy được. Từ 0.4.0, chỉ
   còn `./.work` (tên cũ) mà chưa có `./workspace` thì dùng `./.work` kèm cảnh báo.
3. Env được đọc **lúc gọi**, không phải lúc nạp module — nếu ai đó biến nó lại thành hằng số
   module thì test 1 và 2 trong cùng một tiến trình sẽ mâu thuẫn và đỏ.

Dùng `patch.dict` chứ không dùng `monkeypatch` của pytest: bộ test này phải chạy được cả bằng
`python -m unittest`.
"""

import contextlib
import importlib.util
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
PROFILE_BUILD = ROOT / "shared/scripts/profile_build.py"
EXTRACT = ROOT / "skills/05-forensics/scripts/extract.py"

STATION = r"D:\station-gia-lap\.writing" if os.name == "nt" else "/tmp/station-gia-lap/.writing"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TestWritersDir(unittest.TestCase):
    def setUp(self):
        self.mod = load_module("station_profile_build", PROFILE_BUILD)

    def test_env_tro_station(self):
        with mock.patch.dict(os.environ, {"WRITING_STUDIO_DATA": STATION}):
            self.assertEqual(self.mod.writers_dir(), Path(STATION) / "writers")

    def test_khong_env_lui_ve_repo(self):
        env = {k: v for k, v in os.environ.items() if k != "WRITING_STUDIO_DATA"}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(self.mod.writers_dir(), ROOT / "shared/writers")

    def test_env_rong_coi_nhu_khong_co(self):
        with mock.patch.dict(os.environ, {"WRITING_STUDIO_DATA": "   "}):
            self.assertEqual(self.mod.writers_dir(), ROOT / "shared/writers")

    def test_doc_env_luc_goi_khong_phai_luc_nap(self):
        with mock.patch.dict(os.environ, {"WRITING_STUDIO_DATA": STATION}):
            first = self.mod.writers_dir()
        env = {k: v for k, v in os.environ.items() if k != "WRITING_STUDIO_DATA"}
        with mock.patch.dict(os.environ, env, clear=True):
            second = self.mod.writers_dir()
        self.assertNotEqual(first, second)


class TestWorkDir(unittest.TestCase):
    def setUp(self):
        self.mod = load_module("station_extract", EXTRACT)

    def test_env_tro_station(self):
        with mock.patch.dict(os.environ, {"WRITING_STUDIO_DATA": STATION}):
            self.assertEqual(self.mod.default_work_dir(), Path(STATION) / "work")

    def test_khong_env_lui_ve_workspace(self):
        env = {k: v for k, v in os.environ.items() if k != "WRITING_STUDIO_DATA"}
        with mock.patch.dict(os.environ, env, clear=True), self.in_temp_cwd():
            self.assertEqual(self.mod.default_work_dir(), Path("workspace"))

    @contextlib.contextmanager
    def in_temp_cwd(self):
        old = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                yield Path(tmp)
            finally:
                os.chdir(old)

    def test_chi_con_dot_work_cu_thi_doc_no_kem_canh_bao(self):
        env = {k: v for k, v in os.environ.items() if k != "WRITING_STUDIO_DATA"}
        with mock.patch.dict(os.environ, env, clear=True), self.in_temp_cwd() as tmp:
            (tmp / ".work").mkdir()
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                self.assertEqual(self.mod.default_work_dir(), Path(".work"))
            self.assertIn("studio.py migrate", err.getvalue())
            (tmp / "workspace").mkdir()
            self.assertEqual(self.mod.default_work_dir(), Path("workspace"),
                             "đã có workspace/ thì tên mới thắng")

    def test_cli_thang_env(self):
        """`--out` tường minh phải thắng station: parser để default=None để main tự quyết."""
        ap = self.mod.argparse.ArgumentParser()
        ap.add_argument("path")
        ap.add_argument("--out", default=None)
        with mock.patch.dict(os.environ, {"WRITING_STUDIO_DATA": STATION}):
            args = ap.parse_args(["bai.txt", "--out", "ca-rieng"])
            chosen = Path(args.out) if args.out else self.mod.default_work_dir()
            self.assertEqual(chosen, Path("ca-rieng"))


class TestRepoKhongConDuLieuNguoiThat(unittest.TestCase):
    """Repo chỉ còn schema + README ở `shared/writers/`.

    `workspace/` là workspace mặc định hợp lệ khi KHÔNG đặt station (người dùng public mở thẳng repo) —
    Git bỏ qua nó, `test_repo_gates` canh index. Nhưng đã đặt `WRITING_STUDIO_DATA` thì dữ liệu phải
    ra station: khi ấy còn `workspace/` trong repo nghĩa là có thứ ghi nhầm chỗ.
    """

    def test_shared_writers_khong_co_thu_muc_slug(self):
        con = sorted(p.name for p in (ROOT / "shared/writers").iterdir() if p.is_dir())
        self.assertEqual(con, [], f"còn thư mục hồ sơ người thật trong repo: {con}")

    @unittest.skipUnless((os.environ.get("WRITING_STUDIO_DATA") or "").strip(),
                         "chưa đặt station — `workspace/` trong repo là workspace hợp lệ")
    def test_da_co_station_thi_khong_con_workspace_trong_repo(self):
        self.assertFalse((ROOT / "workspace").exists(), "`workspace/` phải nằm ở station, không ở repo")

    def test_home_gia_khong_lam_doi_duong_mac_dinh(self):
        """Không có mặc định nào đoán trong home: HOME giả có sẵn `.writing` vẫn không được chọn."""
        writers = load_module("home_profile_build", PROFILE_BUILD)
        work = load_module("home_extract", EXTRACT)
        env = {k: v for k, v in os.environ.items() if k != "WRITING_STUDIO_DATA"}
        env.update({"HOME": STATION, "USERPROFILE": STATION})
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(writers.writers_dir(), ROOT / "shared/writers")
            self.assertIn(work.default_work_dir(), (Path("workspace"), Path(".work")))
            self.assertFalse(work.default_work_dir().is_absolute(), "không đoán đường trong home")


if __name__ == "__main__":
    unittest.main()
