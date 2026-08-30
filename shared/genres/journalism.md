# Hồ sơ thể loại: báo chí

Hồ sơ này là dữ liệu dùng chung cho năm trục, áp cho tin, bài phản ánh, phóng sự và bài điều tra
ngắn. Nếu quy tắc của toà soạn hoặc yêu cầu của ban biên tập mâu thuẫn với hồ sơ, quy tắc toà soạn
thắng và phải được ghi trong phạm vi đánh giá.

Hồ sơ này **tự soạn**, không chưng cất từ repo nào. Nguồn tri thức là ba thứ nghề báo có sẵn: quy
tắc hai nguồn độc lập, quyền được trả lời của bên bị nêu tên, và cấu trúc tháp ngược. Ba thứ đó đã
là chuẩn nghề trước khi có mô hình ngôn ngữ, nên hồ sơ chỉ viết chúng ra thành dữ liệu máy đọc được.

Một câu phân biệt báo chí với bài luận: bài luận chịu trách nhiệm về lập luận, bài báo chịu trách
nhiệm về **dữ kiện và về người bị nêu tên**. Vì vậy cả năm trục ở đây đều nặng về việc truy nguồn và
về việc hỏi đủ các bên.

## 1. Intent và bối cảnh

Trục 1 đọc mục này để biết phải hỏi những gì trước khi cho phép bắt đầu viết.

Xác định sự việc, mốc thời gian, các nguồn đã liên hệ được và chưa liên hệ được, quyền lợi của từng
bên, khuôn khổ bài và hạn nộp. Câu hỏi quan trọng nhất không phải "chuyện gì xảy ra" mà **"vì sao
đăng hôm nay"** — nếu không trả lời được thì đó là chủ đề, chưa phải tin.

Câu hỏi thứ hai hay bị bỏ qua: ai được lợi khi tin này lan ra. Nguồn chủ động tìm đến phóng viên
thường là nguồn có lợi ích, và điều đó không làm họ sai, chỉ làm họ không đủ một mình.

```yaml
required_inputs:
  - su_viec_va_moc_thoi_gian
  - danh_sach_nguon_da_lien_he
  - cac_ben_co_quyen_loi
  - tai_lieu_goc_dang_co
  - khuon_kho_bai_va_han_nop
  - quy_tac_toa_soan
intent_questions:
  - "Tin này viết thành một câu ai làm gì, ở đâu, khi nào thì ra câu gì?"
  - "Vì sao đăng hôm nay — cái gì mới so với thứ đã đăng?"
  - "Ai được lợi khi tin này lan ra, và ai chịu thiệt?"
  - "Hai nguồn độc lập nào cùng xác nhận sự việc trung tâm? Nếu chỉ có một, nguồn đó là ai và có lợi ích gì?"
  - "Bên bị nêu tên bất lợi đã được hỏi chưa, hỏi lúc nào, và đã chờ trả lời bao lâu?"
  - "Có tài liệu gốc không — văn bản, ảnh, ghi âm, số liệu — hay chỉ có lời kể?"
  - "Điều gì phóng viên tự chứng kiến, điều gì đọc trong tài liệu, điều gì nghe kể lại?"
audience_fields:
  - doc_gia_da_biet_gi_ve_vu_viec
  - ly_do_ho_quan_tam
  - kenh_doc_va_thoi_luong
  - hau_qua_neu_ho_hieu_sai
stop_if_missing:
  - "Khẳng định trung tâm chỉ có một nguồn, và nguồn đó là bên có lợi ích trong vụ việc"
  - "Bên bị nêu tên bất lợi chưa được liên hệ"
  - "Không phân biệt được điều phóng viên chứng kiến với điều được kể lại"
  - "Không có mốc thời gian và địa điểm cụ thể của sự việc"
```

## 2. Khung viết

Trục 2 đọc mục này để chọn khung dàn bài và biết khuôn nào bị cấm ngay từ bản nháp đầu.

Mặc định là tháp ngược: thông tin quan trọng nhất nằm ở câu đầu, phần sau bổ sung theo mức giảm dần,
để bài cắt từ dưới lên vẫn đứng. Câu lead gói ai – làm gì – ở đâu – khi nào và nên ở dưới ba mươi
chữ; cái *vì sao* và *như thế nào* để dành cho đoạn sau.

Outline chỉ hai tầng, và tầng hai là ràng buộc thật sự: **mỗi khối thông tin phải gắn tên một nguồn
hoặc một tài liệu ngay khi dựng dàn ý.** Khối nào không gắn được gì thì hoặc chưa hỏi đủ, hoặc là
suy đoán của phóng viên và phải bị đánh dấu như vậy. Gắn nguồn sau khi viết xong là cách nhanh nhất
để có một bài mà nguồn được chọn vì khớp câu đã viết.

