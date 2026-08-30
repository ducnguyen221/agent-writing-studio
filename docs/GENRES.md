# Soạn một hồ sơ thể loại

> Dành cho người **biết nghề viết** chứ không nhất thiết biết lập trình. Soạn một hồ sơ thể loại là
> viết một file văn bản, không phải viết code. Nếu bạn chấm được bài của học viên và nói được "bài
> loại này bắt buộc phải có gì", bạn soạn được hồ sơ.

---

## 1. Hồ sơ thể loại là gì, và vì sao nó không nằm trong skill

Repo này có năm **trục** — năm giai đoạn của một bài viết: dựng bối cảnh, viết nháp, phản biện, biên
tập, giám định. Mỗi trục là một **skill**: một thư mục hướng dẫn cho AI agent biết làm theo trình tự
nào.

Nhưng năm trục ấy phải làm việc trên nhiều loại bài rất khác nhau. Chấm một bài luận thi và chấm một
chương tiểu thuyết dùng **cùng một quy trình chấm**, chỉ khác **tiêu chí**. Nếu nhét cái khác nhau đó
vào trong skill thì skill phải rẽ nhánh `nếu là tiểu thuyết thì…`, và mỗi thể loại mới lại phải sửa
năm skill.

Nên luật của repo là một câu:

> **Thể loại là dữ liệu, skill là logic.**

Một thể loại = **một file** `shared/genres/<slug>.md`, có đúng năm mục đánh số. Mục §1 dành cho trục
1, §2 cho trục 2, và cứ thế. Trục *i* chỉ đọc mục §*i*. Thêm thể loại mới = thêm một file, không sửa
dòng code nào; và không skill nào được phép viết `if genre == "novel"`.

Hợp đồng đầy đủ về hình dạng file nằm ở `shared/genres/_schema.md` — file đó là **luật**, tài liệu bạn
đang đọc là **hướng dẫn dùng luật**. Chỗ nào hai bên lệch nhau thì `_schema.md` thắng.

### Nội dung một file: văn xuôi cho người, YAML cho máy

Mỗi mục §1…§5 gồm hai phần, và **cả hai đều bắt buộc**:

- **Văn xuôi** — giải thích cho người soạn thể loại kế tiếp hiểu vì sao lại khai như vậy. Không được
  lược bỏ vì "máy không đọc phần này".
- **Đúng một khối YAML** — phần máy đọc. *YAML* là cách viết danh sách và cặp khoá–giá trị bằng chữ
  thường và dấu hai chấm; nhìn ví dụ ở mục 4 dưới là quen ngay.

---

## 2. `full` hay `partial` — hai trạng thái, không có trạng thái thứ ba

| Trạng thái | Nhận biết | Dùng được cho |
|---|---|---|
| `full` | có đủ `## 1.` … `## 5.` | cả năm trục |
| `partial` | **chỉ có `## 5.`** | riêng trục 5 (giám định) |

`partial` tồn tại vì một lý do thực tế: có những thể loại **đã phải giám định thật** trước khi ai kịp
soạn phần viết cho chúng. Bốn thể loại Việt Nam đặc thù trong repo — `chinh-luan`,
`de-cuong-nghien-cuu`, `bao-cao-thuc-tap`, `sang-kien-kinh-nghiem` — đang ở trạng thái này. Trục 1
đến trục 4 **không đọc** file `partial` nào; chúng chỉ tồn tại để trục 5 có căn cứ hạ tín hiệu thay vì
báo oan văn phong hành chính chuẩn.

Mọi tổ hợp khác đều là **lỗi**, không phải "một phần": một file có `## 3.` mà thiếu `## 1.` sẽ làm test
đỏ. Lý do là hợp đồng phải đọc được bằng mắt — nhìn file là biết ngay trục nào dùng được.

---

## 3. Thứ tự soạn: §5 → §3 → §2 → §1 → §4

