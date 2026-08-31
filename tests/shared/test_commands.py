"""`commands/` — bảy lệnh chạy lẻ từng bước có đúng hợp đồng không?

Lệnh là **cửa vào hẹp**: người dùng gõ `/agent-writing-studio:phan-bien` là muốn chạy ĐÚNG một bước,
không phải khởi động lại cả chuỗi. Ba thứ hỏng thì hỏng im lặng, nên bị khoá ở đây:

1. **`description` phải là tiếng Anh** — đó là câu harness đọc để định tuyến (luật ngôn ngữ tài liệu:
   frontmatter tiếng Anh, thân tiếng Việt). Một dòng mô tả tiếng Việt vẫn "chạy" nhưng định tuyến kém.
2. **Mỗi lệnh phải nói rõ đầu vào của nó ở đâu và thiếu thì làm gì** — không thì agent sẽ tự phỏng
   vấn lại, tự bịa bối cảnh, tự chạy lại chuỗi; đúng thứ lệnh sinh ra để tránh.
3. **`danh-sach` không được chép cứng bảng** — bảng chép cứng + bảy file lệnh = hai nguồn sự thật,
   lệch nhau ngay lần sửa đầu.
"""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMANDS = ROOT / "commands"

# Thứ tự chuỗi công việc; `danh-sach` là lệnh tra cứu, đứng ngoài chuỗi.
CHUOI = ("boi-canh", "viet-nhap", "phan-bien", "bien-tap", "giam-dinh", "giao-docx")
MONG_DOI = set(CHUOI) | {"danh-sach"}

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
# Dấu tiếng Việt: đủ để bắt một `description` lỡ viết bằng tiếng Việt.
DAU_TIENG_VIET = re.compile(r"[ăâđêôơưĂÂĐÊÔƠƯáàảãạấầẩẫậéèẻẽẹíìỉĩịóòỏõọúùủũụýỳỷỹỵ]")


def doc(ten):
    return (COMMANDS / f"{ten}.md").read_text(encoding="utf-8")


def frontmatter(text):
    khop = FRONTMATTER.match(text)
    assert khop, "file lệnh phải mở đầu bằng frontmatter YAML"
    return khop.group(1)


class BoLenhTests(unittest.TestCase):
    def test_dung_bay_lenh_khong_thua_khong_thieu(self):
        tren_dia = {path.stem for path in COMMANDS.glob("*.md")}
        self.assertEqual(tren_dia, MONG_DOI)


class FrontmatterTests(unittest.TestCase):
    def test_moi_lenh_co_description(self):
        for ten in sorted(MONG_DOI):
            with self.subTest(lenh=ten):
                self.assertRegex(frontmatter(doc(ten)), r"(?m)^description: \S")

    def test_description_viet_bang_tieng_anh(self):
        """Frontmatter là thứ harness đọc để định tuyến — giữ tiếng Anh, thân bài tiếng Việt."""
        for ten in sorted(MONG_DOI):
            with self.subTest(lenh=ten):
                dong = [
                    d for d in frontmatter(doc(ten)).splitlines() if d.startswith("description:")
                ][0]
                self.assertIsNone(
                    DAU_TIENG_VIET.search(dong), f"{ten}.md: `description` đang viết tiếng Việt"
                )

    def test_moi_lenh_co_argument_hint(self):
        for ten in sorted(MONG_DOI):
            with self.subTest(lenh=ten):
                self.assertRegex(frontmatter(doc(ten)), r"(?m)^argument-hint: \S")

    def test_than_bai_viet_tieng_viet(self):
        for ten in sorted(MONG_DOI):
            with self.subTest(lenh=ten):
                than = doc(ten)[FRONTMATTER.match(doc(ten)).end():]
                self.assertIsNotNone(DAU_TIENG_VIET.search(than), f"{ten}.md: thân bài không phải tiếng Việt")


class HopDongThanBaiTests(unittest.TestCase):
    def test_moi_lenh_nhan_arguments(self):
        for ten in sorted(MONG_DOI):
            with self.subTest(lenh=ten):
                self.assertIn("$ARGUMENTS", doc(ten))

    def test_lenh_trong_chuoi_noi_ro_thu_muc_ca(self):
        for ten in CHUOI:
            with self.subTest(lenh=ten):
                text = doc(ten)
                self.assertIn("$WRITING_STUDIO_DATA/work/", text)
                self.assertIn(".work/", text, f"{ten}.md thiếu đường lui khi chưa đặt station")

    def test_lenh_trong_chuoi_deu_co_o_tom_tat_cho_danh_sach(self):
        """`danh-sach` đọc đúng khối này; thiếu nó là bảng thủng một dòng."""
        for ten in CHUOI:
            with self.subTest(lenh=ten):
                text = doc(ten)
                self.assertIn("## Tóm tắt cho `/agent-writing-studio:danh-sach`", text)
                for nhan in ("**Trục:**", "**Làm gì:**", "**Cần đầu vào:**", "**Ra file:**"):
                    self.assertIn(nhan, text, f"{ten}.md thiếu dòng {nhan}")

    def test_lenh_can_buoc_truoc_deu_chi_ra_lenh_sinh_ra_dau_vao(self):
        """Thiếu artifact thì nói thiếu gì + lệnh nào tạo ra nó, KHÔNG tự chạy lại cả chuỗi."""
        for ten in ("viet-nhap", "phan-bien", "bien-tap", "giam-dinh", "giao-docx"):
            with self.subTest(lenh=ten):
                text = doc(ten)
                self.assertRegex(
                    text,
                    r"/agent-writing-studio:(boi-canh|viet-nhap|phan-bien|bien-tap)",
                    f"{ten}.md không chỉ ra lệnh sinh ra đầu vào của nó",
                )

    def test_khong_lenh_nao_tu_chay_lai_ca_chuoi(self):
        for ten in CHUOI:
            with self.subTest(lenh=ten):
                self.assertIn("## Chỉ làm đúng bước này", doc(ten))


class DanhSachTests(unittest.TestCase):
    def test_danh_sach_doc_dong_khong_chep_cung_bang(self):
        text = doc("danh-sach")
        bang = [d for d in text.splitlines() if d.lstrip().startswith("|")]
        self.assertEqual(bang, [], "`danh-sach.md` đang chép cứng bảng thay vì đọc file lệnh anh em")

    def test_danh_sach_noi_ro_doc_tu_dau(self):
        text = doc("danh-sach")
        self.assertIn("`## Tóm tắt cho /agent-writing-studio:danh-sach`", text.replace("**", ""))
        self.assertIn("cùng thư mục", text)


class LenhGiaoDocxTests(unittest.TestCase):
    def test_tro_dung_script_xuat_docx(self):
        text = doc("giao-docx")
        self.assertIn("shared/scripts/xuat_docx.py", text)
        self.assertTrue((ROOT / "shared/scripts/xuat_docx.py").is_file())

    def test_noi_ro_ban_giao_nam_o_thu_muc_nguoi_dung(self):
        """Quyết định 31/08/2026: `.writing` là xưởng của agent, không phải chỗ người dùng vào lấy bài."""
        text = doc("giao-docx")
        self.assertIn("--provenance", text)
        self.assertIn("xưởng cục bộ của agent", text)


if __name__ == "__main__":
    unittest.main()
