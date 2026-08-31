# Hồ sơ thể loại: tiểu thuyết

Hồ sơ này là dữ liệu dùng chung cho năm trục, áp cho tiểu thuyết, truyện dài kỳ và truyện đăng theo
chương. Nếu yêu cầu của biên tập viên, của nhà xuất bản hoặc của chính tác giả mâu thuẫn với hồ sơ,
yêu cầu của nhiệm vụ thắng và phải được ghi trong phạm vi đánh giá.

Một câu phân biệt tiểu thuyết với bốn thể loại còn lại trong repo: bài luận thuyết phục bằng lập
luận, bài nghiên cứu thuyết phục bằng phương pháp lặp lại được, còn tiểu thuyết thuyết phục bằng
**thứ người đọc tin là đã xảy ra**. Vì vậy mọi tiêu chí ở đây đều đo tính nhất quán bên trong tác
phẩm, không đo tính đúng đắn bên ngoài. Chi tiết trong tiểu thuyết không cần kiểm chứng được ngoài
đời — luật này viết đầy đủ ở §4 và là ngoại lệ lớn nhất của cả repo.

Phương pháp trong file này thuộc bộ luật của studio; nguồn gốc tri thức ghi ở sổ xưởng (không nằm trong repo). Bộ chỉ số gốc dựng cho hai nền tảng truyện mạng
tiếng Trung; ở đây chỉ giữ những chỉ số còn có nghĩa với tiểu thuyết tiếng Việt, và mọi ví dụ là tự
soạn.

## 1. Intent và bối cảnh

Trục 1 đọc mục này để biết phải hỏi những gì trước khi cho phép bắt đầu viết.

Xác định nhân vật chính muốn gì, cái gì cản, luật của thế giới truyện, giọng kể, và truyện dừng ở
đâu. Hai câu hỏi hay bị bỏ qua nhất: *nhân vật mất gì nếu thua* (không có mất mát thì không có
truyện, chỉ có chuỗi sự kiện) và *người kể biết những gì* (ngôi kể quyết định điều nào được phép
xuất hiện trên trang).

Với truyện đăng theo chương, hỏi thêm một câu mang tính kỹ thuật: chương nào đã đăng rồi. Chương đã
đăng là ràng buộc cứng như luật thế giới — sửa nó là chuyện của tác giả với người đọc, không phải
chuyện của trục 2 hay trục 4.

```yaml
required_inputs:
  - the_loai_phu_va_doc_gia
  - nhan_vat_chinh_muon_gi_va_mat_gi
  - luat_cua_the_gioi_truyen
  - ngoi_ke_va_gioi_han_cua_nguoi_ke
  - do_dai_va_hinh_thuc_dang
  - cac_chuong_da_dang_khong_sua_duoc
intent_questions:
  - "Nhân vật chính muốn gì, cái gì cản, và họ mất gì nếu thua?"
  - "Truyện dừng ở đâu — viết một câu tả cảnh cuối, kể cả khi cảnh đó còn thay đổi được?"
  - "Luật nào của thế giới truyện không được vi phạm, kể cả khi tình tiết đang cần một lối thoát?"
  - "Người kể là ai, biết những gì, và có được vào đầu nhân vật nào?"
  - "Chi tiết nào trong truyện đến từ thứ tác giả đã thấy, đã làm hoặc đã nghe kể ngoài đời?"
  - "Người đọc thể loại này thường bỏ sách ở đâu, và lần gần nhất chính tác giả bỏ một cuốn là vì sao?"
audience_fields:
  - the_loai_phu_da_doc
  - ky_vong_ve_nhip
  - muc_chiu_duoc_ve_bao_luc_va_chu_de_nang
  - kenh_doc_va_do_dai_moi_lan_doc
  - thu_khien_ho_bo_truyen
stop_if_missing:
  - "Không nói được nhân vật chính muốn gì và mất gì khi thua"
  - "Không viết ra được luật nào của thế giới truyện trước khi viết chương đầu"
  - "Không biết ai đang kể và người kể được biết tới đâu"
  - "Truyện đang đăng theo chương mà không biết chương nào đã đăng"
```

