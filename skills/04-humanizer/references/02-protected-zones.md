# Vùng bảo vệ

Danh sách những thứ trục 4 **không được đụng vào**. Vùng bảo vệ có hai tầng: tầng mặc định áp cho mọi
thể loại, tầng thể loại lấy từ `preserve[]` ở `§4` của `shared/genres/<genre>.md`. Hai tầng **cộng
lại**, không thay thế nhau: thể loại chỉ được mở rộng vùng bảo vệ, không được thu hẹp.

---

## 1. Tầng mặc định — mọi thể loại

| Vùng | Vì sao | Được làm gì |
|---|---|---|
| **Số liệu, đơn vị, sai số, mốc thời gian** | Đổi một con số là làm sai lệch, không phải biên tập | Không đổi. Được tách câu chứa số ra khỏi câu chứa diễn giải |
| **Trích dẫn nguyên văn** | Sửa lời người khác trong ngoặc kép là ngụy tạo | Không đổi một chữ, kể cả lỗi chính tả trong trích dẫn |
| **Nguồn, tên tác giả, năm, số hiệu văn bản** | `(Nguyễn Văn A, 2025)`, `Thông tư 23/2021/TT-BGDĐT` | Không đổi. Không "làm gọn" tên tổ chức |
| **Đường dẫn, DOI, mã, tên file** | Sửa một ký tự là hỏng | Không đổi |
| **Tên riêng: người, tổ chức, địa danh, sản phẩm** | Kể cả khi viết hoa không nhất quán — hỏi, đừng tự sửa | Chỉ thống nhất khi tác giả xác nhận |
| **Thuật ngữ chuyên môn cần thiết** | "Suy diễn" ≠ "quy nạp"; "tương quan" ≠ "nhân quả" | Bỏ phần chú giải lặp lại từ lần thứ hai trở đi, giữ thuật ngữ |
| **Code, công thức, frontmatter YAML, khối cấu hình** | Không phải văn xuôi | Không đụng, kể cả thụt lề |
| **Luận điểm và lập trường của tác giả** | Trục 4 sửa cách nói, không sửa điều được nói | Không đổi |
| **Mức mạnh của khẳng định** | Đổi "có liên hệ với" thành "dẫn tới" là đổi nội dung — và đổi ngược lại cũng thế. Xem mục 1.1 | Chỉ được làm rõ điều kiện **đã có sẵn** trong câu |
| **Trải nghiệm cá nhân do tác giả kể** | Kể cả khi kể vụng | Được rút gọn, không được xoá và không được bịa thêm |

### 1.1. Mức mạnh của khẳng định — kể cả khi `must_fix` đòi hạ

Đây là vùng bảo vệ duy nhất mà một mệnh lệnh hợp lệ của trục 3 vẫn **không** mở khoá được.

Trục 3 được phép — và thường phải — viết `must_fix` kiểu *"hạ mức khẳng định ở câu này: bài chưa có
bằng chứng cho một quan hệ nhân quả"*. Việc ấy đúng. Nhưng thi hành nó là **đổi điều được nói**, tức
là việc của vòng viết lại (`02-cowriter`, vòng 2), không phải của biên tập câu chữ. Trục 4 gặp
`must_fix` loại này thì:

1. **Không sửa.** Kể cả khi `blocking: true`.
2. Ghi một phần tử `warnings[]` dạng object:
   `{"message": "…", "route_to": "02-cowriter:round2", "sentence_id": "s0032", "must_fix_ref": "F2"}`.
3. Trả bài kèm cảnh báo đó; người dùng quyết định có mở vòng viết lại hay không.

`critique.schema.json` có trường `owner` để trục 3 nói thẳng điều này ngay lúc viết `must_fix`
(`owner: 02-cowriter`). Trục 4 đọc `owner` trước khi đọc nội dung: `owner` khác `04-humanizer` thì
dừng ở bước 2 bên trên.

**Vì sao nghiêm đến thế.** Ca cột B (mục 3 và 6 trong sổ đo nội bộ của đợt xây): trục 3 chấm
đúng một câu khái quát hoá vội, trục 4 hạ mức câu đó theo `must_fix` — nhát sửa **chính đáng**, có
`reason` cho người đọc — và người chấm mù độc lập, vốn đã gắn `NOTE` cho câu ấy ở lượt trước, thôi
gắn cờ. Không ai lách gì cả; "tốt cho người đọc" và "ít bị máy chấm để ý" đơn giản là **trùng nhau**
ở đúng ranh này, và `polish.diff.json` không tách được hai động cơ ấy ra vì cả hai sinh ra cùng một
diff. Thứ duy nhất tách được chúng là ai làm việc đó và ở bước nào: vòng viết lại có outline, có
`context.json`, có người duyệt; biên tập câu chữ thì không.

---

## 2. Tầng thể loại — đọc `preserve[]` ở `§4`

Cách đọc: mỗi khoá trong `preserve[]` là một danh mục; gặp một câu chạm vào danh mục đó thì áp luật
"không đổi" của tầng mặc định.

- `essay.md` mở rộng thêm: luận điểm và lập trường, ví dụ cá nhân do tác giả kể.
- `research.md` mở rộng nhiều nhất: sai số, ký hiệu biến và công thức, **mô tả phương pháp và tham
  số**, điều kiện và giới hạn của kết luận, tên bộ dữ liệu. Sửa một chữ trong mô tả phương pháp có
  thể làm nghiên cứu không lặp lại được nữa — đây là vùng bảo vệ nghiêm nhất trong repo.

Thể loại chưa có hồ sơ: dùng tầng mặc định và ghi vào `warnings[]` rằng chưa có `§4` để đọc.

---

## 3. Ngoại lệ hư cấu

Luật "không thêm fact" có đúng một ngoại lệ: **hư cấu**. Trong tiểu thuyết và truyện, bịa chi tiết là
việc của thể loại, không phải lỗi liêm chính.

Ngoại lệ này chỉ có hiệu lực khi `§4` của hồ sơ thể loại khai nó ra (`novel.md`, Phase 1b). Cho tới
khi hồ sơ đó tồn tại, trục 4 **không tự suy ra ngoại lệ** từ việc người dùng nói "đây là truyện".

Ngay trong hư cấu, ba thứ vẫn được bảo vệ:

- **Hội thoại nhân vật** — giọng nhân vật là dữ liệu nhân vật, không phải văn phong cần chuẩn hoá.
- **Chi tiết đã gieo ở chương trước** — đổi màu mắt một nhân vật ở chương 12 là lỗi nhất quán.
- **Sự kiện có thật được nhắc trong truyện** — năm, địa danh, nhân vật lịch sử.

---

## 4. Phép thử một câu

Trước mỗi nhát sửa, hỏi: *"Nếu tác giả đọc bản sau và nói **tôi không viết thế**, họ có lý không?"*

Có lý → hoàn tác. Không chắc → giữ nguyên và ghi vào `warnings[]` để tác giả tự quyết. Vùng bảo vệ
tồn tại vì trục 4 mạnh hơn nó tưởng: nó viết trơn hơn tác giả, và văn trơn hơn không có nghĩa là đúng
hơn.
