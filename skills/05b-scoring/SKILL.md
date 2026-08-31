---
name: 05b-scoring
description: Use when sealed forensic findings must be converted into a reproducible review-priority score, AI-signal coverage, uncertainty range, and action band.
---

# Chấm điểm bằng chứng giám định

## Tổng quan

Chấm hai câu hỏi riêng: dấu hiệu mạnh đến đâu (`S`) và phủ bao nhiêu nội dung (`C`). Điểm chỉ được
tính sau khi `05a-reading` đã khóa bản đọc mù.

## Điều kiện đầu vào

- danh sách câu hợp lệ cùng nhãn `PLAIN/NOTE/FLAG`;
- findings có phản chứng;
- thể loại đã tiền đăng ký;
- trạng thái hiệu chỉnh ngôn ngữ/thể loại;
- số đếm tùy chọn, chỉ dùng sau đọc mù.

Thiếu nội dung, dưới 300 âm tiết hoặc OCR hỏng: trả `insufficient_evidence`. Chưa có profile cho tổ
hợp ngôn ngữ × thể loại: trả `insufficient_calibration`, `S=null`, `C=null`, không tạo action band.
Khoảng ±25/±10 chỉ áp dụng khi profile phù hợp đã có nhưng corpus chưa đủ để thu hẹp khoảng.

## Luật cụm — cổng vào của G1/G2

**Tín hiệu đứng cụm mới được cộng điểm.** Đứng cụm nghĩa là thoả một trong hai: cùng một đoạn có
**≥2 họ tín hiệu khác nhau**, hoặc **một họ lặp ≥3 lượt** toàn bài. Cả hai đều phải liệt kê được
`sentence_id` từng lượt; không liệt kê được thì không tính.

Tín hiệu **đơn lẻ** tối đa `NOTE`, **không bao giờ `FLAG`**, **không cộng điểm** — vẫn ghi vào bản
đọc, nhưng ghi nhận không phải buộc tội. Lý do: một khuôn lẻ là văn người bình thường; nhiều họ dồn
một chỗ, hoặc một họ lặp như phản xạ, mới là dáng máy. Rule máy đọc: `cluster_requirement` trong
`shared/rules/forensics-scoring-v3.json`. Luật này **không đổi thang** — G1 vẫn 30, G2 vẫn 20 — chỉ
thêm điều kiện trước khi tra bậc. G3, G4 không chịu luật cụm.

## Tính S

Áp đúng [bảng điểm](../05-forensics/references/09-cham-diem-agent-first.md): G1 khuôn/cấu trúc,
G2 độ rỗng/từ vựng, G3 dẫn chứng, G4 chuẩn thể loại. Qua cổng cụm trước, rồi áp trần từng nhóm và
giảm tổng nếu chỉ G1/G2 kích hoạt vì đây là hai nhóm dễ báo oan nhất. Không cộng điểm ngoài bảng.

## Tính C

Mặc định agent-first:

```text
C = 100 × (FLAG + 0,4 × NOTE) / số câu hợp lệ
```

`SKIP` không vào tử hoặc mẫu. Báo cả phép đếm, ví dụ `6 FLAG + 9 NOTE / 55 câu`.

## Kiểm tra xung đột

- Hơn 25% câu bị gắn cờ: đọc lại thể loại.
- S ≥60 nhưng C <10%: nói rõ nghi vấn nằm ở cấu trúc/nguồn, không ở từng câu.
- C ≥30% nhưng S <30: hạ nhãn; cờ dàn trải nhưng yếu.
- Chỉ G1/G2: không được lên kết luận nặng.
- G1/G2 có điểm mà không liệt kê được cụm: trả nhóm đó về 0, tính lại.

## Khoảng và nhãn

Không có fixtures cùng thể loại: dùng khoảng rộng trong reference và ghi `chưa hiệu chỉnh`. Chỉ thu
hẹp khi `05d-calibration` xác nhận đủ corpus. Không đổi tên C thành “tỷ lệ AI thật”.

## Script hỗ trợ

Agent có thể tự tính từ bảng. Script chỉ giúp tái lập phép cộng trên hồ sơ dài; không được tự tạo
finding hay sửa nhãn câu. Bàn giao kết quả sang `05c-reporting`.
