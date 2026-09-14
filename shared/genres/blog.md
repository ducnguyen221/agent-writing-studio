# Hồ sơ thể loại: blog chia sẻ

Hồ sơ này là dữ liệu dùng chung cho năm trục, áp cho mọi bài blog mà người viết đứng ra chia sẻ bằng
tiếng nói của mình: bài kể lại một trải nghiệm, bài nêu quan điểm, bài hướng dẫn từng bước, bài kể
lại một ca thật, bài giải thích một thứ cho người mới, bài giới thiệu công cụ, bài về nghề nghiệp và
cách làm việc, và bài đăng mạng xã hội dạng dài. Nếu yêu cầu của kênh đăng hoặc của người đặt bài
mâu thuẫn với hồ sơ, yêu cầu của nhiệm vụ thắng và phải được ghi trong phạm vi đánh giá.

**Một hồ sơ cho cả ba dòng blog.** Blog kỹ thuật, blog kiến thức và blog chia sẻ không tách thành ba
thể loại, vì thứ phân biệt chúng là **chủ đề**, không phải cách viết hay cách chấm. Ép mọi bài blog
phải có ảnh chụp màn hình, số liệu và phiên bản công cụ là lấy chuẩn của một dòng áp cho cả ba: bài
kể chuyện nghề, bài quan điểm, bài viết cho người mới sẽ rớt ở đúng chỗ chúng không cần phải có.
Thước chung của thể loại này không phải *tác giả đã làm thật việc này chưa*, mà là **bài có gì của
riêng người viết** mà người đọc không lấy được ở nơi khác.

Hồ sơ **tự soạn**. Phần phương pháp — cách chọn vai và góc nhìn, chuỗi triển khai một mục, mức
nghiên cứu nguồn, ba lớp khi viết về một công cụ, danh sách việc không được làm — chưng cất từ một
bộ hướng dẫn viết blog đang dùng thật, đã bỏ toàn bộ tên người, tên tổ chức và lĩnh vực riêng: giữ
lại cách làm, không giữ chân dung ai. Phần còn lại là thứ đo được ở chính kênh: người đọc blog đến
từ một truy vấn hoặc một dòng tiêu đề trên bảng tin, đọc trên điện thoại, và rời đi ngay khi thấy
bài không nói trúng thứ họ quan tâm. Từ đó ra ba ràng buộc của thể loại — mở bài phải chạm ngay, mỗi
đoạn phải thêm được cái mới, và lời mời cuối bài phải xứng với thứ bài vừa cho.

Một câu phân biệt blog với bài luận: bài luận được chấm bởi người **buộc phải đọc hết**, blog thì
không. Vì vậy thể loại này là thể loại duy nhất trong repo bật lăng kính `retention`.

## 1. Intent và bối cảnh

Trục 1 đọc mục này để biết phải hỏi những gì trước khi cho phép bắt đầu viết.

Xác định người đọc mục tiêu, chỗ họ đang mắc hoặc thứ họ đang băn khoăn, thứ họ mang về sau khi đọc,
kênh đăng và độ dài, và quan trọng nhất: **bài này có gì của riêng tác giả**.

Thứ người đọc mang về **không nhất thiết là một kỹ năng**. Bốn dạng đều đủ: hiểu đúng một thứ họ
đang hiểu sai, bớt sợ và bớt chạy theo đám đông, làm được một việc cụ thể, hoặc nhìn một chuyện quen
bằng con mắt khác. Không nói được bài cho người đọc thứ nào trong bốn dạng đó thì bài chưa có lý do
tồn tại.

Chất liệu riêng cũng **không nhất thiết là kinh nghiệm nghề**: một quan sát, một câu chuyện đã được
phép kể, một cách sắp xếp vấn đề chưa ai viết, hay một quan điểm có lập luận đều tính. Thứ không
tính là bài chỉ chép lại và tóm tắt thứ đọc được ở nơi khác — phần đó người đọc cũng đọc được ở nơi
khác.

`nhom_doc_gia` khai người đọc thuộc nhóm nào trong bốn nhóm hay gặp: người mới chưa quen chủ đề,
người đang đi làm muốn dùng được ngay, người đang học muốn hiểu sâu, người ra quyết định muốn biết
nên hay không nên. Cùng một nội dung viết cho bốn nhóm này ra bốn bài khác nhau, nên đây là trường
đầu tiên phải chốt.

