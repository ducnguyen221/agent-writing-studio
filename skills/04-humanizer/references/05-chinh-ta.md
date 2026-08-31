# Chính tả — phụ thuộc tuỳ chọn, không phải thành phần của repo

## 1. Quyết định cấp phép: KHÔNG vendor

Kiểm tay các bộ từ điển chính tả tiếng Việt dạng hunspell ngày 30/08/2026, xác nhận lại ở Phase 3:

- Bộ trưởng thành nhất **không có file `LICENSE`** ở gốc. API license của GitHub vì thế trả rỗng —
  rỗng ở đây nghĩa là "không xác định được", không nghĩa là "tự do dùng".
- Điều khoản duy nhất tìm được nằm trong README của thư mục từ điển: dữ liệu bắt nguồn từ gói GNU
  Aspell tiếng Việt của Hồ Ngọc Đức, **Copyright Terms: GPLv2**.
- GPLv2 là copyleft. Mang một file `.dic` hoặc `.aff` vào đây sẽ kéo nghĩa vụ cấp phép sang cả repo
  này, vốn không phải là repo GPL.

**Kết luận vận hành:** không vendor một dòng nào. Không rút danh sách từ ra khỏi từ điển. Không sinh
một file dẫn xuất nào từ nó. Sổ xưởng giữ bản kiểm chi tiết (không nằm trong repo).

Repo này vì vậy **không có bộ kiểm chính tả**. Đó là lựa chọn, không phải thiếu sót.

---

## 2. Người dùng tự cài (tuỳ chọn)

Nếu muốn có kiểm chính tả trong lượt hai, người dùng tự cài từ điển trên máy mình. Việc cài đó nằm
ngoài repo và không tạo ràng buộc cấp phép cho repo.

Ba đường phổ biến, xếp theo mức dễ:

1. **Bộ soạn thảo có sẵn.** Microsoft Word, LibreOffice và Google Docs đều có gói tiếng Việt. Đây là
   lựa chọn mặc định: không cài gì thêm, và tác giả nhìn thấy gạch chân ngay trong file của mình.
2. **Hunspell trên máy.** Cài `hunspell` qua trình quản lý gói của hệ điều hành, rồi cài gói từ điển
   tiếng Việt do bản phân phối cung cấp. Kiểm bằng `hunspell -d vi_VN -l <file>` để in ra danh sách
   từ lạ.
3. **Trình kiểm tra chính tả tiếng Việt khác** mà người dùng đã tin dùng. Trục 4 không xếp hạng công
   cụ.

Trục 4 **không tự cài gì**, không tải từ điển về, và không nhắc lại đề nghị này nếu người dùng đã từ
chối một lần.

---

## 3. Hai chuẩn đặt dấu — không được coi là lỗi

Từ điển tiếng Việt thường có hai biến thể: **kiểu cũ** (`hòa`, `thủy`, `úy`) và **kiểu mới** (`hoà`,
`thuỷ`, `uý`). Cả hai đều đúng chính tả; khác nhau ở quy ước đặt dấu thanh, không ở đúng sai.

Luật cho trục 4:

- **Không đổi kiểu đặt dấu của tác giả.** Đây là thói quen gõ, thuộc "chi tiết người phải giữ"
  (`03-chong-sua-oan.md` mục 3).
- **Trộn hai kiểu trong một bài** là điều đáng nói với tác giả, nhưng chỉ ở mức hỏi. `counters.py`
  xuất `unicode.tone_style` với ba trường `old` / `new` / `mixed`; con số đó là mô tả, không phải
  lệnh sửa. Bài ghép từ nhiều nguồn hợp pháp cũng trộn.
- **Chọn kiểu nào khi tác giả nhờ thống nhất:** hỏi tác giả, không tự quyết. Nếu writer profile có
  trường `tone_style` thì theo profile.

---

## 4. Lỗi chính tả nói về ai

Lỗi chính tả nói về **người gõ**, không nói về máy. Một bài nhiều lỗi gõ là bằng chứng có người ngồi
gõ, không phải bằng chứng ngược lại. Trục 4 không được dùng mật độ lỗi chính tả làm tín hiệu nguồn
gốc, và trục 5 cũng không.

Khi sửa lỗi chính tả, ba chỗ vẫn thuộc vùng bảo vệ:

- **Trích dẫn nguyên văn** — kể cả lỗi nằm trong trích dẫn. Sai thì ghi `[sic]`, đừng sửa.
- **Tên riêng** — người, tổ chức, địa danh, tên sản phẩm. Hỏi, đừng đoán.
- **`known_typos[]` của writer profile**, nếu có. Sửa được, nhưng phải liệt kê ra cho tác giả, không
  sửa lặng lẽ.
