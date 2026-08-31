# KIẾN TRÚC — agent-writing-studio theo Ma trận 5×5

> Tài liệu kiến trúc và hiện trạng triển khai. Tài liệu này ánh xạ đủ 25 giao điểm thành cấu trúc
> skill cụ thể, chỉ rõ cái đã có / còn thiếu / thứ tự xây, và phần dùng chung.
>
> **Cập nhật 30/08/2026:** hiện trạng không còn là "một hàng" nữa — **cả năm hàng đã có `SKILL.md`**,
> và trục X có **9 hồ sơ thể loại** (5 `full` + 4 `partial`). Bảng skill và bảng 25 ô dưới đây đã được
> viết lại theo thực tế; các mục 2.x ghi thêm những thứ sinh ra trong lúc xây (`check_spans.py`,
> sidecar provenance, hai chế độ của Y5). Bản đọc cho người không kỹ thuật là `README.md`.
>
> Nguồn chân lý về tầm nhìn: ma trận 2 chiều 5 GIAI ĐOẠN × 5 LOẠI HÌNH của chủ repo
> (Intent&Persona → Co-writer → Critique&Grading → Humanize&Polish → Forensics&Integrity ×
> Blog · Bài luận/Thi cử · Nghiên cứu · Báo chí · Tiểu thuyết).

---

## 1. Quyết định kiến trúc trung tâm: **5 trục × 5 hồ sơ thể loại, KHÔNG phải 25 giao điểm thành skill**

25 giao điểm không được đẻ thành 25 skill. Lý do:

1. **Trục Y là quy trình, trục X là tham số.** Cách *chấm barem* một bài luận và một bài blog khác nhau
   ở *tiêu chí*, không khác ở *quy trình chấm*. Bản thân tài liệu tầm nhìn cũng đã thiết kế đúng như vậy:
   5 lệnh `/context /draft /critique /humanize /audit`, mỗi lệnh nhận cờ `--type`.
2. **Chống skill rác.** 25 skill = 25 chỗ drift, 25 mô tả cạnh tranh nhau khi agent chọn skill.
3. **Tri thức thể loại phải là DỮ LIỆU, không phải code**, để cả 5 giai đoạn cùng đọc một nguồn —
   nếu không, kỳ vọng thể loại của giai đoạn chấm (Y3) và giai đoạn giám định (Y5) sẽ lệch nhau.

Vậy: **mỗi hàng Y = một cửa vào công khai**; **mỗi cột X = một hồ sơ thể loại** (file Markdown có 5
mục đánh số theo giai đoạn). Một trục dài được phép tách thành skill con theo công đoạn, miễn cửa vào
vẫn duy nhất và thứ tự gọi được ghi rõ. Giao điểm (Yi, Xj) = skill Yi đọc mục §i của hồ sơ Xj.

### Bảng skill (tên chuẩn kebab-case, prefix số biểu thị thứ tự trục)

| Hàng | Skill | Vai | Trạng thái |
|---|---|---|---|
| Y1 | `01-context-architect` | Kiến trúc sư tư duy: intent, persona người viết & độc giả, nạp Brain, xuất context-pack | ✅ chạy thật ca `cot-b-ai-baitap` |
| Y2 | `02-cowriter` | Đồng sáng tác bản thảo theo cấu trúc thể loại, chống khuôn LLM ngay khi sinh | ✅ chạy thật (bài 994 từ, tự khai 100% máy) |
| Y3 | `03-critique` | Hội đồng phản biện: chấm barem thể loại, soi ngụy biện, plot holes | ✅ chạy thật trên bài hội thảo 6.307 chữ |
| Y4 | `04-humanizer` | Biên tập: de-nominalization, bơm nhịp câu, thuần Việt hoá — sửa đúng thứ Y5 đo | ✅ chạy thật (9 nhát / 8 câu, `facts_added=[]`) |
| Y5 | `05-forensics` | Router giám định: reading → scoring → reporting; **hai chế độ `blind` / `audit`** (§2.5) | ✅ **đã tách skill con** |
| Y5a | `05-forensics/05a-reading` | Đọc mù trực tiếp, finding có phản chứng | ✅ |
| Y5b | `05-forensics/05b-scoring` | S/C, khoảng vận hành, kiểm tra xung đột | ✅ |
| Y5c | `05-forensics/05c-reporting` | Báo cáo tiếng Việt, cách sửa, câu hỏi xác minh | ✅ |
| Y5d | `05-forensics/05d-calibration` | Corpus, false positive, ngôn ngữ/thể loại | ✅ |

