"""NOTICE + `provenance.json`: thứ repo mang theo và thứ nó gọi tới đều có nguồn và giấy phép.

Hỏng kiểu này thì hỏng im lặng: ai đó sửa kho thành ngữ mà không ai nhìn lại giấy phép, thêm một thư
viện tuỳ chọn mà NOTICE không kể, hay gỡ notice MIT vì "trông gọn hơn". Test khoá bốn điều:

1. mỗi file `bundled` tồn tại và mã băm (nội dung chuẩn hoá LF) khớp — sửa file là phải nhìn lại nguồn;
2. file bundled giữ commit nguồn đã ghim (40 ký tự hex) ở đúng trường provenance chỉ;
3. mọi thư viện tuỳ chọn mà `studio.py doctor` kiểm và mọi dòng `requirements-dev.txt` đều có trong
   `runtime_optional` kèm giấy phép, và NOTICE nhắc tên chúng;
4. không thành phần nào tự nhận là đi kèm mà thật ra là thư viện ngoài.
"""

import hashlib
import importlib.util
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def sha256_lf(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def studio_module():
    spec = importlib.util.spec_from_file_location("studio_for_provenance", ROOT / "studio.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dotted(data, dotted_path):
    for key in dotted_path.split("."):
        data = data[key]
    return data


class ProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prov = load("provenance.json")
        cls.notice = (ROOT / "NOTICE").read_text(encoding="utf-8")

    def test_notice_points_to_license_and_provenance(self):
        self.assertIn("MIT", self.notice)
        self.assertIn("LICENSE", self.notice)
        self.assertIn("provenance.json", self.notice)
        self.assertTrue((ROOT / "LICENSE").is_file())

    def test_bundled_files_exist_and_hashes_match(self):
        self.assertTrue(self.prov["bundled"], "phải kê ít nhất kho thành ngữ")
        for item in self.prov["bundled"]:
            with self.subTest(path=item["path"]):
                path = ROOT / item["path"]
                self.assertTrue(path.is_file())
                self.assertEqual(sha256_lf(path), item["sha256"],
                                 "file bundled đã đổi — xem lại nguồn/giấy phép rồi cập nhật sha256")
                self.assertIn(item["path"], self.notice)

    def test_bundled_data_keeps_its_pinned_upstream_commit(self):
        for item in self.prov["bundled"]:
            with self.subTest(path=item["path"]):
                data = load(item["path"])
                for field in ("upstream_commit_field", "upstream_blob_field"):
                    self.assertRegex(dotted(data, item[field]), HEX40)
                self.assertEqual(dotted(data, "attribution.license"), item["license"])

    def test_every_optional_library_is_declared_with_a_license(self):
        declared = {entry["name"].lower(): entry for entry in self.prov["runtime_optional"]}
        wanted = {package.lower() for _, package, _ in studio_module().OPTIONAL_LIBS}
        for line in (ROOT / "requirements-dev.txt").read_text(encoding="utf-8").splitlines():
            name = re.split(r"[<>=!~\s\[]", line.strip(), maxsplit=1)[0]
            if name and not name.startswith("#"):
                wanted.add(name.lower())
        for name in sorted(wanted):
            with self.subTest(package=name):
                self.assertIn(name, declared, "thư viện chưa khai trong provenance.json")
                self.assertTrue(declared[name]["license"].strip())
                self.assertFalse(declared[name]["bundled"], "thư viện ngoài không đi kèm repo")
                self.assertIn(declared[name]["name"], self.notice)

    def test_checked_date_is_iso(self):
        self.assertRegex(self.prov["checked"], r"^\d{4}-\d{2}-\d{2}$")

    def test_methods_are_not_vendored(self):
        self.assertIs(self.prov["methods_distilled"]["code_copied"], False)
        self.assertTrue((ROOT / self.prov["methods_distilled"]["fence"]).is_file())

    def test_hash_detector_catches_an_edit(self):
        """Đột biến: đổi một byte thì mã băm phải đổi — không để phép so thành xanh giả."""
        path = ROOT / self.prov["bundled"][0]["path"]
        raw = path.read_bytes().replace(b"\r\n", b"\n")
        self.assertNotEqual(hashlib.sha256(raw + b" ").hexdigest(), sha256_lf(path))


if __name__ == "__main__":
    unittest.main()