Đây không phải thứ tự tuỳ hứng. Mỗi bước dựa trên bước trước:

1. **§5 trước tiên.** Đây là mục **ít mang định kiến nhất**: "bài loại này bắt buộc phải có gì" là
   câu hỏi trả lời được mà chưa cần biết ai viết, viết hay hay dở. Liệt kê 2–4 mục bắt buộc, và liệt
   kê những tín hiệu **bình thường** của thể loại.
2. **§3 — chấm cái gì.** Từ danh sách "phải có" ở §5, suy ra "chấm cái gì và bằng chứng nào".
3. **§2 — viết theo khung nào**, và cấm khuôn máy nào ngay từ bản nháp đầu.
4. **§1 — hỏi gì trước khi cho viết.** Viết sau §2 vì phải biết khung mới biết thiếu thông tin nào là
   chưa viết được.
5. **§4 cuối cùng.** Vùng cấm sửa của trục 4 là hệ quả của những gì §3 và §5 đã quyết định — viết §4
   trước thì sẽ cấm nhầm hoặc cho phép nhầm.

Xong thì chạy:

```bash
python -m pytest tests/genres -q
```

---

## 4. Năm mục, từng mục một — đối chiếu `essay` và `novel`

Hai hồ sơ dưới đây là hai cực xa nhau nhất trong repo: một bài luận thi và một cuốn tiểu thuyết. Đọc
song song hai cột là cách nhanh nhất để thấy **cái gì là dữ liệu thể loại** và **cái gì là quy trình
dùng chung**.

### §1 · Intent và bối cảnh — trục 1 đọc

Trục 1 phỏng vấn cho tới khi trả lời hết `intent_questions`, dựng chân dung độc giả theo
`audience_fields`, rồi xuất `context.json`. Còn mục nào trong `stop_if_missing` chưa gỡ được thì trục
1 **dừng và hỏi**, không chuyển sang trục 2.

| Khoá | Nghĩa |
|---|---|
| `required_inputs` | thiếu thứ này thì chưa được viết: đề bài, barem, người chấm, hạn nộp… |
| `intent_questions` | câu hỏi trục 1 phải trả lời được và ghi lại |
| `audience_fields` | trường bắt buộc của chân dung độc giả cho thể loại này |
| `stop_if_missing` | điều kiện dừng, viết ở dạng khẳng định kiểm được |

| | `essay.md` | `novel.md` |
|---|---|---|
| `required_inputs` | `de_bai` · `nguoi_cham_va_barem` · `gioi_han_tu` · `chuan_trich_dan` | `the_loai_phu_va_doc_gia` · `nhan_vat_chinh_muon_gi_va_mat_gi` · `luat_cua_the_gioi_truyen` · `ngoi_ke_va_gioi_han_cua_nguoi_ke` · `cac_chuong_da_dang_khong_sua_duoc` |
| câu hỏi tiêu biểu | *"Luận đề viết lại thành một câu có thể bị phản bác là gì?"* | *"Nhân vật chính muốn gì, cái gì cản, và họ mất gì nếu thua?"* |
| điều kiện dừng | không viết lại được luận đề thành câu phản bác được | không nói được nhân vật chính mất gì khi thua |

Cùng một hình dạng, nội dung khác hoàn toàn. Chỗ giống nhau đáng chú ý: cả hai đều có một điều kiện
dừng dạng "không phát biểu nổi cái lõi thì chưa viết được" — bài luận là luận đề, tiểu thuyết là mất
mát của nhân vật.

**Lỗi hay gặp:** viết `intent_questions` thành câu hỏi mà agent tự trả lời được từ đề bài. Câu hỏi tốt
là câu **chỉ người dùng mới trả lời được** — họ có bằng chứng gì trong tay, ai sẽ chấm, họ định dừng
truyện ở đâu.

### §2 · Khung viết — trục 2 đọc

