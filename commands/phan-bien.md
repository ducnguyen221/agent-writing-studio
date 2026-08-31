---
description: Axis 3 — score a draft per criterion against the genre rubric, with quotable evidence and no total score
argument-hint: [slug ca, hoặc đường dẫn file cần chấm]
---

Người dùng muốn **phản biện** (trục Y3): **$ARGUMENTS**

## Nạp trước khi làm

Đọc `skills/03-critique/SKILL.md` của repo agent-writing-studio
(dạng plugin: `${CLAUDE_PLUGIN_ROOT}/skills/03-critique/SKILL.md`). Barem của thể loại nằm ở
**mục §3** của `shared/genres/<thể-loại>.md`.

## Đầu vào

Từ `$WRITING_STUDIO_DATA/work/<slug>/` (fallback `./.work/<slug>/`):

- `draft.md` (hoặc file người dùng đưa thẳng) — **bắt buộc**;
- `sentences.json` — **bắt buộc** để neo mọi nhận xét vào `sentence_id`;
- `context.json` — nên có: barem và kỳ vọng độc giả nằm trong đó.

Thiếu `draft.md` hoặc `sentences.json` thì **dừng và nói rõ thiếu gì**, kèm lệnh sinh ra nó
(`/agent-writing-studio:viet-nhap <slug>`). Bài từ ngoài đưa vào mà chưa có `sentences.json`: sinh
index cho lượt này, ghi xuống thư mục ca, và **nói rõ đã sinh** — đừng đếm câu trong đầu.

Thiếu `context.json` thì vẫn chấm được, nhưng phải ghi vào phần giới hạn của báo cáo rằng barem đang
lấy mặc định của thể loại chứ không lấy barem người chấm thật.

## Đầu ra

`<thư-mục-ca>/critique.json` theo `shared/schemas/critique.schema.json`. **Không có điểm tổng** —
điểm tổng che mất chỗ yếu. Mỗi nhận xét phải có `sentence_id`, câu trích và việc phải sửa.

## Chỉ làm đúng bước này

Chấm xong thì dừng. **Không tự sửa bài** — sửa là việc của `/agent-writing-studio:bien-tap`, và trục
4 không được xem điểm trục 5 của chính bài đang sửa.

## Tóm tắt cho `/agent-writing-studio:danh-sach`

- **Trục:** Y3 · Phản biện
- **Làm gì:** chấm từng tiêu chí theo barem thể loại, soi ngụy biện, xếp việc phải sửa
- **Cần đầu vào:** `draft.md` + `sentences.json` (nên có `context.json`)
- **Ra file:** `critique.json`
