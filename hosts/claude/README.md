# Dùng agent-writing-studio với Claude Code

## Cài plugin (khuyến nghị)

Terminal nào cũng được (PowerShell, Terminal của macOS):

```bash
claude plugin marketplace add ducnguyen221/agent-writing-studio
claude plugin install agent-writing-studio@agent-writing-studio
```

Plugin mang nguyên cây repo — 9 skill, 7 lệnh và dữ liệu dùng chung `shared/` — nên không cần chép
thư mục nào. Mở phiên Claude Code mới rồi gõ `/agent-writing-studio:list` để thấy bảng lệnh.

## Chạy thẳng từ bản clone

Khi đang sửa repo và muốn thử ngay mà không cài lại plugin:

```bash
git clone https://github.com/ducnguyen221/agent-writing-studio
cd agent-writing-studio
python studio.py install --host claude     # dựng .work/, in lệnh — không sửa cấu hình Claude
claude --plugin-dir .
```

`--plugin-dir` nạp plugin từ chính thư mục đó cho phiên này; sửa file xong mở phiên mới là thấy.

## Cập nhật, kiểm, gỡ

```bash
claude plugin marketplace update agent-writing-studio
claude plugin update agent-writing-studio@agent-writing-studio
python studio.py doctor            # dòng host:claude so phiên bản plugin với repo
claude plugin uninstall agent-writing-studio@agent-writing-studio
```

Gỡ plugin **không** xoá `.work/`, station hay kho tri thức của bạn.

Bản 0.2.0 đổi tên bảy lệnh sang tiếng Anh; ai còn cài 0.1.x thì thấy lệnh cũ (`01-boi-canh`…) cho tới
khi cập nhật — xem [CHANGELOG](../../CHANGELOG.md).
