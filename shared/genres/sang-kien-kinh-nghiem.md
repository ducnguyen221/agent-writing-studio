# Hồ sơ thể loại: sáng kiến kinh nghiệm

**Hồ sơ một phần (`partial`): chỉ có §5.** Thể loại này đã phải giám định thật trước khi tới lượt
soạn phần viết, nên hồ sơ chỉ khai thứ trục 5 cần: yêu cầu bắt buộc của thể loại và các tín hiệu là
văn phong chuẩn. Trục 1–3 không đọc file này; trục 4 chỉ đọc `§5 genre_baseline` dưới đây qua
`polish_check.py`, để không báo oan các cột counter ở thể loại này.

Phạm vi: sáng kiến kinh nghiệm của giáo viên, báo cáo giải pháp dự thi cấp trường – huyện – tỉnh,
đề tài cải tiến phương pháp dạy học. Nguồn của mục dưới đây là bảng "thể loại bắt buộc có gì" ở
`skills/05-forensics/references/01-rubric-5-truc.md` trục 4.

## 5. Must-have cho forensics

Trục 5 đọc mục này để tiền đăng ký yêu cầu thể loại và biết tín hiệu nào là bình thường ở sáng kiến kinh nghiệm.

Tiền đăng ký các mục dưới đây trước khi đọc bài. Yêu cầu đặc trưng của thể loại: **số liệu của chính
lớp mình, trường mình, có so sánh trước và sau khi áp dụng**. Đây là điều kiện tồn tại của thể loại
— một sáng kiến không đo được ở lớp nào thì chưa phải sáng kiến, mới là ý tưởng. Số liệu chung của
ngành, dù đúng và có nguồn, không thay thế được, vì thứ hội đồng chấm là hiệu quả tại chỗ.

Yêu cầu thứ hai: giải pháp mô tả ở mức **người khác làm lại được** — các bước, thời lượng, phương
tiện, ai làm. Một sáng kiến viết ở mức "tăng cường ứng dụng công nghệ thông tin vào giảng dạy" là
một khẩu hiệu, không phải một giải pháp.

Thiếu một mục là dấu hiệu về **năng lực thể loại**, không tự nó chứng minh nguồn gốc AI. Cách theo
đuổi là hỏi tác giả về lớp, sĩ số, năm học và cách đo — những thứ chỉ người dạy lớp đó trả lời được.

Cảnh báo báo oan riêng của thể loại: đây là văn bản viết theo hướng dẫn của Phòng hoặc Sở, nên cấu
trúc "Đặt vấn đề – Giải quyết vấn đề – Kết luận, kiến nghị", phần trích nghị quyết và thông tư ở lý
do chọn đề tài, mục hạn chế và phương hướng cuối bài (`T06`), bộ ba song hành (`T10`) và câu kết bày
tỏ quyết tâm (`T25`) đều là **khung bắt buộc**. Giữ khung, chỉ hỏi về nội dung bên trong. Xem
`skills/05-forensics/references/03-chong-bao-oan.md` §2 và §6.

```yaml
must_have:
  - level: core
    statement: "Có số liệu của chính lớp hoặc trường mình, so sánh trước và sau khi áp dụng"
    verify: "Tìm bảng hoặc con số trước – sau kèm tên lớp, sĩ số, năm học; số liệu chung của ngành không thay thế được"
  - level: core
    statement: "Giải pháp mô tả ở mức người khác làm lại được: các bước, thời lượng, phương tiện, ai làm"
    verify: "Đọc riêng phần giải pháp và liệt kê thứ còn thiếu để một giáo viên khác áp dụng được ngay"
  - level: core
    statement: "Nêu điều kiện áp dụng và chỗ giải pháp không hiệu quả"
    verify: "Tìm câu nói về lớp, môn hoặc hoàn cảnh mà giải pháp không dùng được; không có thì hỏi tác giả đã thử ở lớp nào khác chưa"
  - level: minor
    statement: "Có sản phẩm kèm theo: giáo án, phiếu học tập, đề kiểm tra, ảnh hoặc biên bản"
    verify: "Kiểm phụ lục; đối chiếu sản phẩm với giải pháp được mô tả trong thân bài"
  - level: minor
    statement: "Nêu rõ tên trường, năm học, môn và khối lớp áp dụng"
    verify: "Tìm bốn thông tin này trong bài; thiếu thì sáng kiến không gắn với bối cảnh nào"
genre_baseline:
  normal_signals:
    - "Cấu trúc 'Đặt vấn đề – Giải quyết vấn đề – Kết luận, kiến nghị' theo hướng dẫn của Phòng hoặc Sở"
    - "Mục hạn chế và phương hướng cuối bài (T06): bố cục bắt buộc, chỉ nội dung rỗng bên trong mới đáng nói"
    - "Bộ ba danh từ hoặc tính từ song hành (T10): phép tu từ được dạy"
    - "Trích nghị quyết, thông tư, chỉ thị của ngành ở phần lý do chọn đề tài: mẫu bắt buộc"
    - "Câu mở toàn cảnh 'Trong bối cảnh đổi mới giáo dục…' (T01)"
    - "Cụm 'đóng vai trò quan trọng', 'có ý nghĩa thiết thực' (T08)"
    - "Danh từ hoá và câu bị động không nêu chủ thể (T13)"
    - "Cụm dẫn quy ước 'có thể nói rằng', 'nhìn chung' (T23)"
    - "Câu kết bày tỏ quyết tâm và mong muốn nhân rộng (T25): quy ước của thể loại"
```
