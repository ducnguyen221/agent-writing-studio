---
description: Deliver the finished text as a Word .docx in the user own folder, with the provenance sidecar beside it
argument-hint: [slug ca hoặc file .md] [thư mục người dùng muốn nhận bản giao]
---

Người dùng muốn **giao bản docx**: **$ARGUMENTS**

## Việc của lệnh này

Chạy `shared/scripts/xuat_docx.py` để biến bản Markdown cuối thành `.docx` đúng quy cách văn bản
tiếng Việt (Times New Roman 13pt, giãn dòng 1,5, lề trên/dưới 2cm · trái 3cm · phải 2cm, heading
đậm 14–16), rồi **đặt bản giao vào đúng thư mục người dùng đang làm việc**.

```bash
python shared/scripts/xuat_docx.py <file.md> --out "<thư-mục-người-dùng>" --provenance <sidecar.json>
```

`--out` nhận thư mục (tên file lấy theo file nguồn) hoặc đường dẫn `.docx` cụ thể.

## Đầu vào

Từ `$WRITING_STUDIO_DATA/work/<slug>/` (fallback `./.work/<slug>/`):

- `polished.md` — bản đã biên tập; chưa có thì dùng `draft.md` và **nói rõ đang giao bản chưa biên
  tập**, kèm lệnh `/agent-writing-studio:bien-tap <slug>`;
- `polished.provenance.json` — sidecar tự khai nguồn gốc.

Không có file `.md` nào để giao thì dừng và nói rõ thiếu gì cùng lệnh sinh ra nó. **Không tự viết
lại bài** để có cái mà xuất.

Thiếu sidecar provenance: script vẫn xuất nhưng in cảnh báo. Nói lại cảnh báo đó cho người dùng —
bản giao của studio phải mang theo bản tự khai nguồn gốc; đây là ranh giới đạo đức, không phải tuỳ chọn.

## Đích giao — chỗ hay làm sai nhất

- Bản giao ghi **CHÍNH XÁC vào thư mục người dùng yêu cầu hoặc đang làm việc**, không phải station.
- `$WRITING_STUDIO_DATA` (`.writing`) là **xưởng cục bộ của agent**: mọi file làm việc ở lại đó, và
  **không bắt người dùng mò vào đó lấy bài**.
- Người dùng chưa nói giao vào đâu → **hỏi một câu**. Chỉ khi họ nói không quan tâm mới để ở
  `$WRITING_STUDIO_DATA/out/` rồi báo đường dẫn tuyệt đối.
- Thiếu `python-docx` → script báo `pip install python-docx`. Nói lại nguyên văn, đừng lặng lẽ giao
  bản `.md` thay thế.

## Đầu ra

`<thư-mục-người-dùng>/<tên>.docx` + `<tên>.provenance.json` nằm cạnh nó. Cuối lượt in **đường dẫn
tuyệt đối** của cả hai.

## Chỉ làm đúng bước này

Chỉ xuất và giao. Không sửa chữ trong bài (đó là `/agent-writing-studio:bien-tap`), không giám định
lại, không tự chạy lại chuỗi để "cho chắc".

## Tóm tắt cho `/agent-writing-studio:danh-sach`

- **Trục:** giao hàng (sau Y4)
- **Làm gì:** md → docx đúng quy cách Việt, đặt vào thư mục người dùng, kèm sidecar provenance
- **Cần đầu vào:** `polished.md` (nên có `polished.provenance.json`)
- **Ra file:** `<tên>.docx` + `<tên>.provenance.json` trong thư mục người dùng
