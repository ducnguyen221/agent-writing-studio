---
description: Axis 1 — interview the user until the brief is real, then write context.json for the case folder
argument-hint: [đề bài, hoặc slug ca đang làm]
---

Người dùng muốn dựng **bối cảnh** (trục Y1) cho: **$ARGUMENTS**

## Nạp trước khi làm

Đọc `skills/01-context-architect/SKILL.md` của repo agent-writing-studio
(cài dạng plugin thì là `${CLAUDE_PLUGIN_ROOT}/skills/01-context-architect/SKILL.md`), rồi làm theo
đúng trình tự trong đó. Hồ sơ thể loại nằm ở `shared/genres/<slug>.md` — đọc **mục §1** của đúng
thể loại người dùng nói; chưa biết thể loại thì hỏi, đừng đoán.

## Thư mục ca

`$WRITING_STUDIO_DATA/work/<slug>/`, không đặt biến thì `./.work/<slug>/`. Chưa có slug thì đề xuất
một slug kebab-case từ đề bài và xác nhận với người dùng trước khi tạo thư mục.

## Đầu vào

Lệnh này là **bước đầu chuỗi** — không cần artifact nào có sẵn. Nếu thư mục ca đã có `context.json`,
**không ghi đè im lặng**: nói rõ đã có, hỏi người dùng muốn bổ sung hay dựng lại từ đầu.

Tuỳ chọn có thì tốt: hồ sơ giọng người viết `$WRITING_STUDIO_DATA/writers/<slug>/profile.yaml`
(dựng bằng `shared/scripts/profile_build.py`, cần ≥3 bài chính chủ).

## Đầu ra

`<thư-mục-ca>/context.json` theo `shared/schemas/context.schema.json`.

## Chỉ làm đúng bước này

Xong `context.json` thì **dừng**. Không tự dựng dàn ý, không tự viết nháp — đó là
`/agent-writing-studio:viet-nhap`, và cổng cứng của trục 1 là *chưa gỡ hết điều kiện thì dừng và
hỏi*, không phải *cứ viết rồi tính*. Cuối lượt in đường dẫn tuyệt đối của `context.json` và câu lệnh
chạy bước kế tiếp.

## Tóm tắt cho `/agent-writing-studio:danh-sach`

- **Trục:** Y1 · Bối cảnh
- **Làm gì:** phỏng vấn ý đồ, luận đề, độc giả, ràng buộc, bằng chứng đang có
- **Cần đầu vào:** không (bước đầu chuỗi)
- **Ra file:** `context.json`
