# Hồ sơ thể loại: blog chuyên môn

Hồ sơ này là dữ liệu dùng chung cho năm trục, áp cho bài blog chuyên môn, bài hướng dẫn, bài kể lại
một ca thật và bài giới thiệu công cụ. Nếu yêu cầu của kênh đăng hoặc của người đặt bài mâu thuẫn
với hồ sơ, yêu cầu của nhiệm vụ thắng và phải được ghi trong phạm vi đánh giá.

Hồ sơ này **tự soạn**, không chưng cất từ repo nào. Nguồn tri thức là thứ đo được ở chính kênh:
người đọc blog đến từ một truy vấn cụ thể, đọc trên điện thoại, và rời đi ngay khi thấy bài không
gỡ đúng chỗ họ đang mắc. Từ đó ra ba ràng buộc của thể loại — mở bài phải chạm ngay vào vấn đề, mỗi
đoạn phải thêm được cái mới, và lời mời cuối bài phải xứng với thứ bài vừa cho.

Một câu phân biệt blog với bài luận: bài luận được chấm bởi người **buộc phải đọc hết**, blog thì
không. Vì vậy thể loại này là thể loại duy nhất trong repo bật lăng kính `retention`.

## 1. Intent và bối cảnh

Trục 1 đọc mục này để biết phải hỏi những gì trước khi cho phép bắt đầu viết.

Xác định người đọc mục tiêu, chỗ họ đang mắc, thứ họ làm được sau khi đọc, kênh đăng và độ dài, và
quan trọng nhất: **tác giả đã tự làm việc này chưa**. Blog không có bằng chứng nào ngoài kinh nghiệm
và số liệu của chính tác giả; bài viết từ thứ đọc được ở nơi khác thì người đọc cũng đọc được ở nơi
khác.

Nếu không nói được người đọc **làm được việc gì thêm** sau khi đọc, bài chưa có lý do tồn tại.

```yaml
required_inputs:
  - doc_gia_muc_tieu
  - van_de_ho_dang_mac
  - viec_ho_lam_duoc_sau_khi_doc
  - kenh_dang_va_do_dai
  - kinh_nghiem_hoac_so_lieu_that_cua_tac_gia
  - loi_moi_cuoi_bai
intent_questions:
  - "Người đọc đang mắc ở đâu, và bài này gỡ đúng chỗ nào trong đó?"
  - "Sau khi đọc, họ làm được việc gì mà trước đó chưa làm được? Viết thành một câu có động từ."
  - "Tác giả đã tự làm việc này chưa — chi tiết nào chỉ người làm rồi mới biết?"
  - "Ai đã viết về chủ đề này rồi, và bài này khác ở chỗ nào?"
  - "Lời khuyên trong bài sai ở trường hợp nào?"
  - "Lời mời cuối bài là gì, và nó có xứng với thứ bài vừa cho không?"
audience_fields:
  - trinh_do_hien_tai
  - viec_ho_dang_lam_do
  - thoi_gian_ho_san_sang_bo_ra
  - kenh_va_thiet_bi_doc
  - thu_khien_ho_dong_tab
stop_if_missing:
  - "Không nói được người đọc làm được việc gì thêm sau khi đọc"
  - "Không có chi tiết nào từ kinh nghiệm hoặc dữ liệu của chính tác giả"
  - "Không biết bài đăng ở đâu và người đọc đến từ đâu"
```

## 2. Khung viết

Trục 2 đọc mục này để chọn khung dàn bài và biết khuôn nào bị cấm ngay từ bản nháp đầu.

Mặc định là hook → giải quyết → lời mời. Hook không phải câu giật gân: nó là câu nêu đúng chỗ người
đọc đang mắc, đủ cụ thể để ai không mắc chỗ đó sẽ tự bỏ đi — đó là tính năng, không phải lỗi. Phần
giải quyết đi theo bước, mỗi bước kèm cách kiểm mình đã làm đúng. Lời mời cuối bài phải là bước tiếp
theo tự nhiên của thứ vừa đọc.

Outline hai tầng: tầng một là lời hứa của bài và các bước; tầng hai là bằng chứng cho từng bước —
ảnh chụp màn hình, con số của chính tác giả, lỗi thật đã gặp. Mục nào ở tầng hai trống là mục sẽ
được lấp bằng câu định nghĩa chung chung khi viết prose.