Trục 1 cũng chốt **vai** mà tác giả đứng để nhìn vấn đề — người đang làm nghề, người dạy, người xây
sản phẩm, người quản lý, người vừa bắt đầu. Vai quyết định bài được phép khẳng định tới đâu, nên nó
thuộc bối cảnh chứ không phải chuyện văn phong.

```yaml
required_inputs:
  - doc_gia_muc_tieu
  - dieu_ho_dang_mac_hoac_dang_ban_khoan
  - thu_ho_mang_ve_sau_khi_doc
  - kenh_dang_va_do_dai
  - chat_lieu_rieng_cua_tac_gia
  - loi_moi_cuoi_bai
intent_questions:
  - "Người đọc đang mắc hoặc đang băn khoăn ở đâu, và bài này chạm đúng chỗ nào trong đó?"
  - "Sau khi đọc, họ mang về gì — hiểu đúng một thứ, bớt sợ, làm được một việc, hay nhìn khác đi? Viết thành một câu."
  - "Bài này có gì của riêng tác giả — một trải nghiệm, một quan sát, một câu chuyện, hay một quan điểm — mà chỉ tổng hợp tài liệu thì không ra được?"
  - "Tác giả đứng ở vai nào để nhìn chuyện này, và vai đó cho phép khẳng định tới đâu?"
  - "Ai đã viết về chủ đề này rồi, và bài này khác ở chỗ nào?"
  - "Lời khuyên hoặc quan điểm trong bài sai ở trường hợp nào?"
  - "Lời mời cuối bài là gì, và nó có xứng với thứ bài vừa cho không?"
audience_fields:
  - nhom_doc_gia
  - trinh_do_hien_tai
  - viec_ho_dang_lam_do
  - thoi_gian_ho_san_sang_bo_ra
  - kenh_va_thiet_bi_doc
  - thu_khien_ho_dong_tab
stop_if_missing:
  - "Không nói được người đọc mang về gì sau khi đọc"
  - "Không nói được bài có gì của riêng tác giả ngoài thứ đọc được ở nơi khác"
  - "Không biết bài đăng ở đâu và người đọc đến từ đâu"
```

## 2. Khung viết

Trục 2 đọc mục này để chọn khung dàn bài và biết khuôn nào bị cấm ngay từ bản nháp đầu.

Mặc định là hook → giải quyết → lời mời. Hook không phải câu giật gân: nó là câu nêu đúng chỗ người
đọc đang mắc hoặc đang băn khoăn, đủ cụ thể để ai không quan tâm chuyện đó sẽ tự bỏ đi — đó là tính
năng, không phải lỗi. Lời mời cuối bài phải là bước tiếp theo tự nhiên của thứ vừa đọc.

**Chuỗi triển khai một mục** dùng cho mọi khung: *ý chính → giải thích → chất liệu (trải nghiệm, ví
dụ, câu chuyện hoặc nguồn) → bài học → khuyến nghị*. Mục nào dừng ở "giải thích" là mục mới nói lại
điều người đọc đã biết. Riêng khung hướng dẫn thì mỗi bước kèm thêm **cách tự kiểm đã làm đúng** —
đó là đặc thù của khung ấy, không phải yêu cầu chung của thể loại.

Khung `ba_lop_ve_mot_cong_cu` dành cho bài giới thiệu một công cụ, một phương pháp hay một xu hướng.
Ba lớp phải đủ: **khái niệm** (nó là gì, nói cho người chưa biết), **ứng dụng** (nó giúp được ai,
việc gì), và **phản biện** (hợp với ai, không hợp với ai, khi nào chưa cần dùng, kỳ vọng nào là
sai). Thiếu lớp ba thì bài thành quảng cáo, dù không ai trả tiền.

Outline hai tầng: tầng một là lời hứa của bài và các ý chính; tầng hai là chất liệu cho từng ý. Mục
nào ở tầng hai trống là mục sẽ được lấp bằng câu định nghĩa chung chung khi viết prose.

**Bài đăng mạng xã hội dạng dài** dùng chung hồ sơ này, chỉ khác ràng buộc trình bày của kênh: nhiều
nền tảng không đọc markdown, nên tiêu đề mục hiện ra nguyên dấu sao và người viết phải dùng chữ in
đậm Unicode thay cho cú pháp markdown; gạch đầu dòng, đánh số, emoji và vạch ngăn thì dùng được bình
thường. Bài suy ngẫm ở kênh này thường dài hơn hẳn bài tin: mốc tham khảo là sáu tới chín nghìn ký
tự cho bài suy ngẫm và hai tới bốn nghìn cho bài tin, **đo trên một mẫu nhỏ của một người viết,
không phải chuẩn của nền tảng** — dùng để đừng ngạc nhiên khi gặp bài dài, không dùng để chấm. Link
ngoài đặt ở bình luận đầu thay vì trong thân bài khi mục tiêu là tiếp cận. Đây là ràng buộc của
kênh, không phải tiêu chí chất lượng — trục 3 không chấm những thứ này.