Trục 2 chọn một khung trong `structures[]` (mặc định là `default_structure`), duyệt dàn ý đủ
`outline_depth` tầng rồi mới viết văn xuôi, và **cấm ngay khi sinh** các khuôn trong `anti_llm_defaults`.

| Khoá | Nghĩa |
|---|---|
| `structures` | các khung có tên: PEEL, IMRAD, tháp ngược, ba hồi… mỗi khung có `id` và `parts` |
| `default_structure` | phải là một `id` có trong `structures` |
| `anti_llm_defaults` | khuôn mở bài, chuyển đoạn, kết bài bị cấm **ngay từ bản nháp đầu** |
| `outline_depth` | số tầng dàn ý phải duyệt xong trước khi viết văn xuôi |
| `outline_layers` | nghĩa của từng tầng, đúng `outline_depth` mục, xếp từ tầng một |

`essay` khai ba khung (`peel`, `mo_than_ket`, `luan_de_phan_de`) và cấm những thứ như *"Mở bài bằng
mệnh đề toàn cảnh kiểu 'Trong bối cảnh … đang diễn ra mạnh mẽ'"*. `novel` khai khung ba hồi và cấm
những khuôn khác hẳn — kiểu *"Nhưng cô không biết rằng…"*.

**Số tầng là của skill, nghĩa từng tầng là của thể loại.** Trục 2 ép `outline_depth` và cổng duyệt;
còn tầng một là gì thì hồ sơ nói: `essay` đi luận đề → đoạn → bằng chứng, `novel` đi hồi → chương →
cảnh, `journalism` đi khối thông tin → nguồn gắn cho từng khối. Vì thế `outline_layers` nằm trong dữ
liệu thể loại chứ không nằm trong SKILL.md — thêm một thể loại có cách dựng dàn ý khác thì không phải
sửa skill.

**Phân biệt quan trọng nhất của cả file:** `anti_llm_defaults` ở §2 là **cấm khi sinh**;
`tell_families` ở §4 là **sửa khi biên tập**. Cấm sớm rẻ hơn sửa muộn, và tránh cái vòng luẩn quẩn
"máy sinh khuôn rồi máy tự khen là đã xoá khuôn".

### §3 · Rubric chất lượng — trục 3 đọc

Trục 3 chấm **riêng từng** tiêu chí (không cộng gộp thành một điểm tổng), chạy đúng những lăng kính
được bật, rồi xuất `critique.json`.

| Khoá | Nghĩa |
|---|---|
| `criteria` | mỗi tiêu chí có `id`, `name`, `evidence` (bằng chứng bắt buộc trưng ra) và `question` (câu hỏi người chấm phải trả lời) |
| `lenses` | tập con của **danh mục 13 lăng kính** ở `_schema.md` mục 3 — hồ sơ chỉ **bật/tắt**, không định nghĩa lăng kính mới |
| `blind_referee` | `true` = người chấm không được xem bản tự khai `draft.meta.json` trước khi chấm xong |

| | `essay.md` | `novel.md` |
|---|---|---|
| số tiêu chí | 6 — `task_response` · `logic` · `evidence` · `counterargument` · `cohesion` · `language` | 5 — `character_consistency` · `plot_logic` · `pacing` · `dialogue_voice` · `scene_over_summary` |
| lăng kính bật | `task_response` · `fallacy_scan` · `claim_check` | `plot_consistency` · `character_consistency` · `pacing_curve` · `three_chapter_selfcheck` |
| `blind_referee` | `true` | `true` |

**Không một `id` tiêu chí nào trùng nhau, và cả hai xuất ra cùng một file `critique.json`.** Đó chính
là ranh giới dữ liệu/logic mà cả kiến trúc dựa vào: thay thể loại thì nội dung chấm đổi, hình dạng kết
quả không đổi.

`evidence` là chỗ dễ viết hỏng nhất. So sánh:

- ❌ *"đánh giá xem nhân vật có nhất quán không"* — đây là kết luận, không phải bằng chứng.
- ✅ *"hồ sơ động cơ rút từ chính văn bản cho mỗi nhân vật có thoại; danh sách quyết định lớn kèm chỗ
  truyện đã dựng động cơ"* — đây là thứ trưng ra được, và người khác kiểm lại được.

Một mẹo của `novel.md` đáng học: tiêu chí `dialogue_voice` yêu cầu bằng chứng là *"mười lượt thoại của
hai nhân vật chính, xoá tên và câu dẫn, nhờ người khác gán lại"*. Đó là một **phép thử mù** — nó không
phụ thuộc vào việc người chấm có thiện chí hay không.

### §4 · Quy tắc biên tập — trục 4 đọc

Trục 4 chỉ được dùng các phép trong `moves_allowed`, tuyệt đối không đụng vùng `preserve`, và chỉ soi
các họ dấu hiệu liệt kê ở `tell_families`.

| Khoá | Nghĩa |
|---|---|
| `preserve` | vùng cấm sửa: số liệu, trích dẫn, tên riêng, thuật ngữ, hội thoại nhân vật… |
| `moves_allowed` | phép biên tập được dùng |
| `moves_forbidden` | phép bị cấm riêng cho thể loại này |
| `tell_families` | mã dấu hiệu (`T01`, `T09`…) trong `shared/rules/vi-ai-tells.json` áp cho thể loại này |
| `voice_priority` | thứ tự thắng khi mâu thuẫn |

`voice_priority: [writer_profile, genre_default]` là luật **"bài mẫu của người viết thắng mọi quy tắc
văn phong"**. Nếu hồ sơ giọng của tác giả ghi rằng họ hay mở đoạn bằng câu hỏi, trục 4 không được xoá
thói quen đó — kể cả khi có một dấu hiệu nói rằng câu hỏi mở đoạn là khuôn máy.

`moves_forbidden` của `essay.md` có một dòng đáng chép sang mọi thể loại mới: *"Đổi mức mạnh của khẳng
định (thêm hoặc bớt rào đón)"*. Đổi "có thể" thành "chắc chắn" là đổi **điều được nói**, không phải
biên tập — việc đó thuộc về trục 2 vòng hai, và trục 4 chỉ được ghi cảnh báo.

### §5 · Must-have cho forensics — trục 5 đọc; trục 2 và 3 dùng lại

Trục 5 **tiền đăng ký** danh sách `must_have[]` **trước khi đọc bài**, và dùng
`genre_baseline.normal_signals` để **hạ** tín hiệu, không bao giờ để tạo thêm nghi vấn.

| Khoá | Nghĩa |
|---|---|
| `must_have` | mỗi mục có `level` (`core` hoặc `minor`), `statement` (điều bắt buộc phải có) và `verify` (cách kiểm cụ thể) |
| `genre_baseline.normal_signals` | những tín hiệu **bình thường** ở thể loại này |

"Tiền đăng ký" nghĩa là: viết danh sách ra **trước**, rồi mới mở bài ra đọc. Thêm một tiêu chí sau khi
đã thấy lỗi là chọn tiêu chí theo kết quả — đó là cách tự chứng minh mình đúng.

Và một luật phải nhắc lại mỗi lần:

> **Thiếu một `must_have` là dấu hiệu về NĂNG LỰC THỂ LOẠI, không tự nó chứng minh nguồn gốc AI.**

`verify` phải là **thao tác**, không phải cảm nhận:

- ❌ *"kiểm tra xem luận đề có rõ ràng không"*
- ✅ *"viết lại luận đề thành một câu, rồi ánh xạ mỗi đoạn thân về luận đề đó"*

---

## 5. `genre_baseline` — hàng rào chống báo oan, và luật khai ở đâu

Đây là phần quan trọng nhất của một hồ sơ thể loại, vì nó là thứ ngăn hệ thống **báo oan văn phong
được dạy trong trường**.