## 2. Khung viết

Trục 2 đọc mục này để chọn khung dàn bài và biết khuôn nào bị cấm ngay từ bản nháp đầu.

Mặc định là ba hồi: thiết lập – đối đầu – giải quyết, với biến cố khởi đầu đóng hồi một và khủng
hoảng đóng hồi hai. Ba hồi là khung để **kiểm** chứ không phải để lấp: mỗi hồi phải trả lời được câu
"sau hồi này, điều gì khác trước", nếu không thì hồi đó chưa tồn tại.

**Luật ba chương tự kiểm.** Cứ viết xong ba chương thì quét ngay, không dồn tới cuối bản thảo. Đây
là con số chưng cất từ bộ chỉ số gốc, và lý do là một con số khác: trong bản thảo dài mà bộ đó đo,
một khuôn câu duy nhất lặp **663 lượt** vì không ai quét sớm; quét theo cụm ba chương
thì lượt thứ mười đã lộ. Sửa muộn tốn hơn sửa sớm nhiều lần, vì tới lúc đó khuôn đã thành nhịp của
cả cuốn. Quét cái gì thì §3 liệt kê; lăng kính tương ứng là `three_chapter_selfcheck`.

Vòng viết vì vậy là: outline ba tầng → viết ba chương → tự kiểm cụm ba chương → sửa tại chỗ → viết
tiếp. Không có bước "viết xong hết rồi sửa".

```yaml
structures:
  - id: ba_hoi
    parts: [thiet_lap, bien_co_khoi_dau, doi_dau_va_leo_thang, khung_hoang, giai_quyet]
  - id: don_vi_dang_ky
    parts: [moc_mo_chuong, su_kien_rieng_cua_chuong, thay_doi_trang_thai, moc_ket_chuong]
  - id: da_tuyen
    parts: [tuyen_chinh, tuyen_phu, diem_giao_cat, hoi_tu, giai_quyet_tung_tuyen]
default_structure: ba_hoi
anti_llm_defaults:
  - "Mở truyện bằng đoạn giới thiệu bối cảnh và lai lịch nhân vật trước khi có việc gì xảy ra"
  - "Gọi tên cảm xúc thay cho cho thấy nó: 'cô cảm thấy buồn' đứng ở chỗ lẽ ra là một hành động cụ thể"
  - "Mọi nhân vật nói cùng một giọng: che tên đi thì không phân biệt được ai đang nói"
  - "Chương nào cũng kết bằng cùng một kiểu câu treo, ví dụ 'Nhưng cô không biết rằng…'"
  - "Đặt đoạn giải thích luật thế giới dài như trang từ điển vào giữa một cảnh đang diễn ra"
  - "Dùng khuôn 'không phải X mà là Y' làm nhịp tu từ mặc định thay vì dùng đúng một lần khi thật sự có tương phản"
outline_depth: 3
outline_layers:
  - "Hồi — sau hồi này điều gì khác trước"
  - "Chương — chương đổi trạng thái nào, mốc mở và mốc kết là gì"
  - "Cảnh — ai muốn gì trong cảnh, cái gì cản, cảnh dừng ở trạng thái nào"
```

## 3. Rubric chất lượng

Trục 3 đọc mục này để biết chấm những gì, bằng chứng nào phải trưng ra và bật lăng kính nào.

Năm tiêu chí, chấm riêng: nhất quán nhân vật, logic cốt truyện, nhịp thắt mở, hội thoại có cá tính,
và cho thấy thay vì kể lại. Bốn lăng kính được bật khác nhau ở chỗ chúng đọc thứ khác nhau:
`plot_consistency` đọc ràng buộc mà truyện tự đặt, `character_consistency` đọc động cơ nhân vật,
`pacing_curve` đọc bản đồ độ dài kèm cái thay đổi trong mỗi phần, `three_chapter_selfcheck` đọc ba
chương gần nhất như một khối. Một bản thảo có thể qua ba lăng kính đầu mà trượt lăng kính thứ tư:
từng chương ổn, ba chương liền nhau lặp cùng một nước cờ.

