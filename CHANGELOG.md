# Nhật ký thay đổi

Chỉ ghi thứ **người dùng repo nhìn thấy**: tên lệnh, tên file, hợp đồng dữ liệu, hành vi mặc định.
Chi tiết thiết kế và lý do nằm ở tài liệu tương ứng, không chép lại ở đây.

## [0.4.2] — 2026-09-30

Bản vệ sinh repo. Hành vi chạy không đổi, trừ việc thêm `workspace/.gitignore` khi tạo workspace.
Không đổi hợp đồng dữ liệu, không đổi thứ tự phân giải đường dữ liệu.

### Sửa

- **Workspace tự mang `.gitignore`.** `./workspace` tính theo thư mục đang mở, nên mở một dự án riêng
  thì bài thật rơi vào `<dự án>/workspace/`, nơi `.gitignore` của repo này không với tới. Nay
  `extract.py` (khi thư mục ca nằm trong `./workspace`) và `studio.py install` (khi dựng `workspace/`
  mới) ghi `workspace/.gitignore` chứa `*` nếu file đó chưa có. Không bao giờ ghi đè file đã có;
  station `WRITING_STUDIO_DATA` và `--out` ngoài `workspace/` không bị đụng.
- `skills/README.md` bỏ câu dạy chép skill sang thư mục của host (trái `hosts/README.md`), thay bằng
  con trỏ tới `hosts/README.md`.
- `AGENTS.md`: ghi chú macOS cho lệnh `doctor` và lệnh chạy test (`python3.12`, hoặc Python của venv).

### Repo và CI

- Thêm `.gitattributes` (`* text=auto`, `*.docx binary`): xuống dòng trong Git không còn phụ thuộc
  `core.autocrlf` của máy commit. Không file nào trong index đổi xuống dòng.
- `.gitignore` chặn thêm rác hệ điều hành (`.DS_Store`, `._*`, `Thumbs.db`, `desktop.ini`), cấu hình
  riêng của máy (`/.claude/settings.local.json`, `/.idea/`, `/.vscode/`), `/venv/`, cache công cụ
  (`.mypy_cache/`, `.ruff_cache/`, `*.egg-info/`) và nháp tạm `/.tmp/`.
- CI: `actions/checkout` v4.2.2 → v5.1.0, `actions/setup-python` v5.6.0 → v6.3.0 (chạy Node 24), vẫn
  ghim theo SHA commit.

### Test

- `test_station_paths.py`: `extract.py` tạo workspace thì có `.gitignore`, chạy lại không đổi, file
  người dùng có sẵn không bị đè, `--out` ngoài workspace không sinh gì, Git thật bỏ qua bài trong đó.
- `test_studio_lifecycle.py`: `install` dựng workspace mới thì có `.gitignore`, workspace có sẵn thì
  không thêm gì.
- `test_install_docs.py` quét cả `skills/README.md`; `test_repo_gates.py` thêm ca cho các dòng
  `.gitignore` mới.

## [0.4.1] — 2026-09-30

Bản vá tài liệu cho macOS. Không đổi mã, không đổi hợp đồng dữ liệu, không đổi thứ tự phân giải đường
dữ liệu (`--station` → `WRITING_STUDIO_DATA` → `<repo>/workspace/`).

### Sửa

- `install/index.html` bỏ lời khuyên "macOS có thể là `python3`": trên Mac `python3` của hệ thống có
  thể là 3.9, quá cũ cho `studio.py` (cần 3.10+). Trang nay nói `python3.12`, giống `INSTALL.md`.
- Thêm ghi chú macOS `python3.12` ở những trang dạy `python studio.py` mà còn thiếu: `index.html`
  (cả dòng `pip install`), `START-HERE.md`, `hosts/README.md`, `hosts/{claude,codex,antigravity}/README.md`.
- `docs/ARCHITECTURE.md` bỏ số test ghi cứng đã trôi xa số thật.

### Test

- `test_docs_drift.py`: cổng "không ghi cứng số test" quét **mọi** `.md`/`.html` public (trừ
  CHANGELOG), không chỉ danh sách trang chỉ đường — danh sách cũ bỏ sót `docs/ARCHITECTURE.md`.
- `test_install_docs.py` (`MacPythonTests`): trang nào dạy `python studio.py` phải nói `python3.12`;
  `python3` trơn chỉ được nhắc để cảnh báo bản 3.9.

## [0.4.0] — 2026-09-29

