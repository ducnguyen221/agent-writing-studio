# Hồ sơ thể loại: bài chính luận

**Hồ sơ một phần (`partial`): chỉ có §5.** Thể loại này đã phải giám định thật trước khi tới lượt
soạn phần viết, nên hồ sơ chỉ khai thứ trục 5 cần: yêu cầu bắt buộc của thể loại và các tín hiệu là
văn phong chuẩn. Trục 1–3 không đọc file này; trục 4 chỉ đọc `§5 genre_baseline` dưới đây qua
`polish_check.py`, để không báo oan các cột counter ở thể loại này. Khi cần **viết** một bài chính luận, dùng `essay.md`
và ghi rõ trong phạm vi rằng phần must-have thể loại lấy từ đây.

Phạm vi: bài chính luận trên báo và tạp chí lý luận, bài dự thi bảo vệ nền tảng tư tưởng, bài bình
luận chính trị – xã hội. Nguồn của mục dưới đây là bảng "thể loại bắt buộc có gì" ở
`skills/05-forensics/references/01-rubric-5-truc.md` trục 4.

## 5. Must-have cho forensics

Trục 5 đọc mục này để tiền đăng ký yêu cầu thể loại và biết tín hiệu nào là bình thường ở bài chính luận.

Tiền đăng ký các mục dưới đây trước khi đọc bài. Yêu cầu đặc trưng và cũng là thứ bị bỏ sót nhiều
nhất khi giám định: **trích kinh điển phải nằm trong thân bài**. Thực đo đã ghi ở rubric trục 4: một
bài do người viết đăng tạp chí lý luận có **15 lượt** trích Mác – Lênin – tư tưởng Hồ Chí Minh – văn
kiện Đại hội trong thân bài; bài nghi vấn cùng thể loại có **2 lượt**, và cả hai nằm ở danh mục tham
khảo chứ không trong thân bài. Người dự thi thật **biết** đó là yêu cầu của thể loại; một bản thảo
sinh ra từ đề bài chung chung thì không biết.

Đặc trưng thứ hai: bài chính luận phản bác thì phải **dẫn lại luận điệu bị phản bác** trước khi bác.
Bài bác một đối tượng vô hình, không trích được câu nào của ai, là bài chưa làm đúng nghề — dù văn
có chặt tới đâu.

Thiếu một mục là dấu hiệu về **năng lực thể loại**, không tự nó chứng minh nguồn gốc AI. Mọi finding
phải kèm câu hỏi để tác giả giải thích lựa chọn của mình.

Cảnh báo báo oan riêng của thể loại — đây là thể loại dễ bị chấm oan nhất trong repo. Văn chính luận
Việt Nam có đăng ký ngôn ngữ riêng: câu mở toàn cảnh, bộ ba song hành, phép đối, danh từ hoá, cụm
dẫn quy ước, câu chốt đoạn nhắc lại luận điểm. Thực đo ở `01-rubric-5-truc.md`: bài do người viết có
mật độ cụm sáo **cao hơn** bài do máy sinh. Mật độ cliché ở đây đo **thể loại**, không đo nguồn gốc.
Xem `skills/05-forensics/references/03-chong-bao-oan.md` §2 và §6.

```yaml
must_have:
  - level: core
    statement: "Trích Mác – Lênin – tư tưởng Hồ Chí Minh – văn kiện Đại hội trong THÂN BÀI, không chỉ ở danh mục tham khảo"
    verify: "Đếm số lượt trích trong thân bài và ghi vị trí từng lượt; đếm riêng số lượt chỉ xuất hiện ở danh mục tham khảo"
  - level: core
    statement: "Mỗi trích dẫn kinh điển ghi được nguồn cấp văn kiện: tên tác phẩm, tập, trang, hoặc số nghị quyết và kỳ đại hội"
    verify: "Lấy mẫu 3 trích dẫn, đối chiếu với văn kiện gốc; trích chỉ ghi tên người nói mà không có nguồn tra được là chưa đạt"
  - level: core
    statement: "Luận điệu bị phản bác được dẫn lại cụ thể trước khi bác"
    verify: "Tìm chỗ bài dẫn nguyên văn hoặc thuật lại luận điệu kèm nơi nó xuất hiện; không có thì hỏi tác giả đang bác điều ai nói"
  - level: minor
    statement: "Có liên hệ thực tiễn ở địa phương, ngành hoặc cơ quan của tác giả với số liệu cụ thể"
    verify: "Liệt kê số liệu và sự việc trong bài; đánh dấu cái thuộc phạm vi tác giả tiếp cận được"
  - level: minor
    statement: "Kết luận nêu việc làm cụ thể của một chủ thể xác định, không dừng ở lời khẳng định quyết tâm"
    verify: "Đọc riêng phần kết; tìm chủ thể, việc làm và mốc thời gian"
genre_baseline:
  normal_signals:
    - "Câu mở toàn cảnh kiểu 'Trong bối cảnh…' (T01): khuôn mở chuẩn của thể loại"
    - "Bộ ba song hành và phép đối (T10): phép tu từ được dạy trong văn nghị luận và diễn văn tiếng Việt"
    - "Cụm 'đóng vai trò quan trọng', 'có ý nghĩa sâu sắc' (T08): đăng ký ngôn ngữ chính luận"
    - "Danh từ hoá và câu bị động không nêu chủ thể (T13): văn phong chuẩn của văn bản lý luận"
    - "Cụm dẫn quy ước 'có thể nói rằng', 'nhìn chung', 'tóm lại' (T23)"
    - "Mục kết quả – hạn chế – phương hướng và câu kết khẳng định quyết tâm (T06, T25): bố cục được dạy"
    - "Câu chốt đoạn nhắc lại luận điểm (T31): yêu cầu của khung nghị luận"
    - "Mật độ cụm sáo cao: thực đo cho thấy bài do người viết còn cao hơn bài do máy sinh — chỉ số này đo thể loại, không đo nguồn gốc"
```