Từ **v0.1.1** bốn sub-skill của Y5 nằm **bên trong** `skills/05-forensics/`, mỗi cái một thư mục con.
Cây `skills/` vì thế còn đúng **năm thư mục — một thư mục một trục**; mọi đường vào Y5 vẫn qua router,
router trỏ sub-skill bằng đường tương đối nên không phụ thuộc việc harness có tự dò skill lồng hay không.
| — | `writing-studio` *(tuỳ chọn)* | Router mỏng: nhận yêu cầu tự nhiên, định tuyến vào 1 trong 5 skill trên, quản lý thư mục ca | ❌ chưa có, xây cuối |

### Hồ sơ thể loại (`shared/genres/*.md`) — mỗi file đúng 5 mục

| Cột | File | §1 Intent | §2 Khung viết | §3 Rubric chấm | §4 Quy tắc humanize | §5 Chuẩn mực & must-have (forensics) |
|---|---|---|---|---|---|---|
| A | `blog.md` | Search intent, pain point, góc nhìn độc bản | Hook → giải quyết → CTA | Độ giữ chân, tính ứng dụng, mật độ giá trị | Giọng đàm thoại, năng lượng | Cliché mạng, cam kết nguyên bản |
| B | `essay.md` | Đề bài, luận đề, barem | 4–5 đoạn PEEL/TEEL | Barem Task Response, soi ngụy biện | Xoá danh từ hoá, liên từ tự nhiên | Quét dấu hiệu AI theo chuẩn thi cử |
| C | `research.md` | Research gap, khung lý thuyết, Brain | IMRAD | Phương pháp luận, độ tin cậy trích dẫn | Thuật ngữ chuẩn, khách quan | Liêm chính data, kiểm chứng trích dẫn |
| D | `journalism.md` | Góc nhìn sự kiện, các bên liên quan | Tháp ngược, nhân chứng | Khách quan, nguồn độc lập | Đanh gọn, xoá sáo rỗng | Kiểm soát trích dẫn, nguồn tin |
| E | `novel.md` | Character 3D, world-building, xung đột | 3 hồi, thắt/mở nút | Plot holes, nhất quán nhân vật, nhịp | Nhạc tính, show-don't-tell | Giữ dấu ấn tác giả, bản quyền |

Ngoài 5 cột gốc, `shared/genres/` chứa thêm **thể loại Việt Nam đặc thù** đã có thực đo từ v1
(mở rộng cột, không phá ma trận): `chinh-luan.md`, `de-cuong-nghien-cuu.md`, `bao-cao-thuc-tap.md`,
`sang-kien-kinh-nghiem.md`. Bảng "thể loại bắt buộc phải có gì" trong `references/01` trục 4 chính
là phôi của §5 các file này — v2 tách nó ra khỏi skill Y5 để cả Y2 (viết cho đủ) và Y3 (chấm cho đúng)
cùng dùng.

Bốn file đó ở trạng thái **`partial`**: chỉ có `## 5.`, dùng riêng cho trục 5. Đây là trạng thái hợp
lệ do `_schema.md` khai, không phải file viết dở — trục 1–4 không đọc file `partial` nào. Cách soạn
một hồ sơ mới: `docs/GENRES.md`.

