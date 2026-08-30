# Ghi chú chưng cất hunspell-vi

## Đã chưng cất

| Nguyên lý upstream | Cách chuyển hóa trong studio |
|---|---|
| Ghi nhận đây là bộ từ điển chính tả tiếng Việt trưởng thành | `skills/04-humanizer/references/05-chinh-ta.md` chỉ hướng dẫn người dùng TỰ CÀI từ điển; đây là phụ thuộc tuỳ chọn, không phải thành phần của repo. Repo này KHÔNG có bộ kiểm chính tả, và đó là lựa chọn |

## Không mang sang

- Mọi file `.dic` và `.aff`. KHÔNG vendor một dòng nào.
- Mọi danh sách từ rút ra từ từ điển.
- Ý tưởng dùng lỗi chính tả làm dấu hiệu nguồn gốc — lỗi chính tả nói về người gõ, không nói về máy.

## Ranh giới

KIỂM TAY 30/08/2026, xác nhận lại ở Phase 3 (30/08/2026, đọc lại `dictionaries/README-en.txt` qua `gh api`): API license trả rỗng vì repo KHÔNG có file `LICENSE` ở gốc. File `dictionaries/README-en.txt` ghi rõ dữ liệu bắt nguồn từ gói GNU Aspell tiếng Việt của Hồ Ngọc Đức, điều khoản GPLv2. GPLv2 là copyleft: mang dữ liệu vào đây sẽ kéo nghĩa vụ cấp phép sang cả repo. Kết luận vận hành: KHÔNG VENDOR, giữ ở mức phụ thuộc tuỳ chọn do người dùng tự cài.

## Kiểm lại ở Phase 3

Gốc repo có 7 mục: `.gitignore`, `CONTRIBUTING.md`, `README.md`, `dictionaries/`, `firefox_thunderbird/`,
`openoffice/`, `tools/` — **không có `LICENSE`**. `dictionaries/README-en.txt` dòng 16–17 ghi tác giả
Hồ Ngọc Đức và `Copyright Terms: GPLv2`. Kết luận Phase 0 giữ nguyên: KHÔNG VENDOR.

Một chi tiết có ích cho trục 4 đã được ghi lại ở `05-chinh-ta.md` mục 3, **không chép dữ liệu**: bộ từ
điển có hai biến thể theo hai quy ước đặt dấu thanh. Cả hai đều đúng chính tả, nên trục 4 không được
đổi kiểu đặt dấu của tác giả, và `counters.py` xuất `unicode.tone_style` chỉ để mô tả.
