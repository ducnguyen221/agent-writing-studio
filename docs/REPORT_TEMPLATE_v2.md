# Mẫu báo cáo giám định v2

> **Thuật ngữ** (S, C, G1–G4, FLAG/NOTE/SKIP, tell, lăng kính, provenance): bảng giải nghĩa đầy đủ ở
> [README](../README.md) mục 6. *Finding* = một nhận định có vị trí, câu trích, bằng chứng và phản chứng.

Mẫu này dùng cho cả agent-first và chế độ có số đếm hỗ trợ. Báo cáo luôn bằng tiếng Việt; câu trích
ngoại ngữ giữ nguyên và được diễn giải riêng. Không một con số hay finding nào được đứng một mình.

## 1. Hợp đồng đầu ra

Báo cáo bắt buộc có:

1. phạm vi, ngôn ngữ, thể loại và phần không đọc được;
2. S — điểm dấu hiệu, C — độ phủ câu mang dấu hiệu, cùng khoảng vận hành;
3. finding có vị trí bền, trích dẫn, bằng chứng, phản chứng, cách sửa, câu hỏi xác minh;
4. dấu hiệu ngược lại cho thấy cách giải thích vô tội hoặc sự tham gia của con người;
5. câu hỏi vấn đáp, nguồn/số liệu cần trưng ra, giới hạn và hành động tiếp theo.

## 2. Khung Markdown

```markdown
# BÁO CÁO RÀ SOÁT DẤU HIỆU AI TRONG VĂN BẢN

> Đây không phải kết luận về tác giả và không phải xác suất AI. Các chỉ số chỉ giúp
> xếp thứ tự phần cần đọc lại, hỏi nguồn hoặc vấn đáp.

**Tài liệu:** {tên hoặc hash} · **Ngôn ngữ:** {language} · **Thể loại:** {genre}
**Phạm vi:** {toàn văn/phần đọc được} · **Hiệu chỉnh:** {trạng thái corpus}

| Chỉ số | Kết quả | Khoảng vận hành | Cách đọc |
|---|---:|---:|---|
| S — điểm dấu hiệu | {S}/100 | {S_low}–{S_high} | Mức ưu tiên xem lại |
| C — độ phủ dấu hiệu | {C}% | {C_low}–{C_high}% | Tỷ lệ câu hợp lệ có trọng số NOTE/FLAG |

**Phép đếm C:** {FLAG} FLAG + 0,4 × {NOTE} NOTE / {eligible} câu hợp lệ
**Nhãn:** `{label}` · **Độ tin cậy:** `{confidence}`

## Điểm theo nhóm

| Nhóm | Điểm sau trần | Bằng chứng chính |
|---|---:|---|
| G1 · Khuôn/cấu trúc | {..}/30 | {finding ids} |
| G2 · Từ vựng/độ rỗng | {..}/20 | {finding ids} |
| G3 · Dẫn chứng | {..}/25 | {finding ids} |
| G4 · Chuẩn thể loại | {..}/25 | {finding ids} |

## Findings cần xem lại

### F01 · §{section} · đoạn {paragraph} · {group} · {severity}

> {quoted_text}

- **Dấu hiệu:** {evidence}
- **Phản chứng:** {counterevidence}
- **Cách sửa:** {suggested_fix}
- **Câu hỏi xác minh:** {verification_question}
- **Cơ sở thể loại:** {genre_basis}

## Dấu hiệu ngược lại

- {bằng chứng nguồn gốc, ví dụ riêng, lỗi sửa tay, bản nháp hoặc phản chứng đáng kể}

## Nguồn và số liệu cần trưng ra

- {khẳng định} → cần {tác giả/tổ chức, năm, phạm vi, URL hoặc số hiệu}

## Câu hỏi trao đổi với tác giả

1. {câu hỏi rút từ finding mạnh nhất}
2. {câu hỏi kiểm nguồn hoặc quyết định lập luận}
3. {câu hỏi về quá trình tạo bản nháp}

## Giới hạn

- {chưa có corpus mốc / OCR / thiếu writer baseline / không đọc được phụ lục / xung đột model}
- S và C là chỉ số sàng lọc; không xác định ai đã viết.

## Khuyến nghị

{đọc lại trong ngữ cảnh → xin nguồn/bản nháp → vấn đáp; không dùng báo cáo làm căn cứ kỷ luật độc lập}
```

## 3. Quy tắc trình bày S/C

- Khi chưa có corpus cùng ngôn ngữ và thể loại: S ±25, C ±10 điểm phần trăm, chặn 0–100.
- C viết là “X% câu hợp lệ mang dấu hiệu đo được”, không viết “X% bài do AI viết”.
- Chỉ G1/G2 kích hoạt thì áp hệ số giảm và không được tự lên kết luận nặng.
- S cao nhưng C thấp phải nói rõ nghi vấn nằm ở mức tài liệu/nguồn/chuẩn thể loại.
- C cao nhưng S thấp phải hạ nhãn vì cờ dàn trải nhưng yếu.

## 4. Quy tắc finding

Vị trí gồm section, paragraph index, sentence ID và quote anchor để vẫn tìm lại được sau khi văn bản
dịch vài ký tự. Finding không có phản chứng hoặc không có câu hỏi xác minh là finding chưa hoàn chỉnh.
Một finding `high` không được dựa trên một cụm từ sáo rỗng đơn lẻ.

## 5. Hành động

Ưu tiên hành động rẻ và đảo ngược được: hỏi tác giả, xin nguồn, xem bản nháp, đối chiếu lịch sử chỉnh
sửa. Không lưu hồ sơ nghi vấn hoặc đưa ra quyết định bất lợi chỉ từ S/C. `verified_fabrication` chỉ
dùng sau khi con người kiểm chứng nguồn cụ thể.

Renderer tùy chọn: `python skills/05-forensics/scripts/report.py evidence.json --out report.md`.
