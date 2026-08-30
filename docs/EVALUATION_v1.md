# Giao thức đánh giá Forensics v1

> **Thuật ngữ** (S, C, FLAG/NOTE, `priority_check`, tell, provenance): bảng giải nghĩa ở
> [README](../README.md) mục 6. Riêng tài liệu này thêm mấy từ của nghề đo: *FPR* = tỷ lệ báo oan
> (bài của người bị đẩy lên mức kiểm tra ưu tiên) · *recall* = tỷ lệ bắt được trong số bài AI thật ·
> *precision* = trong số lần báo, bao nhiêu lần báo đúng · *span* = đoạn văn được đánh dấu ·
> *abstention* = biết từ chối kết luận khi dữ liệu không đủ.

## Mục tiêu

Đo khả năng sàng lọc của skill trong điều kiện thật, ưu tiên tránh báo oan. Không dùng một chỉ số
“accuracy” gộp vì corpus lệch lớp có thể làm con số đẹp giả.

## Corpus

Mỗi thể loại có bốn nhánh:

1. `human`: trước 2022, viết có giám sát hoặc có lịch sử chỉnh sửa đủ mạnh;
2. `ai`: nhiều model, nhiệt độ và họ prompt, lưu generation log;
3. `mixed`: AI sinh rồi người sửa và người viết rồi AI trau chuốt, có span gốc;
4. `adversarial`: paraphrase, humanizer, homoglyph, lỗi chính tả, đổi khoảng trắng, chèn đoạn người.

Chia train/dev/test theo tác giả và họ prompt. Không để bài cùng tác giả hoặc cùng prompt template
lọt qua nhiều split. Văn bản thật ở `fixtures/` và bị Git bỏ qua; Git chỉ nhận manifest/schema và số
liệu tổng hợp không chứa trích dẫn.

## Metrics bắt buộc

| Metric | Câu hỏi |
|---|---|
| FPR `priority_check` trên human | Bao nhiêu bài người bị đẩy lên kiểm tra ưu tiên? |
| Recall tại ngưỡng low-FPR | Giữ FPR cố định thì bắt được bao nhiêu AI? |
| Precision từng `rule_id` | Finding nào thường báo oan? |
| Span overlap trên mixed | Có định vị đúng vùng AI can thiệp không? |
| Abstention | Có biết dừng khi ngắn, OCR hỏng, sai ngôn ngữ không? |
| Deterministic stability | Cùng input khóa có ra cùng S/C không? |
| Agent repeatability | Ba lượt đọc có trùng finding ổn định không? |

## Cổng quy mô

- Pilot: ít nhất 30 human + 30 AI + 30 mixed cho một thể loại. Không human nào được lên
  `priority_check` mà không mở lại rubric và chạy lại dev.
- Pre-release: ít nhất 100 human + 50 AI; báo recall thật và cận trên FPR.
- Vùng FPR khoảng 1%: ít nhất 300 human cùng thể loại/pipeline. Quy tắc ba: 0 lỗi trên `n` cho cận
  trên 95% xấp xỉ `3/n`.

## Quy trình khóa ngưỡng

1. Chạy baseline chưa sửa.
2. Chỉnh rule/trọng số chỉ trên dev.
3. Tắt hoặc giảm rule có precision dưới 50% trên human.
4. Đóng băng version rules.
5. Chạy hidden test đúng một lần.
6. Công bố cỡ mẫu, slices, FPR, recall, abstention và failure modes.

Không xuất xác suất tác giả dùng AI cho đến khi có tập held-out đủ lớn và kiểm reliability curve,
Brier score cùng calibration error. S/C vẫn là đầu ra mặc định.

`shared/scripts/evaluate.py` chỉ nhận nhãn, rule ID và span số; nó từ chối trường chứa nguyên văn.
Chạy `python shared/scripts/evaluate.py records.jsonl --out aggregate.json` để xuất FPR người thật,
recall AI, precision theo rule, mixed-span IoU, abstention và cỡ từng slice. Đây là lớp đánh giá hỗ
trợ; việc gán nhãn fixture vẫn do con người kiểm soát.

## Kiểm thử ngôn ngữ khác

Phương pháp nguồn phải được chưng cất thành hướng dẫn tiếng Việt. Câu trích và khóa tra cứu có chức
năng giữ nguyên. Mỗi ngôn ngữ mới cần corpus và ngưỡng riêng; không dịch blacklist tiếng Anh/Việt để
giả lập hiệu chỉnh.
