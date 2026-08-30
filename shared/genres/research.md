# Hồ sơ thể loại: bài nghiên cứu

Hồ sơ này là dữ liệu dùng chung cho năm trục, áp cho bài báo khoa học, báo cáo nghiên cứu, khoá luận
và đề cương nghiên cứu. Nếu hướng dẫn của tạp chí, hội đồng hoặc đề bài cụ thể mâu thuẫn với hồ sơ,
barem của nhiệm vụ thắng và phải được ghi trong phạm vi đánh giá.

Một câu phân biệt bài nghiên cứu với bài luận: bài luận thuyết phục bằng lập luận, bài nghiên cứu
thuyết phục bằng **phương pháp lặp lại được**. Vì vậy mọi trục ở đây đều nặng về việc truy được số
liệu về nguồn và truy được kết luận về thiết kế nghiên cứu.

## 1. Intent và bối cảnh

Trục 1 đọc mục này để biết phải hỏi những gì trước khi cho phép bắt đầu viết.

Xác định câu hỏi nghiên cứu, phạm vi và đơn vị phân tích, dữ liệu thật sự đang có, chuẩn trích dẫn và
nơi bài sẽ nộp. Cách hỏi mượn từ `storm`: thay vì hỏi một chuỗi câu chung, **liệt kê các góc nhìn
trước rồi hỏi từ từng góc** — người phản biện phương pháp, người dùng kết quả trong thực tế, và người
đã công bố kết quả ngược lại đều hỏi những câu khác nhau. Một câu hỏi nghiên cứu chỉ đứng vững khi
trả lời được cả ba.

Nếu chưa nêu được kết quả nào sẽ **bác bỏ** giả thuyết thì chưa có câu hỏi nghiên cứu, mới chỉ có
chủ đề.

```yaml
required_inputs:
  - cau_hoi_nghien_cuu
  - pham_vi_va_don_vi_phan_tich
  - du_lieu_da_co_trong_tay
  - chuan_trich_dan
  - noi_nop_va_tieu_chi_phan_bien
intent_questions:
  - "Câu hỏi nghiên cứu viết thành một câu có biến số, phạm vi và mốc thời gian là gì?"
  - "Kết quả nào sẽ bác bỏ giả thuyết? Nếu không có, đây là chủ đề chứ chưa phải câu hỏi."
  - "Ba góc nhìn nào cùng quan tâm câu hỏi này — người phản biện phương pháp, người dùng kết quả, người đã công bố kết quả ngược lại — và mỗi góc hỏi gì đầu tiên?"
  - "Dữ liệu nào tác giả thật sự có trong tay, thu bằng cách nào, và ai đã chạm vào nó trước đó?"
  - "Công trình gần nhất đã trả lời được đến đâu, và bài này thêm được đúng cái gì?"
  - "Kết luận dự kiến là tương quan hay nhân quả, và thiết kế nghiên cứu có đỡ nổi mức đó không?"
audience_fields:
  - vai_tro_chuyen_mon
  - muc_do_quen_phuong_phap
  - tieu_chi_phan_bien_hoac_barem
  - ky_vong_ve_muc_bang_chung
  - dinh_kien_ve_ket_qua_mong_doi
stop_if_missing:
  - "Không viết được câu hỏi nghiên cứu thành một câu có biến số và phạm vi"
  - "Không nêu được kết quả nào sẽ bác bỏ giả thuyết"
  - "Không biết dữ liệu nào đã có trong tay và dữ liệu nào mới chỉ là dự định thu"
  - "Không biết chuẩn trích dẫn và nơi nộp"
```

## 2. Khung viết

Trục 2 đọc mục này để chọn khung dàn bài và biết khuôn nào bị cấm ngay từ bản nháp đầu.

Mặc định là IMRAD: Mở đầu – Phương pháp – Kết quả – Bàn luận. Ranh giới giữa Kết quả và Bàn luận là
ranh giới cứng: Kết quả chỉ trình bày cái đo được, Bàn luận mới được diễn giải. Trộn hai phần là lỗi
thể loại nặng nhất, và cũng là chỗ máy hay trộn nhất.

Không phải bài nghiên cứu nào cũng có mục Kết quả. Bài phân tích chính sách và bài tổng hợp tường
thuật — dạng phổ biến ở hội thảo và tạp chí ngành Việt Nam — đi theo `phan_tich_chinh_sach`: đặt vấn
đề, khung phân tích, bằng chứng, hàm ý, giới hạn. Khung này không phải IMRAD lỏng lẻo hơn: nó thay
ranh giới Kết quả – Bàn luận bằng ranh giới **khung phân tích – bằng chứng**, và khung phân tích phải
được nêu trước khi bằng chứng được gọi ra, nếu không thì bằng chứng chỉ là minh hoạ cho kết luận đã
có sẵn.

