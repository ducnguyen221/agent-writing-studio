# Hồ sơ thể loại: bài luận

Hồ sơ này là dữ liệu dùng chung cho năm trục. Nếu đề bài hoặc barem cụ thể mâu thuẫn với hồ sơ,
barem của nhiệm vụ thắng và phải được ghi trong phạm vi đánh giá.

## 1. Intent và bối cảnh

Trục 1 đọc mục này để biết phải hỏi những gì trước khi cho phép bắt đầu viết.

Xác định đề bài, người chấm, mục tiêu lập luận, giới hạn từ và chuẩn trích dẫn. Viết lại luận đề bằng
một câu có thể phản biện; nếu không làm được thì chưa đủ bối cảnh.

```yaml
required_inputs:
  - de_bai
  - nguoi_cham_va_barem
  - gioi_han_tu
  - chuan_trich_dan
intent_questions:
  - "Luận đề viết lại thành một câu có thể bị phản bác là gì?"
  - "Đề bài hỏi giải thích, thuyết phục, hay so sánh? Ba dạng này cho ba dàn bài khác nhau."
  - "Người chấm cho điểm theo barem nào, và barem đó nặng về đâu?"
  - "Bằng chứng nào tác giả thật sự có trong tay, không phải bằng chứng mong có?"
  - "Phản đề mạnh nhất chống lại luận đề là gì?"
audience_fields:
  - vai_tro
  - tieu_chi_cham
  - muc_do_quen_chu_de
  - dinh_kien_co_the_co
stop_if_missing:
  - "Không viết lại được luận đề thành một câu có thể bị phản bác"
  - "Không biết đề bài yêu cầu dạng lập luận nào"
  - "Không có bằng chứng nào cho luận điểm trung tâm"
```

## 2. Khung viết

Trục 2 đọc mục này để chọn khung dàn bài và biết khuôn nào bị cấm ngay từ bản nháp đầu.

Ưu tiên mở bài nêu luận đề, các đoạn thân có luận điểm–lý do–bằng chứng–liên hệ và kết bài trả lời
trực tiếp đề bài. PEEL/TEEL là công cụ gợi ý, không phải khuôn bắt buộc cho mọi đoạn.

```yaml
structures:
  - id: peel
    parts: [luan_diem, ly_do, bang_chung, lien_he]
  - id: mo_than_ket
    parts: [mo_bai_neu_luan_de, than_bai_cac_luan_diem, ket_bai_tra_loi_de]
  - id: luan_de_phan_de
    parts: [luan_de, phan_de, phan_bien_phan_de, ket_luan_co_dieu_kien]
default_structure: mo_than_ket
anti_llm_defaults:
  - "Mở bài bằng mệnh đề toàn cảnh kiểu 'Trong bối cảnh … đang diễn ra mạnh mẽ'"
  - "Kết bài bằng lời kêu gọi chung chung không gắn với luận đề"
  - "Chuyển đoạn bằng 'Bên cạnh đó' / 'Không những vậy' khi quan hệ logic thật là đối lập hoặc nhân quả"
  - "Câu chốt cuối đoạn chỉ nhắc lại câu đầu đoạn bằng từ khác"
  - "Danh sách gạch đầu dòng có tiêu đề in đậm thay cho đoạn văn lập luận"
outline_depth: 3
outline_layers:
  - "Luận đề và các ý chính — mỗi ý là một mệnh đề có thể sai, không phải một chủ đề"
  - "Đoạn — mỗi đoạn một câu 'để làm gì' và quan hệ thật với đoạn trước"
  - "Bằng chứng — mỗi đoạn gắn ít nhất một thứ đỡ được nó"
```

## 3. Rubric chất lượng

Trục 3 đọc mục này để biết chấm những gì, bằng chứng nào phải trưng ra và bật lăng kính nào.

Chấm riêng mức trả lời đề, logic, bằng chứng, phản biện, liên kết và độ chính xác ngôn ngữ. Không
đồng nhất “văn trơn tru” với lập luận tốt; một câu đẹp nhưng không thêm thông tin vẫn là câu yếu.

```yaml
criteria:
  - id: task_response
    name: "Trả lời đề bài"
    evidence: "Luận đề viết lại một câu, và ánh xạ từng đoạn thân về luận đề đó"
    question: "Đoạn nào không phục vụ luận đề? Bỏ nó đi thì bài có yếu hơn không?"
  - id: logic
    name: "Mạch lập luận"
    evidence: "Chuỗi tiền đề → kết luận của luận điểm trung tâm, viết lại thành 3–5 dòng"
    question: "Bước nào trong chuỗi cần thêm tiền đề mà tác giả chưa nêu?"
  - id: evidence
    name: "Bằng chứng"
    evidence: "Danh sách khẳng định thực chứng kèm nguồn hoặc phạm vi kiểm chứng"
    question: "Khẳng định nào quan trọng nhất mà không có gì đỡ?"
  - id: counterargument
    name: "Phản biện"
    evidence: "Đoạn nêu phản đề, giới hạn hoặc điều kiện kết luận không còn đúng"
    question: "Người phản đối mạnh nhất sẽ nói gì, và bài đã trả lời chưa?"
  - id: cohesion
    name: "Liên kết"
    evidence: "Quan hệ logic thật giữa các đoạn, đọc theo thứ tự đảo xem có vỡ không"
    question: "Từ nối đang dùng có mô tả đúng quan hệ giữa hai đoạn không?"
  - id: language
    name: "Chính xác ngôn ngữ"
    evidence: "Lỗi ngữ pháp, dùng từ sai nghĩa, câu tối nghĩa — đếm và trích"
    question: "Chỗ nào người đọc phải đọc lại lần hai mới hiểu?"
lenses:
  - task_response
  - fallacy_scan
  - claim_check
blind_referee: true
```

