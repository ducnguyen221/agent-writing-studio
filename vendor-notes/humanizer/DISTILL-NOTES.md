# Ghi chú chưng cất humanizer

## Đã chưng cất

| Nguyên lý upstream | Cách chuyển hóa trong studio |
|---|---|
| Quy trình hai lượt, lượt 1 không giữ cấu trúc cố định | `references/01-quy-trinh-hai-luot.md` của trục 4 — đây là thuốc chống Goodhart: sửa theo nghĩa, không sửa theo thước đo |
| Hai câu hỏi kiểm sau lượt 1 | Ánh xạ thẳng vào `polish.diff.json`: mỗi sửa có `reason`, và hai mảng `facts_added` / `facts_removed` bắt buộc rỗng |
| Luật không bịa fact, có ngoại lệ cho hư cấu | `preserve[]` ở §4 từng thể loại; ngoại lệ hư cấu ghi ở §4 của `novel.md` |
| Bài mẫu của người viết thắng mọi luật văn phong | `voice_priority: [writer_profile, genre_default]` ở §4 mọi thể loại |
| Danh sách những thứ KHÔNG được gắn cờ và chi tiết người phải giữ | `references/03-chong-sua-oan.md`, kế thừa và hợp nhất với `03-chong-bao-oan` §2 và §6 |
| Cách phân họ 35 pattern | `shared/rules/vi-ai-tells.json`: 29 họ `candidate` + 1 họ `needs_corpus`, mọi ví dụ và phản chứng tự soạn bằng tiếng Việt |

## Không mang sang

- Toàn bộ câu ví dụ tiếng Anh. Không dịch câu nào.
- Danh sách từ mà mô hình hay dùng (pattern 7): giữ chỗ ở trạng thái `needs_corpus`, để rỗng cho tới khi có corpus tiếng Việt có provenance.
- Pattern 14 em dash, 15 in đậm quá tay ở dạng thuần mật độ, 17 Title Case, 19 ngoặc kép cong, 26 cặp gạch nối — đặc thù tiếng Anh, và 14 với 19 đã bị bác bằng thực đo.
- Mục tiêu không nghe giống AI. Trục 4 làm văn hay hơn cho người đọc; né máy chấm là mục tiêu khác và repo này từ chối nó.
- Cấm em dash như một luật văn phong: không có cơ sở trong tiếng Việt.

## Ranh giới

Đây là nguồn distill nặng nhất của trục 4 và cũng là nguồn rủi ro báo oan lớn nhất. Hàng rào: mọi họ tell phải có phản chứng tiếng Việt; hai họ trùng khuôn hành chính (T06, T10) phải khai `genre_baseline`; trục 5 chỉ được dùng mục đã `calibrated` để tạo finding, và đợt này chưa mục nào `calibrated`.
