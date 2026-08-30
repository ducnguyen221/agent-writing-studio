# Chống báo oan — đọc TRƯỚC khi kết luận

Đây là file quan trọng nhất trong skill. Sai ở đây thì mọi thứ khác vô nghĩa, vì cái giá của một
kết luận sai không đối xứng: bỏ lọt một bài gian lận là mất công bằng; buộc tội oan một người
trung thực là huỷ hoại họ.

---

## 1. Con số phải nhớ

> **GPT-4 khi được prompt trực tiếp làm "chuyên gia giám định": nhận đúng 97–100% văn AI, nhưng gắn nhầm >95% văn NGƯỜI thành AI.**
> — *Fighting Fire with Fire: Can ChatGPT Detect AI-generated Text?*, arXiv 2308.01284, SIGKDD Explorations 2024

Và GPT-3.5 lệch **ngược lại**: phát hiện dưới 50% văn AI. Cùng một task, hai phiên bản model sai
theo hai hướng đối lập.

**Nghĩa là:** bản năng "đọc thấy giống AI" của chính bạn — agent đang đọc file này — **có thiên lệch
mạnh và đã được đo**. Bạn nghiêng về việc nói "AI". Hãy chủ động chống lại xu hướng đó bằng cách
bắt buộc viết `alternative_explanation` cho mọi nhận định.

Các thiên lệch khác đã có tài liệu:
- **Self-recognition bias** (arXiv 2404.13076, NeurIPS 2024): LLM nhận ra được văn của chính mình, và
  khả năng tự-nhận-ra càng cao thì self-preference bias càng mạnh. → **Không dùng model X để giám định
  văn nghi do chính họ hàng model X viết.** Nếu nghi bài do Claude viết, đừng để Claude là giám định
  viên duy nhất.
- **Overconfidence 20–60%** (arXiv 2505.02151): LLM đánh giá quá cao xác suất đúng của mình.
  → **Đừng tin `confidence` do chính bạn tự khai.**

---

## 2. Văn phong hành chính – học thuật tiếng Việt vốn dĩ là văn công thức

Đây là nguồn báo oan số một trong bối cảnh Việt Nam.

*"Đóng vai trò quan trọng"*, *"trong bối cảnh"*, *"tóm lại"*, *"đòi hỏi sự chung tay của toàn xã hội"*,
*"góp phần không nhỏ"* — đây là **văn phong chuẩn mực được dạy trong trường**, dùng trong mọi báo cáo,
tờ trình, sáng kiến kinh nghiệm ở Việt Nam **từ trước khi có ChatGPT**.

**Thực đo trong ca giám định 2026-08-29:**

| Văn bản | Cliché / 1000 âm tiết |
|---|---|
| Bài Tạp chí Cộng sản (người viết, Trưởng khoa Học viện Cán bộ) | **1,04** |
| Bài nghi vấn | **0,50** |

→ Bài của **người** có mật độ cliché **gấp đôi** bài nghi vấn. Nếu chấm bằng danh sách cliché viết tay,
hệ thống sẽ **kết tội bài của Tạp chí Cộng sản nặng hơn**.

**Kết luận vận hành:** mật độ cliché đo **THỂ LOẠI**, không đo nguồn gốc. Chỉ dùng nó sau khi đã
chuẩn hoá theo thể loại, và không bao giờ dùng một mình.

---

## 3. Người viết tiếng Anh không phải bản ngữ

Nếu bài là **tiếng Anh** do người Việt viết: Liang et al. (*Patterns*, arXiv 2304.02819) đo được
**7 detector thương mại phân loại nhầm 61,22% bài luận TOEFL của người viết không bản ngữ thành AI**,
trong khi gần 0% với học sinh bản ngữ Mỹ. Nguyên nhân: văn người học ngoại ngữ có perplexity thấp
do vốn từ hạn chế — **chính là tín hiệu bị coi là "AI"**.

→ Với bài tiếng Anh của học viên Việt Nam: **giảm mạnh trọng số mọi tín hiệu về "độ trơn tru ngôn ngữ"**,
và dựa nhiều hơn vào chuẩn mực thể loại + dẫn chứng + forensics file.

---

## 4. Bẫy "control tồi" — bài học đắt nhất của skill này

