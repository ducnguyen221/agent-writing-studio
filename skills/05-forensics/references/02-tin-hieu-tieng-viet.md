# Tín hiệu tiếng Việt — ý nghĩa từng con số `counters.py` xuất ra

Mọi ngưỡng dưới đây là **mốc tham chiếu thực đo**, không phải hằng số thiêng. Chúng đến từ 3 văn bản
trong ca 2026-08-29 (n rất nhỏ) — dùng để định hướng, và **phải được thay bằng phân bố của chính
cohort bạn** khi có đủ 30+ bài mốc.

---

## Cái gì vỡ khi văn bản là tiếng Việt

**Tách từ.** Khoảng trắng tiếng Việt ngăn **âm tiết**, không ngăn **từ**. *"Trí tuệ nhân tạo"* là
4 âm tiết nhưng 1 đơn vị từ vựng. Mọi chỉ số dựa trên đếm từ — TTR, MTLD, biến thiên độ dài câu —
**sai hệ thống** nếu tokenizer tách theo khoảng trắng.

→ `underthesea.word_tokenize` phải đứng trước mọi phép đo lexical. Nếu chưa cài, `counters.py`
báo cờ `tokenizer: syllable` và mọi chỉ số lexical bị hạ độ tin cậy.

**TTR lệch theo độ dài.** Văn bản càng dài TTR càng giảm. Cùng một tác giả bị phạt chỉ vì viết dài hơn.
→ Dùng **MATTR-100** hoặc **MTLD**, không dùng TTR trần.

**Đừng dịch sang tiếng Anh rồi chấm.** Dịch máy làm phẳng văn phong, xoá tín hiệu gốc, và thêm dấu vân
tay của chính hệ dịch. Detector cuối cùng phát hiện *bản dịch*, không phát hiện *AI*.

---

## Bảng mốc tham chiếu

| Chỉ số | AI thuần | Người (chính luận chuyên nghiệp) | Bài nghi vấn (ca 2026-08-29) | Đọc thế nào |
|---|---|---|---|---|
| **Gloss tiếng Anh /1000 âm tiết** | — | **0,26** | **5,79** | **Tín hiệu mạnh.** >3/1000 là bất thường rõ với văn tiếng Việt |
| **Lặp cùng một khuôn tu từ** | — | — | **7 lần / 18k ký tự** | **Tín hiệu mạnh.** ≥5 lần cùng khuôn = bất thường |
| **Con số /1000 âm tiết** | — | 8,04 | **18,63** | Chỉ đáng ngờ khi kèm **tỷ lệ có nguồn thấp** |
| **Tỷ lệ số liệu có nguồn** (`sourced_ratio`) | 0,0%¹ | **93,9%**² | ~20% | ⚠️ Đọc mục dưới trước khi tin |

² Bài báo hội thảo Tam giác 3C (30/08), đo bằng `counters.py` **sau 5 lượt vá**. Trước vá: **7,5%** — tức
script từng báo oan chính bài trích nguồn tốt nhất. Mốc "văn rắc số" là mẫu tự tạo 8 câu, không phải corpus.

### ⚠️ `sourced_ratio` — thước dễ hỏng nhất, lịch sử vá 30/08

| Bản | Bài tốt (3C) | Văn rắc số | Lỗi bị lộ |
|---|---:|---:|---|
| "nguồn cùng câu" | **7,5%** | 0% | Không nhận APA `(Fraillon, 2025)` |
| + APA | 17,9% | 0% | Đếm cả **số điện thoại** khối tác giả; văn VN nêu nguồn câu N rồi trình bày số ở N+1, N+2 |
| + thừa kế ≤2 câu, bỏ liên hệ | 29,5% | 0% | Bài trích kiểu **Việt hoá** (`Bastani và cộng sự`, `TALIS 2024 cho thấy`) — regex chỉ biết tiếng Anh |
| + trích Việt hoá + tổ chức/dataset | 59% | 0% | Rác từ **danh mục tham khảo** (`122(26)`, `e2422633122`) |
| + cắt vùng tham khảo | **93,9%** | **0%** | 2 số còn lại là câu *bình luận số đã dẫn* — ngoài tầm carry=2, chấp nhận |

