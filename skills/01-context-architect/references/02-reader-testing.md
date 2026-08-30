# Reader testing — giả lập độc giả đọc dàn ý

Chưng cất từ `doc-coauthoring` (**idea-only**, không license): ý tưởng *thử tài liệu bằng cách đọc
nó bằng mắt người nhận trước khi gửi*. Ở đây ý đó có một hình dạng kiểm được: dựng độc giả từ
`shared/writers/audience.schema.json`, cho họ đọc dàn ý, thu về **đúng ba câu hỏi họ sẽ hỏi**.

Chạy khi đã có `context.json` và một dàn ý (trục 2 sinh tầng 1–2). Chạy **trước** khi viết prose:
sửa dàn ý tốn vài phút, sửa bài đã viết tốn cả buổi.

## Vì sao ba câu

Ba là con số ép chọn. Một câu thì chỉ ra được lỗ hổng dễ thấy nhất; mười câu thì thành danh sách
mong muốn và không ai xử lý hết. Ba câu buộc phải xếp hạng, và thứ hạng chính là thông tin.

## Cách chạy

**Bước 1 — nạp chân dung, không nạp ý đồ tác giả.** Đọc `audience` trong `context.json`. **Không**
đọc `intent.thesis_one_sentence` trước khi ra câu hỏi. Biết trước luận đề thì sẽ sinh ra những câu
mà luận đề trả lời được — bài kiểm tự nghiệm đúng, và vô giá trị. Đây là biến thể của luật chấm mù ở
trục 3.

**Bước 2 — đọc dàn ý một lượt, đúng kênh của độc giả.** `reading_channel` và `time_budget_minutes`
là ràng buộc thật: người đọc trên điện thoại giữa hai cuộc họp không đọc tới mục 7. Đọc tới đâu hết
thời gian thì ghi lại mốc đó.

**Bước 3 — ba câu hỏi, mỗi câu neo vào một trường.** Sinh câu hỏi từ chân dung, không từ cảm giác:

| Câu hỏi bật ra từ | Dạng câu hỏi |
|---|---|
| `does_not_know` gặp thuật ngữ chưa chú | "Chỗ này nghĩa là gì?" |
| `pains` không được mục nào chạm tới | "Vậy tôi phải làm gì với trường hợp của tôi?" |
| `evidence_bar` cao hơn bằng chứng dàn ý đang có | "Con số này lấy ở đâu?" |
| `prior_beliefs` ngược với một mục | "Tôi nghe ngược lại, sao lại thế?" |
| `expectations` chưa mục nào đáp | "Bài này trả lời được câu tôi cần chưa?" |

**Bước 4 — chấm mốc bỏ đọc.** Với từng mục trong `drop_off_triggers`, trả lời có/không kèm vị trí
trong dàn ý. Đây là phần kiểm được, không phải cảm nhận.

**Bước 5 — ghi vào `context.json`.** Ba câu hỏi và các mốc bỏ đọc đi vào `constraints[]` dạng phát
biểu ("phải giải thích X trước khi dùng", "phải có số có nguồn trong ba đoạn đầu"), hoặc vào
`intent.unresolved[]` nếu chúng cho thấy bối cảnh còn thiếu. Reader testing **không sửa dàn ý** — nó
chỉ báo cáo; sửa là việc của người viết cùng trục 2.

## Hai độc giả, hai bài

Phép thử của chính cơ chế này: lấy một đề bài, dựng hai chân dung khác nhau, chạy reader testing hai
lần. Nếu ba câu hỏi thu về giống nhau thì hoặc hai chân dung chưa đủ khác, hoặc chân dung chưa được
dùng thật. Trường tạo khác biệt mạnh nhất theo thứ tự: `evidence_bar`, `already_knows`,
`drop_off_triggers`, `time_budget_minutes`.

## Cấm

- **Không bịa độc giả.** Chân dung `source: inferred` phải được người dùng xác nhận trước, đúng luật
  của `answers[].source`.
- **Không biến câu hỏi độc giả thành lệnh phải sửa.** Chúng là dữ liệu cho người viết cân nhắc; có
  câu hỏi đúng mà vẫn không sửa là lựa chọn hợp lệ, miễn ghi lại lý do.
- **Không dùng reader testing để chấm bài.** Chấm là trục 3, có barem và có bằng chứng trích được.
- **Không suy ra chân dung từ chính bài đang viết.** Suy ngược như vậy chỉ khẳng định lại bài.