### Trạng thái 25 giao điểm

- **Hàng Y5**: ✅ router + bốn skill con, thêm hai chế độ `blind` / `audit` (§2.5).
- **Hàng Y1–Y4**: ✅ đã có `SKILL.md` + `references/`, mỗi trục có ≥1 kịch bản nghiệm thu trong
  `tests/skills/scenarios/`, và cả bốn đã chạy trên ca thật.
- **Trục X**: 5 cột gốc `full` (đủ §1–§5) + 4 thể loại Việt Nam `partial` (chỉ §5) = **9 hồ sơ**.
  Ma trận thực tế vì thế là **5 × 9**, trong đó 5 × 5 = 25 ô có dữ liệu cho cả năm trục và 4 cột
  `partial` chỉ có ô hàng Y5.
- **Còn thiếu**: router `writing-studio`, và — quan trọng hơn nhiều — **corpus hiệu chuẩn**. 33 tell
  trong `vi-ai-tells.json` đang là 32 `candidate` + 1 `needs_corpus`, **0 `calibrated`**; theo luật
  của chính repo, trục 5 chưa được dùng tell nào để tạo finding. Ô nào của ma trận cũng chạy được,
  nhưng con số của hàng Y5 vẫn là con số chưa neo.
- Tài sản v1 dùng lại được: `vi_segment.py` (tách câu), `counters.py` (đo),
  `result.schema.json` (mẫu schema), toàn bộ `references/` (đặc biệt 01, 02, 03 — Y4 cần chúng
  ngang Y5, xem §4 dưới).

---

## 2. Phần dùng chung (`shared/`) — xương sống của cả 5 giai đoạn

### 2.1 Thư viện script

| File | Nguồn gốc | Ai dùng |
|---|---|---|
| `skills/05-forensics/scripts/vi_segment.py` | **CHƯA di trú** sang `shared/scripts/` — vẫn nằm ở trục 5, các trục khác import từ đó. Di trú (kèm shim `from shared… import *`) để ở PR riêng | Y2 (đo nhịp câu khi sinh), Y3, Y4, Y5 |
| `skills/05-forensics/scripts/counters.py` | như trên | Y4 (đo trước/sau khi sửa), Y5 |
| `shared/scripts/scoring.py` | **ĐÃ CÓ** — phép cộng tất định sau bản đọc mù: trần nhóm, khoảng vận hành, độ phủ C; không tự tạo finding | Y3, Y5 |
| `shared/scripts/profile_build.py` | **ĐÃ CÓ** — dựng writer profile từ ≥3 bài đã xác nhận chính chủ; đọc `samples/`, lấy **trung vị** làm vân tay; <3 bài ⇒ profile ở trạng thái `draft` | Y1, Y4, Y5 |
| `shared/scripts/check_spans.py` | **MỚI (P0, 30/08)** — cổng 0-token đối chiếu `machine_written_spans[].sentence_id` của `draft.meta.json` ↔ `sentences.json` bản cuối. Báo *id lệch*, *câu chưa khai*, và cờ **NGHI INDEX CŨ** khi bản tự khai viết theo hệ đánh số trước đó | Y5 (chế độ `audit`), người rà provenance |
| `shared/scripts/xuat_docx.py` | **MỚI (v0.1.1)** — md ➜ docx quy cách Việt (Times New Roman 13pt, giãn dòng 1,5, lề 2/2/3/2cm, heading đậm 14–16); parser tự viết, không thêm phụ thuộc md; `--provenance` chép sidecar sang **cạnh** bản giao. Không dựng bảng Markdown — giới hạn đã khai | Y4 (giao thành phẩm), lệnh `/giao-docx` |
| `shared/scripts/evaluate.py` | **ĐÃ CÓ** — gộp bản ghi đánh giá thành aggregate; chỉ nhận nhãn, rule id và span số, từ chối nguyên văn | 05d |
| `skills/04-humanizer/scripts/polish_check.py` | **MỚI** — cổng 0-token trước/sau khi biên tập: đọc `genre_baseline` trước khi in cột counter, gộp `warnings[]`, và **đòi sidecar provenance** cạnh bản giao (thiếu ⇒ exit 1) | Y4 |
| `skills/05-forensics/scripts/report.py` | **ĐÃ NÂNG** — renderer tùy chọn cho S/C, finding, phản chứng, cách sửa và câu hỏi | Y5 |