**Mười ba chỉ số cứng của bộ gốc — giữ gì, bỏ gì.** Bộ gốc dựng cho truyện mạng
tiếng Trung nên có chỉ số đo bằng đơn vị không tồn tại trong tiếng Việt, và có chỉ số là tối ưu nền
tảng chứ không phải chất lượng văn. Giữ chín, gộp lại thành tám phép kiểm, bỏ bốn:

| Chỉ số gốc | Quyết định | Lý do |
|---|---|---|
| Khuôn "không phải X mà là Y" ≤ 2 lượt/chương | **giữ, ngưỡng chưa hiệu chuẩn** | Khuôn này có thật trong tiếng Việt và là khuôn máy hay dùng nhất. Cùng họ G1 với `T09`, nhưng `T09` hiện chỉ khai "không chỉ… mà còn" / "vừa… vừa"; khuôn "không phải… mà là" **chưa có** trong danh mục tell lẫn `counters.TEMPLATES` — trục 3 đếm tay cho tới khi bổ sung. Con số 2 là của bộ chỉ số gốc, giữ để có mốc, không phải ngưỡng đã đo trên văn Việt |
| Không gọi tên cấu trúc trong thân truyện | **giữ** | "Như đã kể ở phần trước", "trong chương này" là giọng người biên tập lọt vào giọng người kể |
| Không có đoạn khuôn lặp giữa các chương | **giữ** | Đo bằng cách đọc chéo hai chương xa nhau, tìm đoạn cùng cấu trúc |
| Mỗi chương có ít nhất một cảnh, một câu thoại, một hình ảnh chỉ thuộc chương đó | **giữ** | Phép kiểm chống tự lặp vô thức khi viết nhiều chương liền |
| Một từ tả trạng thái lặp ≤ 3 lần/chương · nhóm từ đệm cảm xúc | **giữ, gộp một** | Danh sách phải tự soạn tiếng Việt ("bất giác", "khẽ", "trong lòng dâng lên"), và phải kèm phản chứng: từ láy lặp có chủ ý là nhịp. Lưu ý ba ví dụ trên đều là **đăng ký ngôn ngữ của truyện dịch Trung** (convert, ngôn tình, tiên hiệp) — với tác giả viết đúng dòng ấy cho độc giả dòng ấy (`the_loai_phu_da_doc` ở §1), chúng là chuẩn của dòng truyện, không phải từ đệm; phép kiểm chỉ đếm mật độ, không cấm từ |
| Cùng một bối cảnh kéo quá 3 chương mà không có gì đổi | **giữ** | Đo được, và đổ thẳng vào tiêu chí nhịp |
| Không dùng lại cùng một mối treo dài ở hai chương kề nhau | **giữ** | Mối treo lặp là chỗ người đọc bỏ truyện |
| Che tên vẫn phân biệt được ai đang nói | **giữ** | Phép thử mù, mạnh nhất trong bộ, và không phụ thuộc ngôn ngữ |
| Số chữ tối thiểu mỗi chương | **bỏ** | Đơn vị đếm chữ Hán, và là chỉ tiêu doanh thu của nền tảng, không phải chất lượng |
| Đoạn văn ≤ 200 chữ | **bỏ** | Tối ưu cho màn hình điện thoại; giữ lại thì phạt oan văn xuôi Việt vốn có đoạn dài. Chuyển thành trường `kenh_doc_va_do_dai_moi_lan_doc` ở §1 |
| Gạch ngang ≤ 20 lần/chương | **bỏ** | Tiếng Việt dùng gạch ngang để dẫn lời thoại; đếm dấu là cấm phong cách, đúng loại `03-chong-bao-oan.md` §6 cấm |
| Dấu chấm than ≥ 2 lần ở chương hành động | **bỏ** | Ép giọng theo một dòng truyện mạng cụ thể |