Luật lấy từ `storm`: **outline mang nguồn ngay khi dựng**, không gắn nguồn sau khi viết xong prose.
Mỗi mục ở tầng hai của dàn ý phải kèm ít nhất một nguồn hoặc một dòng dữ liệu; mục nào không gắn được
gì thì hoặc là chưa đọc đủ, hoặc là ý của chính tác giả và phải được đánh dấu rõ như vậy. Gắn nguồn
sau khi viết là công thức sinh ra trích dẫn trang trí — nguồn được chọn vì nó khớp câu đã viết, chứ
không phải câu được viết ra vì nguồn nói thế.

```yaml
structures:
  - id: imrad
    parts: [mo_dau, phuong_phap, ket_qua, ban_luan]
  - id: imrad_day_du
    parts: [tom_tat, mo_dau, tong_quan_tai_lieu, phuong_phap, ket_qua, ban_luan, ket_luan, tai_lieu_tham_khao]
  - id: de_cuong
    parts: [dat_van_de, tong_quan_tai_lieu, muc_tieu_va_cau_hoi, phuong_phap_du_kien, ke_hoach_va_san_pham]
  - id: phan_tich_chinh_sach
    parts: [dat_van_de, khung_phan_tich, bang_chung, ham_y, gioi_han]
default_structure: imrad
anti_llm_defaults:
  - "Mở đầu bằng mệnh đề toàn cảnh kiểu 'Trong bối cảnh … ngày càng phát triển mạnh mẽ' thay cho khoảng trống nghiên cứu cụ thể"
  - "Tổng quan tài liệu viết thành chuỗi 'Tác giả A cho rằng… Tác giả B cho rằng…' không có tranh luận giữa các nguồn"
  - "Đưa diễn giải, nguyên nhân hoặc đánh giá vào phần Kết quả"
  - "Bàn luận kết thúc bằng câu kêu gọi 'cần có thêm nghiên cứu trong tương lai' không nói rõ nghiên cứu nào"
  - "Mục Hạn chế liệt kê hạn chế chung chung không ảnh hưởng tới kết luận nào của chính bài"
  - "Trích dẫn nêu tên tác giả hoặc tên tạp chí thay cho kết quả cụ thể được trích"
outline_depth: 3
outline_layers:
  - "Câu hỏi nghiên cứu và các mục lớn của khung đã chọn"
  - "Tiểu mục — mỗi mục kèm ít nhất một nguồn hoặc một dòng dữ liệu, gắn ngay khi dựng"
  - "Bằng chứng — nguồn nào đỡ khẳng định nào và ở mức nào; ý của chính tác giả phải đánh dấu"
```

## 3. Rubric chất lượng

Trục 3 đọc mục này để biết chấm những gì, bằng chứng nào phải trưng ra và bật lăng kính nào.

Chấm riêng câu hỏi nghiên cứu, phương pháp, kết quả, bàn luận, trích dẫn và ngôn ngữ học thuật. Ba
lăng kính được bật ở đây trả lời ba câu khác nhau: `claim_check` hỏi *khẳng định này dựa vào đâu*,
`source_reliability` hỏi *nguồn đó có đỡ nổi mức khẳng định không*, `method_rigor` hỏi *thiết kế
nghiên cứu có đỡ nổi kết luận không*. Một bài có thể qua hai lăng kính đầu mà trượt lăng kính thứ ba:
nguồn tốt, số liệu thật, nhưng cỡ mẫu không cho phép phát biểu nhân quả.

Văn học thuật trơn tru không được cộng điểm cho phương pháp. Một mục Phương pháp viết đẹp nhưng
thiếu tiêu chí chọn mẫu vẫn là mục Phương pháp hỏng.

**Bài không có mục Kết quả thì đọc tiêu chí `results` như thế nào.** Với khung
`phan_tich_chinh_sach`, `results` đọc là **"mọi số liệu và dẫn chứng trong bài truy được về nguồn
đã nêu"**, còn `method` đọc là **"khung phân tích và tiêu chí chọn dẫn chứng"**. Không được vì bài
thiếu heading "Kết quả" mà chấm hai tiêu chí này là 0 — đó là chấm theo hình thức trình bày chứ
không theo chất lượng bằng chứng. Nguồn của luật này là một ca chấm thật, xem cổng Phase 2.

