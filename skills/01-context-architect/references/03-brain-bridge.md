# Cầu Brain — luật con trỏ

Trục 1 **đọc** kho tri thức cá nhân và thư mục dự án để dựng bối cảnh, nhưng **không copy nội dung**
vào repo. `context.json` chỉ ghi **con trỏ**: đường dẫn, một đoạn trích ngắn, và lý do liên quan.
Nguồn luật: `docs/ARCHITECTURE.md` §2.3.

Ba lý do, mỗi lý do đủ mạnh một mình:

1. **Một fact, một nơi canonical.** Chép sang đây là đẻ ra bản sao thứ hai sẽ lệch với bản gốc.
2. **Riêng tư.** Kho cá nhân có thứ không được vào một repo có thể công khai — và `context.json`
   nằm trong thư mục ca, thứ đi qua tay nhiều công cụ.
3. **Bản quyền.** Tài liệu trong kho thường không phải của người dùng.

## Tìm Brain ở đâu

Gốc kho tri thức đọc từ biến môi trường `WRITING_STUDIO_KNOWLEDGE`. Máy dựng trước bản 0.3.0 có thể chỉ có
tên biến cũ `OPCOS_BRAIN_PATH` — đọc nó làm **đường lùi** khi `WRITING_STUDIO_KNOWLEDGE` chưa đặt (tên cũ sẽ bỏ ở
0.4). Không biến nào được đặt thì **không có kho tri thức**: không đoán một thư mục nào trong home.
**Không hardcode đường dẫn tuyệt đối nào trong skill.** Ngoài kho tri thức, đọc cả thư mục dự án hiện
hành — bối cảnh gần bài viết nhất thường nằm ở đó.

Không có kho tri thức trên máy là chuyện bình thường: `brain_pointers[]` để rỗng và đi tiếp. Không có kho
tri thức không phải lý do dừng phỏng vấn.

## Vùng cấm — không đọc, không trỏ

Kho cá nhân không phải một thư mục đồng nhất. **Không trỏ vào** — và không đọc để lấy trích:

- **tài chính** (thu nhập, hợp đồng, giá, sổ sách, đầu tư);
- **sức khoẻ** (bệnh án, thuốc, kết quả xét nghiệm, sức khoẻ người thân);
- **đời tư** (nhật ký, quan hệ, chuyện gia đình, ảnh riêng);
- **bí mật của bên thứ ba** (thông tin khách hàng, dữ liệu học viên, tài liệu nội bộ có dấu mật);
- **thứ có secret** (`.env*`, token, khoá, credential) — kể cả khi bài đang viết là về kỹ thuật.

Nghi ngờ một tài liệu thuộc vùng cấm thì **hỏi người dùng**, đừng tự phân xử. Người dùng chỉ đích
danh một tài liệu trong vùng cấm thì được trỏ tới nó — chỉ tài liệu đó, và chỉ trong ca đó.

## Ba trường của một con trỏ

Hình dạng ở `shared/schemas/context.schema.json`, mục `brain_pointers[]`:

- **`path`** — đường dẫn **tương đối** tính từ gốc Brain hoặc gốc dự án. Không đường dẫn tuyệt đối:
  `C:\Users\<tên>\...` là thông tin định danh, và nó không chạy được trên máy khác.
- **`excerpt`** — **tối đa 300 ký tự**, schema chặn cứng. Không phải giới hạn để lách bằng cách
  chia một tài liệu thành sáu con trỏ mỗi con 300 ký tự. Ngưỡng đúng: **trích để nhận ra tài liệu**,
  không phải để dùng thay tài liệu. Dài hơn nghĩa là đang copy.
- **`why`** — vì sao tài liệu này liên quan tới **bài đang viết**. Không viết nổi `why` thì con trỏ
  đó không thuộc về đây. Đây là trường hay bị bỏ trống nhất và cũng là trường có giá trị nhất: nó là
  thứ duy nhất giải thích tại sao trục 2 phải mở tài liệu ra đọc.

## Ba lỗ rò mà trần 300 không tự bịt

