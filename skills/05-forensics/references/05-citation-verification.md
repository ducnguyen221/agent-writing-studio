# Kiểm chứng trích dẫn & con số — tầng bằng chứng CỨNG

Đây là tầng **duy nhất** cho ra khẳng định nhị phân kiểm chứng được: nguồn đó tồn tại hoặc không.
Mọi tầng khác chỉ cho ra xác suất.

---

## Luật vàng

> **`not_found` KHÔNG đồng nghĩa `bịa`.**
> Mọi cơ sở dữ liệu đều thiếu sót, index không đầy đủ, metadata lệch. Chỉ được ghi **"bịa đặt"**
> sau khi **con người** đã tra tay trên nhiều nguồn và không thấy.

Bốn trạng thái bắt buộc, không được gộp:
`verified` · `not_found` · `ambiguous` · `service_unavailable`

---

## Phân tầng nguồn Việt Nam

| Tier | Loại nguồn | Cách xử lý |
|---|---|---|
| **A** | Có DOI / arXiv ID / PMID / ISBN | Tra tự động (Crossref, OpenAlex, Semantic Scholar, Open Library) |
| **B** | Tạp chí VN có website | VJOL `vjol.info.vn`, VCGate `vcgate.vnu.edu.vn`. ⚠️ **Độ phủ rất hạn chế** — chỉ ~83/600 tạp chí VN đủ chuẩn được index. **"Không thấy trên VCGate" gần như không có giá trị chứng minh gì.** |
| **C** | **Văn bản pháp quy VN** | Verify bằng **số hiệu + ngày ban hành + cơ quan ban hành**. LLM bịa số hiệu rất giỏi và **rất dễ bắt** — đây là chỗ bắt hallucination sạch nhất cho bài tiếng Việt |
| **D** | Giáo trình nội bộ, kỷ yếu không xuất bản, luận văn thư viện | **Chuyển gánh nặng, không suy đoán.** Yêu cầu tác giả nộp ảnh trang bìa + trang trích dẫn. Ai trích thật làm được trong 5 phút |

---

## Pattern nguy hiểm nhất — "chimeric citation"

Tác giả **có thật** + tạp chí **có thật** + **sai năm / số / trang**. Hoặc ghép tên tác giả A với bài
của tác giả B. Nó vượt qua kiểm tra "tác giả có tồn tại" nhưng **chết ở kiểm tra metadata khớp**.

→ Chấm điểm riêng cho từng thành phần: `title` · `author` · `year` · `venue`.

---

## Con số không nguồn — đường điều tra rẻ nhất

Trong ca 2026-08-29, bài nghi vấn có **74 con số**, hầu như không con số nào có nguồn:
*"hơn 40% doanh nghiệp lớn tích hợp AI vào tuyển dụng"*, *"tự động hoá tăng 35% so với 2020"*,
*"150 tỷ USD giao dịch số"*.

Dấu hiệu "stat-sprinkling" của LLM:
- Con số **tròn trịa**, rắc đều mỗi đoạn một con số
- Đơn vị đo **mơ hồ** (*"tỷ lệ tự động hoá"* của cái gì?)
- Con số **không ăn nhập logic câu** — gắn theo phản xạ để "làm dày" bài
- Văn bản được nêu **tên nhưng không số hiệu, không cơ quan ban hành**

**Quy trình:** liệt kê toàn bộ con số không nguồn thành một bảng, đưa cho tác giả, yêu cầu trưng nguồn.
Đây **không phải buộc tội** — đây là thủ tục học thuật hợp lệ. Kết quả có ba khả năng: có nguồn thật
(tín hiệu đảo chiều), không nhớ nguồn (suy yếu nhưng không kết luận), hoặc nguồn không tồn tại (bằng chứng cứng).

---

## Công cụ

| Công cụ | License | Ghi chú |
|---|---|---|
| [RefChecker](https://github.com/markrussinovich/refchecker) | MIT | `pip install academic-refchecker` · có installer Windows · tra Semantic Scholar + OpenAlex + Crossref + DBLP + ACL · nhận PDF, fallback GROBID |
| [GROBID](https://grobid.readthedocs.io/en/latest/Grobid-docker/) `0.9.1-crf` | Apache-2.0 | Docker ~500MB · CPU · RAM 3GB. **Chọn `-crf` không phải `-full` (8GB)** — GPU qua container không hỗ trợ trên Windows |
| Hallucinator | 🔴 AGPL-3.0 | 12+ nguồn nhưng AGPL — **không nhúng vào dịch vụ cho trường** |

## Rate limit đã verify (2026)

| API | Giới hạn |
|---|---|
| **Crossref** | Đổi từ 01.12.2025: public **5 req/s** (bản ghi đơn), **1 req/s** (list). Polite pool 10/3 — vào bằng tham số `mailto=` |
| **OpenAlex** | **Bắt buộc API key từ 13.02.2026** (miễn phí, phải đăng ký) |
| **PubMed** | 3 req/s → **10 req/s** có key |
| **arXiv** | **1 request / 3 giây**, 1 connection |
| **Semantic Scholar** | ⚠️ Nguồn mâu thuẫn (1 RPS vs 5.000/5 phút) — **tự đo trước khi thiết kế nhịp gọi** |
