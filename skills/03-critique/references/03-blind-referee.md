# Chấm mù — quy trình bốn bước

Phương pháp trong file này thuộc bộ luật của studio; nguồn gốc tri thức ghi ở sổ xưởng (không nằm trong repo). Luật gốc: **người chấm không được nhận câu hỏi
mớm, và không được biết phần nào do máy viết, trước khi chấm xong.** Đây là luật quan trọng nhất của
trục 3; hồ sơ thể loại bật nó bằng `blind_referee: true` ở §3.

## Vì sao

Ba cơ chế, cơ chế nào cũng đủ để làm hỏng một lượt chấm:

1. **Neo bởi câu hỏi mớm.** "Anh xem giúp đoạn 3 có yếu không" biến việc chấm thành việc đi tìm bằng
   chứng cho một kết luận đã có. Sau câu đó, đoạn 3 sẽ yếu — kể cả khi nó không yếu.
2. **Neo bởi nguồn gốc.** Biết trước đoạn nào do máy viết thì điểm sẽ chấm cho *nguồn gốc* chứ không
   cho *chất lượng*. Nguy hiểm gấp đôi ở repo này, vì trục 2 tự khai `machine_written_spans[]` — bản
   tự khai trung thực sẽ trở thành hình phạt, và lần sau sẽ không ai khai nữa.
3. **Thiên vị bản thân.** Khi bài do chính mô hình này viết ở trục 2, việc đọc `draft.meta.json`
   trước làm hỏng nốt lớp bảo vệ cuối. Xem `skills/05-forensics/references/03-chong-bao-oan.md` mục 1
   về self-recognition bias.

## Bốn bước, đúng thứ tự

### Bước 1 — Đọc trôi

Đọc hết một mạch. **Chưa chấm, chưa ghi finding.** Ghi đúng ba dòng:

- bài này nói gì, viết lại thành một câu;
- chỗ nào phải đọc lại lần hai mới hiểu;
- câu hỏi đầu tiên muốn hỏi tác giả.

Được xem: bản thảo, đề bài hoặc barem thật (`rubric_source`), §3 của hồ sơ thể loại.
Cấm xem: `draft.meta.json`, lịch sử hội thoại của trục 2, mọi lời dặn kiểu "chú ý đoạn X".

### Bước 2 — Chấm từng tiêu chí

Với **mỗi** `criteria[]` mà §3 khai: trưng ra thứ trường `evidence` đòi, trả lời câu hỏi ở trường
`question`, rồi mới cho điểm. Đúng thứ tự đó — cho điểm trước rồi đi tìm lý do là cách nhanh nhất để
biến ấn tượng thành điểm số.

Chấm **riêng** từng tiêu chí. `critique.schema.json` cố ý không có điểm tổng: cộng gộp che mất
chuyện văn trơn tru đang gánh cho lập luận yếu, đúng thứ repo này tồn tại để không làm.

### Bước 3 — Chạy lăng kính

Chạy đúng các `lenses[]` mà §3 bật, không hơn không kém, theo
[`01-lang-kinh.md`](01-lang-kinh.md). Mỗi finding phải có vị trí, câu trích, bằng chứng, **phản
chứng** và câu hỏi xác minh.

Vị trí neo bằng `sentence_id` của `sentences.json` **do studio sinh** (`extract.py`), **không tự đếm
câu**. Ca cổng Phase 5 có ba hệ đánh số cho cùng một bài — bản thảo 43, `sentences.json` 45, người
chấm tự đếm 46 — nên `critique.json`, `draft.meta.json` và báo cáo của trục 5 không map được vào
nhau bằng ID, phải map bằng trích dẫn. Không có `sentences.json` thì xin sinh trước khi chấm; sinh
rồi mà văn bản còn sửa thì sinh lại, và chạy `shared/scripts/check_spans.py` để biết id nào đã dịch. Lăng kính chạy thừa hoặc không chạy được đều ghi vào `limitations[]`.

Điểm ở bước 2 được phép hạ nếu lăng kính tìm ra thứ chưa thấy — nhưng phải ghi rõ finding nào làm
đổi điểm nào.

### Bước 4 — Mở phong bì, rồi viết `must_fix`

Chỉ đến đây mới được đọc `draft.meta.json`, `context.json` và mọi lời dặn đã tạm gác.

Được dùng cho: **xếp thứ tự ưu tiên** `must_fix[]`, và ghi thêm vào `limitations[]` thứ mình đã không
thấy được.

**Không** được dùng để: đổi điểm ở bước 2, thêm finding mới, hoặc rút finding đã có. Bằng chứng
không đổi vì biết ai viết ra nó.

## Niêm phong

Chỉ ghi `blind_referee: true` vào `critique.json` khi cả bốn bước đã chạy đúng thứ tự. Nếu người dùng
đã kịp mớm câu hỏi, hoặc `draft.meta.json` đã nằm sẵn trong ngữ cảnh trước bước 1, thì:

- vẫn chấm bình thường;
- ghi `blind_referee: false`;
- ghi vào `limitations[]` đúng thứ đã nhìn thấy trước.

Khai `true` khi thực tế không mù là hỏng thứ duy nhất mà trường đó dùng để bảo đảm.

## Khi hồ sơ thể loại khai `blind_referee: false`

Có thể loại mà bối cảnh là một phần của tiêu chí — bản thảo tiếp theo của một loạt bài, hay bài viết
cho một khách hàng có hồ sơ giọng riêng. Khi §3 khai `false`, được đọc bối cảnh từ đầu, nhưng ba
điều vẫn giữ nguyên: chấm từng tiêu chí riêng, mỗi finding có phản chứng, và câu hỏi mớm vẫn bị gác
đến bước 4.