Nguyên tắc không đổi từ v1: **script chỉ ĐO, không kết luận**; đọc là việc của agent. Hai script mới
(`check_spans.py`, `polish_check.py`) giữ đúng nguyên tắc đó theo nghĩa chặt hơn: chúng **0 gọi mô
hình**, chỉ so tập hợp và đếm — nên kết quả của chúng tái lập được và không phụ thuộc phiên chạy.

### 2.2 Writer profile — hồ sơ vân tay người viết

`$WRITING_STUDIO_DATA/writers/<slug>/profile.yaml` (+ `samples/`) — **station ngoài repo** từ 31/08/2026,
vì đây là văn bản của người thật. Chưa đặt biến thì lui về `shared/writers/<slug>/` trong repo, chỗ đó
vẫn gitignored.

```yaml
name: duc-nguyen
built_from: 3            # số bài mốc chính chủ; <3 thì profile ở trạng thái draft
fingerprint:
  sentence_len: {mean: 21.3, cv: 0.51}     # đo bằng vi_segment + underthesea
  gloss_per_1000: 1.8
  nominal_per_1000: 9.2
  tone_style: new                           # hoà/hoà — kiểu bỏ dấu quen dùng
  pet_templates: ["vua_X_vua_Y"]            # khuôn tu từ ưa dùng (để Y5 KHÔNG phạt oan)
  known_typos: ["biến thế/biến thể"]
voice_notes: |
  Giọng thực chiến, câu ngắn xen dài, hay mở bằng câu hỏi...
```

Một profile, bốn người dùng:

- **Y1** nạp làm "persona người viết" của tài liệu tầm nhìn.
- **Y2** viết đúng giọng chính chủ thay vì giọng LLM mặc định.
- **Y4** đánh bóng **về phía giọng của tác giả**, không phải về "văn hay chung chung" — đây là điểm khác
  biệt với mọi công cụ máy-làm-mượt trên thị trường.
- **Y5** so bài nghi vấn với baseline chính chủ (*authorship verification* — bài toán "có phải văn của
  đúng người này không?" có cơ sở hơn hẳn "có phải AI không?", và `pet_templates` chống báo oan:
  người mê phép đối có hồ sơ chứng minh mình mê phép đối từ trước).

### 2.3 Kết nối `Brain/`

- Y1 **đọc** Brain (và thư mục dự án) để dựng bối cảnh; **không copy nội dung** vào repo — context-pack
  chỉ ghi **con trỏ** (đường dẫn + đoạn trích ngắn + lý do liên quan), đúng luật "1 fact = 1 nơi canonical".
- Chiều ngược: kết thúc một ca viết/giám định đáng nhớ, bài học đi về Brain/memory theo quy trình
  reflection chung của máy — **repo này không tự đẻ kho tri thức thứ hai**.

### 2.4 Hợp đồng dữ liệu giữa các giai đoạn (thư mục ca)

Mỗi ca một thư mục làm việc — `$WRITING_STUDIO_DATA/work/<case>/`, fallback `.work/<case>/` khi chưa đặt
biến — mỗi giai đoạn đọc sản phẩm giai đoạn trước, schema đặt tại `shared/schemas/`:

