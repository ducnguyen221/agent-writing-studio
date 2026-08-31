---
description: Axis 5 — forensic review for AI-written passages; audit mode by default, blind only for calibration
argument-hint: [slug ca hoặc đường dẫn tài liệu; thêm --blind để chấm mù]
---

Người dùng muốn **giám định** (trục Y5): **$ARGUMENTS**

## Nạp trước khi làm

Đọc router `skills/05-forensics/SKILL.md`
(dạng plugin: `${CLAUDE_PLUGIN_ROOT}/skills/05-forensics/SKILL.md`), rồi gọi **ba skill con nằm ngay
trong thư mục đó**, đúng thứ tự:

1. `skills/05-forensics/05a-reading/SKILL.md` — đọc mù, gán nhãn câu, lập findings;
2. `skills/05-forensics/05b-scoring/SKILL.md` — tính S/C sau khi bản đọc đã khoá;
3. `skills/05-forensics/05c-reporting/SKILL.md` — báo cáo, phản chứng, câu hỏi xác minh.

Chuẩn mực thể loại nằm ở **mục §5** của `shared/genres/<thể-loại>.md`.

## Chọn chế độ — chọn sai là đọc sai kết quả

- **`audit` (mặc định)** — bật khi thư mục ca có **cả** `draft.meta.json` lẫn `sentences.json`. Đọc
  hai file đó **sau** khi bản đọc mù đã khoá, đối chiếu với bản tự khai và **báo câu máy chưa khai**.
  Phần đối chiếu ID chạy bằng `python shared/scripts/check_spans.py`, 0 gọi mô hình. Kết quả là
  **báo cáo liêm chính, không phải điểm**.
- **`blind`** — chỉ khi người dùng gõ `--blind`, hoặc tài liệu đến từ ngoài và không có bản tự khai.
  Dùng cho hiệu chuẩn và đối chứng độc lập.

Trên văn đã đi qua chính studio này, `low_signal` ở chế độ mù là **kết quả kỳ vọng, không phải bằng
chứng** — trục 2 tránh đúng danh mục mà trục 5 dùng để soi. Nói rõ điều đó trong báo cáo.

## Đầu vào

Từ `$WRITING_STUDIO_DATA/work/<slug>/` (fallback `./.work/<slug>/`): văn bản cần đọc (`polished.md`
hoặc `draft.md`, hoặc file người dùng đưa), `sentences.json`, và — cho chế độ `audit` —
`draft.meta.json`.

Thiếu `sentences.json`: sinh bằng `python skills/05-forensics/scripts/extract.py <file> --out <ca>`
rồi nói rõ đã sinh. Thiếu `draft.meta.json`: **không chạy `audit`**, nói rõ đang chạy `blind` vì
không có bản tự khai (bài của studio thì `/agent-writing-studio:02-viet-nhap` là chỗ sinh ra nó), và
đừng đọc điểm mù thành phán xét.

## Đầu ra

`<thư-mục-ca>/evidence.json` (theo `skills/05-forensics/assets/result.schema.json`) và `report.md`.
Mọi finding phải có vị trí, trích dẫn, **phản chứng** và cách kiểm tra. Không đầu ra nào đủ để kỷ
luật một người.

## Chỉ làm đúng bước này

Không tự sửa bài sau khi giám định. Hiệu chuẩn ngưỡng và dựng corpus là
`skills/05-forensics/05d-calibration/SKILL.md`, không gọi trong lượt review thường.

## Tóm tắt cho `/agent-writing-studio:danh-sach`

- **Trục:** Y5 · Giám định
- **Làm gì:** đọc mù → S/C → báo cáo; mặc định `audit`, `--blind` chỉ để hiệu chuẩn
- **Cần đầu vào:** văn bản + `sentences.json` (thêm `draft.meta.json` cho `audit`)
- **Ra file:** `evidence.json` · `report.md`
