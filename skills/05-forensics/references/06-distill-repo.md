# Distill từ các repo detection — tín hiệu nào đáng mang sang, cái nào bỏ

Skill này **không chạy model ML**. Nhưng các repo dưới đây đã tốn nhiều công tìm ra *nên đo cái gì*.
File này chưng cất phần tri thức đó thành tín hiệu mà một agent + script nhẹ thực hiện được.

Trạng thái repo đã kiểm tra lại ngày **2026-08-29**.

## Quyết định nguồn nền

Không có repo nào đồng thời đạt bốn điều: **tiếng Việt-native · agent đọc trực tiếp · finding có vị trí
và cách sửa · điểm/tỷ lệ minh bạch**. Vì vậy skill chọn **một nguồn kiến trúc** và dùng các repo còn
lại làm đối chiếu, không trộn nhiều codebase thành một hệ khó kiểm soát:

1. **Nguồn kiến trúc chính — `SalZaki/antislop` (MIT).** Chọn vì nó tách rõ phần đếm ổn định và phần
   agent phán đoán ngữ nghĩa; mọi finding có category, vị trí, trích dẫn, severity và fix; một shared spec
   ngăn các lens detect/score/rewrite trôi định nghĩa. Phần mang sang: schema finding, progressive
   disclosure, ngưỡng hội tụ nhiều dấu hiệu và nguyên tắc sửa nguyên nhân thay vì thay từ.
2. **Comparator tiếng Việt-native — `trieuntu/VietAIDetector` (MIT).** Chỉ dùng để đối chiếu cách chia
   văn bản thành chunk, gắn nhãn từng vùng và biểu diễn độ phủ. Không mang tầng model hoặc code vào
   skill mặc định vì cần hai PhoGPT-4B, 20GB model và tối thiểu khoảng 24GB VRAM; điều đó trái yêu cầu
   agent-first.

`VietAIDetector` tính `AI percentage = số chunk dưới ngưỡng / tổng chunk`. Skill này distill **hình thức
đo độ phủ**, nhưng thay chunk-model bằng câu do agent gắn `PLAIN/NOTE/FLAG` và báo rõ C chỉ là độ phủ
dấu hiệu. Không sao chép ngưỡng 0,928 sang rubric ngôn ngữ; hai hệ đo khác bản chất.

`SalZaki/antislop` cố ý không xuất headline score để chống Goodhart. Yêu cầu sản phẩm hiện tại cần S/C,
nên skill giữ điểm nhưng bảo toàn rào chắn của repo nguồn: luôn kèm finding có vị trí, phản chứng, cách
sửa, khoảng bất định và hành động của con người. Con số không được đứng một mình.

---

## 1. `stef41/lmscan` — Apache-2.0 · 27★ · push 2026-04-11 · zero dependency

**Đáng học nhất về mặt kiến trúc.** Chạy 0,01s, không GPU, không API key, có trên PyPI, 193 test.

Bộ feature nó đo: `burstiness` · `sentence length variance` · `slop word density` ·
`transition word ratio` · `readability consistency`.

| Mang sang | Bỏ |
|---|---|
| ✅ Ý tưởng **bảng feature minh bạch + cờ giải thích được**, thay vì một điểm mờ đục | ❌ Từ điển "slop word" — **chỉ tiếng Anh** (`delve`, `tapestry`, `beacon`) |
| ✅ `readability consistency` — độ ổn định của độ khó giữa các đoạn | ❌ Tokenizer whitespace — sai với tiếng Việt |
| ✅ Cách trình bày verdict + confidence + per-signal | ❌ **"Model Attribution"** (đoán GPT-4 62% / Claude 13%) — chỉ dựa danh sách từ, không có cơ sở. **Không tái tạo tính năng này.** |

---

## 2. `HendrikStrobelt/detecting-fake-text` (GLTR) — Apache-2.0 · 500★ · push 2024-01-18 *(2,5 năm không cập nhật)*

**Đóng góp bất tử: cách trình bày bằng chứng.** Tô màu từng token theo hạng dự đoán —
xanh (top-10) · vàng (top-100) · đỏ (top-1000) · tím (>1000).

| Mang sang | Bỏ |
|---|---|
| ✅ **Nguyên tắc 3–4 mức rời rạc, không gradient giả chính xác** — đã đưa vào thang `review_priority` | ❌ Backend GPT-2 tiếng Anh |
| ✅ Ý tưởng "bằng chứng trực quan trước hội đồng" | ❌ Chấm từng token — trong thực đo, top/bottom toàn **tiêu đề và câu ngắn**, tức nhiễu thuần |

**Bài học thực nghiệm quan trọng:** khi chấm từng câu, cả đầu "máy nhất" lẫn đầu "người nhất" đều bị
tiêu đề chiếm chỗ. → **Bỏ mọi đoạn dưới 40 token; dùng cửa sổ 2–4 câu; lấy median chứ không lấy cực trị.**

---

## 3. `satyamshivam13/AI_Text_Detector` — MIT · 2★ · push 2026-07-14

⚠️ Mô tả "siêu nhẹ không cần GPU" là **sai**: `requirements.txt` có `torch>=2.6` + `transformers>=4.48`,
RAM 2–6GB cho mode GPT-2/ensemble.

| Mang sang | Bỏ |
|---|---|
| ✅ Cấu trúc `AnalysisResult`: **verdict + confidence + per-signal metrics + narrative explanation** | ❌ Toàn bộ tầng model |
| ✅ Có **evaluation harness thật** — ý tưởng `fixtures/` bắt buộc | ❌ NLTK punkt/brown — tiếng Anh |
| ✅ Thái độ "honest about its limits" trong README | |