```yaml
criteria:
  - id: research_question
    name: "Câu hỏi nghiên cứu"
    evidence: "Câu hỏi viết lại thành một câu có biến số và phạm vi, kèm khoảng trống nghiên cứu mà bài lấp"
    question: "Bài này trả lời được câu hỏi nào mà công trình trước chưa trả lời?"
  - id: method
    name: "Phương pháp"
    evidence: "Dữ liệu, cỡ mẫu, tiêu chí chọn và loại, công cụ, tham số — đủ để người khác lặp lại"
    question: "Người khác đọc riêng mục Phương pháp có làm lại được nghiên cứu này không?"
  - id: results
    name: "Kết quả và bằng chứng"
    evidence: "Mỗi con số trong Kết quả truy về được nguồn dữ liệu và bước xử lý đã mô tả"
    question: "Con số nào xuất hiện trong Kết quả mà không truy được về Phương pháp?"
  - id: discussion
    name: "Bàn luận và giới hạn"
    evidence: "Ánh xạ từng kết luận về kết quả đỡ nó, kèm mục giới hạn nêu điều kiện kết luận không còn đúng"
    question: "Kết luận nào mạnh hơn thứ dữ liệu cho phép nói?"
  - id: citation
    name: "Trích dẫn và nguồn"
    evidence: "Danh sách trích dẫn kèm điều được trích; đối chiếu nguồn có thật sự nói điều đó"
    question: "Trích dẫn nào đang được dùng để đỡ một khẳng định mà bản thân nguồn không đưa ra?"
  - id: academic_language
    name: "Ngôn ngữ học thuật"
    evidence: "Chỗ thuật ngữ dùng sai nghĩa, câu tối nghĩa, hoặc mức chắc chắn của động từ lệch với dữ liệu"
    question: "Chỗ nào cách diễn đạt làm kết luận nghe chắc hơn dữ liệu cho phép?"
lenses:
  - claim_check
  - source_reliability
  - method_rigor
blind_referee: true
```

## 4. Quy tắc biên tập

Trục 4 đọc mục này để biết được phép sửa gì và tuyệt đối không được đụng vào đâu.

Vùng bảo vệ ở thể loại này rộng hơn mọi thể loại khác: số liệu và đơn vị, sai số, trích dẫn nguyên
văn, thuật ngữ chuyên ngành, ký hiệu biến và công thức, mô tả phương pháp và tham số. Sửa một chữ
trong mô tả phương pháp có thể làm nghiên cứu không lặp lại được nữa.

Phép cấm đặc trưng của thể loại là **thêm cảm xúc**. Tính từ đánh giá, giọng kể chuyện, câu cảm thán
làm phần Kết quả mất tính trung lập và đẩy bài từ báo cáo sang bài quan điểm. Cấm luôn việc nới hoặc
siết mức chắc chắn: đổi "có liên hệ với" thành "dẫn tới" là sửa nội dung nghiên cứu, không phải sửa
văn.

```yaml
preserve:
  - so_lieu_don_vi_va_sai_so
  - trich_dan_nguyen_van_va_nguon
  - thuat_ngu_chuyen_nganh
  - ky_hieu_bien_va_cong_thuc
  - mo_ta_phuong_phap_va_tham_so
  - dieu_kien_va_gioi_han_cua_ket_luan
  - ten_rieng_ten_to_chuc_va_ten_bo_du_lieu
moves_allowed:
  - "Tách câu dài thành hai câu khi chủ thể của hành động bị chôn"
  - "Đưa kết quả lên gần khẳng định mà nó đỡ"
  - "Xoá cụm đệm không thêm thông tin"
  - "Thay liên từ máy móc bằng quan hệ logic đúng, hoặc bỏ hẳn"
  - "Chuyển câu diễn giải bị lạc trong mục Kết quả sang mục Bàn luận, giữ nguyên chữ"
  - "Thống nhất cách gọi một biến trong toàn bài khi bài đang gọi bằng nhiều tên"
moves_forbidden:
  - "Thêm cảm xúc, tính từ đánh giá hoặc giọng kể chuyện, đặc biệt trong Mở đầu và Kết quả"
  - "Đổi mức chắc chắn của khẳng định: nới tương quan thành nhân quả, hoặc thêm/bớt rào đón"
  - "Diễn đạt lại mô tả phương pháp, tham số hoặc tiêu chí chọn mẫu"
  - "Làm tròn, đổi đơn vị hoặc chỉnh cách trình bày số liệu"
  - "Sửa hoặc rút gọn trích dẫn nguyên văn"
  - "Thay thuật ngữ chuyên ngành bằng từ thông dụng khiến sai nghĩa"
  - "Ép độ dài câu về một mức đồng đều để trông 'tự nhiên' hơn"
tell_families:
  - T01
  - T02
  - T03
  - T05
  - T08
  - T09
  - T10
  - T11
  - T12
  - T13
  - T16
  - T20
  - T21
  - T23
  - T24
  - T25
  - T28
  - T29
  - T30
  - T31
  - T32
  - T34
  - T35
voice_priority:
  - writer_profile
  - genre_default
```

