# Bản đồ lỗi → cách sửa

Bản đồ đầy đủ **đã tồn tại** và không được chép lại ở đây:
`skills/05-forensics/references/10-mau-bao-cao-va-cach-sua.md` **mục 3**, mười dòng, mỗi dòng ba cột
*lỗi · không nên · nên làm*.

File này chỉ làm một việc mà bản gốc không làm được: nối mỗi dòng của nó với **`tell_id`** trong
`shared/rules/vi-ai-tells.json`, để trục 4 đọc được cột `fix` và ghi đúng `tell_id` vào
`polish.diff.json`. Bản gốc viết cho người đọc báo cáo giám định; cột dưới đây viết cho người sửa.

Cách dùng: mở `references/10` §3 bên cạnh, tra dòng, rồi tra `tell_id` ở đây.

| Dòng ở `references/10` §3 | `tell_id` | Ghi chú riêng của trục 4 |
|---|---|---|
| Câu đệm / rỗng | `T03`, `T23`, `T24` | `T23` có `genre_baseline` cho `chinh-luan`, `sang-kien-kinh-nghiem` — ở đó chỉ sửa khi cụm đệm thay cho một phép đối lập thật |
| Danh từ hoá dày | `T13` | Trùng counter `NOMINAL`. Có baseline ở 4 thể loại hành chính–học thuật; đọc mục 5 của `03-chong-sua-oan.md` trước khi coi là lỗi |
| Khuôn `không chỉ X mà còn Y` lặp | `T09` | Trùng counter `TEMPLATES`. Giữ một lần có tác dụng, các lần sau viết quan hệ trực tiếp |
| Gloss tiếng Anh dày | *(không có tell riêng)* | Counter `G2.english_gloss`. Giữ lần đầu của thuật ngữ cần thiết; bỏ chú giải lặp |
| Nguồn mơ hồ | `T05`, `T02` | `T02` là khoe tên báo thay cho nguồn. **Tuyệt đối không bịa nguồn cho vừa câu** — chuyển sang danh sách "khẳng định chưa có nguồn" |
| Số liệu không nguồn | `T05` | Counter `G3.unsourced_numbers`. Không làm tròn, không xoá đơn vị — cả hai đều chạm vùng bảo vệ |
| Đoạn quá cân đối | `T10`, `T16` | `T10` có baseline ở 3 thể loại. **Không chèn câu ngắn ngẫu nhiên**; `polish_check.py` cảnh báo đúng hành vi này |
| Giọng đổi giữa các phần | *(không có tell riêng)* | Chọn baseline của tác giả rồi sửa riêng khối lệch. Không làm phẳng cả bài |
| Thiếu chuẩn thể loại | `T06`, `T25` | Đây là lỗ hổng **nội dung**, không phải lỗi văn phong. Giữ khung, bơm nội dung; không thêm câu chung chung cho đủ mục |
| Kết luận recap máy móc | `T29`, `T31`, `T25`, `T32` | `T31` là chỗ dễ sửa oan nhất: câu Link của PEEL là cấu trúc bắt buộc, xem `03-chong-sua-oan.md` mục 2.4 |

Ba họ tell còn lại không có dòng tương ứng ở `references/10` vì chúng là lỗi lắp ráp hoặc lỗi giọng,
không phải lỗi đo được: `T20` rác chatbot (xoá thẳng, không cần cân nhắc), `T22` nịnh người hỏi,
`T33` mở giả-thẳng-thắn.

**Luật ghi `tell_id`:** chỉ ghi khi nhát sửa thật sự thuộc họ đó. Sửa vì lý do văn phong thuần tuý thì
ghi `null` — `polish.schema.json` nói rõ `null` là hợp lệ và trung thực hơn gán bừa một tell. Đừng
biến `tell_id` thành chỉ tiêu.