```yaml
structures:
  - id: hook_giai_quyet_cta
    parts: [hook, van_de_cu_the, cach_go_van_de, chat_lieu_hoac_vi_du, gioi_han, loi_moi]
  - id: huong_dan_tung_buoc
    parts: [muc_tieu, dieu_kien_can, cac_buoc, cach_kiem_da_dung, loi_hay_gap]
  - id: ke_lai_mot_ca_that
    parts: [tinh_huong, thu_da_lam, cho_hong, thu_rut_ra, viec_ban_doc_lam_khac_di]
  - id: chia_se_trai_nghiem_va_quan_diem
    parts: [hook, cau_chuyen_hoac_quan_sat, dieu_tac_gia_nghi_khac_di, ly_le_va_chat_lieu, cho_minh_co_the_sai, goi_mo]
  - id: giai_thich_cho_nguoi_moi
    parts: [cho_nguoi_moi_hay_hieu_sai, no_thuc_ra_la_gi, vi_du_doi_thuong, cho_de_vap, buoc_dau_tien]
  - id: ba_lop_ve_mot_cong_cu
    parts: [khai_niem_cho_nguoi_chua_biet, no_giup_duoc_ai_viec_gi, hop_ai_khong_hop_ai, khi_nao_chua_can_dung, bat_dau_tu_dau]
default_structure: hook_giai_quyet_cta
anti_llm_defaults:
  - "Mở bài định nghĩa lại một khái niệm người đọc đã biết trước khi vào việc"
  - "Hook giả thẳng thắn kiểu 'Nói thật nhé, hầu hết mọi người đều sai về…' rồi nói một điều hiển nhiên"
  - "Kết bài bằng lời chúc hoặc lời hứa tương lai thay cho một việc người đọc làm được ngay"
  - "Câu báo trước kiểu 'Trong bài này chúng ta sẽ cùng tìm hiểu…' chỉ nhắc lại tiêu đề"
  - "Danh sách 'X điều bạn cần biết' mà mỗi mục chỉ có một câu định nghĩa"
  - "Lời mời cuối bài không liên quan tới thứ bài vừa đưa"
  - "Động viên chung chung kiểu khẩu hiệu, không kèm một việc người đọc làm được ngay"
  - "Giới thiệu một công cụ hoặc một xu hướng mà chỉ khen: không nói hợp với ai, không hợp với ai, khi nào chưa cần dùng"
  - "Tóm tắt lại thứ đọc được ở nơi khác mà không thêm nhận định nào của người viết"
  - "Tiêu đề hoặc hook thổi mức khẩn cấp — 'không thể bỏ lỡ', 'ai cũng đang dùng rồi' — mà thân bài không đỡ nổi mức đó"
outline_depth: 2
outline_layers:
  - "Lời hứa của bài và các ý chính"
  - "Chất liệu cho từng ý — trải nghiệm, câu chuyện, ví dụ cụ thể, con số kèm nguồn, hoặc lập luận riêng của tác giả"
```

## 3. Rubric chất lượng

Trục 3 đọc mục này để biết chấm những gì, bằng chứng nào phải trưng ra và bật lăng kính nào.

Chấm riêng thứ người đọc mang về, câu mở, chất liệu riêng của người viết, quan điểm, mức dễ hiểu với
người mới, khả năng đọc lướt, sự trung thực về giới hạn, và mức xứng của lời mời. Ba lăng kính được
bật: `value_density` hỏi *đoạn này thêm được gì*, `retention` hỏi *người đọc bỏ ở đâu*, `claim_check`
hỏi *con số này lấy ở đâu ra* — blog là nơi số liệu vay mượn không nguồn sống lâu nhất. Khi bài có
dữ kiện, tính năng, số liệu hay thông tin vừa cập nhật, chuẩn của thể loại là **ba tới bảy nguồn
đáng tin và ghi ngày truy cập**; bài thuần trải nghiệm hoặc thuần quan điểm không có dữ kiện nào thì
chuẩn này không áp dụng.