Bảy phép kiểm đầu chạy được ở cụm ba chương; phép thử mù về giọng nhân vật chạy mỗi mười chương hoặc
mỗi khi thêm nhân vật có thoại.

```yaml
criteria:
  - id: character_consistency
    name: "Nhất quán nhân vật"
    evidence: "Hồ sơ động cơ rút từ chính văn bản cho mỗi nhân vật có thoại; danh sách quyết định lớn kèm chỗ truyện đã dựng động cơ"
    question: "Nhân vật này có làm điều mà chương trước đã loại trừ, mà truyện không cho thấy vì sao họ đổi không?"
  - id: plot_logic
    name: "Logic cốt truyện"
    evidence: "Danh sách ràng buộc truyện tự đặt ra (luật thế giới, khoảng cách, thời gian, ai biết gì) kèm chỗ dựng và chỗ dùng"
    question: "Sự kiện nào chỉ xảy ra được nếu vi phạm một ràng buộc mà chính truyện đã dựng?"
  - id: pacing
    name: "Nhịp thắt mở"
    evidence: "Bản đồ độ dài từng chương kèm một câu 'sau chương này, điều gì khác trước'; đánh dấu chương không viết được câu đó"
    question: "Đoạn nào dài mà không có gì thay đổi, và thay đổi lớn nào xảy ra nhanh tới mức người đọc không kịp cảm nhận?"
  - id: dialogue_voice
    name: "Hội thoại có cá tính"
    evidence: "Mười lượt thoại của hai nhân vật chính, xoá tên và câu dẫn, nhờ người khác gán lại"
    question: "Che tên đi thì còn phân biệt được ai đang nói không, và phân biệt bằng cái gì?"
  - id: scene_over_summary
    name: "Cho thấy thay vì kể lại"
    evidence: "Danh sách câu gọi tên cảm xúc hoặc phẩm chất nhân vật, kèm chi tiết cụ thể đang có sẵn trong cùng cảnh"
    question: "Chỗ nào truyện đang nói cho người đọc biết phải cảm thấy gì, thay vì cho họ thấy thứ khiến họ tự cảm thấy?"
lenses:
  - plot_consistency
  - character_consistency
  - pacing_curve
  - three_chapter_selfcheck
blind_referee: true
```

## 4. Quy tắc biên tập

Trục 4 đọc mục này để biết được phép sửa gì và tuyệt đối không được đụng vào đâu.

**Ngoại lệ lớn nhất của repo nằm ở đây: bịa chi tiết là việc của tiểu thuyết.** Ở mọi thể loại khác,
một chi tiết không kiểm chứng được là finding. Ở đây thì không: nhân vật, sự việc, địa danh, số liệu
trong truyện là hư cấu theo đúng nghề của thể loại, và trục 5 không được coi "chi tiết không truy
được ra ngoài đời" là tín hiệu nguồn gốc. Ranh giới vẫn còn nguyên và nó nằm ở chỗ khác: hư cấu là
việc của **tác giả**, nên trục 4 không được tự thêm hay đổi một chi tiết nào. Luật "không thêm dữ
kiện" của trục 4 giữ nguyên hiệu lực — chỉ có nghĩa của chữ "dữ kiện" đổi từ *sự thật ngoài đời*
thành *thứ đã có trên trang*.

Vùng bảo vệ nặng nhất là hội thoại. Lời nhân vật không phải văn của tác giả: nhân vật được phép nói
sai ngữ pháp, nói lặp, nói cụt, dùng phương ngữ và tiếng lóng. Sửa những chỗ đó là xoá nhân vật chứ
không phải sửa văn. Phép cấm đặc trưng của thể loại là **làm phẳng giọng**: ép mọi nhân vật về cùng
một độ dài câu, cùng vốn từ, cùng cách xưng hô. Đó cũng chính là chỗ bản thảo do máy sinh hỏng nặng
nhất, nên một trục biên tập vô ý sẽ xoá đúng thứ mà trục 3 vừa chấm.

