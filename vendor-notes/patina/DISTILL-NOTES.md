# Ghi chú chưng cất patina

## Đã chưng cất

| Nguyên lý upstream | Cách chuyển hóa trong studio |
|---|---|
| Tách tầng luật chung khỏi tầng luật theo ngôn ngữ | `shared/rules/vi-ai-tells.json`: `usage_rules` và `families` là tầng chung, `entries` là tầng tiếng Việt |
| Mỗi luật là một bản ghi có id, ví dụ và cách sửa | Mỗi entry có `id`, `vi_example`, `fix` — và repo này thêm hai trường upstream không có: `vi_counterexample` và `genre_baseline` |

## Không mang sang

- Nội dung pack tiếng Anh, Hàn, Trung, Nhật.
- Mọi danh sách từ. Dịch danh sách từ sang tiếng Việt đúng là thứ `05d-calibration` cấm.
- Cách chạy như một công cụ dòng lệnh độc lập.

## Ranh giới

Chỉ lấy HÌNH DẠNG dữ liệu, không lấy dữ liệu. Hai trường `vi_counterexample` và `genre_baseline` là bổ sung của repo này, sinh ra từ ca giám định thật ngày 29/08/2026 chứ không từ upstream.