```
<work>/<case>/
├─ context.json                Y1 → intent, persona, genre, con trỏ Brain, ràng buộc
│                                   (shared/schemas/context.schema.json)
├─ draft.md                    Y2 → bản thảo
├─ draft.meta.json             Y2 → tự khai: cấu trúc dùng, các câu agent viết
│                                   (shared/schemas/draft.schema.json)
├─ sentences.json              hệ đánh số câu do studio sinh — nguồn `sentence_id` DUY NHẤT
├─ critique.json               Y3 → điểm barem + danh sách lỗi + việc phải sửa
│                                   (shared/schemas/critique.schema.json)
├─ polished.md                 Y4 → bản đã biên tập
├─ polished.provenance.json    Y4 → sidecar tự khai ĐI KÈM bản giao
│                                   (shared/schemas/provenance.schema.json)
├─ polish.diff.json            Y4 → từng sửa đổi: vị trí, tín hiệu nào, trước/sau
│                                   (shared/schemas/polish.schema.json)
├─ evidence.json               Y5 → gói bằng chứng
│                                   (skills/05-forensics/assets/result.schema.json)
└─ report.md                   Y5/Y3 → báo cáo render
```

Năm schema trong `shared/schemas/` (`context` · `draft` · `critique` · `polish` · `provenance`) là
những schema có **từ hai consumer trở lên**. `result.schema.json` vẫn nằm ở `skills/05-forensics/assets/`
vì tới giờ chỉ trục 5 đọc nó; chuyển sang `shared/` khi có consumer thứ hai, không chuyển trước.

**`sentence_id` là hợp đồng, không phải tiện ích.** `sentences.json` do studio sinh một lần; Y3, Y4,
Y5 **không được tự đếm câu**. Ca `cot-b` đã trả giá cho luật này: ba hệ đánh số khác nhau (43 / 45 /
46 câu) khiến bản tự khai phải map bằng trích dẫn thay vì bằng ID. `check_spans.py` là cổng kiểm.

Từ 31/08/2026 thư mục ca mặc định nằm ở **station** `$WRITING_STUDIO_DATA/work/`, ngoài repo hẳn —
chứa văn của người thật. `.work/` vẫn nằm trong `.gitignore` làm lưới an toàn cho ai chạy không có station.

### 2.5 Luật xung đột lợi ích (mới, bắt buộc)

1. **Y5 không giám định bài do chính pipeline này viết bằng cùng một model.** Self-recognition bias
   đã có tài liệu (`references/03` mục 1). Bài đi qua Y2/Y4 bằng Claude → nhánh giám định mù phải chạy
   model khác (Codex/Gemini qua bridge) hoặc tối thiểu ghi rõ xung đột vào `limitations`.
2. **Y4 và Y5 dùng chung định nghĩa tín hiệu** (`CHAM-DIEM.md` phần I) nhưng **Y4 không được xem điểm Y5 của
   bài đang sửa trước khi sửa xong** — nếu không sẽ tối ưu hoá vào thước đo (Goodhart), thước hỏng.
3. **`draft.meta.json` là bắt buộc khi Y2 tham gia**: studio tự khai phần máy viết. Cổng Y5 của chính
   studio mà không có bản tự khai thì mất tư cách nói về liêm chính.
4. **Y5 có hai chế độ, và chọn nhầm chế độ là đọc nhầm kết quả** *(mới, 30/08 — hệ quả của phép thử
   cột B; sổ đo nội bộ của đợt xây giữ số liệu thô)*:
   - **`blind`** (mặc định) — chỉ thấy văn bản, kèm `sentences.json` để neo finding, **không** kèm
     `draft.meta.json`. Dùng cho tài liệu từ ngoài, cho hiệu chuẩn, cho đối chứng độc lập.
   - **`audit`** — bật khi thư mục ca có **cả** `draft.meta.json` lẫn `sentences.json`. Đọc hai file
     đó **sau** khi `05a-reading` đã khoá bản đọc mù, rồi đối chiếu bản tự khai với văn bản và báo
     câu máy chưa khai; phần đối chiếu ID chạy bằng `check_spans.py`, 0 gọi mô hình. Kết quả là một
     **báo cáo liêm chính, không phải điểm**.

   Lý do phải tách: bài 100% máy do chính studio viết, chấm mù, cho `S=2` · `C=2,0%` · `low_signal` ·
   **0 FLAG** · 2 NOTE (4,4% số câu). Trục 2 tránh đúng danh mục mà trục 5 dùng để soi — một danh
   sách, hai chiều — nên **trên văn đã qua studio, `low_signal` mù là kết quả kỳ vọng, không phải
   bằng chứng**. Không lấy S/C mù của sản phẩm studio ra phán xét.