**Bài học:** mỗi lần siết một quy tắc để chống một lỗi phải chạy lại trên **văn bản tốt** xem có báo oan
chiều ngược không. Hằng số `SOURCE_CARRY=2` chọn tay từ **một** ca — cần fixture để hiệu chuẩn.
Với thể loại học thuật, **agent đọc trước, script kiểm sau** — không phải ngược lại.
| **Trích kinh điển / văn bản có số hiệu** | — | **15 lượt** | **2 lượt** | **Tín hiệu mạnh theo thể loại** — xem trục 4 |
| **Cliché /1000 âm tiết** | 13,53¹ | 1,04 | 0,50 | ⚠️ **Yếu và dễ báo oan.** Người > nghi vấn ở đây |
| **CV độ dài câu** | 0,215 | 0,542 | 0,460 | Thấp = phẳng. <0,25 đáng chú ý |
| **MATTR-100** | 0,865² | 0,823² | 0,851² | ⚠️ **Không phân biệt được.** Giữ để tham khảo, không tính điểm |

¹ Mẫu AI do chính agent sinh ra và **cố ý nhồi cliché** → con số này một phần tự chứng minh, không khách quan.

² ⚠️ **Ba giá trị MATTR này đo ở mức ÂM TIẾT** (lúc đo chưa cài `underthesea`). Sau khi cài, `counters.py`
mặc định đo ở mức **TỪ** và cho giá trị khác: bài nghi vấn 0,851 → **0,8128**. Cùng văn bản đó,
3.972 âm tiết chỉ là **2.699 từ** — chênh **32%**. ⇒ **Không so MATTR đo bằng hai tokenizer khác nhau.**
Kiểm trường `size.tokenizer` trong `counters.json` trước khi so bất kỳ chỉ số lexical nào.
Các mốc âm tiết ở trên cần đo lại toàn bộ ở mức từ trước khi dùng làm chuẩn.

---

## Nhóm tín hiệu và trần điểm

Các tín hiệu dưới đây **tương quan mạnh với nhau** — cộng thẳng là đếm trùng cùng một nguyên nhân.
Mỗi nhóm có **trần đóng góp**, không cộng vượt trần:

| Nhóm | Gồm | Trần |
|---|---|---|
| **G1 · Khuôn hình thức** | lặp khuôn tu từ · đối xứng bullet · CV độ dài câu | 30 |
| **G2 · Từ vựng ngoại lai** | gloss tiếng Anh · danh từ hoá | 20 |
| **G3 · Dẫn chứng** | con số không nguồn · nguồn mơ hồ · thiếu trải nghiệm | 25 |
| **G4 · Chuẩn mực thể loại** | thiếu thứ thể loại bắt buộc phải có | 25 |
| **G5 · Lắp ráp** | vỡ đánh số · mục đơn độc · lỗi gõ | *không tính điểm* — ghi nhận để diễn giải |
| **G6 · File** | TotalTime chuẩn hoá · revision · khoảng cách ngày | *không tính điểm* — ghi nhận |

`review_priority` = tổng có trần, tối đa 100. **Nếu chỉ có G1 và G2 kích hoạt mà G3/G4 im lặng →
hạ một bậc**, vì G1+G2 là hai nhóm dễ báo oan nhất với văn hành chính.

---

## Hai tín hiệu chỉ tiếng Việt mới có — và tình trạng của chúng

> ⚠️ **Cách đếm đúng (Opus tự bắt lỗi 30/08 khi viết `profile_build.py`):** chỉ **âm tiết mở** — `hòa/hoà`,
> `khỏe/khoẻ`, `thủy/thuỷ` — mới phân biệt được hai kiểu bỏ dấu. `toán`, `khoảng`, `hoạt`, `huyện` viết
> **giống nhau ở cả hai kiểu**, đếm chúng là kết luận sai (bản đầu kết luận `new` cho bài 3C; sửa xong: `old` 11–0).
> Loại `qu` (`quý` luôn bỏ dấu trên y). Regex ở `counters.py` và `profile_build.py` phải giữ cùng luật này.

**Vị trí dấu thanh kiểu cũ/mới** (`hòa` vs `hoà`, `thúy` vs `thuý`): người thật hiếm khi nhất quán
trong tài liệu dài; máy nhất quán tuyệt đối. **Trạng thái: chưa kiểm chứng đủ.** Trong ca đã đo, tỷ lệ
kiểu cũ/mới là 1/11 — có lẫn lộn, nghiêng "người", nhưng n=1. Giữ làm tín hiệu **bổ trợ**, không tính điểm.

**Lỗi gõ dấu kiểu Telex** (*"biến thế"* ← *"biến thể"*): LLM hầu như không sai kiểu này. Đây là dấu tay
người **gõ**, nhưng nhớ đọc theo hướng lắp ráp (xem trục "dấu vết lắp ráp").

**Chuẩn hoá Unicode NFC/NFD: ĐÃ BỊ BÁC BỎ.** Word tự chuẩn hoá NFC khi lưu. Xem `03-chong-bao-oan.md` mục 6.
