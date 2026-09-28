# `samples/` — một ca mẫu tổng hợp, kèm kết quả kỳ vọng

Thư mục này là **bài thực hành đầu tiên** và là thứ `python studio.py doctor` kiểm offline. Mọi thứ ở
đây **tự soạn, không của người thật**: bài không có tên người, tên đơn vị hay số liệu lấy từ công việc
thật. Bài của người thật không bao giờ vào đây — chúng ở workspace `.work/` hoặc station.

| File | Là gì |
|---|---|
| `bai-mau.md` | bài luận ngắn thể loại `essay`, có **một** chỗ yếu cố ý (khẳng định tỷ lệ không có nguồn ở đoạn 2) |
| `context.json` | bối cảnh trục 1 đã gỡ hết — hợp lệ theo `shared/schemas/context.schema.json` |
| `critique.expected.json` | bản chấm trục 3 **kỳ vọng**: đủ sáu tiêu chí của `essay` §3, ba lăng kính, một finding trỏ đúng câu yếu, kết quả rà dẫn nguồn được nói ra |

## Chạy thử

Mở thư mục repo trong ứng dụng AI rồi nói:

> *"Chấm `samples/bai-mau.md` theo hồ sơ `essay`, dùng bối cảnh `samples/context.json`. Ghi `critique.json`
> vào `.work/mau/`. Đừng mở `samples/critique.expected.json` trước khi chấm xong."*

Rồi so kết quả với `critique.expected.json`. Điểm từng tiêu chí được phép lệch — người chấm khác nhau cho
điểm khác nhau. Thứ **không** được lệch: bắt được câu *"Hầu hết người đi làm…"* là chỗ thiếu bằng chứng,
không có điểm tổng, `limitations[]` không rỗng và có một dòng nói kết quả rà dẫn nguồn.

Test `tests/shared/test_samples.py` khoá hình dạng của ba file này: đúng schema, tiêu chí và lăng kính
khớp hồ sơ `essay`, và mọi câu trích trong finding có thật trong bài mẫu.