**Không tiêu chí nào đòi bài phải là bài kỹ thuật.** `chat_lieu_rieng` chấp nhận trải nghiệm, quan
sát, câu chuyện, con số riêng hoặc lập luận riêng — bất kỳ thứ nào trong đó là đủ, và phép thử là
*gạch hết câu có thể chép từ một bài tổng quan bất kỳ, phần còn lại là gì*. `de_hieu` chỉ có việc
làm khi bài thật sự dùng thuật ngữ; bài không có thuật ngữ nào thì tiêu chí này qua, không phải ép
tác giả thêm phần giải nghĩa.

Ba luật giữ cho việc chấm không thành báo oan. Thứ nhất, `retention` chạy ở **chế độ tư vấn**:
finding của nó không được đổi `criteria_scores[]` và không được vào `must_fix[]`, vì nó mô phỏng một
độc giả chứ không đọc được văn bản (xem `skills/03-critique/references/01-lenses.md` mục 12). Thứ
hai, `value_density` chỉ được đề nghị xoá **đoạn thân**: mở bài nhắc lại lời hứa của tiêu đề và kết
bài chốt lại việc cần làm là **chức năng** của thể loại, không phải đoạn rỗng. Thứ ba, `quan_diem`
chấm **có nêu lập trường và có tách dữ kiện khỏi ý kiến hay không**, tuyệt đối không chấm lập trường
ấy đúng hay sai — người chấm không đồng ý với tác giả không phải là một finding.

```yaml
criteria:
  - id: reader_gain
    name: "Thứ người đọc mang về"
    evidence: "Một câu nói người đọc mang về gì — hiểu đúng, bớt sợ, làm được, hay nhìn khác đi — kèm chỗ trong bài cho họ thứ đó"
    question: "Người đọc mang về được gì sau khi đọc, và chỗ nào trong bài cho họ thứ đó?"
  - id: hook
    name: "Câu mở"
    evidence: "Ba câu đầu, và một câu nói rõ chúng chạm vào chỗ mắc hoặc chỗ băn khoăn nào của người đọc"
    question: "Ba câu đầu có nêu đúng chỗ người đọc đang mắc, hay mới chỉ giới thiệu chủ đề?"
  - id: chat_lieu_rieng
    name: "Chất liệu riêng của người viết"
    evidence: "Danh sách chi tiết không lấy được từ một bài tổng quan: trải nghiệm, quan sát, câu chuyện, con số của chính tác giả, hoặc một lập luận riêng"
    question: "Gạch hết phần ai cũng viết lại được thì còn lại gì của riêng tác giả?"
  - id: quan_diem
    name: "Quan điểm và lập trường"
    evidence: "Câu nêu tác giả nghĩ nên hay không nên, và các chỗ bài tách rõ đâu là dữ kiện đâu là ý kiến"
    question: "Bài đứng về phía nào, và người đọc có phân biệt được đâu là dữ kiện đâu là ý kiến của tác giả không?"
  - id: de_hieu
    name: "Người mới đọc có theo được"
    evidence: "Danh sách thuật ngữ và từ viết tắt xuất hiện trong bài, kèm chỗ bài giải nghĩa: nó là gì, dùng để làm gì, vì sao đáng quan tâm, ví dụ đời thường"
    question: "Người mới trong nhóm độc giả đã khai vấp ở thuật ngữ nào chưa được giải thích?"
  - id: structure_scan
    name: "Đọc lướt vẫn hiểu"
    evidence: "Đọc riêng các tiêu đề mục theo thứ tự; ghi lại bài nói gì khi chỉ đọc bấy nhiêu"
    question: "Chỉ đọc tiêu đề các mục thì có nắm được bài nói gì và đứng về phía nào không?"
  - id: honesty
    name: "Giới hạn và chỗ dựa của khẳng định"
    evidence: "Danh sách lời khuyên và quan điểm kèm điều kiện áp dụng và ít nhất một trường hợp không đúng; kèm mọi số liệu, tính năng và trích dẫn có nguồn hoặc được nói rõ là ý kiến"
    question: "Lời khuyên hoặc quan điểm nào đang được nói như thể đúng trong mọi hoàn cảnh, và con số nào chưa rõ lấy ở đâu ra?"
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

Giọng đàm thoại là **đặc tính của thể loại, không phải lỗi cần sửa**. Xưng "mình" với người đọc, gọi
người đọc bằng đại từ thân mật của kênh, hỏi thẳng người đọc một câu, chêm một câu đùa, tự trào về
lỗi mình từng mắc, ví von bằng chuyện đời thường — tất cả là thứ giữ người đọc lại. Một trục biên
tập quen văn trang trọng sẽ xoá đúng những chỗ đó và trả lại một bài đúng ngữ pháp mà không ai đọc
hết.

Định dạng bắt buộc của kênh đăng cũng là vùng cấm, và đây là chỗ dễ phá nhất vì nó trông như trang
trí. Chữ in đậm kiểu Unicode, vạch ngăn giữa các mục, khối hashtag cuối bài, vị trí emoji: ở kênh đòi
những thứ đó, xoá đi là bài hiện ra sai khi đăng. Trục 4 không được xoá, kể cả khi thấy chúng thừa.

Quan điểm cũng nằm trong vùng bảo vệ. Câu "mình nghĩ không nên dùng thứ này" bị làm mềm thành "việc
sử dụng cần được cân nhắc tuỳ trường hợp" là mất đúng thứ khiến bài đáng đọc. Trục 4 được phép đề
nghị bổ sung điều kiện áp dụng, không được phép hạ độ mạnh của lập trường.

Ba họ tell `T04` (giọng quảng cáo), `T18` (emoji trang trí) và `T37` (câu hỏi tu từ mở đoạn) **cố ý
không có** trong `tell_families` dưới đây: `genre_baseline` của chính ba họ đó khai `blog` là thể
loại mà giọng chào hàng, emoji và câu hỏi tu từ mở đoạn đều là bình thường. Điều còn phải giữ không nằm ở việc xoá emoji, mà ở việc mỗi lời hứa
phải kèm một điều kiện — và đó là việc của tiêu chí `honesty` ở §3, không phải của trục 4.

```yaml
preserve:
  - giong_dam_thoai_va_dai_tu_xung_ho
  - cach_xung_ho_voi_nguoi_doc
  - trai_nghiem_va_so_lieu_cua_tac_gia
  - quan_diem_va_lap_truong_cua_tac_gia
  - cau_hoi_truc_tiep_voi_nguoi_doc
  - code_lenh_va_thong_bao_loi_nguyen_van
  - ten_cong_cu_va_so_phien_ban
  - duong_dan_va_anh_chup_man_hinh
  - cau_dua_va_cau_tu_trao_cua_tac_gia
  - vi_von_doi_thuong_va_quote_ca_nhan
  - dinh_dang_trinh_bay_bat_buoc_cua_kenh
