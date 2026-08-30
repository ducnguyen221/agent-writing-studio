# Ghi chú chưng cất storm

## Đã chưng cất

| Nguyên lý upstream | Cách chuyển hóa trong studio |
|---|---|
| Perspective-guided questioning: sinh nhiều góc nhìn rồi hỏi từ từng góc | `intent_questions[]` ở §1 của `research.md` — phải trả lời được từ nhiều góc trước khi lập dàn ý |
| Outline mang citation ngay khi dựng, không gắn nguồn sau khi viết xong | §2 của `research.md`: mỗi mục outline kèm nguồn trước khi viết prose |
| Tách pha thu thập bối cảnh khỏi pha viết | Trục 1 xuất `context.json`; trục 2 từ chối viết nếu chưa có |

## Không mang sang

- Toàn bộ runtime Python, phụ thuộc mô hình và bộ tìm kiếm.
- Mục tiêu sinh bài kiểu bách khoa tự động — studio này viết cùng người, không viết thay người.
- Cách tự chấm chất lượng bằng chính mô hình đã sinh ra bài.

## Ranh giới

Chỉ chưng cất phương pháp hỏi và cách gắn nguồn vào outline. Không có dòng mã nào của storm trong repo này.
