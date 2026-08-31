---
description: Axis 4 — edit prose toward the author own voice in one of three output modes, never touching facts
argument-hint: [slug ca hoặc đường dẫn file; thêm "dán-text" nếu dán thẳng văn bản]
---

Người dùng muốn **biên tập** (trục Y4): **$ARGUMENTS**

## Nạp trước khi làm

Đọc `skills/04-humanizer/SKILL.md` của repo agent-writing-studio
(dạng plugin: `${CLAUDE_PLUGIN_ROOT}/skills/04-humanizer/SKILL.md`), và **chọn chế độ đầu ra trước
khi sửa chữ nào** theo `skills/04-humanizer/references/06-che-do-dau-ra.md`:

- người dùng dán văn bản vào lượt → *dán-text*;
- người dùng đưa đường dẫn file → *file*;
- lệnh này được một quy trình lớn hơn gọi vào → *nhúng-trong-task*.

Quy tắc biên tập của thể loại nằm ở **mục §4** của `shared/genres/<thể-loại>.md`.

## Đầu vào

Từ `$WRITING_STUDIO_DATA/work/<slug>/` (fallback `./.work/<slug>/`):

- văn bản cần sửa — `draft.md`, hoặc file người dùng chỉ định, hoặc đoạn dán thẳng;
- `sentences.json` — để mỗi nhát sửa neo được vào `sentence_id`;
- `critique.json` — nên có: `must_fix[]` nào có `owner: 04-humanizer` là việc của lượt này;
- `draft.meta.json` — **ranh giới đạo đức**: trục 4 chỉ chạy trên bản thảo đã biết nguồn gốc.

Thiếu văn bản thì dừng và nói rõ. Thiếu `critique.json` thì vẫn sửa được, nhưng nói rõ đang sửa mà
chưa có danh sách việc phải sửa của trục 3 (`/agent-writing-studio:phan-bien <slug>`). Thiếu
`draft.meta.json` mà bài đến từ ngoài studio: vẫn sửa được, nhưng phải nói thẳng rằng bản giao sẽ
mang ghi chú "đã qua biên tập máy" và **không** có bản tự khai nguồn gốc phần trước đó. Trục 4
**không phải dịch vụ né máy chấm AI**.

## Cổng fail-closed

Phát hiện mình đã thêm hoặc bớt một dữ kiện (`facts_added` / `facts_removed` khác rỗng) →
**trả lại bản gốc**, không sửa tiếp, và báo lỗi.

## Đầu ra

- `<thư-mục-ca>/polished.md`
- `<thư-mục-ca>/polish.diff.json` — từng nhát sửa: vị trí, lý do, trước/sau
- `polished.provenance.json` — sidecar **đi theo bản giao**, không ở lại thư mục ca

Kiểm bằng `python skills/04-humanizer/scripts/polish_check.py` trước khi báo xong.

## Chỉ làm đúng bước này

Không tự giám định, không tự xuất docx. Giao thành phẩm là `/agent-writing-studio:giao-docx`.

## Tóm tắt cho `/agent-writing-studio:danh-sach`

- **Trục:** Y4 · Biên tập
- **Làm gì:** sửa về phía giọng tác giả, có vùng cấm sửa; 3 chế độ đầu ra
- **Cần đầu vào:** `draft.md` + `sentences.json` (nên có `critique.json`, `draft.meta.json`)
- **Ra file:** `polished.md` · `polish.diff.json` · `polished.provenance.json`