```yaml
preserve:
  - hoi_thoai_nguyen_van_cua_nhan_vat
  - giong_va_ngoi_ke
  - ten_rieng_dia_danh_va_luat_the_gioi_da_neu
  - chi_tiet_giac_quan_cu_the
  - lap_co_chu_y_dung_lam_diep
  - cau_cut_cau_khong_chu_ngu_dung_lam_nhip
  - phuong_ngu_tieng_long_va_cach_xung_ho
  - hinh_anh_tac_gia_co_y_de_mo
moves_allowed:
  - "Thay câu gọi tên cảm xúc bằng chi tiết hành động ĐÃ CÓ trong chính cảnh đó"
  - "Chuyển đoạn giải thích luật thế giới lạc giữa cảnh sang chỗ khác trong truyện, giữ nguyên chữ"
  - "Xoá từ đệm lặp không có chủ ý sau khi đã đối chiếu với chỗ lặp có chủ ý"
  - "Tách đoạn dài thành hai đoạn tại chỗ cảnh đổi"
  - "Đổi một câu treo cuối chương trùng khuôn sang kiểu treo khác mà chính truyện đã dùng"
  - "Thống nhất cách gọi một nhân vật hoặc một vật khi truyện đang gọi bằng nhiều tên mà không có lý do trong truyện"
moves_forbidden:
  - "Làm phẳng giọng: ép các nhân vật về cùng độ dài câu, cùng vốn từ, cùng cách xưng hô"
  - "Sửa ngữ pháp trong lời thoại của nhân vật vốn nói sai"
  - "Chuẩn hoá phương ngữ, tiếng lóng hoặc cách xưng hô về giọng phổ thông"
  - "Xoá lặp dùng làm điệp, hoặc gộp các câu ngắn dùng làm nhịp"
  - "Thêm, đổi hoặc xoá tình tiết, nhân vật, luật thế giới, tên riêng"
  - "Giải thích một hình ảnh mà tác giả cố ý để mở"
  - "Ép độ dài câu về một mức đồng đều để trông 'tự nhiên' hơn"
  - "Sửa chương đã đăng khi tác giả chưa quyết định sửa"
tell_families:
  - T09
  - T11
  - T12
  - T20
  - T23
  - T24
  - T25
  - T27
  - T28
  - T32
voice_priority:
  - writer_profile
  - genre_default
```

## 5. Must-have cho forensics

Trục 5 đọc mục này để tiền đăng ký yêu cầu thể loại và biết tín hiệu nào là bình thường ở tiểu thuyết.

Tiền đăng ký các mục dưới đây trước khi đọc bài. Ở thể loại này, must-have xoay quanh **dấu ấn tác
giả**: những thứ chỉ người dựng ra thế giới ấy mới có, và những thứ chỉ người sống mới quan sát được.
Đó cũng là các mục có ích nhất khi đối thoại với tác giả, vì chúng hỏi về quyết định sáng tác chứ
không hỏi về xuất xứ của từng câu.

- `core` — Nhân vật chính có mong muốn và mất mát cụ thể, và các quyết định lớn truy được về hai thứ đó.
- `core` — Truyện tự đặt luật và không phá luật để gỡ tình tiết.
- `core` — Che tên đi vẫn phân biệt được ít nhất hai nhân vật chính qua cách nói.
- `minor` — Mỗi chương có ít nhất một cảnh, một câu thoại hoặc một hình ảnh chỉ thuộc về chương đó.
- `minor` — Mối treo đã gieo có đường thu: đặt → nhắc lại → trả, hoặc được nói rõ là bỏ.
- `minor` — Bản quyền: nhân vật, thế giới và tình tiết là của tác giả; thơ, lời bài hát, văn bản của
  người khác trích vào truyện đều được ghi nguồn.

Thiếu một mục là dấu hiệu về **năng lực thể loại**, không tự nó chứng minh nguồn gốc AI. Riêng mục
bản quyền: viết theo thế giới có sẵn (đồng nhân) không phải đạo văn nếu tác giả khai rõ; điều đáng
theo đuổi là đoạn văn của người khác nằm trong truyện mà không được khai, và cách theo đuổi là đối
chiếu nguồn, không phải suy đoán ai đã viết.