moves_allowed:
  - "Cắt đoạn mở vòng vo, đưa chỗ người đọc đang mắc lên câu đầu"
  - "Đổi câu định nghĩa thành một ví dụ đã có sẵn trong bài"
  - "Đưa câu giải nghĩa đã có sẵn trong bài lên ngay lần thuật ngữ xuất hiện đầu tiên"
  - "Tách đoạn dài thành đoạn hai đến bốn câu cho dễ đọc trên điện thoại"
  - "Đổi tiêu đề mục chung chung thành lời hứa cụ thể của mục đó"
  - "Gộp hoặc xoá mục chỉ có một câu định nghĩa, đưa nội dung về chỗ nó thuộc về"
  - "Xoá câu chỉ báo trước mình sắp nói gì"
moves_forbidden:
  - "Đổi giọng 'mình / bạn' thành giọng trang trọng vô nhân xưng"
  - "Xoá câu đùa, câu chêm, câu tự trào của tác giả"
  - "Làm mềm quan điểm nên hoặc không nên thành câu trung lập"
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
cho nó là tác giả đứng tên sau thứ mình viết. Vì vậy mục đầu tiên hỏi bài có gì của riêng tác giả,
và mục về nguồn gốc hỏi thẳng: đoạn nào mượn, đoạn nào do công cụ sinh, đã khai chưa.

Mục đầu tiên **cố ý không hỏi tác giả đã tự làm việc đó chưa**. Câu hỏi ấy chỉ đúng với một dòng
blog và báo oan cả ba dòng còn lại: người kể chuyện nghề, người nêu quan điểm, người viết cho người
mới đều không có ảnh chụp màn hình nào để trưng. Thứ đo được ở mọi bài blog là **chất liệu riêng** —
gạch hết phần chép được từ một bài tổng quan, phần còn lại là câu trả lời.

Thiếu một mục là dấu hiệu về **năng lực thể loại hoặc về cam kết nguyên bản**, không tự nó chứng
minh nguồn gốc AI. Mục thứ ba là mục duy nhất trong repo nói thẳng tới công cụ, và cách theo đuổi
nó là đọc `draft.meta.json` nếu bài đi qua trục 2, hoặc hỏi tác giả — không phải suy đoán từ câu chữ.

