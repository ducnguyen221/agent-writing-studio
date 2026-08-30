# Quy trình hai lượt

Chưng cất từ `blader/humanizer` (MIT, pin ở `vendor-notes/humanizer/SOURCES.md`). Lấy **quy trình và
hàng rào**, không lấy một câu ví dụ nào của bản gốc. Mọi ví dụ dưới đây tự soạn bằng tiếng Việt.

---

## 0. Trước khi sửa: điều kiện khởi động

Trục 4 **không chạy trên một văn bản không rõ nguồn gốc**. Phải có một trong hai:

- `draft.meta.json` do trục 2 sinh, có `machine_written_spans[]`; hoặc
- người dùng tự khai bằng lời: bài này tôi viết, bài này tôi nhờ mô hình viết rồi sửa, bài này của
  học viên và tôi được phép biên tập.

Ghi vào `source_declared.how` của `polish.diff.json` là `draft_meta` hay `user_declared`. Không có
khai báo thì dừng và hỏi — biên tập một bài không biết của ai là chỉnh sửa bài người khác.

Đọc thêm, theo đúng thứ tự: `§4` của hồ sơ thể loại (`shared/genres/<genre>.md`) → writer profile nếu
có → cột `fix` của những `tell_families` mà `§4` bật trong `shared/rules/vi-ai-tells.json`.

**Không mở điểm trục 5 của chính bài đang sửa.** Xem điểm rồi sửa cho điểm đẹp lên là tối ưu theo
thước đo, không phải biên tập. Trường `metadata.forensics_score_seen` phải là `false`.

---

## 1. Lượt một — viết lại theo nghĩa, không vá theo cờ

Lượt một **không giữ cấu trúc cố định**. Được gộp hai đoạn rời rạc thành một, tách một đoạn ôm ba ý
thành hai, đổi thứ tự câu trong đoạn, viết lại cả đoạn quanh ý chính của nó.

Đây là hàng rào chống Goodhart, không phải quyền tự do. Lý do: nếu chỉ được vá đúng những cụm bị đếm,
người sửa sẽ đi tìm cách làm cho counter tụt xuống thay vì làm cho đoạn văn nói đúng hơn. Vá từng cụm
sinh ra văn lai — câu đã hết cụm đệm nhưng vẫn không nói gì.

Cách làm trong một đoạn:

1. Đọc cả đoạn, viết ra **một câu** nói đoạn này để làm gì.
2. Nếu không viết nổi câu đó: đoạn rỗng. Đừng sửa câu chữ — báo lên như một finding nội dung, để tác
   giả bổ sung. Trục 4 không có quyền phát minh nội dung thay tác giả.
3. Viết nổi câu đó: sửa để đoạn phục vụ đúng câu đó, dùng các phép trong `moves_allowed` của `§4`.

Ví dụ (tự soạn):

> **Trước:** "Việc ứng dụng công nghệ số trong quản lý đóng vai trò quan trọng, góp phần nâng cao
> hiệu quả công tác điều hành của nhà trường trong bối cảnh hiện nay."
> **Câu-đoạn-để-làm-gì:** nói phần mềm mới rút ngắn thời gian duyệt đơn.
> **Sau:** "Từ tháng 3/2026, nhà trường duyệt đơn nghỉ học trên phần mềm thay vì trên giấy. Thời gian
> duyệt một đơn giảm từ hai ngày xuống nửa ngày."

Chú ý: bản sau **không thêm fact**. Con số "hai ngày xuống nửa ngày" chỉ được viết nếu tác giả đã nói
ở chỗ khác trong bài hoặc trong ngữ cảnh. Nếu tác giả chưa có số, bản sau dừng ở câu thứ nhất và phần
còn lại vào danh sách "chỗ cần tác giả bổ sung".

---

## 2. Hai câu hỏi kiểm — bắt buộc, không được bỏ

Sau lượt một, đọc lại bản mới và trả lời **thành văn** hai câu:

**Câu 1 — "Còn chỗ nào nghe như máy?"**
Không hỏi "còn tell nào chưa gạch". Hỏi: chỗ nào người đọc thật sẽ dừng lại vì câu văn không do ai cụ
thể nói ra? Thường là: câu không có chủ thể hành động, câu khen mà không kiểm được, câu chuyển đoạn
báo trước điều mục tiếp theo sẽ nói, câu kết hứa hẹn không có người chịu trách nhiệm.