Cảnh báo báo oan riêng của thể loại: gần như mọi thước đo thống kê dùng cho văn xuôi lập luận đều
mất nghĩa ở đây. Độ dài câu chênh nhau rất lớn là **chủ ý** (cảnh hành động khác cảnh tĩnh); lặp mở
đầu câu là **phép điệp**; câu không chủ ngữ là **nhịp kể**. Xem `T11` trong `shared/rules/vi-ai-tells.json`
và `skills/05-forensics/references/03-chong-bao-oan.md` §6.

```yaml
must_have:
  - level: core
    statement: "Nhân vật chính có mong muốn và mất mát cụ thể, và các quyết định lớn truy được về hai thứ đó"
    verify: "Liệt kê 5 quyết định lớn của nhân vật chính; với mỗi quyết định, chỉ ra chỗ truyện đã dựng động cơ trước đó"
  - level: core
    statement: "Truyện tự đặt luật và không phá luật để gỡ tình tiết"
    verify: "Liệt kê luật thế giới đã nêu và chỗ nêu; tìm sự kiện chỉ xảy ra được nếu vi phạm một luật trong danh sách"
  - level: core
    statement: "Che tên đi vẫn phân biệt được ít nhất hai nhân vật chính qua cách nói"
    verify: "Bốc 10 lượt thoại của 2 nhân vật, xoá tên và câu dẫn, nhờ người khác gán lại; ghi tỷ lệ gán đúng"
  - level: minor
    statement: "Mỗi chương có ít nhất một cảnh, một câu thoại hoặc một hình ảnh chỉ thuộc về chương đó"
    verify: "Với 3 chương bất kỳ, viết ra thứ chỉ chương đó có; chương không viết được là chương lặp"
  - level: minor
    statement: "Mối treo đã gieo có đường thu: đặt, nhắc lại, rồi trả hoặc được nói rõ là bỏ"
    verify: "Lập bảng mối treo kèm trạng thái (đã trả · đang treo · bị bỏ quên); mối bị bỏ quên phải hỏi tác giả"
  - level: minor
    statement: "Nhân vật, thế giới và tình tiết là của tác giả; đoạn trích của người khác được ghi nguồn"
    verify: "Liệt kê mọi đoạn thơ, lời hát, văn bản trích trong truyện và đối chiếu nguồn; hỏi tác giả về thế giới mượn nếu có"
genre_baseline:
  normal_signals:
    - "Lặp lại kiểu mở đầu câu qua nhiều đoạn liền: phép điệp là kỹ thuật của thể loại, không phải khuôn máy (đối chiếu T11)"
    - "Câu cụt, câu không chủ ngữ, đoạn chỉ một câu: nhịp kể, không phải lỗi ngữ pháp"
    - "Hội thoại có từ đệm, nói sai, bỏ lửng, lặp lời: đó là cách người thật nói"
    - "Độ dài câu chênh nhau rất lớn trong cùng một chương: cảnh hành động và cảnh tĩnh có nhịp khác nhau, nên mọi thước đo dựa trên độ đều của câu đều vô nghĩa ở đây"
    - "Nhân vật lặp câu cửa miệng của mình qua nhiều chương: đó là thẻ giọng nhân vật"
    - "Chi tiết không kiểm chứng được ngoài đời: hư cấu là nghề của thể loại, xem §4"
    - "Chương kết bằng câu treo: yêu cầu của truyện đăng kỳ; chỉ đáng lưu ý khi mọi chương treo bằng cùng một kiểu câu"
    - "Vốn từ kiểu truyện dịch ('bất giác', 'khẽ', 'trong lòng dâng lên', xưng hô 'hắn / nàng') ở truyện viết theo dòng ngôn tình, tiên hiệp, kiếm hiệp: đăng ký ngôn ngữ của dòng truyện mà độc giả chờ đợi, không phải dấu vết dịch máy; chỉ đáng nói khi §1 khai dòng truyện khác"
```