```yaml
structures:
  - id: hook_giai_quyet_cta
    parts: [hook, van_de_cu_the, cach_lam_tung_buoc, bang_chung_hoac_vi_du, gioi_han, loi_moi]
  - id: huong_dan_tung_buoc
    parts: [muc_tieu, dieu_kien_can, cac_buoc, cach_kiem_da_dung, loi_hay_gap]
  - id: ke_lai_mot_ca_that
    parts: [tinh_huong, thu_da_lam, cho_hong, thu_rut_ra, viec_ban_doc_lam_khac_di]
default_structure: hook_giai_quyet_cta
anti_llm_defaults:
  - "Mở bài định nghĩa lại một khái niệm người đọc đã biết trước khi vào việc"
  - "Hook giả thẳng thắn kiểu 'Nói thật nhé, hầu hết mọi người đều sai về…' rồi nói một điều hiển nhiên"
  - "Kết bài bằng lời chúc hoặc lời hứa tương lai thay cho một việc người đọc làm được ngay"
  - "Câu báo trước kiểu 'Trong bài này chúng ta sẽ cùng tìm hiểu…' chỉ nhắc lại tiêu đề"
  - "Danh sách 'X điều bạn cần biết' mà mỗi mục chỉ có một câu định nghĩa"
  - "Lời mời cuối bài không liên quan tới thứ bài vừa đưa"
outline_depth: 2
outline_layers:
  - "Lời hứa của bài và các bước"
  - "Bằng chứng cho từng bước — ảnh chụp màn hình, con số của chính tác giả, lỗi thật đã gặp"
```

## 3. Rubric chất lượng

Trục 3 đọc mục này để biết chấm những gì, bằng chứng nào phải trưng ra và bật lăng kính nào.

Chấm riêng thứ người đọc mang về, câu mở, bằng chứng đã trải, khả năng đọc lướt, sự trung thực về
giới hạn, và mức xứng của lời mời. Ba lăng kính được bật: `value_density` hỏi *đoạn này thêm được
gì*, `retention` hỏi *người đọc bỏ ở đâu*, `claim_check` hỏi *con số này lấy ở đâu ra* — blog là nơi
số liệu vay mượn không nguồn sống lâu nhất.

Hai luật giữ cho việc chấm không thành báo oan. Thứ nhất, `retention` chạy ở **chế độ tư vấn**:
finding của nó không được đổi `criteria_scores[]` và không được vào `must_fix[]`, vì nó mô phỏng một
độc giả chứ không đọc được văn bản (xem `skills/03-critique/references/01-lang-kinh.md` mục 12). Thứ
hai, `value_density` chỉ được đề nghị xoá **đoạn thân**: mở bài nhắc lại lời hứa của tiêu đề và kết
bài chốt lại việc cần làm là **chức năng** của thể loại, không phải đoạn rỗng.

```yaml
criteria:
  - id: reader_gain
    name: "Thứ người đọc mang về"
    evidence: "Một câu có động từ nói người đọc làm được gì sau khi đọc, kèm chỗ trong bài dạy họ làm việc đó"
    question: "Người đọc làm được việc gì sau khi đọc mà trước đó chưa làm được?"
  - id: hook
    name: "Câu mở"
    evidence: "Ba câu đầu, và một câu nói rõ chúng chạm vào chỗ mắc nào của người đọc"
    question: "Ba câu đầu có nêu đúng chỗ người đọc đang mắc, hay mới chỉ giới thiệu chủ đề?"
  - id: evidence_lived
    name: "Bằng chứng đã trải"
    evidence: "Danh sách chi tiết chỉ người đã tự làm mới biết: lỗi gặp phải, con số của chính tác giả, ảnh chụp màn hình, phiên bản công cụ"
    question: "Chi tiết nào trong bài chứng tỏ tác giả đã thật sự làm việc này?"
  - id: structure_scan
    name: "Đọc lướt vẫn hiểu"
    evidence: "Đọc riêng các tiêu đề mục theo thứ tự; ghi lại bài nói gì khi chỉ đọc bấy nhiêu"
    question: "Chỉ đọc tiêu đề các mục thì có nắm được cách làm không?"
  - id: honesty
    name: "Giới hạn và điều kiện"
    evidence: "Danh sách lời khuyên kèm điều kiện áp dụng và ít nhất một trường hợp lời khuyên đó không đúng"
    question: "Lời khuyên nào đang được nói như thể đúng trong mọi hoàn cảnh?"
  - id: cta_fit
    name: "Lời mời xứng với bài"
    evidence: "Lời mời cuối bài, đặt cạnh thứ bài đã cho, và bước tiếp theo tự nhiên của người đọc"
    question: "Lời mời này có phải bước kế tiếp của thứ vừa đọc, hay là việc của người viết?"
lenses:
  - value_density
  - retention
  - claim_check
blind_referee: true
```

