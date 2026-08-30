# Hệ chấm điểm agent-first

Hệ này dành cho lượt review mà agent **đọc trực tiếp** và không cần script. Nó tạo hai chỉ số khác nhau:

- **S — Điểm nghi vấn 0–100:** mức độ mạnh của các họ dấu hiệu trên toàn tài liệu.
- **C — Tỷ lệ nội dung mang dấu hiệu AI:** độ phủ của các câu bị gắn cờ.

S và C là chỉ số sàng lọc. Chúng không phải xác suất thống kê rằng AI đã viết văn bản.

## 1. Đơn vị phân tích và nhãn câu

Loại khỏi mẫu số: tiêu đề, mục lục, danh mục tài liệu tham khảo, bảng thuần số, câu dưới 8 âm tiết và
phần trích dẫn dài nguyên văn.

| Nhãn | Trọng số C | Khi dùng |
|---|---:|---|
| `PLAIN` | 0 | Không có dấu hiệu đáng kể |
| `NOTE` | 0,4 | Một dấu hiệu, có thể giải thích vô tội |
| `FLAG` | 1,0 | Ít nhất hai dấu hiệu khác bản chất hội tụ, hoặc một khuôn mạnh lặp có hệ thống |

`SKIP` không vào tử số hoặc mẫu số.

## 2. Điểm S theo bốn nhóm

### G1 · Khuôn và cấu trúc — tối đa 30

| Quan sát | Điểm |
|---|---:|
| Khuôn tu từ lặp nhiều nhất: 0–2 / 3–4 / 5–6 / ≥7 lượt | 0 / 8 / 14 / 18 |
| Mỗi khuôn khác lặp ≥3 lượt | +3, tối đa +6 |
| Nhịp/khung đoạn quá đều: không / nhẹ / lặp rõ ở ≥3 đoạn / xuyên suốt | 0 / 2 / 5 / 10 |
| Đối xứng bullet hoặc section máy móc: không / vừa / rõ | 0 / 3 / 6 |

Áp trần 30. Không phạt một phép đối đơn lẻ hoặc một đoạn có cấu trúc cân đối hợp lý.

> ⚠️ **Số "lượt" phải là số ĐẾM, không phải số ƯỚC.** Trước khi tra bậc, liệt kê **từng lượt kèm
> `sentence_id`**. Không liệt kê được thì không được tính. Ước lượng kiểu "~20 lượt" **cấm** đưa vào bảng.
>
> *Ca 2026-08-30:* agent ước ~20, gắn 3 FLAG; đếm thật = 13 (khuôn hẹp 4). Sai ~50%, kéo sai cả
> G1 → S → C. Nếu có `counters.json`, số của script **thắng** số ước của agent ở trục này — nhưng
> agent phải kiểm regex của script có bắt đúng họ khuôn mình đang nói không (script chỉ đếm mẫu nó biết).

### G2 · Từ vựng và độ rỗng ngữ nghĩa — tối đa 20

| Quan sát | Điểm |
|---|---:|
| Gloss/thuật ngữ Anh không cần thiết: không / cụm cục bộ / lặp nhiều đoạn / xuyên suốt | 0 / 4 / 8 / 12 |
| Danh từ hóa, chủ thể mờ, câu đệm rỗng: không / nhẹ / lặp ≥3 đoạn / xuyên suốt | 0 / 2 / 5 / 8 |

Áp trần 20. Thuật ngữ nghề nghiệp đúng ngữ cảnh không phải lỗi; chỉ chấm phần thừa hoặc giải thích lại
những khái niệm độc giả mục tiêu đã biết.

### G3 · Dẫn chứng và khả năng kiểm chứng — tối đa 25

Đếm các khẳng định thực chứng có thể kiểm tra (số liệu, mốc, nghiên cứu, quy định). Nếu có ít hơn 5,
không dùng tiêu chí tỷ lệ nguồn.

| Quan sát | Điểm |
|---|---:|
| Tỷ lệ khẳng định có nguồn `r`: ≥0,5 / 0,25–<0,5 / 0,1–<0,25 / <0,1 | 0 / 5 / 9 / 12 |
| Rắc số liệu tròn, dàn đều nhưng không làm rõ đơn vị/phạm vi: không / vừa / rõ | 0 / 2 / 4 |
| Nguồn mơ hồ: 0 / 1–2 / ≥3 lượt | 0 / 2 / 4 |
| Thiếu trải nghiệm riêng: thể loại không cần / trung tính / bắt buộc cần | 0 / 2 / 5 |

Áp trần 25. Một con số sai hoặc nguồn không tồn tại chỉ thành `verified_fabrication` sau khi con người
tra tay; trong lượt agent chỉ ghi `cần kiểm chứng`.

### G4 · Chuẩn mực thể loại — tối đa 25

Tiền đăng ký 2–4 mục `core`/`minor` trước khi chấm.

| Tình trạng | Điểm |
|---|---:|
| Đủ mọi mục | 0 |
| Thiếu 1 mục `minor` | 8 |
| Thiếu 1 mục `core` | 18 |
| Thiếu ≥2 mục, trong đó có `core` | 25 |

G4 đo mức am hiểu thể loại, không trực tiếp đo nguồn gốc. Finding G4 phải kèm câu hỏi chuyên môn.

## 3. Công thức S và nhãn

```text
S_raw = min(G1,30) + min(G2,20) + min(G3,25) + min(G4,25)

Nếu G3 = 0 và G4 = 0:
    S = round(S_raw × 0,6)
Ngược lại:
    S = S_raw
```

| S | Nhãn | Hành động |
|---:|---|---|
| 0–29 | `low_signal` | Không lưu hồ sơ nghi vấn |
| 30–59 | `worth_reviewing` | Đọc lại trong ngữ cảnh, chưa thông báo tác giả |
| 60–100 | `priority_check` | Vấn đáp, xin nguồn và bản nháp |

## 4. Công thức C

```text
C = 100 × (số FLAG + 0,4 × số NOTE) / số câu hợp lệ
```

Làm tròn một chữ số thập phân. Đây là **độ phủ dấu hiệu theo câu**, không phải tỷ lệ token và không phải
tỷ lệ thật sự do AI sinh. Báo cả số đếm: `8 FLAG + 12 NOTE / 96 câu hợp lệ`.

## 5. Khoảng bất định khi chưa có fixtures

Điều kiện tiên quyết: đã có profile cho đúng tổ hợp ngôn ngữ × thể loại. Nếu chưa có, trả
`insufficient_calibration`, `S=null`, `C=null` và không tạo action band.

Nếu chưa có corpus mốc cùng thể loại:

- S báo `S ±25 điểm`, chặn trong 0–100.
- C báo `C ±10 điểm phần trăm`, chặn trong 0–100.
- Ghi rõ `khoảng vận hành chưa hiệu chuẩn`, không gọi là khoảng tin cậy thống kê.

Nếu văn bản OCR, nhiều bảng, nhiều trích dẫn dài hoặc agent không thể đọc đủ từng câu, tăng biên thêm
10 điểm và hạ confidence một bậc.

## 6. Kiểm tra chéo bắt buộc

- Hơn 25% câu là `NOTE`/`FLAG`: hiệu chỉnh lại thể loại; rubric có thể đang quá nhạy.
- S ≥60 nhưng C <10%: nghi vấn nằm ở cấu trúc/nguồn/chuẩn thể loại, không ở từng câu.
- C ≥30% nhưng S <30: cờ dàn trải nhưng yếu; hạ kết luận một bậc.
- Chỉ G1/G2 kích hoạt: không được kết luận nặng; đây là hai nhóm dễ báo oan nhất.
