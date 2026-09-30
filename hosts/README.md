# Chọn ứng dụng AI để dùng xưởng viết

"Host" là ứng dụng chạy AI agent. Cách dễ nhất: dán prompt trong
[`INSTALL.md`](../INSTALL.md#prompt-copy-dán) vào ứng dụng bạn đang dùng, agent tự chọn đúng đường.

| Bạn dùng | Đường cài | Có gì | Hướng dẫn |
|---|---|---|---|
| Claude Code (terminal, IDE, tab Code của ứng dụng Claude) | plugin | 9 skill + 7 lệnh `/agent-writing-studio:*` | [Claude Code](claude/README.md) |
| Codex (CLI và desktop) | plugin, hoặc mở thư mục repo | 9 skill; lệnh đọc từ `commands/` | [Codex](codex/README.md) |
| Google Antigravity | mở thư mục repo | skill theo bảng chọn trong `AGENTS.md` | [Antigravity](antigravity/README.md) |
| Claude Desktop (tab chat) | — | chưa hỗ trợ: tab chat không nạp skill từ repo | [Claude Desktop](claude-desktop/README.md) |

Mọi host dùng **cùng một nguồn**: `skills/`, `commands/`, `shared/` trong repo (plugin mang nguyên cây
repo). Không chép skill bằng tay sang thư mục của host — hai bản sẽ trôi khỏi nhau.

**Chọn một đường cho mỗi host.** Đã cài plugin mà vẫn mở thư mục repo thì host có thể thấy cùng một
skill hai lần (bản plugin và bản đọc qua `AGENTS.md`); không hỏng gì, nhưng dễ gọi nhầm bản cũ khi
plugin chưa cập nhật. `python studio.py doctor` (macOS: `python3.12 studio.py doctor`) báo phiên bản
plugin Claude Code đang cài.

Dữ liệu các ca viết ở `workspace/` trong thư mục bạn mở (Git bỏ qua), hoặc ở station
`WRITING_STUDIO_DATA` nếu bạn đặt — như nhau cho mọi host. Chạy được trên Windows và macOS.
