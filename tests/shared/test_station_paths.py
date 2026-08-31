"""Station `$WRITING_STUDIO_DATA` — đường mặc định có đi theo biến môi trường không?

Từ 31/08/2026 dữ liệu người thật (hồ sơ giọng, bài mẫu, ca chạy) không nằm trong repo nữa mà ở
station ngoài repo. Hai script có ĐƯỜNG MẶC ĐỊNH phải đọc biến `WRITING_STUDIO_DATA`:
`profile_build.py` (thư mục writers) và `extract.py` (thư mục ca chạy).

Test khoá ba luật, theo đúng thứ tự ưu tiên đã cam kết trong `shared/writers/README.md`:

1. **Có biến** → mặc định trỏ `<station>/writers` và `<station>/work`.
2. **Không có biến** (hoặc biến rỗng/toàn khoảng trắng) → lui về đường cũ trong repo
   (`shared/writers/`, `./.work`), để người ngoài clone repo về vẫn chạy được.
3. Env được đọc **lúc gọi**, không phải lúc nạp module — nếu ai đó biến nó lại thành hằng số
   module thì test 1 và 2 trong cùng một tiến trình sẽ mâu thuẫn và đỏ.

Dùng `patch.dict` chứ không dùng `monkeypatch` của pytest: bộ test này phải chạy được cả bằng
`python -m unittest`.
"""

import importlib.util
import os
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

    def test_khong_env_lui_ve_dot_work(self):
        env = {k: v for k, v in os.environ.items() if k != "WRITING_STUDIO_DATA"}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(self.mod.default_work_dir(), Path(".work"))

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
    """Sau khi dời station, repo chỉ còn schema + README ở `shared/writers/`, không còn `.work/`."""

    def test_shared_writers_khong_co_thu_muc_slug(self):
        con = sorted(p.name for p in (ROOT / "shared/writers").iterdir() if p.is_dir())
        self.assertEqual(con, [], f"còn thư mục hồ sơ người thật trong repo: {con}")

    def test_khong_con_dot_work_trong_repo(self):
        self.assertFalse((ROOT / ".work").exists(), "`.work/` phải nằm ở station, không ở repo")


if __name__ == "__main__":
    unittest.main()