## 4. Quy tắc biên tập

Trục 4 đọc mục này để biết được phép sửa gì và tuyệt đối không được đụng vào đâu.

Giữ nguyên luận điểm và giọng người viết. Giảm danh từ hóa, làm rõ chủ thể–hành động, thay liên từ
máy móc bằng quan hệ logic thật. Không cố làm mọi câu dài/ngắn giống nhau và không thêm trải nghiệm giả.

```yaml
preserve:
  - so_lieu_va_don_vi
  - trich_dan_nguyen_van_va_nguon
  - ten_rieng_va_thuat_ngu_chuyen_mon
  - luan_diem_va_lap_truong_cua_tac_gia
  - vi_du_ca_nhan_do_tac_gia_ke
moves_allowed:
  - "Tách câu dài thành hai câu khi chủ thể bị chôn"
  - "Đổi danh từ hoá thành động từ có chủ thể"
  - "Thay liên từ máy móc bằng quan hệ logic đúng, hoặc bỏ hẳn"
  - "Xoá cụm đệm không thêm thông tin"
  - "Đưa bằng chứng lên gần khẳng định mà nó đỡ"
moves_forbidden:
  - "Thêm trải nghiệm cá nhân mà tác giả không kể"
  - "Đổi mức mạnh của khẳng định (thêm hoặc bớt rào đón)"
  - "Ép độ dài câu về một mức đồng đều để trông 'tự nhiên' hơn"
  - "Xoá lặp có chủ ý dùng làm phép nhấn"
  - "Thay thuật ngữ chuyên môn bằng từ thông dụng khiến sai nghĩa"
tell_families:
  - T01
  - T03
  - T05
  - T09
  - T10
  - T11
  - T12
  - T13
  - T16
  - T20
  - T23
  - T24
  - T25
  - T27
  - T28
  - T31
  - T32
  - T33
  - T34
  - T35
voice_priority:
  - writer_profile
  - genre_default
```

## 5. Must-have cho forensics

Trục 5 đọc mục này để tiền đăng ký yêu cầu thể loại và biết tín hiệu nào là bình thường ở bài luận.

Tiền đăng ký các mục dưới đây trước khi đọc bài. Barem cụ thể được phép thay thế nhưng không được
thêm tiêu chí sau khi đã thấy lỗi.

- `core` — Có luận đề trả lời trực tiếp đề bài và giữ nhất quán đến kết luận. Xác minh bằng cách viết
  lại luận đề và ánh xạ mỗi đoạn thân về luận đề.
- `core` — Mọi khẳng định thực chứng quan trọng có nguồn, dữ kiện hoặc phạm vi kiểm tra được. Không
  phạt bài thuần khái niệm vì ít số liệu.
- `minor` — Có ít nhất một bước xử lý phản đề, giới hạn hoặc điều kiện mà kết luận không còn đúng.
- `minor` — Ví dụ phục vụ luận điểm và đủ cụ thể để giải thích; không yêu cầu trải nghiệm cá nhân nếu
  đề bài không đòi hỏi.

Thiếu mục là dấu hiệu về năng lực thể loại, không tự nó chứng minh nguồn gốc AI. Finding G4 phải kèm
câu hỏi chuyên môn để tác giả giải thích lựa chọn lập luận.

```yaml
must_have:
  - level: core
    statement: "Có luận đề trả lời trực tiếp đề bài và giữ nhất quán đến kết luận"
    verify: "Viết lại luận đề thành một câu, rồi ánh xạ mỗi đoạn thân về luận đề đó"
  - level: core
    statement: "Mọi khẳng định thực chứng quan trọng có nguồn, dữ kiện hoặc phạm vi kiểm tra được"
    verify: "Liệt kê khẳng định thực chứng; đánh dấu cái không có gì đỡ. Không phạt bài thuần khái niệm vì ít số liệu"
  - level: minor
    statement: "Có ít nhất một bước xử lý phản đề, giới hạn hoặc điều kiện kết luận không còn đúng"
    verify: "Tìm đoạn nêu phản đề; nếu không có, hỏi tác giả người phản đối sẽ nói gì"
  - level: minor
    statement: "Ví dụ phục vụ luận điểm và đủ cụ thể để giải thích"
    verify: "Với mỗi ví dụ, hỏi nó chứng minh điều gì; không đòi trải nghiệm cá nhân nếu đề bài không yêu cầu"
genre_baseline:
  normal_signals:
    - "Bố cục mở bài – thân bài – kết bài rành mạch: đây là khung được dạy trong trường, không phải dấu vết máy"
    - "Cụm chuyển đoạn quy ước như 'Trước hết', 'Thứ hai', 'Tóm lại' ở mật độ vừa phải"
    - "Kết bài nhắc lại luận đề bằng lời khác: yêu cầu của thể loại, chỉ đáng lưu ý khi kết bài không gắn với luận đề nào"
    - "Câu dài nhiều mệnh đề ở bài học thuật: dấu hiệu văn phong, không phải dấu hiệu nguồn gốc"
```