**Câu 2 — "Tôi đã thêm hoặc bớt fact, tên, số, ngày, trích dẫn nào?"**
Trả lời bằng cách liệt kê, không bằng cách khẳng định "không có". Mọi thứ liệt kê được đưa vào
`facts_added[]` / `facts_removed[]`. Hai mảng này **phải rỗng**; có phần tử là fail-closed: dừng, trả
bản gốc, báo người dùng chỗ nào suýt bị thêm hoặc mất.

**Cách trả lời câu 2 sao cho không tự lừa mình:** liệt kê mọi **số, ngày, tên riêng, nguồn, và
mệnh đề khẳng định** có trong bản sau; với từng mục, chỉ ra nó nằm ở đâu trong bản trước (hoặc ở
đoạn khác của bài, ghi vị trí). Mục nào không chỉ được vị trí → đó là fact vừa thêm, dù câu "nghe
hợp lý". Khoảng trống mà tác giả cần điền không được lấp bằng câu chung chung: nó đi vào
`warnings[]` với tiền tố **"Chỗ cần tác giả bổ sung:"**, mỗi chỗ một dòng, nói rõ thiếu gì (ai làm,
mốc nào, việc gì). Bản sau dừng ở câu đã có căn cứ.

Câu 2 là lý do trục 4 an toàn hơn "viết lại cho hay". Người biên tập tự tin nhất vẫn hay đánh rơi một
mệnh đề điều kiện, và mệnh đề điều kiện là chỗ nghiên cứu sống hay chết.

---

## 3. Lượt hai — sửa nhỏ, không được mở lại cấu trúc

Lượt hai chỉ làm ba việc:

- Xử lý những chỗ câu 1 nêu tên.
- Thống nhất cách gọi một khái niệm trong toàn bài (chọn một tên, giữ nguyên).
- Kiểm lại `preserve[]` của `§4` — xem `02-vung-bao-ve.md`.

Không gộp/tách đoạn ở lượt hai. Đổi cấu trúc hai lần liên tiếp là dấu hiệu người sửa đang mò, và
`polish.diff.json` sẽ không đọc được nữa.

Chạy `scripts/polish_check.py` sau lượt hai. Script là cổng 0-token: nó đếm trước/sau và cảnh báo,
**nó không quyết định bản nào tốt hơn**. Cảnh báo CV độ dài câu tăng vọt nghĩa là bản sửa đang chèn
câu ngắn ngẫu nhiên cho "tự nhiên hơn" — đó là bơm burstiness giả, phải hoàn tác.

---

## 4. Bài mẫu thắng mọi luật

`voice_priority: [writer_profile, genre_default]` ở `§4` mọi thể loại không phải trang trí.

Khi có writer profile (`shared/writers/<slug>/`) hoặc người dùng đưa 1–3 bài cũ của chính họ: **bài
mẫu thắng**. Người viết hay mở câu bằng "Thật ra", hay dùng câu 40 âm tiết, hay lặp một cụm làm nhịp,
hay gọi "học sinh" chứ không gọi "người học" — giữ nguyên, kể cả khi một mục trong `vi-ai-tells.json`
nói ngược lại. Danh mục tell là mặc định khi chưa biết gì về người viết; biết rồi thì nó nhường.

Không có profile mà cũng không có bài mẫu: giữ những đặc điểm lặp lại **trong chính bản thảo** — đó
là bằng chứng gần nhất về giọng của tác giả.

---

## 5. Ba chế độ trả kết quả

Hỏi người dùng muốn nhận kiểu nào; mặc định là chế độ 2.

| Chế độ | Trả gì | Dùng khi |
|---|---|---|
| **Dán thẳng** | Bản đã sửa in ra màn hình, kèm bảng các nhát sửa lớn | Đoạn ngắn, sửa nhanh trong hội thoại |
| **File** | `polished.md` + `polish.diff.json` cạnh bản gốc | Bài dài, cần rà lại từng nhát sửa |
| **Nhúng** | Sửa tại chỗ trong file gốc, giữ nguyên frontmatter, code block và định dạng | Bài đã nằm trong repo hoặc trong vault |

Cả ba chế độ đều **bắt buộc** sinh `polish.diff.json` với `metadata.stylometric_polish: true`. Chế độ
"dán thẳng" cũng phải in phần diff ra, không được im lặng.