## 4. Quy tắc biên tập

Trục 4 đọc mục này để biết được phép sửa gì và tuyệt đối không được đụng vào đâu.

Giọng đàm thoại là **đặc tính của thể loại, không phải lỗi cần sửa**. Xưng "mình" với người đọc, hỏi
thẳng người đọc một câu, chêm một câu đùa, tự trào về lỗi mình từng mắc — tất cả là thứ giữ người
đọc lại. Một trục biên tập quen văn trang trọng sẽ xoá đúng những chỗ đó và trả lại một bài đúng ngữ
pháp mà không ai đọc hết.

Hai họ tell `T04` (giọng quảng cáo) và `T18` (emoji trang trí) **cố ý không có** trong
`tell_families` dưới đây: `genre_baseline` của chính hai họ đó khai `blog` là thể loại mà giọng chào
hàng và emoji là bình thường. Điều còn phải giữ không nằm ở việc xoá emoji, mà ở việc mỗi lời hứa
phải kèm một điều kiện — và đó là việc của tiêu chí `honesty` ở §3, không phải của trục 4.

```yaml
preserve:
  - giong_dam_thoai_va_dai_tu_xung_ho
  - trai_nghiem_va_so_lieu_cua_tac_gia
  - cau_hoi_truc_tiep_voi_nguoi_doc
  - code_lenh_va_thong_bao_loi_nguyen_van
  - ten_cong_cu_va_so_phien_ban
  - duong_dan_va_anh_chup_man_hinh
  - cau_dua_va_cau_tu_trao_cua_tac_gia
moves_allowed:
  - "Cắt đoạn mở vòng vo, đưa chỗ người đọc đang mắc lên câu đầu"
  - "Đổi câu định nghĩa thành một ví dụ đã có sẵn trong bài"
  - "Tách đoạn dài thành đoạn hai đến bốn câu cho dễ đọc trên điện thoại"
  - "Đổi tiêu đề mục chung chung thành lời hứa cụ thể của mục đó"
  - "Gộp hoặc xoá mục chỉ có một câu định nghĩa, đưa nội dung về chỗ nó thuộc về"
  - "Xoá câu chỉ báo trước mình sắp nói gì"
moves_forbidden:
  - "Đổi giọng 'mình / bạn' thành giọng trang trọng vô nhân xưng"
  - "Xoá câu đùa, câu chêm, câu tự trào của tác giả"
  - "Thêm số liệu, tên công cụ, phiên bản hoặc kết quả mà tác giả không nêu"
  - "Sửa nội dung code, lệnh hoặc thông báo lỗi được trích nguyên văn"
  - "Thêm emoji, in đậm hoặc tiêu đề phụ để bài 'trông hấp dẫn hơn'"
  - "Ép các mục dài bằng nhau"
  - "Nới lời khuyên có điều kiện thành lời khuyên chung"
tell_families:
  - T01
  - T09
  - T12
  - T16
  - T20
  - T21
  - T22
  - T23
  - T24
  - T25
  - T27
  - T28
  - T31
  - T32
  - T33
voice_priority:
  - writer_profile
  - genre_default
```

## 5. Must-have cho forensics

Trục 5 đọc mục này để tiền đăng ký yêu cầu thể loại và biết tín hiệu nào là bình thường ở blog.

Tiền đăng ký các mục dưới đây trước khi đọc bài. Ở thể loại này, must-have xoay quanh **cam kết
nguyên bản**: bài blog không có barem, không có hội đồng, không có toà soạn — thứ duy nhất bảo chứng
cho nó là tác giả đã tự làm và tự chịu trách nhiệm về thứ mình khuyên. Vì vậy mục đầu tiên hỏi đúng
điều đó, và mục về nguồn gốc hỏi thẳng: đoạn nào mượn, đoạn nào do công cụ sinh, đã khai chưa.