Văn hành chính – học thuật Việt Nam vốn là văn công thức: mục "kết quả – tồn tại – phương hướng", cụm
"đóng vai trò quan trọng", câu mở "Trong bối cảnh…", bộ ba song hành. Tất cả những thứ đó có **trước**
khi có mô hình ngôn ngữ. Một hệ thống đo mật độ sáo ngữ mà không biết điều này thì nó đang đo **thể
loại**, và gọi kết quả là **nguồn gốc**.

`normal_signals` chỉ làm một việc: **hạ tín hiệu**. Nó không bao giờ được dùng theo chiều ngược lại.

### Hai nguồn khai, và đó là cố ý

| Khai ở đâu | Khai theo chiều nào | Ai đọc |
|---|---|---|
| `genre_baseline[]` của từng mục trong `shared/rules/vi-ai-tells.json` | theo **dấu hiệu**: dấu hiệu này bình thường ở những thể loại nào | trục 4, trục 5 |
| `genre_baseline.normal_signals` ở §5 của hồ sơ thể loại | theo **thể loại**: ở thể loại này những tín hiệu nào là chuẩn | trục 4, trục 5 |

**Luật hợp nhất: phép HỢP, không phải phép giao.** Một tín hiệu được khai ở bất kỳ nguồn nào cũng là
baseline. Hai nguồn tồn tại vì có tín hiệu không thuộc họ dấu hiệu nào (mật độ trích dẫn cao của bài
nghiên cứu chẳng hạn), và có họ dấu hiệu trải trên nhiều thể loại nên khai một lần ở phía dấu hiệu thì
gọn hơn.

Khi soạn hồ sơ mới: **khai ở §5 trước**. Nếu tín hiệu đó ứng đúng một mã dấu hiệu, thêm slug của bạn
vào mục đó trong `vi-ai-tells.json` để hai nguồn không lệch nhau, và ghi tên mã ngay trong
`normal_signals` để người đọc lần ngược được.

### Ba cách viết `normal_signals`, theo thứ tự nên dùng

1. **Ghi thẳng mã dấu hiệu** — `"Cụm dẫn quy ước 'Trước hết', 'Tóm lại' (T23)"`. Đường tường minh, máy
   map thẳng vào cột đo, không phải dò từ khoá. **Ưu tiên cách này.**
2. **Ghi thẳng tên cột đo** — cũng map thẳng.
3. **Chỉ ghi hiện tượng bằng lời** — vẫn hợp lệ, nhưng lúc đó `polish_check.py` phải dò bằng từ khoá,
   và dò từ khoá thì có lúc trượt. Đã có một ca thật: `essay.md` §5 khai "cụm chuyển đoạn", từ khoá
   khớp nhầm sang cột đếm khuôn câu ghép đôi, và nhãn sai đó bảo người sửa bỏ qua đúng cột đang đo thứ
   mà chính §2 cấm sinh ra.

### Luật khớp slug — hai chiều, test canh cả hai

Mọi slug xuất hiện trong `genre_baseline` của `vi-ai-tells.json` **phải** có file
`shared/genres/<slug>.md`. Baseline trỏ tới một thể loại không có hồ sơ thì trục 5 không tìm được §5
để hạ tín hiệu, **và lỗi đó im lặng** — không có gì báo đỏ, chỉ có một người bị báo oan.
`tests/genres/test_genre_schema.py` canh cả hai chiều.

Lưu ý một chỗ trông giống lệch nhưng không lệch: `research` và `de-cuong-nghien-cuu` là **hai slug
khác nhau**. `research.md` là hồ sơ **viết** (đủ §1–§5, có khung `de_cuong` cho trục 2);
`de-cuong-nghien-cuu.md` là hồ sơ **giám định** (`partial`, chỉ §5) và khai riêng thứ mà đề cương
nghiên cứu sinh Việt Nam bắt buộc phải có.

---

## 6. Checklist trước khi coi là xong

