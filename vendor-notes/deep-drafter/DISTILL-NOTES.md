# Ghi chú chưng cất deep-drafter

## Đã chưng cất

| Nguyên lý upstream | Cách chuyển hóa trong studio |
|---|---|
| Outline nhiều tầng, duyệt xong tầng cuối mới viết prose | `outline_depth` ở §2 mọi thể loại; `draft.meta.json` ghi `outline_approved` |
| Referee đọc mù, không nhận câu hỏi mớm | `blind_referee: true` ở §3; trục 3 không xem `draft.meta.json` trước khi chấm xong |
| Hiệu chỉnh giọng từ vài bài cũ của chính tác giả | Writer profile dựng từ tối thiểu 3 bài chính chủ; dưới 3 bài thì `status: draft` |

## Không mang sang

- Phần chuyên biệt cho bài báo học thuật tiếng Anh và chuẩn trình bày của tạp chí.
- Cách đóng gói skill riêng cho một trợ lý cụ thể.
- Vòng lặp gọi mô hình nhiều lượt không có người duyệt ở giữa.

## Ranh giới

Repo nhỏ nhưng đúng chỗ cần: đây là nguồn của luật blind referee, luật quan trọng nhất của trục 3.
