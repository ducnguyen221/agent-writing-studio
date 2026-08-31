---
description: Axis 2 — build a three-layer outline, wait for approval, then draft prose with a machine-written self-declaration
argument-hint: [slug ca, hoặc đường dẫn thư mục ca]
---

Người dùng muốn **viết nháp** (trục Y2) cho ca: **$ARGUMENTS**

## Nạp trước khi làm

Đọc `skills/02-cowriter/SKILL.md` của repo agent-writing-studio
(dạng plugin: `${CLAUDE_PLUGIN_ROOT}/skills/02-cowriter/SKILL.md`) và làm theo đúng trình tự.
Khung viết của thể loại nằm ở **mục §2** của `shared/genres/<thể-loại>.md`.

## Đầu vào bắt buộc

Từ `$WRITING_STUDIO_DATA/work/<slug>/` (không đặt biến thì `./.work/<slug>/`):

- `context.json` — đề bài, luận đề, độc giả, thể loại, ràng buộc.

**Thiếu file này thì DỪNG.** Nói đúng một câu: *"chưa có `context.json` trong `<đường dẫn>`; chạy
`/agent-writing-studio:boi-canh <đề bài>` để dựng trước"*. **Không** tự phỏng vấn thay trục 1, không
tự bịa bối cảnh để viết cho xong — một bản nháp dựng trên bối cảnh tự đoán là bản nháp phải bỏ.

## Cổng cứng giữa lệnh

Dàn ý ba tầng phải được **người dùng duyệt** rồi mới viết văn xuôi. Đây là cổng của chính trục 2,
không phải nghi thức: trình dàn ý, chờ trả lời, rồi mới viết.

## Đầu ra

- `<thư-mục-ca>/draft.md`
- `<thư-mục-ca>/draft.meta.json` — bản tự khai câu nào do máy viết, theo
  `shared/schemas/draft.schema.json`
- `<thư-mục-ca>/sentences.json` — hệ đánh số câu dùng chung cho cả chuỗi

`sentences.json` sinh **một lần** ở đây. Các trục sau đọc lại, **không trục nào được tự đếm câu**.

## Chỉ làm đúng bước này

Xong bản nháp thì dừng. Không tự chấm, không tự biên tập — đó là `phan-bien` và `bien-tap`.

## Tóm tắt cho `/agent-writing-studio:danh-sach`

- **Trục:** Y2 · Đồng viết
- **Làm gì:** dàn ý ba tầng → chờ duyệt → viết văn xuôi + tự khai phần máy viết
- **Cần đầu vào:** `context.json` (từ `/boi-canh`)
- **Ra file:** `draft.md` · `draft.meta.json` · `sentences.json`