- [ ] Tiêu đề `# Hồ sơ thể loại: <tên tiếng Việt>` và một đoạn nói hồ sơ dùng cho ai, kèm luật
      **barem của nhiệm vụ thắng hồ sơ**.
- [ ] Đúng năm heading `## 1.` … `## 5.` (hoặc **chỉ** `## 5.` nếu là `partial`), đúng thứ tự, đúng tên.
- [ ] Mỗi mục có **đúng một** khối YAML, và mở đầu bằng một câu "Trục N đọc mục này để …".
- [ ] Văn xuôi giải thích còn nguyên, không bị lược vì "máy không đọc".
- [ ] Không có code, không có nhánh điều kiện, không mô tả quy trình trong hồ sơ thể loại.
- [ ] `default_structure` là một `id` có thật trong `structures`.
- [ ] `lenses[]` là tập con của danh mục 13 lăng kính ở `_schema.md` mục 3.
- [ ] `tell_families[]` chỉ chứa mã có thật trong `shared/rules/vi-ai-tells.json`.
- [ ] Mọi `verify` của `must_have` là **thao tác kiểm được**, không phải cảm nhận.
- [ ] Slug khớp hai chiều với `genre_baseline` trong `vi-ai-tells.json`.
- [ ] `python -m pytest tests/genres -q` xanh.

---

## 7. Ba lỗi đã gặp thật khi soạn hồ sơ

1. **Dịch chỉ số của người khác mà không hỏi nó có nghĩa trong tiếng Việt không.** `novel.md` kế thừa
   13 chỉ số chất lượng chương truyện từ một khung viết truyện mạng tiếng Trung. Bốn chỉ số bị **bỏ**:
   "số chữ tối thiểu mỗi chương" (đơn vị đếm chữ Hán, và vốn là chỉ tiêu doanh thu nền tảng chứ không
   phải chất lượng văn); "đoạn văn ≤ 200 chữ" (tối ưu cho màn hình điện thoại, giữ lại thì phạt oan
   văn xuôi Việt vốn có đoạn dài); "gạch ngang ≤ 20 lần/chương" (tiếng Việt dùng gạch ngang để dẫn
   lời thoại); "dấu chấm than ≥ 2 lần ở chương hành động" (ép giọng theo một dòng truyện cụ thể).
   Phép thử: *chỉ số này đo chất lượng, hay đo một nền tảng đăng truyện?*

2. **Phạt oan đăng ký ngôn ngữ của một dòng truyện.** Danh sách từ đệm của `novel.md` có "bất giác",
   "khẽ", "trong lòng dâng lên". Với tác giả viết đúng dòng truyện dịch Trung cho độc giả dòng đó, ba
   từ ấy là **chuẩn của dòng truyện**, không phải từ đệm. Cách xử lý: phép kiểm chỉ đếm **mật độ**,
   không cấm từ; và §5 khai thêm một `normal_signals` trỏ về trường `the_loai_phu_da_doc` ở §1.

3. **Ép một khung cấu trúc lên bài không thuộc khung đó.** `research.md` ban đầu chỉ có IMRAD (Đặt vấn
   đề – Phương pháp – Kết quả – Bàn luận). Nhưng rất nhiều bài hội thảo Việt Nam là phân tích chính
   sách hoặc tổng hợp tường thuật — **không có mục Kết quả**. Hồ sơ ép IMRAD thì người chấm phải tự
   diễn dịch, và mọi kết quả sau đó đều là diễn dịch của người chấm. Cách xử lý: thêm một `structures`
   thứ hai, không nới lỏng tiêu chí.

Điểm chung của cả ba: **một hồ sơ thể loại sai sẽ không làm test đỏ.** Nó chỉ lặng lẽ làm người chấm
sai, hoặc làm một người bị báo oan. Đó là lý do §5 viết trước, và là lý do mọi `verify` phải là thao
tác mà người khác kiểm lại được.
