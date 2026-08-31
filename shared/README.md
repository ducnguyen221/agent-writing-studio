# `shared/` — dữ liệu dùng chung của năm trục

Năm skill ở `skills/` là **cách làm**. Thư mục này là **thứ chúng đọc**. Tách ra vì nhiều trục cùng
cần một nguồn: kỳ vọng thể loại của người chấm (trục 3) và của người giám định (trục 5) mà nằm ở hai
chỗ thì chúng sẽ trôi xa nhau, mỗi nơi một kiểu.

| Thư mục | Là gì |
|---|---|
| `genres/` | **Hồ sơ thể loại** — 9 file, mỗi thể loại một file, mỗi file đúng năm mục đánh số. Trục *N* đọc mục §*N*. Đây là nơi bạn sửa khi muốn đổi cách chấm hay cách viết một thể loại. |
| `rules/` | **Danh mục tín hiệu** dạng máy đọc được: 33 dấu hiệu tiếng Việt (mỗi dấu hiệu kèm ví dụ **và** một câu người hoàn toàn hợp lệ chứa đúng dấu hiệu đó), cùng bảng chấm điểm. |
| `schemas/` | **Hợp đồng hình dạng file** — 5 schema JSON cho `context` · `draft` · `critique` · `polish` · `provenance`. Chúng bảo đảm bước sau đọc được đúng thứ bước trước ghi ra. |
| `scripts/` | **Lớp kiểm chứng** — script Python đo và đối chiếu: câu tự khai có khớp văn bản không, bản sửa có chạm vùng cấm không, xuất bản giao ra `.docx`. |
| `writers/` | Chỗ **khai hồ sơ giọng** người viết: chỉ có schema và hướng dẫn. |

## Hai điều dễ hiểu nhầm

**Script không phải bộ não.** Agent vẫn đọc, vẫn chấm, vẫn báo cáo được khi không cài thư viện Python
nào — script chỉ là lớp kiểm chứng đứng sau, để những gì agent nói còn có chỗ đối chiếu bằng máy.

**`writers/` không chứa người thật.** Hồ sơ giọng, bài mẫu, các ca chạy, corpus hiệu chuẩn — tất cả
nằm ở **station** riêng ngoài repo, trỏ bằng biến môi trường `WRITING_STUDIO_DATA`. Trong repo chỉ có
`writer.schema.json`, `audience.schema.json` và [hướng dẫn khai hồ sơ](writers/README.md). Đó là quy
tắc cứng: dữ liệu định danh cá nhân không đi vào git.

Muốn soạn một hồ sơ thể loại mới: [`docs/GENRES.md`](../docs/GENRES.md).
Muốn hiểu ai đọc dữ liệu của ai: [`docs/KIEN-TRUC.md`](../docs/KIEN-TRUC.md).
