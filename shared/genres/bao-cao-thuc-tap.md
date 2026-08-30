# Hồ sơ thể loại: báo cáo thực tập

**Hồ sơ một phần (`partial`): chỉ có §5.** Thể loại này đã phải giám định thật trước khi tới lượt
soạn phần viết, nên hồ sơ chỉ khai thứ trục 5 cần: yêu cầu bắt buộc của thể loại và các tín hiệu là
văn phong chuẩn. Trục 1–4 không đọc file này — nhưng trục 4 **có** đọc `genre_baseline` dưới đây qua
`polish_check.py`, để không báo oan các cột counter ở thể loại này.

Phạm vi: báo cáo thực tập, báo cáo kiến tập, nhật ký thực tập có phần tổng kết. Nguồn của mục dưới
đây là bảng "thể loại bắt buộc có gì" ở `skills/05-forensics/references/01-rubric-5-truc.md` trục 4.

## 5. Must-have cho forensics

Trục 5 đọc mục này để tiền đăng ký yêu cầu thể loại và biết tín hiệu nào là bình thường ở báo cáo thực tập.

Tiền đăng ký các mục dưới đây trước khi đọc bài. Yêu cầu đặc trưng của thể loại là thứ **chỉ người
đã đến đó mới có**: tên đầy đủ của đơn vị, tên và chức danh người hướng dẫn tại đơn vị, mốc thời
gian thực tập cụ thể, và công việc kể ở mức việc thật — phần mềm nào, biểu mẫu nào, bao nhiêu hồ sơ
một ngày. Một báo cáo nói về "công ty" chung chung và "các công việc được giao" là báo cáo không có
mặt ở đơn vị nào.

Đây cũng là thể loại mà must-have hữu ích nhất, vì nó không đòi hỏi năng lực viết: một sinh viên đi
thực tập thật, viết vụng, vẫn có đủ bốn thứ trên; một bản thảo trơn tru sinh ra từ tên ngành học thì
không có thứ nào.

Thiếu một mục là dấu hiệu về **năng lực thể loại hoặc về việc có thực tập thật hay không**, và cách
theo đuổi là hỏi tác giả về đơn vị — không phải suy đoán từ câu chữ.

Cảnh báo báo oan riêng của thể loại — **đây là thể loại công thức nhất trong repo và cũng là thể
loại bị chấm oan nhiều nhất**. Bố cục "kết quả đạt được – tồn tại, hạn chế – phương hướng" (`T06`)
và bộ ba song hành trong câu tổng kết (`T10`) là **bố cục bắt buộc và phép tu từ được dạy**, có từ
lâu trước khi có mô hình ngôn ngữ. Sự hiện diện của chúng **không bao giờ** là tín hiệu; chỉ nội
dung rỗng bên trong mới đáng nói, và cách xử lý là bơm nội dung chứ không phá khung. Xem
`skills/05-forensics/references/03-chong-bao-oan.md` §2 và §6, và
`skills/04-humanizer/references/03-chong-sua-oan.md`.

**Cân bằng — baseline hạ tín hiệu ở khung, không hạ ở nội dung.** Với danh sách `normal_signals`
dưới đây, gần như mọi cột counter của trục 5 đều tắt ở thể loại này; một bản thảo máy viết đúng
mẫu khoa sẽ qua trục 5 mù với `low_signal`, và đó là **kết quả kỳ vọng**, không phải lỗi. Thứ còn
lại để phân biệt nằm ở ba chỗ, và cả ba đều là việc **đối chiếu ra ngoài văn bản** chứ không phải
đọc câu chữ:

1. **Nhận xét của đơn vị thực tập có chữ ký và dấu** — mẫu báo cáo Việt Nam yêu cầu trang này. Tên
   đơn vị, tên người hướng dẫn và mốc ngày trong thân bài phải khớp với trang đó; thân bài ghi được
   ba thứ ấy mà không có trang xác nhận, hoặc có mà không khớp, mới là finding đáng theo đuổi. Máy
   bịa được tên công ty, không bịa được con dấu.