## 5. Must-have cho forensics

Trục 5 đọc mục này để tiền đăng ký yêu cầu thể loại và biết tín hiệu nào là bình thường ở bài nghiên cứu.

Tiền đăng ký các mục dưới đây trước khi đọc bài. Ở thể loại này, must-have xoay quanh **liêm chính
dữ liệu**: số liệu truy được về nguồn, phương pháp lặp lại được, kết luận không vượt quá thiết kế.
Đây cũng là các mục có ích nhất khi đối thoại với tác giả, vì chúng hỏi về thứ chỉ người làm nghiên
cứu mới trả lời được.

- `core` — Mọi số liệu trong Kết quả truy được về nguồn dữ liệu và bước xử lý đã mô tả ở Phương pháp.
- `core` — Phương pháp mô tả đủ để người khác lặp lại: dữ liệu, cỡ mẫu, tiêu chí chọn và loại, công
  cụ, tham số.
- `core` — Kết luận không vượt quá thiết kế nghiên cứu; tương quan không được phát biểu thành nhân quả.
- `minor` — Có mục giới hạn nêu điều kiện cụ thể mà kết luận của chính bài không còn đúng.
- `minor` — Trích dẫn phân biệt được ý mượn với ý của tác giả, và nguồn thật sự nói điều được trích.

Thiếu một mục là dấu hiệu về **năng lực thể loại hoặc về liêm chính học thuật**, không tự nó chứng
minh nguồn gốc AI. Trích dẫn không kiểm chứng được là finding đáng theo đuổi bằng cách kiểm nguồn,
không phải bằng cách suy đoán ai đã viết. Mọi finding phải kèm câu hỏi để tác giả giải thích lựa chọn
phương pháp.

Cảnh báo báo oan riêng của thể loại: bài nghiên cứu trích dẫn dày đặc thì phần lớn văn bản là câu
trích và cụm quy ước, nên mọi thước đo dựa trên độ dễ đoán của câu chữ đều tụt xuống. Đó là hệ quả
của mật độ trích dẫn, không phải dấu vết máy — xem `skills/05-forensics/references/03-chong-bao-oan.md`
mục 4.

```yaml
must_have:
  - level: core
    statement: "Mọi số liệu trong Kết quả truy được về nguồn dữ liệu và bước xử lý đã mô tả ở Phương pháp"
    verify: "Chọn 3 con số bất kỳ trong Kết quả; với mỗi con số, chỉ ra dòng nào ở Phương pháp sinh ra nó"
  - level: core
    statement: "Phương pháp mô tả đủ để người khác lặp lại: dữ liệu, cỡ mẫu, tiêu chí chọn và loại, công cụ, tham số"
    verify: "Đọc riêng mục Phương pháp, tách khỏi phần còn lại, rồi liệt kê thứ còn thiếu để làm lại nghiên cứu"
  - level: core
    statement: "Kết luận không vượt quá thiết kế nghiên cứu; tương quan không phát biểu thành nhân quả"
    verify: "Với mỗi kết luận, ghi thiết kế đỡ nó và động từ dùng để phát biểu; đánh dấu chỗ động từ mạnh hơn thiết kế"
  - level: minor
    statement: "Có mục giới hạn nêu điều kiện cụ thể mà kết luận của chính bài không còn đúng"
    verify: "Kiểm mục Hạn chế có gắn với kết luận cụ thể nào của bài không, hay chỉ là hạn chế chung chung"
  - level: minor
    statement: "Trích dẫn phân biệt được ý mượn với ý của tác giả, và nguồn thật sự nói điều được trích"
    verify: "Lấy mẫu 3 trích dẫn, mở nguồn, đối chiếu điều được trích với điều nguồn nói"
genre_baseline:
  normal_signals:
    - "Câu bị động, không nêu chủ thể ở mục Phương pháp: chuẩn viết được dạy, không phải dấu vết máy"
    - "Danh từ hoá và mật độ thuật ngữ cao: đặc trưng đăng ký ngôn ngữ học thuật"
    - "Cấu trúc IMRAD lặp lại giữa các bài cùng ngành: yêu cầu của thể loại và của tạp chí"
    - "Cụm quy ước mở đầu như 'Nghiên cứu này nhằm', 'Kết quả cho thấy', 'Bảng 1 trình bày'"
    - "Câu dài nhiều mệnh đề, nhiều mệnh đề phụ chỉ điều kiện: cách viết cho chính xác, không phải cách viết cho trơn"
    - "Mật độ trích dẫn cao làm câu chữ dễ đoán: hệ quả của thể loại, không phải của nguồn gốc"
    - "Tóm tắt lặp lại gần nguyên văn các câu trong thân bài: yêu cầu của mục Tóm tắt"
```
