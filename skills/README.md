# `skills/` — năm trục của xưởng viết

Đây là thứ bạn chép sang chỗ agent tìm skill (`~/.claude/skills/`, `~/.codex/skills/`). Mỗi thư mục
là **một giai đoạn** của việc viết, và agent tự nạp khi gặp đúng tình huống — bạn không phải gọi tên.

| Thư mục | Trục | Làm gì |
|---|---|---|
| `01-context-architect/` | Y1 | Hỏi cho ra đề bài, luận đề, ai đọc, ai chấm. Chưa rõ thì **dừng, không viết**. |
| `02-cowriter/` | Y2 | Dàn ý ba tầng → chờ bạn duyệt → viết văn xuôi, kèm bản tự khai câu nào máy viết. |
| `03-critique/` | Y3 | Chấm từng tiêu chí theo barem thể loại, có câu trích làm bằng. Không có điểm tổng. |
| `04-humanizer/` | Y4 | Sửa văn về phía giọng tác giả. Cấm đụng số liệu, cấm đổi mức mạnh của khẳng định. |
| `05-forensics/` | Y5 | Đọc bài, chỉ chỗ có dấu hiệu máy viết, kèm phản chứng và câu hỏi xác minh. |

`ls` ra **năm thư mục — một thư mục một trục**. Nhưng trục 5 nặng hơn bốn trục kia nên nó được chia
thành **bốn skill con** nằm ngay bên trong nó, và mọi đường vào đều đi qua router `05-forensics/SKILL.md`:

- `05a-reading/` — đọc mù, gán nhãn từng câu;
- `05b-scoring/` — tính hai con số S và C, **sau khi** bản đọc đã khoá;
- `05c-reporting/` — viết báo cáo tiếng Việt: vị trí, cách sửa, câu hỏi để hỏi lại tác giả;
- `05d-calibration/` — dựng bộ bài mẫu, đo tỷ lệ báo oan, chỉnh ngưỡng.

Vậy là **chín skill trong năm thư mục**.

## Điều quan trọng nhất về cách chúng hoạt động

Không skill nào biết trước bạn đang viết thể loại gì. Kiến thức thể loại nằm ở **dữ liệu**, tại
`shared/genres/<thể-loại>.md` — mỗi hồ sơ có đúng năm mục đánh số, và **trục *N* đọc mục §*N*** của
hồ sơ đó. Trục 3 chấm bài luận thì đọc §3 của `essay.md`; chấm chương tiểu thuyết thì đọc §3 của
`novel.md`. Cùng một quy trình, khác bộ tiêu chí.

Nên: thêm một thể loại mới = thêm **một file** trong `shared/genres/`, không sửa skill nào cả.

Bên trong mỗi thư mục skill: `SKILL.md` là bản ngắn agent luôn đọc; `references/` là các tài liệu dài
chỉ nạp khi cần; `scripts/` và `assets/` là phần máy chạy được. Chi tiết vì sao chia như vậy:
[`docs/KIEN-TRUC.md`](../docs/KIEN-TRUC.md).
