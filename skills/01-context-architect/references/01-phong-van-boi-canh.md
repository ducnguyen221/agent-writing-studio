# Phỏng vấn bối cảnh

Chưng cất từ `doc-coauthoring` của `anthropics/skills` (**không có license — idea-only**, xem
`vendor-notes/anthropics-skills/`). Lấy đúng hai nguyên lý: *thu thập bối cảnh là một pha riêng,
đứng trước pha viết* và *người viết cùng phải hỏi trước khi gõ chữ đầu tiên*. Không câu chữ nào của
upstream có mặt ở đây.

Nguyên lý ấy trong studio này có một hình dạng cụ thể: câu hỏi **không do skill nghĩ ra**. Skill đọc
`intent_questions[]` ở `§1` của hồ sơ thể loại và hỏi đúng từng câu ở đó. Thêm thể loại là thêm một
file trong `shared/genres/`, không sửa skill.

## Luật số một: không viết gì trước khi đủ

`stop_if_missing[]` ở `§1` là **điều kiện dừng, không phải lời khuyên**. Còn một mục chưa gỡ được thì
trục 1 dừng, ghi mục đó vào `intent.unresolved[]` của `context.json`, và trục 2 từ chối viết.

Ba cách lách hay gặp, cả ba đều cấm:

- **Tự trả lời hộ.** Suy ra một đáp án hợp lý rồi coi như đã hỏi. Nếu buộc phải suy, mục
  `answers[].source` phải ghi `inferred`, và người dùng phải xác nhận trước khi trục 2 chạy.
- **Viết thử một đoạn "cho dễ hình dung".** Một đoạn viết ra sẽ neo cả bài vào giả định chưa kiểm.
- **Đổi câu hỏi khó thành câu hỏi dễ.** "Kết quả nào sẽ bác bỏ giả thuyết?" không được thay bằng
  "Anh kỳ vọng kết quả thế nào?".

## Bốn lượt hỏi

**Lượt 1 — lấy nguyên văn.** Đề bài, yêu cầu, hạn nộp, giới hạn từ: chép đúng lời người dùng vào
`intent.task`, không diễn giải. Diễn giải sớm là chỗ mất yêu cầu đầu tiên.

**Lượt 2 — hỏi theo `intent_questions[]`.** Mỗi câu một mục trong `intent.answers[]`. Hỏi **từng
câu**, không gộp năm câu vào một tin nhắn: người trả lời gộp sẽ bỏ qua câu khó nhất. Khi `§1` khai
cách hỏi theo góc nhìn — `research.md` mượn lối này từ `storm` — thì hỏi lần lượt từ từng góc, vì
người phản biện phương pháp và người dùng kết quả không hỏi cùng một câu. Câu trả lời ghi **kết
luận** của người dùng (≤ 600 ký tự); người dùng dán cả tài liệu vào thì tài liệu ấy thành một con trỏ
trong `brain_pointers[]`, không nằm trong `answer` — xem [cầu Brain](03-cau-brain.md) mục "Ba lỗ rò".

**Lượt 3 — lõi một câu.** Viết `intent.thesis_one_sentence`. Phép thử **do `§1` của hồ sơ thể loại
khai, không do skill đặt ra** — hỏi sai phép thử là ép bài vào khuôn của một thể loại khác:

- **Thể loại lập luận** (`essay`, `research`, `chinh-luan`): một câu **có thể bị phản bác**. Nói được
  câu ngược lại mà vẫn là một phát biểu nghiêm túc thì đạt. "Bài này bàn về AI trong giáo dục" không
  đạt — câu ngược lại vô nghĩa.
- **Truyện** (`novel.md` `§1`): một câu gồm **nhân vật chính muốn gì – cái gì cản – mất gì nếu thua**.
  Câu ấy không phản bác được, và không cần phản bác được: tiểu thuyết thuyết phục bằng thứ người đọc
  tin là đã xảy ra, không bằng lập luận. Đòi nó "phản bác được" là đòi sai thể loại.
- **Còn lại:** lấy đúng phép thử mà `intent_questions[]` và `stop_if_missing[]` của hồ sơ khai —
  `blog.md` hỏi sau khi đọc người ta **làm được việc gì**, `journalism.md` hỏi **ai làm gì, ở đâu,
  khi nào**.

Đưa câu ấy lại cho người dùng xác nhận; đây là lúc rẻ nhất để phát hiện hai bên đang nói về hai bài
khác nhau.

**Lượt 4 — ràng buộc.** `constraints[]`: số từ, chuẩn trích dẫn, điều cấm nói, định dạng nộp. Đánh
dấu `hard: true` cho thứ mà vi phạm là hỏng bài chứ không phải trừ điểm.

## Chân dung độc giả

`audience_fields[]` ở `§1` quy định khoá bắt buộc; hình dạng và ý nghĩa từng khoá ở
`shared/writers/audience.schema.json`. Hỏi tối thiểu: trình độ, đã biết gì, chưa biết gì, nỗi đau,
kỳ vọng, thứ khiến họ bỏ đọc, kênh đọc.

Hai nhầm lẫn phải tránh:

- **Độc giả không phải người chấm.** Bài nộp hội đồng có hai đối tượng khác nhau, và `expectations`
  của họ khác nhau. Khai cả hai thì tách thành hai chân dung, đừng trộn.
- **Chân dung không loại trừ ai thì chưa phải chân dung.** Điền `not_this_audience`.

## Persona người viết

`writer_profile_ref` trỏ tới `shared/writers/<slug>/profile.yaml`, **không nhúng nội dung**. Không có
hồ sơ thì để `null` và viết theo giọng mặc định của thể loại — không bịa ra một giọng. Hồ sơ
`status: draft` (dưới 3 bài) chỉ dùng để tham khảo. Cách dựng hồ sơ ở
[hiệu chỉnh giọng](04-hieu-chinh-giong.md).

## Kết thúc phỏng vấn

`context.json` hợp lệ theo `shared/schemas/context.schema.json`, và:

- `answers[]` phủ hết `intent_questions[]` của `§1`;
- `unresolved[]` rỗng, hoặc nếu không rỗng thì đã nói thẳng với người dùng rằng bài chưa viết được;
- mọi `answers[].source: inferred` đã được xác nhận;
- không nguyên văn tài liệu riêng tư nào lọt vào file — Brain chỉ vào bằng con trỏ, xem
  [cầu Brain](03-cau-brain.md).