Cảnh báo báo oan riêng của thể loại: blog là nơi mọi thước đo hình thức sai nhiều nhất. Câu ngắn,
đoạn hai câu, emoji, in đậm, tiếng Anh chuyên ngành giữ nguyên, lặp lại lời hứa của tiêu đề ở mở bài
và kết bài — tất cả là chuẩn trình bày của kênh. Xem
`skills/05-forensics/references/03-false-positive-guard.md` §2 và §6.

```yaml
must_have:
  - level: core
    statement: "Có ít nhất một chất liệu của riêng tác giả: trải nghiệm, quan sát, câu chuyện, con số riêng, hoặc một lập luận riêng"
    verify: "Gạch hết câu có thể chép từ một bài tổng quan bất kỳ; phần còn lại rỗng thì hỏi tác giả bài này của họ ở chỗ nào"
  - level: core
    statement: "Mỗi lời khuyên có điều kiện áp dụng và ít nhất một chỗ nó không đúng"
    verify: "Lập bảng lời khuyên – điều kiện – trường hợp không đúng; ô trống là lời khuyên đang được nói như thể luôn đúng; bài không khuyên gì thì mục này không áp dụng"
  - level: core
    statement: "Nội dung là của tác giả: đoạn mượn, đoạn trích và đoạn do công cụ sinh đều được khai và dẫn nguồn"
    verify: "Soát các đoạn định nghĩa, danh sách và đoạn tổng quan; đối chiếu machine_written_spans trong draft.meta.json nếu có, nếu không thì hỏi tác giả"
  - level: minor
    statement: "Quan điểm của bài nói rõ nó dựa trên gì và chỗ nào nó có thể sai"
    verify: "Tìm câu nêu chỗ tác giả tự thấy mình có thể sai hoặc điều kiện quan điểm đó không còn đúng; không có thì hỏi tác giả, không trừ như thiếu chuẩn mực"
  - level: minor
    statement: "Người đọc mang về một thứ nói được thành câu: hiểu đúng, bớt sợ, làm được, hoặc nhìn khác đi"
    verify: "Viết một câu mô tả thứ đó; không viết được thì bài chưa có lời hứa"
  - level: minor
    statement: "Lời mời cuối bài là bước kế tiếp của thứ bài vừa cho"
    verify: "Đặt lời mời cạnh nội dung bài và hỏi nó phục vụ ai — người đọc hay người viết"
genre_baseline:
  normal_signals:
    - "Giọng đàm thoại, xưng 'mình', gọi người đọc bằng đại từ thân mật của kênh, hỏi thẳng người đọc: đăng ký ngôn ngữ của thể loại"
    - "Tự trào về lỗi mình từng mắc, câu đùa chêm giữa đoạn: cách giữ người đọc, không phải dấu hiệu thiếu nghiêm túc"
    - "Mở bài bằng một câu trích lời người đọc hoặc một câu hỏi tu từ: khuôn mở bài quen của thể loại, T37 khai blog là baseline"
    - "Emoji, in đậm, tiêu đề phụ dày, emoji đặt cuối câu: chuẩn trình bày của kênh — T18 khai blog là baseline"
    - "Tính từ khen ở bài giới thiệu công cụ: T04 khai blog là baseline; chỉ đáng nói khi lời hứa không kèm điều kiện nào"
    - "Bài không có số liệu, không có ảnh chụp màn hình, không có phiên bản công cụ: bài chia sẻ và bài quan điểm không cần những thứ đó"
    - "Câu ngắn, đoạn hai đến ba câu, nhiều lần xuống dòng: viết cho người đọc trên điện thoại"
    - "Mở bài và kết bài cùng nhắc lại lời hứa của tiêu đề: khuôn của thể loại, không phải đoạn rỗng"
    - "Tiếng Anh chuyên ngành giữ nguyên trong lĩnh vực của tác giả: thói quen nghề, không phải dấu vết dịch máy"
    - "Danh sách gạch đầu dòng nhiều: cấu trúc để đọc lướt; chỉ đáng nói khi danh sách thay cho phần lẽ ra phải giải thích"
    - "Chữ in đậm Unicode thay cho cú pháp markdown, khối hashtag ở cuối bài, độ dài hai tới chín nghìn ký tự: chuẩn trình bày của kênh mạng xã hội"
```
