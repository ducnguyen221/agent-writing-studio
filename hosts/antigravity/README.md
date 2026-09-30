# Dùng agent-writing-studio với Google Antigravity

Antigravity dùng đường **mở thẳng thư mục repo**:

```bash
git clone https://github.com/ducnguyen221/agent-writing-studio
cd agent-writing-studio
python studio.py install --host antigravity     # macOS: python3.12 studio.py …
```

Mở thư mục repo trong Antigravity. Agent đọc [`GEMINI.md`](../../GEMINI.md) → [`AGENTS.md`](../../AGENTS.md);
bảng *Chọn skill theo việc* dẫn tới `skills/<trục>/SKILL.md`, và mọi hồ sơ thể loại, schema, script đều
được đọc ngay trong repo. Lệnh chạy lẻ: bảo agent đọc file tương ứng trong [`commands/`](../../commands/).

Chưa kiểm cơ chế nạp skill riêng của Antigravity cho repo này; đường qua `AGENTS.md` không phụ thuộc
cơ chế đó. Kiểm máy: `python studio.py doctor`. Cập nhật: `python studio.py update --yes`.