### Breaking / cần làm khi nâng cấp

- **Workspace mặc định đổi tên `.work/` → `workspace/`** (giống các xưởng anh em: không đặt biến là
  dữ liệu ở `<repo>/workspace/`). Không có gì tự dời, không mất dữ liệu:
  - chỉ có `.work/` → xưởng **vẫn đọc nó** (script `extract.py` cũng vậy, kèm cảnh báo); `doctor` báo
    `data WARN`; `install` giữ nguyên, không tạo `workspace/` bên cạnh;
  - `python studio.py migrate` in kế hoạch (xem trước) · `migrate --yes` đổi tên thư mục một bước, ghi
    nhật ký `workspace/.studio-migrate.json` · `migrate --undo --yes` trả lại;
  - có **cả hai** thư mục → `doctor` báo `data FAIL`, `migrate` và `install` từ chối (mã 2) — không tự
    gộp; cách xử lý ở `docs/troubleshooting.md`;
  - `WRITING_STUDIO_DATA` vẫn thắng cả hai.
- **Bỏ tên biến kho tri thức cũ `OPCOS_BRAIN_PATH`** (đã báo trước ở 0.3.0). Chỉ còn
  `WRITING_STUDIO_KNOWLEDGE`; máy chỉ đặt tên cũ thì `doctor` báo `knowledge NOT_CHECKED` — đặt tên mới.
- Tài liệu cầu kho tri thức đổi tên: `skills/01-context-architect/references/03-knowledge-bridge.md`.
  Trường `brain_pointers[]` của `context.json` **giữ nguyên** (không đổi hợp đồng dữ liệu).
- `README.md` nay là bản **tiếng Anh**; bản tiếng Việt đầy đủ chuyển sang `README.vi.md`.

### Mới

- `studio.py migrate [--undo] [--yes]`.
- `GUIDE.md` / `GUIDE.vi.md`: một ca đi trọn năm trục. `docs/troubleshooting.md`: bảng lỗi (dời từ
  `INSTALL.md`), cách dời workspace, cách xử lý khi có cả hai thư mục, mã thoát.
- `NOTICE` + `provenance.json`: dữ liệu đi kèm (kho thành ngữ MIT, mã băm + commit nguồn đã ghim) và
  thư viện tuỳ chọn kèm giấy phép; test `tests/shared/test_provenance.py`.
- Test mới: `test_host_docs.py` (lệnh dạy trong tài liệu host có thật), `test_docs_drift.py` (phiên bản,
  lệnh, cặp ngôn ngữ, tên workspace), kiểm di trú trong `test_studio_lifecycle.py`.

### Ranh giới public

- `.gitignore` neo gốc `/workspace/`, `/.work/`, `/.venv/`; `.env*` (trừ `.env.example`); test đọc Git
  index canh thêm `workspace/`, `docs/plans/`, `docs/results/`.
- Bỏ tên riêng của kho tri thức cá nhân của tác giả và tên ca thật khỏi cây public (tài liệu, schema,
  lệnh, script, test) — thay bằng "kho tri thức" và ca ví dụ `ca-mau-01` / `ca-mau-02`.
- Cổng chống rò (`test_public_boundary.py`) đọc thêm **danh sách cấm riêng nằm ngoài repo** qua biến
  `WRITING_STUDIO_LEAK_DENYLIST`; không đặt biến thì bỏ qua kèm lời nhắn, báo lỗi không in lại cụm cấm.
- Trang giới thiệu bỏ con số test ghi cứng.
- Provenance giữ luật de-name (31/08/2026): sổ nguồn phương pháp nằm ngoài repo; ngoại lệ có tên nguồn
  duy nhất là notice MIT bắt buộc trong `skills/04-humanizer/assets/idioms.json` (ghi trong `NOTICE`).

### Tài liệu

- `AGENTS.md`: bảng ranh giới dùng `workspace/`; agent thấy `.work/` đầu phiên thì báo người dùng và chỉ
  chạy `migrate --yes` khi được đồng ý; nhắc đặt `WRITING_STUDIO_LEAK_DENYLIST` trước khi phát hành.
- `README.vi.md` mục 5: bảng chế độ trục 5 nói đúng cách chọn — thư mục ca có cả `draft.meta.json` lẫn
  `sentences.json` thì `05-audit` chạy `audit`, không có bản tự khai (hoặc `--blind`) thì `blind`.
  Hành vi không đổi.

### Cài đặt trên macOS

