# Ghi chú chưng cất fabric

## Đã chưng cất

| Nguyên lý upstream | Cách chuyển hóa trong studio |
|---|---|
| Một pattern làm đúng một việc và có một hợp đồng đầu ra | Một lăng kính = một câu hỏi, một loại bằng chứng, một chỗ ghi vào `critique.json` |
| `find_logical_fallacies` liệt kê loại rồi trích câu | Lăng kính `fallacy_scan`: 13 loại tiếng Việt, mỗi finding phải có vị trí và phản chứng |
| `analyze_claims` tách khẳng định khỏi bằng chứng | Lăng kính `claim_check`: mỗi khẳng định thực chứng được xếp mức bằng chứng riêng |
| `rate_content` chấm theo nhiều trục | `criteria_scores[]` chấm riêng từng tiêu chí, cố ý KHÔNG có điểm tổng |
| `analyze_prose_pinker` soi câu văn | Chỉ lấy khung tiêu chí ngôn ngữ; bỏ toàn bộ ví dụ và thuật ngữ tiếng Anh |

## Không mang sang

- Toàn bộ ví dụ, prompt và danh sách từ tiếng Anh.
- Cách đóng gói pattern thành công cụ dòng lệnh và hạ tầng gọi mô hình.
- Điểm tổng gộp nhiều trục — repo này cố ý không có.
- Giả định người viết bài là người nói tiếng Anh bản ngữ.

## Ranh giới

Đây là DERIVED về cách đặt câu hỏi, không phải bản dịch pattern. Không file nào trong studio là bản chuyển ngữ của một pattern Fabric; nếu về sau có, phải ghi rõ ở đây và kiểm lại điều khoản ghi công của MIT.