5. **Provenance đi theo bản giao, không ở lại trong thư mục ca** *(mới, 30/08)*: khi xuất
   `polished.md`, Y4 bắt buộc kèm sidecar `<tên bản giao>.provenance.json` (hoặc footer
   `<!-- provenance: {…} -->` thay thế). `polish_check.py` thiếu file này thì **exit 1**. Lý do:
   ranh giới đạo đức của Y4 phải **quan sát được từ sản phẩm**, không chỉ từ `polish.diff.json` mà
   người nhận bài không bao giờ thấy.

---

## 3. Ranh giới với hai studio còn lại

| | `agent-design-studio` | `agent-voice-studio` | `agent-writing-studio` |
|---|---|---|---|
| Sở hữu | Hình ảnh, layout, banner, UI | Giọng nói, voice clone, audio | **Chữ viết** — từ tư duy đến nghiệm thu |
| Giao diện sang nhau | Bài blog xong → gọi design-studio làm cover/infographic (input: `polished.md` + `context.json`) | Tiểu thuyết/blog xong → voice-studio đọc thành audio (input: `polished.md`, đã qua cổng Y5) | Nhận brief hình/tiếng chỉ ở mức *mô tả bằng chữ* |
| KHÔNG làm | Không viết caption dài, không chấm văn bản | Không sửa văn phong kịch bản | **Không render ảnh, không sinh audio** — kể cả "tiện tay" |

Ba repo cùng chuẩn: public MIT (LICENSE ở gốc repo), `skills/<kebab-case>/SKILL.md + references/ + scripts/ + assets/`,
cài bằng `cp -r` vào `~/.claude/skills/`. Điểm nối kỹ thuật duy nhất là **file** (markdown/json
theo schema), không import code chéo repo.

---

## 4. Thứ tự xây — từ máy đo lên máy viết

Nguyên tắc: **xây tầng đo trước tầng sinh**. Chưa có máy đo đáng tin thì máy viết không tự kiểm được
mình, và mọi lời hứa "Anti-AI-bias by design" của Y2 là khẩu hiệu suông.

| # | Việc | Vì sao đứng ở đây |
|---|---|---|
| 0 | `docs/` (tài liệu này + `CHAM-DIEM.md`) | Khung trước, code sau |
| 1 | **`fixtures/`** — ≥10 human + ≥10 AI + 10 mixed cho thể loại đầu tiên (chính luận/bài luận) | Việc quan trọng nhất của cả repo, v1 đã tự thừa nhận. Mọi con số của `CHAM-DIEM.md` đứng hay đổ ở đây |
| 2 | `shared/scripts/scoring.py` + nâng `05-forensics` xuất điểm tổng & %C theo `CHAM-DIEM.md` | Trả đúng món nợ chủ repo yêu cầu; chạy lại được trên fixtures ngay khi có |
| 3 | 5 + 4 hồ sơ thể loại `shared/genres/` (viết **§5 trước**, rồi §3) | §5 phục vụ G4 của Y5 đang chạy thật; §3 mở đường Y3 |
| 4 | `03-critique` (Y3) | Tái dùng scoring engine + §3; khác Y5 ở rubric (chất lượng vs dấu hiệu) chứ không ở máy móc |
| 5 | `04-humanizer` (Y4) | Nghịch đảo của Y5: mỗi tín hiệu trong `CHAM-DIEM.md` là một mục sửa; vòng kiểm = chạy lại counters trước/sau, ghi `polish.diff.json` |
| 6 | `profile_build.py` + `01-context-architect` (Y1) | Writer profile + Brain — cần trước khi cho máy viết |
| 7 | `02-cowriter` (Y2) | Cuối cùng, vì cần đủ: context (Y1), khung (§2), giọng (profile), và cổng ra (Y5) để tự nghiệm thu |
| 8 | Router `writing-studio` *(tuỳ chọn)* | Chỉ khi 5 skill đã ổn định — đúng thang nâng cấp skill |