- `INSTALL.md`: gọi `python3.12` rõ ràng; kiểm biến môi trường bằng `zsh -lic`; đường plugin Claude Code
  cũng clone repo để chạy được `studio.py doctor` như prompt yêu cầu; đường Codex nói rõ mở thư mục nào.

## [0.3.0] — 2026-09-29

### Luật dẫn nguồn (trục 2 + trục 3)

- `02-cowriter`: **không gán nhận định cho nguồn** — "Theo X…" chỉ viết khi câu ấy có thật trong tư
  liệu đang cầm. Luật đầy đủ + ví dụ: `skills/02-cowriter/references/05-source-attribution.md`.
- `03-critique`: bước 4 **rà dẫn nguồn**, bắt buộc, không phụ thuộc `lenses[]`; `critique.json` phải
  nói ra kết quả rà, im lặng không tính là đã rà. Chi tiết: `skills/03-critique/references/06-source-check.md`.

### Biến kho tri thức đổi tên: `WRITING_STUDIO_KNOWLEDGE`

Gốc kho tri thức cá nhân (bậc 1 khi phân giải `writer_profile_ref`, `brain_pointers[]`) nay đọc từ
`WRITING_STUDIO_KNOWLEDGE`. Tên cũ `OPCOS_BRAIN_PATH` vẫn được đọc làm **đường lùi** khi tên mới chưa
đặt, và sẽ bỏ ở 0.4. **Không còn mặc định đoán một thư mục kho tri thức trong home**: không đặt biến nào là không có kho tri thức
— studio vẫn chạy, bài mang giọng mặc định của thể loại.

### Cài đặt: không còn chép `skills/` bằng tay

- README và trang giới thiệu bỏ hướng dẫn `cp -r skills/*` / `Copy-Item`. Đường cài: plugin Claude Code
  (`claude plugin marketplace add` + `install`), hoặc clone rồi mở thẳng thư mục repo (Codex, Antigravity).
- Mới: `AGENTS.md` (hướng dẫn chuẩn cho mọi agent; `CLAUDE.md`, `GEMINI.md` là con trỏ), `INSTALL.md`
  cho agent kèm prompt dán tiếng Việt/tiếng Anh, `START-HERE.md`, `hosts/` theo từng ứng dụng, trang
  `/install/`.
- Mới: `studio.py doctor · install · update · uninstall` (Python 3.10+, chỉ thư viện chuẩn). `install` chỉ
  dựng thư mục dữ liệu và **in** lệnh đăng ký host; `uninstall` không xoá dữ liệu.
- Mới: `samples/` — một ca mẫu tự soạn kèm `critique.json` kỳ vọng; `doctor` kiểm offline.

### Workspace mặc định `.work/`

Không đặt `WRITING_STUDIO_DATA` thì `.work/` trong thư mục đang mở là **workspace mặc định** (Git bỏ
qua), không còn là "lưới an toàn". Station riêng vẫn dùng như cũ, nay là tuỳ chọn; tài liệu có lệnh cho
cả Windows (`setx`) và macOS (`export`).

### Hạ tầng

- CI `.github/workflows/tests.yml`: Windows + macOS, Python 3.10 · 3.12 · 3.13, mọi nhánh, cả hai runner.
- `.codex-plugin/plugin.json` cho Codex; test khoá một số phiên bản ở bốn chỗ khai.
- `.gitignore` chặn file bí mật (`.env*` trừ `.env.example`, khoá, credential); test đọc Git index.
- Test chạy xanh trên máy chỉ có `requirements-dev.txt` (thiếu `underthesea`, `python-docx` thì tự bỏ
  qua kèm lý do).

## [0.2.1] — 2026-09-14

### Hợp đồng `writer_profile_ref` / `profile_used`: ba gốc, không phá vỡ tương thích

Hai trường là đường **tương đối**, agent tự ghép theo thứ tự: (1) gốc kho tri thức cá nhân
`OPCOS_BRAIN_PATH` → (2) gốc station `WRITING_STUDIO_DATA` → (3) gốc repo. Chuỗi không chứa `/` là slug
(`writers/<slug>/profile.yaml` ở station, rồi `shared/writers/<slug>/` trong repo). Giá trị cũ dạng
`writers/<slug>/profile.yaml` hay slug trần vẫn hợp lệ và phân giải như trước. Mô tả cập nhật ở
`context.schema.json`, `draft.schema.json`, lệnh `01-context`, `04-humanize` và cầu kho tri thức.

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