Trần `excerpt ≤ 300` chỉ chặn **một trường của một con trỏ**. Ba đường khác đưa nguyên văn Brain
vào `context.json` mà schema hiện không chặn — nên phải chặn bằng luật, và Phase 4 đã ghi task đưa
ba con số dưới đây vào `context.schema.json`:

1. **`why` không phải chỗ chứa phần thừa của `excerpt`.** `why` là *lý do liên quan tới bài đang
   viết*, viết bằng lời của trục 1, **≤ 200 ký tự**. Có một câu trích trong `why` là đã rò.
2. **Trần theo tài liệu và theo file, không chỉ theo con trỏ.** Một tài liệu → **tối đa 2 con trỏ**
   (hai đoạn khác nhau của cùng file); cả `context.json` → **tối đa 6 con trỏ** và **tổng `excerpt`
   ≤ 900 ký tự**. Cần nhiều hơn nghĩa là tài liệu ấy phải được *mở ra đọc* ở trục 2, không phải được
   tóm vào đây.
3. **Phỏng vấn là phễu lớn nhất.** `intent.task` chép nguyên văn *lời người dùng*, không phải nguyên
   văn tài liệu người dùng dán vào; tài liệu dán vào thì thành một con trỏ. `answers[].answer` ghi
   *kết luận của người trả lời*, **≤ 600 ký tự**, và không chứa đoạn chép từ Brain — muốn dẫn tài liệu
   thì ghi "xem con trỏ N". Câu trả lời dài hơn 600 gần như chắc chắn đang chứa một đoạn tài liệu.

## Hồ sơ giọng và bài mẫu trong kho tri thức

Hồ sơ giọng đo được (`profile.yaml`), bài mẫu chính chủ và chân dung độc giả dạng máy đọc mang danh
tính người viết, vì vậy **nên** nằm trong kho tri thức cá nhân khi có kho — để dùng lại ngoài xưởng viết.
Không có kho thì chúng ở station (`writers/`, `audiences/`).

**Luật phân giải `writer_profile_ref` (và `profile_used` của `draft.meta.json`).** Đường **tương
đối**, agent tự ghép — cùng cơ chế với `brain_pointers[].path`. Thứ tự: (1) gốc kho tri thức cá nhân
`WRITING_STUDIO_KNOWLEDGE` (đường lùi như mục trên) → (2) gốc station `WRITING_STUDIO_DATA` → (3) gốc repo.
Chuỗi **không chứa `/`** là slug: `writers/<slug>/profile.yaml` ở (2), rồi
`shared/writers/<slug>/profile.yaml` ở (3). `null` = giọng mặc định thể loại. Không bao giờ ghi
đường tuyệt đối.

Hồ sơ giọng là **con trỏ, không phải bản sao**: trục 1 chỉ ghi đường, không copy số đo hay
`voice_notes` vào `context.json`.

**Bài mẫu trong kho tri thức thường có frontmatter YAML.** `profile_build.py --samples-dir <thư mục
bài mẫu> --out <đường profile>` tự bỏ khối frontmatter ở **đầu** file `.md`/`.txt` trước khi đo, nên
mã băm và số đo không phụ thuộc metadata của kho. Vạch `---` giữa thân bài là câu chữ của tác giả,
không bị đụng. Sửa thân bài mẫu thì mã băm trong hồ sơ lệch — đó là tín hiệu, không phải lỗi.

## Phép thử trước khi ghi

1. **Đọc `context.json` một mình, không mở tài liệu gốc — có dùng được nội dung không?** Có nghĩa là
   đã copy quá tay. Con trỏ phải *đòi* người đọc mở tài liệu gốc.
2. **Xoá tài liệu gốc đi thì con trỏ còn giá trị không?** Không. Đúng như vậy — đó là định nghĩa của
   con trỏ.
3. **Trích dẫn này có tên người, số tiền, số điện thoại, địa chỉ, mã số nào không?** Có thì cắt.

## Chiều ngược lại

Kết thúc một ca đáng nhớ, bài học đi **về** kho tri thức theo quy trình reflection chung của máy.
Repo này **không tự đẻ kho tri thức thứ hai**: không thư mục `notes/`, không `learned/`, không file
tổng hợp bối cảnh nằm lại sau khi ca đóng.