---

## 4. `vedangvatsa/ai-detection-at-scale` — **KHÔNG CÓ LICENSE** · 0★

🔴 **Không được dùng lại code.** Không license = mặc định giữ toàn quyền.
Mô tả "35+ features" cũng sai — thực tế **31**.

Chỉ lấy **ý tưởng danh mục**: register-aware ensemble — tức **chuẩn hoá theo thể loại trước khi chấm**.
Đó chính là nguyên tắc trung tâm của skill này.

---

## 5. `ahans30/Binoculars` — BSD-3 · và `baoguangsheng/fast-detect-gpt` — MIT

Cần model để chạy → **ngoài phạm vi skill này**. Nhưng hai bài học khái niệm thì mang sang được:

- **Binoculars mạnh nhất ở vùng low-FPR** (TPR >90% ở FPR 0,01%). Triết lý "thà bỏ lọt còn hơn bắt oan"
  đã được đưa vào thang hành động: dưới 30 điểm thì **không lưu hồ sơ nghi vấn**.
- **Nguyên tắc hai họ phương pháp**: chỉ gắn cờ khi ≥2 nguồn *khác bản chất* cùng chỉ một hướng.
  Trong skill này, hai nguồn đó là **agent đọc mù** và **script đếm tất định**.

---

## 6. `liamdugan/raid` (RAID benchmark) — MIT

6 triệu generation · 11 model · 8 domain · **11 kiểu tấn công đối kháng**.

**Kết luận phải nhớ:** detector đỉnh có thể **rơi từ ~100% xuống gần 0%** chỉ vì đổi decoding strategy;
paraphrase và "humanizer" phá được phần lớn detector.

→ Hệ quả cấu trúc: **học viên biết né thì né được, học viên trung thực thì không né gì cả.** Hệ thống
có xu hướng bắt nhầm người thật thà và bỏ lọt người gian lận có kỹ năng. Đây là lý do skill này
**không bao giờ tự kết luận**, và vì sao cần `fixtures/mixed-edited/`.

---

## 7. `berenslab/llm-excess-vocab` — MIT

Chứa **900 excess words tiếng Anh** kèm annotation + ma trận tần suất theo năm, từ phương pháp
"excess vocabulary" của Kobak et al. (arXiv 2406.07016, Science Advances 2025) — họ đo được **≥13,5%
abstract PubMed 2024** qua xử lý LLM.

**Không dùng danh sách** (tiếng Anh). **Dùng phương pháp** để tự xây bản tiếng Việt:

1. Corpus mốc **≤2021** (VJOL, VCGate, kho báo, Wikipedia-vi) và corpus so sánh **≥2024**.
2. Tách từ bằng `underthesea` **trước khi đếm**.
3. Tần suất **binary theo tài liệu** (bao nhiêu % tài liệu chứa cụm đó) theo từng năm.
4. Lọc từ tăng do **sự kiện thật**: LLM tạo **bậc thang đột ngột tại 2023**, sự kiện thật tạo **đường dốc**.
5. Kết quả là danh sách có **hệ số tăng đo được** — dùng làm z-score, không phải danh sách nhị phân.

⚠️ Excess-vocabulary là công cụ đo trên **corpus lớn**. Áp lên một bài 3.000 từ là **lạm dụng phương pháp**.

**Chưa ai làm việc này cho tiếng Việt** — đây là đóng góp nghiên cứu thật nếu công bố.

---

## 8. `trieuntu/VietAIDetector` — MIT · 0★ · 10 commit tại lần kiểm tra

Hiện thực VietBinoculars (arXiv 2509.26189) với `vinai/PhoGPT-4B` + `PhoGPT-4B-Chat`, ngưỡng đã hiệu
chuẩn cho tiếng Việt (Youden 0.9280 · Low-FPR 0.8993), kèm OCR `5CD-AI/Vintern-1B-v2` cho PDF scan.
Repo có chunk-level highlight, ba mode ngưỡng và báo cáo tỷ lệ vùng nghi AI. Yêu cầu ≥24GB VRAM.

**Ngoài phạm vi skill này** (cần GPU). Ghi lại vì: nếu về sau muốn thêm tầng model cho tiếng Việt,
đây là điểm khởi đầu — nhưng con số >99% là **tự báo cáo trong paper/repo và chưa phải bằng chứng
đủ để dùng cho quyết định kỷ luật**. RAID cho thấy detector có thể suy giảm mạnh khi gặp model, domain,
decoding hoặc tấn công chưa thấy.

---

## 9. Đã loại có chủ đích

| Thành phần | Lý do |
|---|---|
| `openai-community/roberta-base-openai-detector` | Detect GPT-2, từ 2019. Model card tự cảnh báo không dùng cho cáo buộc học thuật |
| `Hello-SimpleAI/chatgpt-detector-roberta` | Train 1 epoch trên HC3 thời ChatGPT-3.5 |
| Ghostbuster | Phụ thuộc API `davinci` OpenAI đã khai tử 01/2024 |
| SynthID watermark | Chỉ detect khi giữ khoá lúc sinh; khoá Gemini là của Google |
| `pip install writeprints` | **Không tồn tại** — Writeprints là bộ feature trong literature, không phải package |
| textstat, TAALED | Công thức readability tính syllable theo tiếng Anh — vô nghĩa với tiếng Việt |
| Hallucinator | Tốt (12+ nguồn) nhưng **AGPL-3.0** — nhúng vào dịch vụ cho trường sẽ kích hoạt nghĩa vụ công bố source |