**Đã đi tới đâu (30/08/2026):** bước 0 và 2–7 xong; bước 8 chưa (và chưa nên). **Bước 1 —
`fixtures/` — vẫn chưa làm, và đó là món nợ lớn nhất còn lại.** Thứ tự "xây tầng đo trước tầng sinh"
vì thế đã bị đảo một nửa: máy viết có rồi, máy đo có rồi, nhưng **thước chưa được neo**. Hệ quả cụ
thể: 0/33 tell `calibrated` ⇒ trục 5 chỉ được NOTE, không được tạo finding; và ngưỡng trong
ngưỡng trong `CHAM-DIEM.md` vẫn là mốc n=1÷3. Datum hiệu chuẩn số 1 đã có
(`skills/05-forensics/05d-calibration/references/01-corpus-log.md`), cần ≥5 bài máy từ studio + ≥5 bài chính chủ
chấm mù bởi model khác trước khi bất kỳ tell nào lên `calibrated`.

Riêng Y4 có một cảnh báo thiết kế phải ghi ngay từ đầu: **Y4 chính là một công cụ máy-làm-mượt** —
thứ mà `references/06` (bài học RAID) chỉ ra là phá được phần lớn detector. Trong cùng một repo, Y4 và Y5
là hai lưỡi của một con dao. Ranh giới đạo đức: Y4 chỉ chạy trên bản thảo có `draft.meta.json`
(nguồn gốc tự khai), và output Y4 luôn kèm ghi chú "đã qua stylometric polish" trong metadata —
studio làm **văn hay hơn**, không làm **dịch vụ né máy chấm**.

---

## 5. Cây thư mục v2 đầy đủ

Đánh dấu: ✅ đã có trên đĩa · ❌ chưa có, giữ trong cây vì là đích đến.

