# Nguồn đối chiếu skills

## Baseline

- Repo: `https://github.com/anthropics/skills`
- Nhánh: `main`
- Commit: `3b3fad96af16a10759d930941b4520ba0c40edae`
- Ngày commit: 21/08/2026
- Ngày rà: 30/08/2026
- License: none — KHÔNG CÓ
- Hình thức: `idea-only` — KHÔNG CÓ LICENSE RÕ RÀNG. Chỉ được lấy sơ đồ, tên hoặc ý tưởng; cấm chép nội dung.

## File đã đọc

- `README.md`
- `THIRD_PARTY_NOTICES.md`
- Danh sách thư mục `skills/`
- `skills/doc-coauthoring/` — liệt kê nội dung thư mục để kiểm license

## Kiểm lại 30/08/2026 (Phase 4)

Ba lệnh, kết quả không đổi:

- `gh api repos/anthropics/skills/license` → **404 Not Found** (không có license nhận dạng được)
- `gh api repos/anthropics/skills/contents` → `.claude-plugin`, `.gitignore`, `README.md`,
  `THIRD_PARTY_NOTICES.md`, `skills`, `spec`, `template` — **không có `LICENSE`**
- `gh api repos/anthropics/skills/contents/skills/doc-coauthoring` → đúng một file `SKILL.md`
  (15.815 byte), **không có license riêng của thư mục**

Giữ nguyên `idea-only`.

Không lưu bản vendored và cũng không được phép lưu. Khi upstream thay đổi, chỉ đọc lại xem sơ đồ có đổi
không; mọi câu chữ trong repo này vẫn phải là của repo này.