- `core` — Có ít nhất một chi tiết chỉ người đã thật sự làm việc này mới biết.
- `core` — Mỗi lời khuyên có điều kiện áp dụng và ít nhất một chỗ nó không đúng.
- `core` — Nội dung là của tác giả: đoạn mượn từ bài khác, từ tài liệu, hoặc do công cụ sinh đều được
  khai và dẫn nguồn.
- `minor` — Người đọc làm được một việc cụ thể sau khi đọc, viết được thành một câu có động từ.
- `minor` — Lời mời cuối bài là bước kế tiếp của thứ bài vừa cho.

Thiếu một mục là dấu hiệu về **năng lực thể loại hoặc về cam kết nguyên bản**, không tự nó chứng
minh nguồn gốc AI. Mục thứ ba là mục duy nhất trong repo nói thẳng tới công cụ, và cách theo đuổi
nó là đọc `draft.meta.json` nếu bài đi qua trục 2, hoặc hỏi tác giả — không phải suy đoán từ câu chữ.

Cảnh báo báo oan riêng của thể loại: blog là nơi mọi thước đo hình thức sai nhiều nhất. Câu ngắn,
đoạn hai câu, emoji, in đậm, tiếng Anh chuyên ngành giữ nguyên, lặp lại lời hứa của tiêu đề ở mở bài
và kết bài — tất cả là chuẩn trình bày của kênh. Xem
`skills/05-forensics/references/03-chong-bao-oan.md` §2 và §6.

```yaml
must_have:
  - level: core
    statement: "Có ít nhất một chi tiết chỉ người đã thật sự làm việc này mới biết"
    verify: "Liệt kê chi tiết dạng lỗi đã gặp, con số của chính tác giả, phiên bản công cụ, ảnh chụp màn hình; không có mục nào thì hỏi tác giả đã chạy thử chưa"
  - level: core
    statement: "Mỗi lời khuyên có điều kiện áp dụng và ít nhất một chỗ nó không đúng"
    verify: "Lập bảng lời khuyên – điều kiện – trường hợp không đúng; ô trống là lời khuyên đang được nói như thể luôn đúng"
  - level: core
    statement: "Nội dung là của tác giả: đoạn mượn, đoạn trích và đoạn do công cụ sinh đều được khai và dẫn nguồn"
    verify: "Soát các đoạn định nghĩa, danh sách và đoạn tổng quan; đối chiếu machine_written_spans trong draft.meta.json nếu có, nếu không thì hỏi tác giả"
  - level: minor
    statement: "Người đọc làm được một việc cụ thể sau khi đọc"
    verify: "Viết một câu có động từ mô tả việc đó; không viết được thì bài chưa có lời hứa"
  - level: minor
    statement: "Lời mời cuối bài là bước kế tiếp của thứ bài vừa cho"
    verify: "Đặt lời mời cạnh nội dung bài và hỏi nó phục vụ ai — người đọc hay người viết"
genre_baseline:
  normal_signals:
    - "Giọng đàm thoại, xưng 'mình / bạn', hỏi thẳng người đọc: đăng ký ngôn ngữ của thể loại"
    - "Emoji, in đậm, tiêu đề phụ dày: chuẩn trình bày của kênh — T18 khai blog là baseline"
    - "Tính từ khen ở bài giới thiệu công cụ: T04 khai blog là baseline; chỉ đáng nói khi lời hứa không kèm điều kiện nào"
    - "Câu ngắn, đoạn hai đến ba câu, nhiều lần xuống dòng: viết cho người đọc trên điện thoại"
    - "Mở bài và kết bài cùng nhắc lại lời hứa của tiêu đề: khuôn của thể loại, không phải đoạn rỗng"
    - "Tiếng Anh chuyên ngành giữ nguyên (deploy, prompt, dashboard): thói quen nghề, không phải dấu vết dịch máy"
    - "Danh sách gạch đầu dòng nhiều: cấu trúc để đọc lướt; chỉ đáng nói khi danh sách thay cho phần lẽ ra phải giải thích"
```
