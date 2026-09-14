# Mẫu báo cáo và cách sửa

## 1. Khối kết quả đầu báo cáo

```markdown
# REVIEW DẤU HIỆU AI TRONG VĂN BẢN

**Tài liệu:** ... · **Thể loại:** ... · **Chế độ đo:** agent_read | agent_plus_optional_counts

| Chỉ số | Kết quả | Khoảng vận hành | Cách đọc |
|---|---:|---:|---|
| S — Điểm nghi vấn | 58/100 | 33–83 | Mức ưu tiên xem lại, không phải xác suất AI |
| C — Tỷ lệ nội dung mang dấu hiệu AI | 17,5% | 7,5–27,5% | Độ phủ có trọng số của NOTE/FLAG |

**Nhãn:** `worth_reviewing` · **Khuyến nghị:** đọc lại các đoạn F02, F04 và hỏi tác giả 3 câu cuối báo cáo.
```

Luôn ghi công thức đếm C ngay dưới bảng, ví dụ: `6 FLAG + 9 NOTE / 55 câu hợp lệ`.

## 2. Bảng finding bắt buộc

| ID | Vị trí + trích dẫn | Nhóm | Mức | Vì sao đáng nghi | Phản chứng | Cách sửa |
|---|---|---|---|---|---|---|
| F01 | §2, đoạn 3 — “…” | G1 | Vừa | Cùng khuôn đã lặp 5 lần | Có thể là thói quen phép đối | Giữ 1 lần mạnh nhất; 4 lần còn lại viết thẳng quan hệ nhân–quả |

Mỗi finding phải đứng độc lập: người đọc nhìn hàng đó phải biết lỗi nằm ở đâu, vì sao và sửa thế nào.

## 3. Bản đồ lỗi → cách khắc phục

| Lỗi | Không nên | Nên làm |
|---|---|---|
| Câu đệm/rỗng | Thay bằng một câu đệm “hay hơn” | Xóa; hoặc thêm chủ thể, hành động, dữ kiện cụ thể |
| Danh từ hóa dày | Thay đồng nghĩa từng từ | Đưa người/vật thật về làm chủ ngữ, chuyển danh từ thành động từ |
| Khuôn `không chỉ X mà còn Y` lặp | Đổi toàn bộ sang một khuôn mới | Giữ một lần có tác dụng; các lần khác viết quan hệ trực tiếp |
| Gloss tiếng Anh dày | Xóa sạch thuật ngữ nghề | Giữ lần đầu của thuật ngữ cần thiết; bỏ các lần chú giải thừa |
| Nguồn mơ hồ | Viết “theo nhiều nghiên cứu” | Ghi tác giả/tổ chức, năm, phạm vi và liên kết hoặc số hiệu |
| Số liệu không nguồn | Làm tròn hoặc xóa đơn vị | Trưng nguồn; nếu không có, bỏ con số hoặc chuyển thành nhận định định tính rõ giới hạn |
| Đoạn quá cân đối | Cố chèn câu ngắn ngẫu nhiên | Tổ chức theo độ quan trọng thật; cho mỗi ý độ dài đúng với lượng bằng chứng |
| Giọng đổi giữa các phần | Làm phẳng cả bài thành một giọng “chuẩn” | Chọn baseline của tác giả, sửa riêng các khối lệch giọng |
| Thiếu chuẩn thể loại | Thêm câu chung chung cho đủ mục | Bổ sung bằng chứng/chi tiết mà người trong nghề thực sự cần |
| Kết luận recap máy móc | Dùng cụm “Tóm lại” khác | Chốt một hệ quả, quyết định hoặc câu hỏi còn mở; nếu không có gì mới thì cắt |

## 4. Mẫu finding chi tiết

```markdown
### F03 — Câu đệm khái quát, thiếu chủ thể (G2 · vừa)

- **Vị trí:** Mục 2.1, đoạn 4
- **Trích dẫn:** “Trong bối cảnh chuyển đổi số diễn ra mạnh mẽ, việc ứng dụng AI đóng vai trò then chốt…”
- **Dấu hiệu:** ba cụm nhấn mạnh chồng nhau; không nêu ai làm gì; bỏ phần đệm thì mệnh đề còn rất ít thông tin.
- **Phản chứng:** đây có thể là câu mở đoạn theo văn nghị luận được dạy ở Việt Nam.
- **Cách sửa:** nêu chủ thể và hành động cụ thể, ví dụ “Từ học kỳ II/2026, tổ bộ môn dùng AI để phản hồi bản nháp…”
- **Câu hỏi xác minh:** “Ở đơn vị của tác giả, ai đã dùng AI cho công việc nào và kết quả đo bằng gì?”
```

## 5. Kết thúc báo cáo

Luôn có:

1. 3–5 câu hỏi vấn đáp lấy từ findings mạnh nhất.
2. Danh sách số liệu/nguồn cần trưng ra.
3. Dấu hiệu ngược lại cho thấy có người thật tham gia.
4. Giới hạn: thể loại, OCR, thiếu writer profile, chưa có fixtures, xung đột model nếu có.
5. Khuyến nghị theo hành động rẻ và đảo ngược được trước: hỏi, kiểm nguồn, xem bản nháp; không kết tội.
