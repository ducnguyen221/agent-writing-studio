# Hướng dẫn dùng: một ca đi trọn năm trục

[English](GUIDE.md) · **Tiếng Việt**

Trang này đi cùng bạn qua **một bài viết từ đầu đến cuối**: dựng bối cảnh → viết nháp → phản biện →
biên tập → giao bản Word → giám định. Chưa cài thì xem [`INSTALL.md`](INSTALL.md); muốn thử mười phút
trước với bài mẫu có sẵn thì xem [`START-HERE.md`](START-HERE.md).

Bạn **nói tiếng Việt bình thường** với agent; agent tự chọn trục. Mỗi bước dưới đây ghi cả câu nói mẫu
lẫn lệnh chạy lẻ tương đương (`/agent-writing-studio:<lệnh>` trong Claude Code; host khác thì bảo agent
*"đọc `commands/<lệnh>.md` rồi làm theo"*).

## 0. Thư mục ca

Mỗi bài một **thư mục ca**, đặt tên ngắn không dấu, ví dụ `bai-luan-ai`. Nó nằm ở:

- `workspace/bai-luan-ai/` trong thư mục bạn mở — mặc định, không cần cấu hình, Git bỏ qua;
- hoặc `$WRITING_STUDIO_DATA/work/bai-luan-ai/` nếu bạn đã đặt station riêng.

Năm trục nói chuyện với nhau **bằng file trong thư mục này**, không bằng trí nhớ hội thoại — nên bạn có
thể dừng giữa chừng, mở phiên mới hôm sau, hoặc đổi sang host khác mà không mất gì.

## 1. Bối cảnh — `01-context` (trục Y1)

> *"Tôi cần viết một bài luận về việc dùng AI khi làm bài tập về nhà, cho giảng viên chấm. Dựng bối
> cảnh giúp tôi trước đã. Ca tên `bai-luan-ai`."*

Agent phỏng vấn: đề bài thật là gì, luận đề của bạn, ai đọc, ai chấm theo barem nào, bằng chứng nào đang
có trong tay. Nó đọc mục §1 của hồ sơ thể loại (`shared/genres/essay.md`). Có kho tri thức cá nhân
(`WRITING_STUDIO_KNOWLEDGE`) thì nó **trỏ** tới tài liệu liên quan, không chép.

**Ra:** `context.json`. **Cổng:** còn câu hỏi chưa gỡ thì agent **dừng và hỏi**, không sang bước 2.

## 2. Viết nháp — `02-draft` (trục Y2)

> *"Đã có `context.json` ở ca `bai-luan-ai`. Dựng dàn ý rồi viết nháp."*

Agent dựng **dàn ý ba tầng** và **chờ bạn duyệt**. Bạn sửa dàn ý bao nhiêu lần tuỳ ý; chỉ khi bạn đồng
ý nó mới viết văn xuôi. Mọi câu máy viết được khai trong `draft.meta.json` — đó là bản tự khai nguồn
gốc, sẽ đi theo bài tới tận bản giao.

**Ra:** `draft.md`, `draft.meta.json`, `sentences.json` (hệ đánh số câu dùng chung cho các bước sau).

## 3. Phản biện — `03-critique` (trục Y3)

> *"Chấm bản nháp ca `bai-luan-ai` theo hồ sơ `essay`, chỉ chỗ lập luận hổng."*

Agent chấm **từng tiêu chí riêng** theo barem ở mục §3 của hồ sơ thể loại, soi ngụy biện, rà dẫn nguồn,
và trích đúng câu làm bằng chứng. **Không có điểm tổng.** Danh sách `must_fix[]` ghi việc nào của ai —
bạn sửa, hay trục 4 sửa.

**Ra:** `critique.json`. Bạn tự sửa nội dung (lập luận, bằng chứng) ở bước này; trục 4 không làm thay.

## 4. Biên tập — `04-humanize` (trục Y4)

> *"Biên tập bản nháp ca `bai-luan-ai` về phía giọng của tôi, giữ nguyên số liệu và trích dẫn."*

Agent sửa văn về phía **giọng của chính bạn** (theo hồ sơ giọng nếu có), trong khi cấm thêm hay bớt dữ
kiện và cấm đổi mức mạnh của khẳng định. Ba chế độ đầu ra: dán-text (in tín hiệu → bản sửa → diff), file
(ghi file đích + diff cạnh nó), nhúng-trong-task. **Cổng:** lỡ thêm hay bớt một dữ kiện → trả lại bản gốc.

**Ra:** `polished.md`, `polish.diff.json` (từng nhát sửa), `polished.provenance.json` (đi kèm bản giao).

## 5. Giao bản Word — `deliver-docx`

> *"Giao bản docx của ca `bai-luan-ai` vào thư mục D:/bai-nop."*

Bản giao mặc định là `.docx` theo quy cách văn bản Việt (Times New Roman 13, giãn dòng 1,5, lề 2/2/3/2
cm), ghi **đúng vào thư mục bạn chỉ**, kèm file provenance đặt cạnh. Cần `python-docx`; thiếu thì agent
báo đúng câu lệnh cài. Bảng Markdown chưa dựng thành bảng Word — bài có bảng thì dựng trong Word sau.

## 6. Giám định — `05-audit` (trục Y5)

> *"Giám định ca `bai-luan-ai`."*

Với văn đi qua chính xưởng, mặc định là chế độ **`audit`**: đọc mù trước, khoá kết quả, rồi mới đối chiếu
bản tự khai `draft.meta.json` với văn bản — câu hỏi đúng là *bản tự khai có khớp không*, không phải *máy
có đoán ra không*. Chế độ **`blind`** (thêm `--blind`) dành cho tài liệu từ ngoài không có bản tự khai,
hoặc để hiệu chuẩn.

**Ra:** `evidence.json`, `report.md` — mỗi nhận định kèm phản chứng và câu hỏi xác minh. **Không đầu ra
nào đủ để kết tội ai**; lý do ở [README mục 5](README.vi.md#5-ranh-giới-đạo-đức--phần-quan-trọng-nhất-của-repo-này).

## Mẹo và giới hạn

- **Không phải lúc nào cũng chạy đủ năm trục.** Chấm bài của người khác: chỉ trục 3 (hoặc 5). Có sẵn bản
  nháp của mình: bắt đầu từ trục 3.
- **Thiếu file của bước trước** thì lệnh nói rõ thiếu gì và lệnh nào sinh ra nó — nó không tự chạy lại
  cả chuỗi.
- **Thể loại** có sẵn: `essay`, `research`, `blog`, `journalism`, `novel` (đủ năm trục); `commentary`,
  `thesis-proposal`, `internship-report`, `teaching-initiative` (chỉ trục 5). Thêm thể loại: [`docs/GENRES.md`](docs/GENRES.md).
- **Có trục trặc:** `python studio.py doctor` (macOS: `python3.12`), rồi [`docs/troubleshooting.md`](docs/troubleshooting.md).
- Xem mọi lệnh bất cứ lúc nào: `/agent-writing-studio:list`.
