# Xử lý sự cố

Bước đầu tiên luôn là `python studio.py doctor` (macOS: `python3.12 studio.py doctor`) trong thư mục repo,
rồi đọc dòng `FAIL` / `WARN`. `WARN` ở `lib:*` chỉ là thư viện tuỳ chọn chưa cài. Cài đặt từ đầu: xem
[`INSTALL.md`](../INSTALL.md); theo từng ứng dụng AI: [`hosts/`](../hosts/README.md).

## Lỗi hay gặp

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| Gõ lệnh `/agent-writing-studio:01-boi-canh` vẫn chạy | plugin còn bản 0.1.x | cập nhật plugin ([INSTALL mục 6](../INSTALL.md#6-cập-nhật-và-gỡ)); tên mới là `01-context` |
| `doctor` báo `host:claude WARN` | plugin cũ hơn repo | cập nhật plugin ([INSTALL mục 6](../INSTALL.md#6-cập-nhật-và-gỡ)) |
| `doctor` báo `data WARN` … `station` | `WRITING_STUDIO_DATA` trỏ thư mục chưa có | `python studio.py install` |
| `doctor` báo `data WARN` … `tên cũ trước 0.4.0` | repo còn workspace tên cũ `.work/` | xem mục *Dời `.work/` sang `workspace/`* dưới đây |
| `doctor` báo `data FAIL` … `cả workspace/ lẫn .work/` | có cả hai thư mục | xem mục *Có cả hai thư mục* dưới đây |
| `install` thoát mã 2 | station đặt bên trong cây source, hoặc có cả hai thư mục workspace | chọn thư mục ngoài repo / bỏ `--station`; hoặc xử lý hai thư mục trước |
| `python` không chạy trên macOS | máy chỉ có `python3`, hoặc `python3` là bản 3.9 của hệ thống | cài `brew install python@3.12` rồi dùng `python3.12 studio.py …` |
| `python` mở Microsoft Store trên Windows | máy chưa có Python thật | `winget install --id Python.Python.3.12 -e --scope user`, mở terminal mới |
| Biến vừa đặt mà `doctor` vẫn không thấy | terminal/ứng dụng AI mở trước khi đặt biến | mở cửa sổ mới; macOS kiểm bằng `zsh -lic 'echo $WRITING_STUDIO_DATA'` |
| `knowledge NOT_CHECKED` dù trước đây có kho tri thức | bản 0.4.0 bỏ tên biến kho tri thức cũ | đặt `WRITING_STUDIO_KNOWLEDGE` trỏ gốc kho (xem [CHANGELOG](../CHANGELOG.md)) |

## Dời `.work/` sang `workspace/`

Bản 0.4.0 đổi tên workspace mặc định. Không có gì tự dời:

1. `python studio.py migrate` — **xem trước**: in số file, số thư mục ca sẽ dời; không đổi gì.
2. Đóng mọi file đang mở trong `.work/` (trình soạn thảo, Word), rồi `python studio.py migrate --yes`.
   Đây là **một lần đổi tên thư mục**, không chép, không xoá; nhật ký nằm ở
   `workspace/.studio-migrate.json`.
3. `python studio.py doctor` — dòng `data` phải là `PASS`.
4. Muốn quay lại: `python studio.py migrate --undo` (xem trước) rồi `python studio.py migrate --undo --yes`.

Đổi tên thất bại (Windows báo thư mục đang được dùng) thì lệnh thoát mã 1 và **không có gì thay đổi**.

## Có cả hai thư mục

`workspace/` và `.work/` cùng tồn tại thường là do đã tạo ca mới ở `workspace/` trước khi dời `.work/`.
Xưởng **không tự gộp**: hai ca trùng tên có thể là hai bài khác nhau.

1. Xem mỗi bên có những thư mục ca nào.
2. Chuyển tay các ca cần giữ từ `.work/` sang `workspace/` (đổi tên ca nếu trùng).
3. Khi `.work/` không còn gì cần giữ, sao lưu nếu muốn, rồi xoá nó.
4. `python studio.py doctor` — dòng `data` phải hết `FAIL`.

Agent làm giúp thì phải hỏi người dùng ở bước 2 và bước 3 — đó là dữ liệu của người dùng.

## Mã thoát của `studio.py`

`0` không có `FAIL` · `1` có `FAIL` (hoặc đổi tên thư mục thất bại) · `2` từ chối làm (tham số sai,
checkout có sửa dở, đích ghi nằm trong cây source, trạng thái workspace mơ hồ).