2. **Mốc thời gian khớp nhau**: kỳ thực tập ghi ở phần mở, số tuần trong nhật ký, kỳ số liệu ở phần
   thân và ngày trên trang xác nhận phải cùng một khoảng. Đây là phép kiểm 0 token và không có trong
   `normal_signals`.
3. **Cụ thể đã sống, không phải cụ thể giả định** (trục 5 rubric: "không có một trải nghiệm hay quan
   sát cá nhân nào"): việc kể bằng con số của chính người viết (bao nhiêu hồ sơ một ngày, lỗi nào bị
   trả lại, phần mềm phiên bản nào) là thứ must-have `core` thứ hai đòi; việc kể bằng "được tiếp cận
   quy trình", "hỗ trợ các anh chị trong phòng" là rỗng dù khung đúng.

Nói ngắn: khung `T06/T10/T01/T08/T13/T25` **không bao giờ** là tín hiệu; nội dung bên trong khung
**vẫn** được đọc bằng must-have và trục 5 rubric; và phán xét chỉ đứng trên bước đối chiếu với đơn vị.

```yaml
must_have:
  - level: core
    statement: "Có tên đầy đủ của đơn vị thực tập, tên và chức danh người hướng dẫn tại đơn vị, và mốc thời gian thực tập cụ thể"
    verify: "Tìm ba thứ này trong bài và ghi vị trí; đối chiếu với trang nhận xét của đơn vị (chữ ký, dấu) và với mốc ngày ở nhật ký, kỳ số liệu; tên đơn vị chỉ ghi chung chung, thiếu mốc ngày, hoặc không khớp trang xác nhận là chưa đạt"
  - level: core
    statement: "Công việc được kể ở mức việc cụ thể: phần mềm, biểu mẫu, số lượng hồ sơ hoặc ca việc mỗi ngày"
    verify: "Liệt kê các việc bài kể; với mỗi việc, hỏi nó được làm bằng công cụ gì và đo bằng con số nào"
  - level: core
    statement: "Số liệu, sơ đồ tổ chức và quy trình lấy từ đơn vị, ghi rõ nguồn và kỳ báo cáo"
    verify: "Với mỗi số liệu và sơ đồ, tìm câu ghi nguồn và năm; đối chiếu với tài liệu công bố của đơn vị nếu có"
  - level: minor
    statement: "Có ít nhất một chỗ kể việc mình làm sai, làm chưa được hoặc phải làm lại"
    verify: "Tìm đoạn nói về khó khăn ở mức cá nhân người viết, không phải khó khăn chung của ngành"
  - level: minor
    statement: "Phần kiến nghị gắn với việc đã quan sát tại đơn vị"
    verify: "Với mỗi kiến nghị, tìm chỗ trong bài mô tả việc làm nảy sinh kiến nghị đó"
genre_baseline:
  normal_signals:
    - "Mục 'kết quả đạt được – tồn tại, hạn chế – phương hướng' (T06): bố cục BẮT BUỘC của báo cáo Việt Nam, không bao giờ là tín hiệu nguồn gốc; chỉ nội dung rỗng bên trong mới đáng nói"
    - "Bộ ba danh từ hoặc tính từ song hành trong câu tổng kết (T10): phép tu từ được dạy, giữ nguyên khung"
    - "Câu mở 'Trong bối cảnh…' hoặc 'Được sự phân công của…' (T01): khuôn mở chuẩn của thể loại"
    - "Cụm 'đóng vai trò quan trọng', 'có ý nghĩa thiết thực' (T08)"
    - "Danh từ hoá và câu bị động không nêu chủ thể (T13): văn phong chuẩn của văn bản hành chính"
    - "Lời cảm ơn và câu kết bày tỏ quyết tâm (T25): quy ước của thể loại, giữ mục và chỉ thay nội dung rỗng"
    - "Đoạn giới thiệu lịch sử hình thành đơn vị chép gần nguyên văn từ hồ sơ hoặc trang tin của đơn vị: mẫu báo cáo yêu cầu phần này và sinh viên được phép chép có dẫn nguồn"
    - "Các mục lặp lại giống nhau giữa mọi báo cáo cùng trường: mẫu do khoa phát"
```
