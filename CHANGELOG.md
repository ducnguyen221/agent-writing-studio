# Nhật ký thay đổi

Chỉ ghi thứ **người dùng repo nhìn thấy**: tên lệnh, tên file, hợp đồng dữ liệu, hành vi mặc định.
Chi tiết thiết kế và lý do nằm ở tài liệu tương ứng, không chép lại ở đây.

## [0.2.1] — 2026-09-14

### Hợp đồng `writer_profile_ref` / `profile_used`: ba gốc, không phá vỡ tương thích

Hai trường là đường **tương đối**, agent tự ghép theo thứ tự: (1) gốc kho tri thức cá nhân
`OPCOS_BRAIN_PATH` → (2) gốc station `WRITING_STUDIO_DATA` → (3) gốc repo. Chuỗi không chứa `/` là slug
(`writers/<slug>/profile.yaml` ở station, rồi `shared/writers/<slug>/` trong repo). Giá trị cũ dạng
`writers/<slug>/profile.yaml` hay slug trần vẫn hợp lệ và phân giải như trước. Mô tả cập nhật ở
`context.schema.json`, `draft.schema.json`, lệnh `01-context`, `04-humanize` và cầu Brain.

### `profile_build.py` 1.1

- Bỏ frontmatter YAML ở **đầu** file `.md`/`.txt` trước khi đo — trỏ `--samples-dir` thẳng vào thư mục
  bài mẫu trong kho tri thức mà mã băm, số đo không đổi. Vạch `---` giữa thân bài không bị đụng.
- Cờ mới `--keep-manual [PATH]`: dựng lại hồ sơ mà giữ phần điền tay (`voice_notes`,
  `ownership_confirmed_by`, `known_typos`, `pet_templates` thêm tay, thuật ngữ, dòng `limitations` viết
  tay). Thiếu hồ sơ cũ: vẫn ghi, thoát mã 1. Chỉ in số lượng đã giữ.
- `voice_notes` nhiều dòng xuất dạng khối YAML `|` để còn sửa tay được.

### Tài liệu

- README §8.2 sửa trạng thái hồ sơ giọng của chủ repo: đã `ready` từ 5 bài chính chủ.
- README, `shared/writers/README.md`, `docs/ARCHITECTURE.md`, `docs/SCORING.md`, trang giới thiệu: station
  giữ ca chạy và sản phẩm; hồ sơ giọng, bài mẫu, chân dung độc giả nên nằm trong kho tri thức.

## [0.2.0] — 2026-09-13 · ĐỔI TÊN, CÓ PHÁ VỠ TƯƠNG THÍCH

### Phá vỡ tương thích: bảy lệnh đổi tên

Tên lệnh cũ **không còn**. Ai đã cài bản 0.1.x phải cập nhật plugin rồi dùng tên mới.

| Lệnh cũ | Lệnh mới |
|---|---|
| `/agent-writing-studio:01-boi-canh` | `/agent-writing-studio:01-context` |
| `/agent-writing-studio:02-viet-nhap` | `/agent-writing-studio:02-draft` |
| `/agent-writing-studio:03-phan-bien` | `/agent-writing-studio:03-critique` |
| `/agent-writing-studio:04-bien-tap` | `/agent-writing-studio:04-humanize` |
| `/agent-writing-studio:05-giam-dinh` | `/agent-writing-studio:05-audit` |
| `/agent-writing-studio:giao-docx` | `/agent-writing-studio:deliver-docx` |
| `/agent-writing-studio:danh-sach` | `/agent-writing-studio:list` |

Không giữ lệnh cũ làm bí danh: hợp đồng test khoá đúng bảy file trong `commands/`, và hai lệnh
cùng trỏ một chỗ sẽ làm lệnh liệt kê in đôi.

### Bốn hồ sơ thể loại Việt đổi slug

| Slug cũ | Slug mới | Tên tiếng Việt giữ nguyên trong bài |
|---|---|---|
| `chinh-luan` | `commentary` | chính luận |
| `de-cuong-nghien-cuu` | `thesis-proposal` | đề cương nghiên cứu sinh |
| `bao-cao-thuc-tap` | `internship-report` | báo cáo thực tập |
| `sang-kien-kinh-nghiem` | `teaching-initiative` | sáng kiến kinh nghiệm |

Mỗi hồ sơ có thêm một dòng khai slug và tên tiếng Việt ngay dưới tiêu đề, để agent khớp được khi
người dùng gọi tên Việt.

### Tên file và tài liệu

- `docs/KIEN-TRUC.md` thành `docs/ARCHITECTURE.md`; `docs/CHAM-DIEM.md` thành `docs/SCORING.md`.
- `shared/scripts/xuat_docx.py` thành `shared/scripts/export_docx.py`.
- `skills/04-humanizer/assets/thanh-ngu.json` thành `assets/idioms.json` (notice MIT giữ nguyên).
- Hai mươi lăm file trong `references/` của năm skill đổi sang tên tiếng Anh. Nội dung vẫn tiếng Việt.

### Cố ý KHÔNG đổi

Mọi `id` trong YAML và JSON — `hook_giai_quyet_cta`, `chat_lieu_rieng`, `luan_de_phan_de`,
`audience_fields`, `pet_templates[].id`, tên họ tell. Đó là **hợp đồng dữ liệu máy đọc**, có trong
hồ sơ giọng và file kết quả của những ca đã chạy; đổi chúng là làm hỏng dữ liệu cũ mà không ai được
lợi. Nội dung tiếng Việt của tài liệu cũng giữ nguyên, đúng luật "frontmatter tiếng Anh, thân bài
tiếng Việt".

### Thêm

- Hàng rào de-name nay chặn cả **tên riêng của chủ repo**, không chỉ tên repo nguồn. Slug ví dụ
  trong tài liệu và test là `writer-a`.
- `README` nói rõ **ba tầng**: repo giữ luật chung, kho tri thức cá nhân giữ giọng riêng, station giữ
  số đo và sản phẩm.

## [0.1.2] — 2026-08-31

README cho mọi thư mục gốc, lệnh đánh số theo trục, tài liệu kế hoạch và kết quả chuyển thành nội
bộ, banner, mục giấy phép và trích dẫn rõ trong README.

## [0.1.1] — 2026-08-31

Gộp bốn sub-skill giám định vào cây năm trục, thêm bảy lệnh chạy lẻ, script xuất `.docx`.

## [0.1.0] — 2026-08-31

Bản công khai đầu tiên: năm trục, chín hồ sơ thể loại, station tách khỏi repo, khử tên nguồn.
