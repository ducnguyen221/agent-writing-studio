# Outline ba tầng — duyệt xong tầng ba mới được viết prose

Phương pháp trong file này thuộc bộ luật của studio; nguồn gốc tri thức ghi ở sổ xưởng (không nằm trong repo). Không chép mã, không chép prompt: ở đây chỉ có
phương pháp.

**Số tầng lẫn nghĩa của từng tầng đều không do file này quyết định.** Trục 2 đọc `outline_depth` và
`outline_layers[]` ở `§2` của hồ sơ thể loại: `outline_depth` cho biết phải duyệt xong bao nhiêu
tầng, `outline_layers[]` cho biết mỗi tầng là gì. Ba tầng mô tả dưới đây là nghĩa của **họ thể loại
lập luận** — `essay.md` và `research.md`, cùng khai `outline_depth: 3`. Thể loại khác khai khác, và
hồ sơ thắng file này: `novel.md` đi hồi → chương → cảnh, `blog.md` và `journalism.md` chỉ hai tầng.
Đọc `outline_layers[]` trước, đừng bê ba tầng dưới đây sang một thể loại không khai như vậy.

---

## 1. Vì sao outline phải xong trước prose

Viết prose trước rồi sửa dàn ý sau là cách rẻ nhất để tự lừa mình. Prose trôi chảy che được một
dàn ý rỗng: câu chuyển đoạn nghe mượt làm hai ý không liên quan trông như có quan hệ nhân quả, và
người viết — kể cả người đọc lại bản của chính mình — không còn thấy chỗ hổng nữa. Đây đúng là ca
mà kịch bản [`03-essay-tron-tru.md`](../../../tests/skills/scenarios/03-essay-tron-tru.md) dựng ra
để thử trục 3: bốn đoạn mượt mà nói lại cùng một điều.

Outline còn là **chỗ duy nhất người dùng can thiệp rẻ**. Sửa một dòng ở tầng hai tốn một phút; sửa
cùng ý đó sau khi đã có 900 chữ tốn một buổi, và thường kết thúc bằng vá víu thay vì viết lại.

## 2. Ba tầng của họ lập luận

### Tầng 1 — luận đề và các ý chính

- **Luận đề** lấy nguyên văn `intent.thesis_one_sentence` trong `context.json`. Trục 2 **không tự
  đặt lại luận đề**; thấy luận đề không phản bác được thì trả về trục 1, không tự sửa.
- **Ý chính**: mỗi ý là một **mệnh đề có thể sai**, không phải một chủ đề. `"Vai trò của dữ liệu"`
  là chủ đề. `"Học viên dùng AI làm bài về nhà vẫn học được, nếu bài kiểm tra chuyển sang khẩu vấn"`
  là mệnh đề — cãi lại được.
- Phép thử của tầng 1: **đảo thứ tự các ý chính**. Đảo mà bài không vỡ thì các ý đang song song
  chứ không đang xây lên nhau; hoặc chấp nhận nó là bài liệt kê và khai rõ, hoặc dựng lại.
- Khung lấy từ `structures[]` ở `§2`; chọn một `id`, ghi vào `draft.meta.json.structure_id`. Không
  có `id` nào vừa thì dùng `default_structure` và ghi lý do, đừng tự chế khung mới.

### Tầng 2 — đoạn

- Mỗi đoạn có **một câu "để làm gì"**: đoạn này làm gì cho ý chính nào. Viết không nổi câu đó thì
  đoạn ấy chưa tồn tại — đừng viết prose cho nó, hãy bỏ hoặc gộp.
- Mỗi đoạn khai **quan hệ thật với đoạn trước**: nối tiếp, đối lập, nhân quả, ví dụ, giới hạn. Ghi
  quan hệ ở tầng này để tầng prose không phải bịa từ nối. Từ nối sai quan hệ là lỗi mà `§3` của
  `essay.md` bắt bằng tiêu chí `cohesion`.
- Mỗi đoạn khai **độ dài dự kiến**. Tổng phải khớp ràng buộc số từ trong `context.json.constraints[]`.
  Vượt ở tầng hai thì cắt ý, đừng cắt bằng cách viết câu ngắn hơn ở tầng ba.

### Tầng 3 — bằng chứng

Tầng này là chỗ dàn ý thường chết, nên nó là tầng cuối cùng phải duyệt.

- Mỗi đoạn ở tầng hai gắn **ít nhất một** thứ đỡ được nó: một con số, một nguồn, một ví dụ cụ thể,
  một trải nghiệm của chính tác giả, hoặc một suy luận được viết ra thành các bước.
- **Chỗ trống ở tầng ba là chỗ trống thật.** Không được lấp bằng prose. Ba đường đi hợp lệ: (a) tìm
  được bằng chứng → điền; (b) không có → hạ mức khẳng định của đoạn cho khớp thứ đang có; (c) không
  hạ được vì đó là ý chính → **dừng, báo người dùng**, ghi vào phần cần bổ sung. Đường thứ tư —
  viết một câu chung chung kiểu "nhiều nghiên cứu đã chỉ ra" — chính là tell `T05` (nguồn mơ hồ).
- **Riêng thể loại nghiên cứu, nguồn phải gắn ngay tại đây, không gắn sau.** `§2` của `research.md`
  khai luật này bằng chữ. Lý do đáng nhắc lại: gắn nguồn sau khi đã viết xong prose thì nguồn được
  chọn vì nó khớp câu đã viết, chứ không phải câu được viết ra vì nguồn nói thế. Kết quả là trích
  dẫn trang trí — đúng thứ mà tiêu chí `citation` ở `§3` của `research.md` trừ điểm.
- Ý của chính tác giả, không có nguồn, **được phép** — nhưng phải đánh dấu là ý của tác giả ngay ở
  tầng ba, để prose không trình bày nó như một phát hiện đã được ai đó chứng minh.

---

## 3. Cổng duyệt

Trục 2 **dừng lại và chờ người dùng** sau khi trình đủ ba tầng. Không có ngoại lệ "viết thử một
đoạn cho dễ hình dung": một đoạn prose đủ hay sẽ khoá luôn dàn ý trong đầu người duyệt.

Trình dàn ý theo đúng ba tầng, kèm ba thứ để người duyệt quyết được:

1. chỗ nào ở tầng ba đang trống, và trống thì đoạn nào sẽ phải hạ mức khẳng định;
2. tổng độ dài dự kiến so với ràng buộc;
3. mục nào trong `context.json.intent.unresolved[]` vẫn chưa gỡ được.

Người dùng duyệt → ghi `outline_approved: true` và `outline_depth_reached` vào `draft.meta.json`
(schema bắt `outline_depth_reached ≥ 1` khi `outline_approved: true`). Chưa duyệt mà vẫn cần một bản
thăm dò thì `outline_approved: false`, và bản đó **không được nộp** — chữ này nằm trong chính
`draft.schema.json`.

## 4. Cái outline này KHÔNG làm

- Không thay `context.json`. Thiếu bối cảnh thì quay lại trục 1.
- Không chấm chất lượng. Chấm là việc của trục 3, sau khi có bản thảo.
- Không giữ nguyên tầng ba khi viết. Prose phát hiện bằng chứng không đỡ nổi đoạn thì **sửa outline
  rồi xin duyệt lại phần đã đổi**, chứ không âm thầm viết khác dàn ý đã duyệt.