Khi so bài nghi vấn với một bài mốc, **bài mốc phải thật sự tương đương**.

Trong ca 2026-08-29, bài mốc là một bài Tạp chí Cộng sản. Nó trích Mác–Lênin–Hồ Chí Minh–Văn kiện
**15 lần** — nghĩa là một phần lớn văn bản là **trích nguyên văn tài liệu chính thống**, thứ mà bất kỳ
mô hình ngôn ngữ nào cũng thấy **cực kỳ dễ đoán**. Perplexity thấp của bài mốc phần lớn phản ánh
*mật độ trích dẫn*, không phản ánh *do người viết*. Bài mốc đó làm bài nghi vấn trông "người" hơn thực tế.

**Luật rút ra:**
- Bài mốc phải **loại bỏ hoặc chuẩn hoá phần trích dẫn nguyên văn** trước khi so sánh.
- Một bài mốc **không phải** phân bố. Không được nói "phân vị" khi chỉ có một bài.
- Mốc phải khớp: **thể loại · độ dài · trình độ tác giả · thời kỳ**.

---

## 5. Diễn giải metadata cho đúng

`TotalTime` (thời gian soạn thảo trong Word) phải đọc **theo tỷ lệ với độ dài**, không theo ngưỡng tuyệt đối.

- 130 phút cho **12 trang lý luận chính trị nguyên gốc** là **NHANH** → khớp với biên tập/lắp ráp hơn là sáng tác.
- 130 phút cho **một bài luận 500 từ** là chậm và bình thường.

`TotalTime` **thấp KHÔNG phải bằng chứng gian lận** — nó bằng 0 hoàn toàn vô tội nếu soạn trên
Google Docs, LibreOffice, WPS hay Word Online.

`RSID` **không phục dựng được thứ tự thời gian** — cài đặt OOXML của Microsoft không tuân chuẩn.
RSID gắn với *sự kiện sửa*, không phải *dấu thời gian*.

### 5.1 Metadata của chính studio: hai chế độ `blind` và `audit`

Ba đoạn trên nói về metadata do phần mềm soạn thảo sinh ra. Còn một loại metadata khác, quan trọng
hơn nhiều khi bài đi qua chính repo này: **bản tự khai nguồn gốc** — `draft.meta.json` của trục 2 và
sidecar `polished.provenance.json` của trục 4. Đọc sai loại này cũng báo oan như đọc sai `TotalTime`,
chỉ khác là báo oan theo chiều ngược lại: **kết luận vô tội từ một phép đo không có thẩm quyền**.

Trục 5 vì thế chạy ở một trong hai chế độ, và phải nói rõ mình đang ở chế độ nào ngay trong báo cáo:

| Chế độ | Đầu vào | Dùng cho |
|---|---|---|
| `blind` (mặc định) | chỉ văn bản + `sentences.json` để neo finding; **không** nhận `draft.meta.json` | tài liệu từ ngoài, hiệu chuẩn, đối chứng độc lập |
| `audit` | thêm `draft.meta.json`, đọc **sau** khi bản đọc mù đã khoá; đối chiếu ID bằng `shared/scripts/check_spans.py` (0 gọi mô hình) | văn từ chính studio — trả **báo cáo liêm chính**, không trả điểm |

**Luật đọc, không thương lượng:**

> Trên văn đã đi qua chính studio này, `low_signal` ở chế độ mù là **kết quả kỳ vọng, không phải bằng
> chứng**. Không lấy S/C mù của sản phẩm studio ra phán xét — dùng `audit`.

Cơ sở là số đo, không phải suy luận. Ca `cot-b-ai-baitap` (30/08/2026, chi tiết ở
`docs/results/self-audit-cot-B.md`): một bài **100 % do máy viết** qua trục 2 và trục 4, chấm mù bởi
một model khác, cho **S = 2/100 · C = 2,0 % · `low_signal` · 0 FLAG (0 %) · 2 NOTE (2/45 câu = 4,4 %)**,
và lớp đếm 0-token cho **0 tín hiệu**.

