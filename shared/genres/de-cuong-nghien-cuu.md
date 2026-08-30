# Hồ sơ thể loại: đề cương nghiên cứu

**Hồ sơ một phần (`partial`): chỉ có §5.** Thể loại này đã phải giám định thật trước khi tới lượt
soạn phần viết, nên hồ sơ chỉ khai thứ trục 5 cần: yêu cầu bắt buộc của thể loại và các tín hiệu là
văn phong chuẩn. Trục 1–4 không đọc file này.

**Quan hệ với `research.md` — đọc trước khi dùng.** Hai slug này không trùng nhau và không thay được
cho nhau. Khi **viết** một đề cương, dùng `research.md` với `structures[].id = de_cuong`: ở đó có
đủ §1–§4 cho trục 1–4. Khi **giám định** một đề cương, dùng file này: nó khai riêng thứ mà đề cương
nghiên cứu sinh Việt Nam bắt buộc phải có, thứ `research.md` không nói vì `research.md` viết chung
cho cả bài báo và khoá luận. Một câu để nhớ: `research` là hồ sơ viết, `de-cuong-nghien-cuu` là hồ
sơ giám định.

Phạm vi: đề cương nghiên cứu sinh, đề cương luận văn, thuyết minh đề tài. Nguồn của mục dưới đây là
bảng "thể loại bắt buộc có gì" ở `skills/05-forensics/references/01-rubric-5-truc.md` trục 4.

## 5. Must-have cho forensics

Trục 5 đọc mục này để tiền đăng ký yêu cầu thể loại và biết tín hiệu nào là bình thường ở đề cương nghiên cứu.

Tiền đăng ký các mục dưới đây trước khi đọc bài. Yêu cầu đặc trưng của thể loại: **khoảng trống
nghiên cứu phải nêu đích danh tác giả và công trình đi trước**, rồi chỉ ra họ chưa trả lời cái gì.
Một đề cương viết "hiện chưa có nhiều nghiên cứu về vấn đề này" là đề cương chưa đọc tài liệu — và
đó cũng chính là chỗ một bản thảo sinh ra từ đề bài chung chung dừng lại, vì nó không có danh sách
công trình thật để đối chiếu.

Đặc trưng thứ hai: đề cương nói về **việc chưa làm**, nên nó phải phân biệt rành mạch việc đã làm
với việc dự định làm. Chỗ lẫn hai thứ đó là chỗ hội đồng hỏi đầu tiên.

Thiếu một mục là dấu hiệu về **năng lực thể loại**, không tự nó chứng minh nguồn gốc AI. Danh mục
tài liệu tham khảo không tra được là finding đáng theo đuổi bằng cách mở từng nguồn, không phải bằng
cách suy đoán ai đã viết.

Cảnh báo báo oan riêng của thể loại: đề cương viết theo **mẫu của cơ sở đào tạo**, nên các mục lặp
lại giữa mọi đề cương cùng trường là điều đương nhiên; mục tiêu và câu hỏi nghiên cứu trùng nội dung
nhau vì biểu mẫu bắt viết cả hai; và toàn bài ở thì dự định nên cụm "sẽ tiến hành", "dự kiến" lặp
dày đặc. Xem `skills/05-forensics/references/03-chong-bao-oan.md` §2.

```yaml
must_have:
  - level: core
    statement: "Khoảng trống nghiên cứu nêu đích danh tác giả và công trình đi trước, kèm điều họ chưa trả lời"
    verify: "Liệt kê công trình được nêu tên trong phần tổng quan; với mỗi công trình, tìm câu nói rõ phần còn thiếu. Câu 'chưa có nhiều nghiên cứu' không tính"
  - level: core
    statement: "Câu hỏi nghiên cứu có biến số, phạm vi và mốc thời gian; nêu được kết quả nào sẽ bác bỏ giả thuyết"
    verify: "Viết lại câu hỏi thành một câu; hỏi tác giả kết quả nào làm giả thuyết sai — không trả lời được thì đây mới là chủ đề"
  - level: core
    statement: "Phương pháp dự kiến nêu nguồn dữ liệu cụ thể, cách tiếp cận mẫu và ai cho phép truy cập"
    verify: "Với mỗi nguồn dữ liệu, tìm tên đơn vị giữ dữ liệu và câu nói về quyền tiếp cận; 'thu thập số liệu thứ cấp' không tính"
  - level: minor
    statement: "Kế hoạch có mốc thời gian và sản phẩm đầu ra của từng giai đoạn"
    verify: "Đối chiếu bảng kế hoạch với thời hạn đào tạo; tìm giai đoạn không có sản phẩm nào"
  - level: minor
    statement: "Phân biệt rõ việc đã làm với việc dự định làm"
    verify: "Đánh dấu từng đoạn theo hai loại; đoạn không xếp được loại nào là đoạn cần hỏi lại"
genre_baseline:
  normal_signals:
    - "Các mục lặp lại giống nhau giữa mọi đề cương cùng cơ sở đào tạo: biểu mẫu bắt buộc"
    - "Mục tiêu và câu hỏi nghiên cứu trùng nội dung nhau: biểu mẫu yêu cầu viết cả hai"
    - "Câu ở thì dự định lặp dày ('sẽ tiến hành', 'dự kiến', 'nhằm mục đích'): toàn bài nói về việc chưa làm"
    - "Câu mở toàn cảnh 'Trong bối cảnh…' ở phần lý do chọn đề tài (T01): khuôn mở chuẩn của thể loại"
    - "Cụm 'đóng vai trò quan trọng', 'có ý nghĩa lý luận và thực tiễn' (T08)"
    - "Danh từ hoá và câu bị động không nêu chủ thể (T13): văn phong chuẩn của văn bản học thuật hành chính"
    - "Danh mục tài liệu tham khảo dài hơn phần thân: yêu cầu của thể loại, không phải dấu hiệu độn chữ"
```
