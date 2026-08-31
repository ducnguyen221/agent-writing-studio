---
name: 05c-reporting
description: Use when forensic evidence and scores must be turned into a Vietnamese review report with located issues, counterevidence, verification questions, and concrete fixes.
---

# Báo cáo kết quả giám định

## Tổng quan

Báo cáo phải giúp người đọc kiểm tra và sửa, không giúp người chấm kết tội nhanh hơn. Con số đứng
sau bằng chứng có vị trí, không đứng một mình.

## Thứ tự báo cáo

1. Phạm vi: tài liệu, ngôn ngữ, thể loại, phần không đọc được, trạng thái hiệu chỉnh.
2. Bảng S/C: điểm, khoảng vận hành, nhãn và cách đọc trung thực; với `insufficient_calibration`, ghi
   `S=null`, `C=null`, lý do và không tạo action band.
3. Findings theo mức độ rồi theo vị trí.
4. Dấu hiệu ngược lại cho thấy có người thật tham gia.
5. Số liệu/nguồn cần trưng ra.
6. Tối đa 3–5 câu hỏi vấn đáp lấy từ findings mạnh nhất; 0 câu hỏi nếu không có finding đứng vững.
7. Giới hạn và hành động rẻ, đảo ngược được.

Dùng [mẫu báo cáo](../05-forensics/references/10-mau-bao-cao-va-cach-sua.md).

## Một finding hoàn chỉnh

```text
F03 · §2.1 đoạn 4 · G2 · vừa
Trích: “Trong bối cảnh chuyển đổi số…”
Dấu hiệu: thiếu chủ thể; bỏ phần đệm thì còn rất ít thông tin.
Phản chứng: có thể là câu mở đoạn theo văn nghị luận.
Cách sửa: nêu đơn vị, hành động và kết quả cụ thể.
Câu hỏi: “Đơn vị nào đã làm việc gì và đo kết quả ra sao?”
```

## Cách sửa

- Câu rỗng: xóa hoặc thêm chủ thể–hành động–dữ kiện.
- Khuôn lặp: giữ lần có tác dụng, viết thẳng quan hệ ở các lần còn lại.
- Nguồn mơ hồ: yêu cầu tác giả/tổ chức, năm, phạm vi và đường kiểm tra.
- Giọng đổi: phục hồi baseline của tác giả ở khối lệch; không làm phẳng cả bài.
- Thiếu chuẩn thể loại: bổ sung bằng chứng thật, không chèn câu chung chung cho đủ mục.

Nếu người dùng chỉ yêu cầu review, không tự viết lại toàn văn.

## Ngôn ngữ

Báo cáo luôn bằng tiếng Việt. Với bài ngôn ngữ khác, giữ nguyên câu trích và thêm diễn giải tiếng
Việt; không dịch câu rồi dùng bản dịch làm bằng chứng ngôn ngữ.

## Ranh giới

Không viết “AI đã viết”. Viết “đoạn này mang các dấu hiệu…, nhưng cũng có thể do…; nên xác minh
bằng…”. `verified_fabrication` chỉ dùng sau khi con người kiểm nguồn.