Đó không phải lỗi cài đặt. `vi-ai-tells.json` tự nhận là *"một danh sách, hai chiều"*: trục 2 dùng nó
để **tránh**, trục 5 dùng nó để **soi**. Văn được sinh ra bằng cách tránh đúng danh sách ấy thì chính
danh sách ấy không thấy nó — **hằng đẳng thức, không phải lỗ hổng bị lợi dụng**. Thêm vào đó, ở trạng
thái 0 tell `calibrated`, trục 5 chỉ nhìn thấy **tell rẻ** (cụm đệm, kết lạc quan, bộ ba); những tật
đắt — cụ-thể-giả-định thay cho cụ-thể-đã-sống, khuôn đối xứng lặp cả bài — cần đọc trọn bài mới thấy.

Hệ quả cho người viết báo cáo:

- Ở `blind`, câu *"không tìm thấy dấu hiệu"* chỉ được phát biểu kèm phạm vi: **không tìm thấy dấu hiệu
  trong danh mục hiện có**, và danh mục đó chưa hiệu chuẩn. Không suy ra "bài do người viết".
- Ở `audit`, câu hỏi đổi hẳn: không phải *máy có đoán ra được không*, mà là **bản tự khai có khớp với
  văn bản không** — câu nào máy viết mà chưa khai, ID nào trỏ trượt. Đó là câu hỏi trả lời được, và
  trả lời được bằng phép so tập hợp chứ không bằng phán đoán.
- Bản giao thiếu sidecar provenance là một **khiếm khuyết quy trình** đáng nêu trong báo cáo — nhưng
  vẫn **không** phải bằng chứng về nguồn gốc. Hai chuyện khác nhau, đừng gộp.

---

## 6. Tín hiệu đã bị BÁC BỎ bằng thực nghiệm — đừng dùng lại

| Tín hiệu | Vì sao bỏ |
|---|---|
| **Tỷ lệ NFC/NFD Unicode** | Word **tự chuẩn hoá NFC khi lưu**. Mọi file `.docx` đều thuần NFC. Vô dụng. |
| Ký tự ẩn (ZWSP, NBSP), em-dash | Đo trong ca thật: **0 lần** ở cả bài AI lẫn bài người. Tín hiệu tiếng Anh, không chuyển sang tiếng Việt. |
| MATTR-100 đơn độc | Thực đo: 0,851 / 0,823 / 0,865 cho bài nghi vấn / người / AI — **không phân biệt được**. |
| Danh sách cliché viết tay | Xem mục 2. |
| Điểm số kiểu `if std_dev < 6.0: += 35` | Hằng số không có cơ sở; kẹp `min(98, max(5, x))` khiến hệ thống không bao giờ được nói "không có dấu hiệu". |

---

## 7. Chính sách và pháp lý

**Thông tư 49/2026/TT-BGDĐT** (hiệu lực 15.08.2026) — lần đầu Việt Nam quy định về AI trong giáo dục
đại học. Nó yêu cầu **xác thực danh tính người học, lưu vết quá trình học tập, truy xuất và kiểm chứng**;
coi việc **không khai báo sử dụng AI khi được yêu cầu** là vi phạm liêm chính.
**Thông tư KHÔNG nêu tên và KHÔNG bắt buộc bất kỳ công cụ phát hiện AI nào.**

→ Luật Việt Nam thưởng cho **khai báo + lưu vết**, không chống lưng cho điểm số detector.

Quốc tế cùng hướng: Vanderbilt tắt Turnitin AI detector từ 16.08.2023 và giữ nguyên (phép tính của họ:
1% lỗi × 75.000 bài = **750 bài bị gắn cờ oan**). Chính Turnitin công bố FPR cấp câu ~**4%** và hướng dẫn
rằng câu được tô sáng là *"khu vực cần quan tâm"*, dùng để **mở đối thoại, không phải kết luận**.

---

## 8. Câu hỏi tự kiểm trước khi xuất báo cáo

1. Tôi đã hiệu chỉnh theo **thể loại** chưa?
2. Mỗi nhận định của tôi có **phản chứng** chưa?
3. Tôi có đang phạt tác giả vì **viết đúng văn phong được dạy** không?
4. Nếu bài này của **con tôi**, tôi có thấy báo cáo này công bằng không?
5. Bằng chứng mạnh nhất của tôi là **cứng** (nguồn không tồn tại) hay **xác suất** (văn nghe giống AI)?
6. Tôi đã nói rõ đây **không phải xác suất AI** chưa?