```yaml
structures:
  - id: thap_nguoc
    parts: [lead, chi_tiet_quan_trong, phan_hoi_cac_ben, boi_canh, thong_tin_phu]
  - id: phong_su
    parts: [canh_mo, nhan_vat, dien_bien, boi_canh_va_so_lieu, phan_hoi_cac_ben, canh_ket]
  - id: tuong_thuat_theo_dong_thoi_gian
    parts: [lead, moc_dau, dien_bien_theo_moc, hien_trang, viec_can_theo_doi]
default_structure: thap_nguoc
anti_llm_defaults:
  - "Lead mở bằng bối cảnh chung chung kiểu 'Trong những năm gần đây…' thay cho sự việc vừa xảy ra"
  - "Cân bằng giả: đặt một phát ngôn của mỗi bên cạnh nhau rồi kết bằng 'vấn đề vẫn còn nhiều tranh cãi'"
  - "Quy nguồn mơ hồ: 'theo các chuyên gia', 'nhiều người dân cho rằng' không kèm tên và tư cách"
  - "Kết bài bằng lời khuyên hoặc lời kêu gọi thay cho việc cần theo dõi tiếp"
  - "Dùng tính từ đánh giá thay cho dữ kiện, ví dụ 'vụ việc gây bức xúc dư luận'"
  - "Đưa suy đoán về động cơ của nhân vật vào phần tường thuật như thể đó là dữ kiện"
outline_depth: 2
outline_layers:
  - "Lead và các khối thông tin xếp theo mức quan trọng giảm dần"
  - "Mỗi khối gắn tên một nguồn hoặc một tài liệu, gắn ngay khi dựng dàn ý"
```

## 3. Rubric chất lượng

Trục 3 đọc mục này để biết chấm những gì, bằng chứng nào phải trưng ra và bật lăng kính nào.

Chấm riêng dữ kiện, nguồn, cân bằng, cấu trúc dẫn, bối cảnh và tác hại. Bốn lăng kính được bật trả
lời bốn câu khác nhau, và thứ tự có ý nghĩa: `claim_check` hỏi *khẳng định này dựa vào đâu*,
`source_reliability` hỏi *nguồn đó có đỡ nổi mức khẳng định không*, `source_independence` hỏi *ba
nguồn này có thật sự là ba nguồn không*, `balance_check` hỏi *bên nào có lợi ích mà bài không cho
tiếng nói*. Bài trượt nặng nhất thường trượt ở lăng kính thứ ba: ba nguồn cùng dẫn lại một thông cáo.

`balance_check` hỏi bài **đã hỏi đủ bên chưa**, không hỏi bài **đứng về bên nào**: phóng sự hay bài
điều tra có lập trường rõ vẫn là bài cân bằng nếu bên bị nêu tên bất lợi đã được hỏi và câu trả lời
(hoặc việc họ từ chối, kèm thời điểm) có mặt trong bài. Bên vắng mà việc vắng không đổi nghĩa câu
nào thì ghi `limitations[]`, không thành finding — đúng luật ở
`skills/03-critique/references/01-lang-kinh.md` mục 6.

Văn báo trơn tru không được cộng điểm cho phần nguồn. Một bài viết chặt, nhịp tốt, nhưng khẳng định
trung tâm chỉ có một nguồn ẩn danh vẫn là bài chưa đủ đăng.