```
agent-writing-studio/
├─ README.md                          # ✅ viết lại 30/08 cho người không kỹ thuật
├─ LICENSE                            # ✅ MIT — Copyright 2026 Nguyễn Quang Đức
├─ index.html                         # ✅ trang giới thiệu tĩnh, mở thẳng bằng trình duyệt
├─ .gitignore                         # ✅ .work/ · fixtures/** · *.docx · shared/writers/**
│
├─ docs/
│  ├─ KIEN-TRUC.md                    # ✅ (file này)
│  ├─ CHAM-DIEM.md                    # ✅ thang S/C + cách đo + mẫu báo cáo (gộp 3 file cũ, 31/08)
│  ├─ GENRES.md                       # ✅ cách soạn hồ sơ thể loại mới
│  ├─ agent-writing-studio.md         # ✅ tầm nhìn gốc của chủ repo
│  ├─ results/                        # ✅ kết quả đo thật (self-audit-cot-B.md)
│  └─ plans/                          # ✅ spec · tasks · nhật ký cổng từng đợt
│
├─ shared/
│  ├─ scripts/
│  │  ├─ scoring.py                   # ✅ hiện thực phép cộng của CHAM-DIEM.md
│  │  ├─ profile_build.py             # ✅ dựng writer profile
│  │  ├─ check_spans.py               # ✅ cổng 0-token: spans ↔ sentences
│  │  ├─ evaluate.py                  # ✅ gộp bản ghi đánh giá thành aggregate
│  │  ├─ xuat_docx.py                  # ✅ md ➜ docx quy cách Việt (v0.1.1)
│  │  ├─ vi_segment.py                # ❌ chưa di trú — vẫn ở skills/05-forensics/scripts/
│  │  └─ counters.py                  # ❌ chưa di trú — như trên
│  ├─ schemas/
│  │  ├─ context.schema.json          # ✅
│  │  ├─ draft.schema.json            # ✅ (có `quote` tuỳ chọn để đối chiếu nội dung, không chỉ ID)
│  │  ├─ critique.schema.json         # ✅ (`must_fix[].owner` enum: 02-cowriter / 04-humanizer / author)
│  │  ├─ polish.schema.json           # ✅ (`warnings[]` nhận object có `route_to`)
│  │  └─ provenance.schema.json       # ✅ sidecar đi theo bản giao
│  ├─ genres/                         # ✅ 9 hồ sơ + _schema.md
│  │  ├─ blog.md · essay.md · research.md · journalism.md · novel.md          (full)
│  │  └─ chinh-luan.md · de-cuong-nghien-cuu.md · bao-cao-thuc-tap.md
│  │     · sang-kien-kinh-nghiem.md                                           (partial, chỉ §5)
│  ├─ rules/                          # ✅ vi-ai-tells.json · forensics-scoring-v3.json
│  │                                  #    · forensic-rule-registry.json
│  └─ writers/                        # ✅ CHỈ schema + README; dữ liệu ở station ngoài repo
│     └─ README.md                    # cách dựng profile, luật riêng tư, hợp đồng station
│
├─ skills/
│  ├─ 01-context-architect/            # ✅ Y1 — SKILL.md + 4 references
│  ├─ 02-cowriter/                     # ✅ Y2 — SKILL.md + references
│  ├─ 03-critique/                     # ✅ Y3 — SKILL.md + references (lăng kính, ngụy biện, barem)
│  ├─ 04-humanizer/                    # ✅ Y4 — SKILL.md + references + scripts/ + assets/
│  └─ 05-forensics/                    # ✅ Y5 — router agent-first, hai chế độ blind/audit
│     ├─ 05a-reading/                  # ✅ đọc mù, finding và phản chứng
│     ├─ 05b-scoring/                  # ✅ S/C và khoảng vận hành
│     ├─ 05c-reporting/                # ✅ báo cáo, cách sửa, câu hỏi
│     ├─ 05d-calibration/              # ✅ corpus và hiệu chỉnh (có 01-corpus-log.md, datum #1)
│     ├─ references/                   # ✅ 11 tài liệu dài của trục 5
│     └─ scripts/                      # ✅ extract · vi_segment · counters · report
│                                      # ❌ writing-studio/ — router toàn studio (xây cuối, tuỳ chọn)
│
├─ commands/                          # ✅ 7 lệnh chạy lẻ từng bước (v0.1.1; đánh số theo trục v0.1.2)
├─ tests/                             # ✅ 372 test: forensics/ · genres/ · shared/ · skills/
└─ fixtures/                          # ✅ gitignored trừ README; hiện CÒN RỖNG
```

---

## 6. Những gì v2 KHÔNG làm

- Không chạy model ML nặng, không GPU — giữ triết lý v1 (tầng model như VietBinoculars ghi nhận
  ở `references/06` là hướng mở rộng, không phải phần thân).
- Không tự kết luận kỷ luật ai — mọi cổng Y5 giữ nguyên "người quyết định".
- Không lưu bài của người thật vào git — từ 31/08/2026 chúng nằm hẳn ở station `$WRITING_STUDIO_DATA`
  ngoài repo; `.work/`, `fixtures/`, `shared/writers/` vẫn gitignored làm lưới an toàn.
- Không đẻ 25 skill, không đẻ router trước khi 5 skill sống thật.
