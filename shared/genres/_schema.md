# Schema hồ sơ thể loại

File này là **hợp đồng** giữa dữ liệu thể loại và bốn skill viết. Mọi file `shared/genres/<slug>.md`
phải theo đúng cấu trúc dưới đây; `tests/genres/test_genre_schema.py` kiểm tự động.

Nguyên tắc một câu: **thể loại là dữ liệu, skill là logic.** Hồ sơ thể loại khai *chọn lăng kính nào,
tiêu chí gì, cấm gì, bảo vệ gì*. Skill sở hữu quy trình và danh mục lăng kính. Không skill nào được
viết `if genre == "novel"`; thêm thể loại mới là thêm một file `.md`, không sửa code.

---

## 1. Hình dạng file

Mỗi hồ sơ mở đầu bằng tiêu đề `# Hồ sơ thể loại: <tên tiếng Việt>` và một đoạn nói rõ hồ sơ dùng cho
ai, kèm luật "barem của nhiệm vụ thắng hồ sơ". Sau đó là năm mục.

Luật cứng:

- Đúng năm heading `## 1.` … `## 5.`, đúng thứ tự, đúng tên như bảng mục 2.
- Mỗi mục có **đúng một** khối YAML rào bằng ba dấu huyền kèm nhãn `yaml`. Văn xuôi giải thích nằm
  ngoài khối YAML và không được lược bỏ — người soạn thể loại đọc văn xuôi, máy đọc YAML.
- Không có code, không có nhánh điều kiện, không mô tả quy trình trong hồ sơ thể loại.

### Hồ sơ đầy đủ và hồ sơ một phần

| Trạng thái | Nhận biết | Dùng được cho |
|---|---|---|
| `full` | có cả `## 1.` … `## 5.` | cả năm trục |
| `partial` | **chỉ có** `## 5.` | riêng trục 5 (giám định) — dùng khi thể loại đã phải giám định thật nhưng chưa tới lượt soạn phần viết |

Không có tổ hợp nào khác hợp lệ. File có `## 3.` mà thiếu `## 1.` là lỗi, không phải "một phần".

---

## 2. Khoá bắt buộc từng mục

### §1 · Intent và bối cảnh — trục 1 (`01-context-architect`) đọc

Trục 1 phỏng vấn người dùng cho tới khi trả lời hết `intent_questions`, dựng chân dung độc giả theo
`audience_fields`, rồi xuất `context.json`. Nếu còn điều kiện trong `stop_if_missing` chưa gỡ được,
trục 1 **dừng và hỏi**, không chuyển sang trục 2.

| Khoá | Kiểu | Nghĩa |
|---|---|---|
| `required_inputs` | list[str] | Thứ thiếu là chưa được viết: đề bài, barem, người chấm, hạn nộp… |
| `intent_questions` | list[str] | Câu hỏi trục 1 phải trả lời được và ghi vào `context.json` |
| `audience_fields` | list[str] | Trường chân dung độc giả bắt buộc cho thể loại này |
| `stop_if_missing` | list[str] | Điều kiện dừng, viết ở dạng khẳng định kiểm được |

Ví dụ ngắn (bài luận):

    required_inputs: [de_bai, barem, gioi_han_tu]
    intent_questions:
      - "Luận đề viết lại thành một câu phản biện được là gì?"
    audience_fields: [vai_tro, tieu_chi_cham, muc_do_quen_chu_de]
    stop_if_missing:
      - "Không viết lại được luận đề thành một câu có thể bị phản bác"

### §2 · Khung viết — trục 2 (`02-cowriter`) đọc

Trục 2 chọn một `structures[]` (mặc định `default_structure`), duyệt outline đủ `outline_depth` tầng
rồi mới viết prose, và **cấm ngay khi sinh** các khuôn trong `anti_llm_defaults`.

| Khoá | Kiểu | Nghĩa |
|---|---|---|
| `structures` | list[{`id`, `parts`}] | Các khung có tên: PEEL, IMRAD, tháp ngược, ba hồi… |
| `default_structure` | str | Phải là một `id` trong `structures` |
| `anti_llm_defaults` | list[str] | Khuôn chuyển đoạn / mở bài / kết bài bị cấm ngay từ bản nháp đầu |
| `outline_depth` | int ≥ 1 | Số tầng outline phải duyệt xong trước khi viết prose |
| `outline_layers` | list[str] | Nghĩa của từng tầng, đúng `outline_depth` mục, xếp từ tầng một |