```yaml
criteria:
  - id: accuracy
    name: "Chính xác dữ kiện"
    evidence: "Bảng dữ kiện: tên, chức danh, con số, mốc thời gian, địa điểm — kèm chỗ kiểm được từng dữ kiện"
    question: "Dữ kiện nào trong bài không chỉ ra được đã kiểm ở đâu?"
  - id: sourcing
    name: "Nguồn và cách quy nguồn"
    evidence: "Danh sách khẳng định kèm nguồn của từng khẳng định, và chuỗi truy ngược của mỗi nguồn về nơi thông tin xuất hiện lần đầu"
    question: "Khẳng định trung tâm có bao nhiêu nguồn thật sự độc lập với nhau?"
  - id: balance
    name: "Các bên và quyền được trả lời"
    evidence: "Danh sách các bên bị ảnh hưởng, đánh dấu bên đã có tiếng nói, bên từ chối, bên chưa hồi đáp kèm thời điểm liên hệ"
    question: "Bên bị nêu tên bất lợi đã được hỏi chưa, và việc họ vắng mặt có làm bài đổi nghĩa không?"
  - id: lead_and_structure
    name: "Câu dẫn và cấu trúc"
    evidence: "Câu lead viết lại; thử cắt bài từ dưới lên từng đoạn xem đoạn nào cắt được mà bài vẫn đứng"
    question: "Nếu người đọc chỉ đọc hai câu đầu, họ có nắm được sự việc không?"
  - id: context
    name: "Bối cảnh đủ để không hiểu sai"
    evidence: "Thông tin nền cần có để con số hoặc phát ngôn trong bài không bị hiểu lệch, và chỗ bài đã cung cấp"
    question: "Thiếu bối cảnh nào thì người đọc rút ra kết luận mà chính dữ kiện trong bài không đỡ?"
  - id: harm
    name: "Tác hại và quyền riêng tư"
    evidence: "Danh sách người được nêu tên hoặc nhận diện được, kèm lý do nghiệp vụ phải nêu"
    question: "Ai bị thiệt vì bài này, và việc nêu danh tính họ phục vụ lợi ích công cộng nào?"
lenses:
  - claim_check
  - source_reliability
  - source_independence
  - balance_check
blind_referee: true
```

## 4. Quy tắc biên tập

Trục 4 đọc mục này để biết được phép sửa gì và tuyệt đối không được đụng vào đâu.

Biên tập báo là biên tập **đanh gọn**: cắt cụm đệm, đưa chủ thể lên đầu câu, đổi bị động thành chủ
động khi biết ai làm, thay tính từ đánh giá bằng dữ kiện đã có trong bài. Câu lead dài quá ba mươi
chữ gần như luôn cắt được mà không mất gì.

Vùng bảo vệ đặc trưng của thể loại là **cách quy nguồn và câu rào pháp lý**. Chữ "theo" không phải
cụm đệm; xoá nó để câu gọn là biến lời kể của một bên thành khẳng định của toà soạn. Tương tự,
"bị can", "chưa có kết luận cuối cùng", "chúng tôi đã liên hệ nhưng chưa nhận được phản hồi" là câu
chịu trách nhiệm, không phải câu thừa. Đây là chỗ một trục biên tập chạy theo độ gọn gây hại thật.

```yaml
preserve:
  - cach_quy_nguon_va_chu_theo
  - trich_dan_nguyen_van_cua_nguon
  - ten_rieng_chuc_danh_va_ten_don_vi
  - so_lieu_don_vi_va_moc_thoi_gian
  - cau_rao_phap_ly_va_muc_do_khang_dinh
  - cau_ghi_nhan_da_lien_he_nhung_chua_hoi_dap
  - cach_viet_ten_rieng_theo_quy_tac_toa_soan
moves_allowed:
  - "Cắt cụm đệm và mệnh đề bối cảnh chung ở đầu câu lead"
  - "Đưa chủ thể hành động lên đầu câu"
  - "Đổi câu bị động thành chủ động khi bài đã nêu rõ ai làm"
  - "Thay tính từ đánh giá bằng dữ kiện đã có sẵn trong bài"
  - "Tách câu dài thành hai câu, giữ nguyên cách quy nguồn của từng vế"
  - "Chuyển một khối thông tin xuống dưới theo trật tự tháp ngược, giữ nguyên chữ"
moves_forbidden:
  - "Xoá chữ 'theo' hoặc gộp lời một bên thành khẳng định của bài"
  - "Ghép hai câu trích rời của cùng một người thành một câu trích liền"
  - "Nâng mức khẳng định pháp lý, ví dụ đổi 'bị can' thành cách gọi hàm ý đã có tội"
  - "Thêm chi tiết hiện trường, cảm xúc nhân vật hoặc động cơ không có trong ghi chép"
  - "Xoá câu ghi nhận đã liên hệ mà chưa nhận được phản hồi"
  - "Làm tròn số liệu hoặc đổi đơn vị"
  - "Rút gọn trích dẫn nguyên văn theo cách đổi nghĩa"
tell_families:
  - T01
  - T02
  - T03
  - T05
  - T09
  - T10
  - T12
  - T13
  - T20
  - T23
  - T25
  - T31
  - T32
  - T34
  - T35
voice_priority:
  - writer_profile
  - genre_default
```

## 5. Must-have cho forensics

Trục 5 đọc mục này để tiền đăng ký yêu cầu thể loại và biết tín hiệu nào là bình thường ở bài báo.

