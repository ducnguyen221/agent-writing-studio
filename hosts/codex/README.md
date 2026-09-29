# Dùng agent-writing-studio với Codex

Codex (CLI và ứng dụng desktop) có hai đường, chọn **một**:

## A. Mở thẳng thư mục repo (không cần plugin)

```bash
git clone https://github.com/ducnguyen221/agent-writing-studio
cd agent-writing-studio
python studio.py install --host codex
```

Mở thư mục repo trong Codex (desktop: mở làm project và tin cậy thư mục). Codex đọc
[`AGENTS.md`](../../AGENTS.md) ở gốc repo; bảng *Chọn skill theo việc* trong đó dẫn agent tới đúng
`skills/<trục>/SKILL.md`. Muốn chạy đúng một bước, bảo agent: *"đọc `commands/03-critique.md` rồi
làm theo"*.

## B. Cài plugin

Repo có manifest [`.codex-plugin/plugin.json`](../../.codex-plugin/plugin.json) (`skills: ./skills/`).
Lệnh plugin của Codex khác nhau theo phiên bản — xem `codex plugin --help` trên máy bạn, thêm
marketplace từ `ducnguyen221/agent-writing-studio` rồi cài plugin `agent-writing-studio`. Codex chưa
nạp lệnh `commands/` như Claude Code; gọi lệnh bằng cách bảo agent đọc file lệnh như đường A.

## Lưu ý

- Sandbox của Codex có thể chặn ghi ra ngoài thư mục đang mở. Workspace mặc định `workspace/` nằm trong
  thư mục repo nên không vướng; đặt station `WRITING_STUDIO_DATA` ngoài repo thì có thể phải duyệt quyền.
- Kiểm máy: `python studio.py doctor`. Dòng `host:codex` là `NOT_CHECKED` — doctor không đọc cấu hình
  Codex; kiểm plugin bằng lệnh plugin của Codex.
- Cập nhật đường A: `python studio.py update --yes` (chỉ `git pull --ff-only`, từ chối khi có sửa dở).