**Trục 2 sở hữu SỐ tầng và cổng duyệt; hồ sơ thể loại sở hữu NGHĨA của từng tầng.** Bài luận đi luận
đề → đoạn → bằng chứng, tiểu thuyết đi hồi → chương → cảnh, bài báo đi khối thông tin → nguồn gắn cho
từng khối. Skill không được đóng cứng một trong ba: viết `outline_layers` vào hồ sơ, không viết vào
SKILL.md.

`anti_llm_defaults` là **cấm khi sinh**, khác với `tell_families` ở §4 là **sửa khi biên tập**. Cấm
sớm rẻ hơn sửa muộn, và tránh vòng lặp "máy sinh khuôn rồi máy tự khen đã xoá khuôn".

### §3 · Rubric chất lượng — trục 3 (`03-critique`) đọc

Trục 3 chấm **riêng từng** `criteria[]` (không cộng gộp mù), chạy đúng các `lenses[]` được bật, và
xuất `critique.json` theo `shared/schemas/critique.schema.json`.

| Khoá | Kiểu | Nghĩa |
|---|---|---|
| `criteria` | list[{`id`, `name`, `evidence`, `question`}] | `evidence` = bằng chứng cần trưng ra; `question` = câu hỏi người chấm phải trả lời |
| `lenses` | list[str] | Tập con của danh mục lăng kính (mục 3 dưới) |
| `blind_referee` | bool | `true` = người chấm không được xem `draft.meta.json` hay câu hỏi mớm trước khi chấm xong |

Hai thể loại khác nhau xuất **cùng** một schema `critique.json`; chỉ nội dung `criteria_scores` và
`lenses_run` khác nhau. Đó chính là ranh giới dữ liệu/logic.

### §4 · Quy tắc biên tập — trục 4 (`04-humanizer`) đọc

Trục 4 chỉ được dùng các phép trong `moves_allowed`, tuyệt đối không đụng vùng `preserve`, và chỉ
soi các họ tell liệt kê ở `tell_families`.

| Khoá | Kiểu | Nghĩa |
|---|---|---|
| `preserve` | list[str] | Vùng cấm sửa: số liệu, trích dẫn, tên riêng, thuật ngữ, hội thoại nhân vật… |
| `moves_allowed` | list[str] | Phép biên tập được dùng |
| `moves_forbidden` | list[str] | Phép bị cấm cho riêng thể loại này |
| `tell_families` | list[str] | `id` trong `shared/rules/vi-ai-tells.json` áp cho thể loại này |
| `voice_priority` | list[str] | Thứ tự thắng khi mâu thuẫn; `writer_profile` luôn đứng trước `genre_default` |

`voice_priority: [writer_profile, genre_default]` là luật "bài mẫu của người viết thắng mọi rule
style". Nếu writer profile ghi tác giả hay mở đoạn bằng câu hỏi, trục 4 không được xoá thói quen đó.

### §5 · Must-have cho forensics — trục 5 (`05-forensics`) đọc; trục 2 và 3 dùng lại

Trục 5 **tiền đăng ký** `must_have[]` trước khi đọc bài, và dùng `genre_baseline.normal_signals` để
**hạ** tín hiệu, không bao giờ để tạo thêm nghi vấn.

| Khoá | Kiểu | Nghĩa |
|---|---|---|
| `must_have` | list[{`level`, `statement`, `verify`}] | `level ∈ {core, minor}`; `verify` = cách kiểm cụ thể |
| `genre_baseline` | {`normal_signals`: list[str]} | Tín hiệu là **bình thường** ở thể loại này → hạ, không phạt |

`genre_baseline` là hàng rào chống báo oan quan trọng nhất trong repo. Văn hành chính Việt Nam vốn
công thức: mục "kết quả – tồn tại – phương hướng" và bộ ba song hành là văn phong **được dạy trong
trường**, không phải dấu vết máy. Xem `skills/05-forensics/references/03-chong-bao-oan.md` §2 và §6.

Thiếu một `must_have` là dấu hiệu về **năng lực thể loại**, không tự nó chứng minh nguồn gốc AI.

---

## 3. Danh mục lăng kính