Tiền đăng ký các mục dưới đây trước khi đọc bài. Ở thể loại này, must-have xoay quanh **kiểm soát
trích dẫn và kiểm soát nguồn**: mỗi câu trích quy được về một người có tên và tư cách, mỗi khẳng
định trung tâm có từ hai nguồn độc lập, và bên bị nêu tên bất lợi có chỗ để nói. Ba mục này cũng là
ba mục mà bài do máy sinh trượt sớm nhất, vì máy không gọi điện được cho ai.

- `core` — Khẳng định trung tâm có ít nhất hai nguồn độc lập; mỗi khẳng định sự việc đều quy được nguồn.
- `core` — Trích dẫn quy về người nói có tên và tư cách, không bị ghép hay cắt đổi nghĩa.
- `core` — Bên bị nêu tên bất lợi đã được hỏi, và phản hồi hoặc việc từ chối trả lời được ghi trong bài.
- `minor` — Phân biệt rõ điều phóng viên chứng kiến, điều tài liệu ghi và điều người khác kể.
- `minor` — Có mốc thời gian, địa điểm và con số cụ thể truy được, không phải mô tả chung.

Thiếu một mục là dấu hiệu về **năng lực thể loại hoặc về quy trình nghiệp vụ**, không tự nó chứng
minh nguồn gốc AI. Trích dẫn không kiểm chứng được và nguồn ẩn danh cho khẳng định trung tâm là
finding đáng theo đuổi bằng cách hỏi phóng viên đã gặp ai, ghi âm ở đâu — không phải bằng cách suy
đoán ai đã viết câu đó.

Cảnh báo báo oan riêng của thể loại: văn báo vốn có khuôn. Câu lead gói bốn thông tin vào một câu,
cụm quy nguồn lặp lại hàng chục lần, đoạn ngắn một hai câu, cấu trúc tháp ngược giống nhau giữa mọi
bài của cùng toà soạn — tất cả là chuẩn nghề. Xem `skills/05-forensics/references/03-chong-bao-oan.md`
§2 và §6.

```yaml
must_have:
  - level: core
    statement: "Khẳng định trung tâm có ít nhất hai nguồn độc lập; mỗi khẳng định sự việc đều quy được nguồn"
    verify: "Lập bảng khẳng định – nguồn; với mỗi nguồn, truy ngược về nơi thông tin xuất hiện lần đầu và đánh dấu nguồn chỉ dẫn lại nguồn khác"
  - level: core
    statement: "Trích dẫn quy về người nói có tên và tư cách, không bị ghép hay cắt đổi nghĩa"
    verify: "Đếm số trích dẫn không tên kiểu 'theo các chuyên gia'; với 3 trích dẫn có tên, đối chiếu với ghi âm hoặc ghi chép gốc"
  - level: core
    statement: "Bên bị nêu tên bất lợi đã được hỏi, và phản hồi hoặc việc từ chối trả lời được ghi trong bài"
    verify: "Với mỗi bên bị nêu tên bất lợi, tìm câu ghi nhận đã liên hệ kèm thời điểm; không có thì hỏi phóng viên đã liên hệ khi nào"
  - level: minor
    statement: "Phân biệt rõ điều phóng viên chứng kiến, điều tài liệu ghi và điều người khác kể"
    verify: "Đánh dấu mỗi đoạn tường thuật theo ba loại; đoạn không xếp được loại nào là đoạn cần hỏi lại"
  - level: minor
    statement: "Có mốc thời gian, địa điểm và con số cụ thể truy được"
    verify: "Liệt kê mốc thời gian, địa điểm, con số trong bài; đánh dấu cái chỉ có ở dạng chung chung"
genre_baseline:
  normal_signals:
    - "Câu lead gói ai – làm gì – ở đâu – khi nào vào một câu dài: khuôn nghề, không phải khuôn máy"
    - "Cụm quy nguồn lặp đi lặp lại ('theo ông X', 'trao đổi với phóng viên', 'cùng ngày'): yêu cầu minh bạch nguồn, đếm lặp ở đây không đo nguồn gốc"
    - "Đoạn ngắn một đến hai câu, xuống dòng liên tục: chuẩn trình bày báo, không phải nhịp câu giả"
    - "Câu rào pháp lý lặp lại ('bị can', 'chưa có kết luận cuối cùng'): bắt buộc theo quy tắc toà soạn"
    - "Cấu trúc tháp ngược giống nhau giữa các bài cùng toà soạn: yêu cầu của thể loại"
    - "Câu kết mở kiểu 'chúng tôi sẽ tiếp tục thông tin': quy ước của tin đang diễn tiến"
```