`lenses[]` ở §3 chỉ được lấy từ danh mục dưới. Danh mục là tài sản của trục 3; hồ sơ thể loại chỉ
**bật/tắt**, không định nghĩa lăng kính mới. Bản đầy đủ (đầu vào · câu hỏi · bằng chứng cần) sẽ nằm
ở `skills/03-critique/references/01-lang-kinh.md`; trước khi file đó tồn tại, test giữ danh mục này.

| Lăng kính | Soi cái gì |
|---|---|
| `fallacy_scan` | 13 loại ngụy biện |
| `claim_check` | mỗi khẳng định có bằng chứng ở mức nào |
| `task_response` | bài có trả lời đúng đề bài không |
| `source_reliability` | nguồn có đủ tin cậy cho mức khẳng định không |
| `source_independence` | các nguồn có độc lập nhau không |
| `balance_check` | các bên liên quan có được nêu không |
| `method_rigor` | phương pháp có đỡ nổi kết luận không |
| `plot_consistency` | tình tiết có mâu thuẫn nhau không |
| `character_consistency` | nhân vật có làm điều đã bị loại trừ trước đó không |
| `pacing_curve` | nhịp thắt/mở có chỗ chùng dài không |
| `three_chapter_selfcheck` | ba chương gần nhất có tự mâu thuẫn không |
| `value_density` | mỗi đoạn có thêm thông tin mới không |
| `retention` | người đọc bỏ đọc ở đâu |

---

## 4. Soạn một thể loại mới

1. Bắt đầu từ **§5**: liệt kê 2–4 `must_have` và `genre_baseline`. Đây là mục ít mang định kiến nhất.
2. Rồi **§3**: chấm cái gì, bằng chứng nào, lăng kính nào.
3. Rồi **§2** → **§1** → **§4**. §4 viết cuối vì nó phụ thuộc vùng `preserve` do §3 và §5 quyết định.
4. Mỗi mục mở đầu bằng một câu "Trục N đọc mục này để …".
5. Chạy `python -m pytest tests/genres -q`.

---

## 5. Hai nguồn `genre_baseline` và luật khớp slug

Tín hiệu "bình thường ở thể loại này" được khai ở **hai chỗ**, và đó là cố ý:

| Nguồn | Khai theo | Ai đọc |
|---|---|---|
| `genre_baseline[]` của từng mục trong `shared/rules/vi-ai-tells.json` | theo **tell**: họ tín hiệu này bình thường ở những thể loại nào | trục 4 (`polish_check.py`), trục 5 |
| `genre_baseline.normal_signals` ở §5 hồ sơ thể loại | theo **thể loại**: ở thể loại này những tín hiệu nào là chuẩn | trục 4, trục 5 |

**Luật hợp nhất: phép HỢP, không phải phép giao.** Một tín hiệu được khai ở bất kỳ nguồn nào cũng là
baseline. Lý do có hai nguồn: một số tín hiệu không phải họ tell nào cả (mật độ trích dẫn cao của bài
nghiên cứu), và một số họ tell trải trên nhiều thể loại nên khai ở phía tell gọn hơn. Khi soạn hồ sơ
mới, khai ở §5 trước; nếu tín hiệu đó ứng đúng một mục tell thì thêm slug vào mục tell ấy để hai
nguồn không lệch nhau, và ghi tên tell trong `normal_signals` để người đọc lần ngược được.

**Luật khớp slug:** mọi slug xuất hiện trong `genre_baseline` của `vi-ai-tells.json` **phải** có file
`shared/genres/<slug>.md`. Baseline trỏ tới một thể loại không có hồ sơ thì trục 5 không tìm được §5
để hạ tín hiệu, và lỗi đó im lặng. `tests/genres/test_genre_schema.py` canh cả hai chiều.

**`research` và `de-cuong-nghien-cuu` là hai slug khác nhau, không phải một chỗ lệch.** `research.md`
là hồ sơ **viết** (đủ §1–§5, có `structures[].id = de_cuong` cho trục 2);
`de-cuong-nghien-cuu.md` là hồ sơ **giám định** (`partial`, chỉ §5) và khai riêng thứ đề cương nghiên
cứu sinh Việt Nam bắt buộc phải có — khoảng trống nghiên cứu nêu đích danh tác giả đi trước. Trục 5
đọc hồ sơ `partial` khi bài được khai đúng thể loại đó; trục 1–4 không đọc file `partial` nào.
