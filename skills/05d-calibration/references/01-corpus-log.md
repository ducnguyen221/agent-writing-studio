# Sổ corpus hiệu chuẩn — datum và kế hoạch

> Chỉ số liệu tổng hợp + `sentence_id`. **Không chép văn bản thật** vào đây (luật `docs/EVALUATION_v1.md`
> và `fixtures/README.md`). Mỗi datum là một dòng của manifest `fixtures/manifest.schema.json` cộng
> kết quả Y5 tại thời điểm đo; văn bản nằm ở `.work/<case>/` (gitignored).

## 0. Cách đọc sổ này

- Trạng thái danh mục tell lúc ghi: **29 `candidate` / 0 `calibrated`** (`shared/rules/vi-ai-tells.json`).
  Khi 0 tell nào `calibrated`, Y5 chỉ được NOTE, không FLAG — nên `S` thấp trên bài máy là **kết quả
  kỳ vọng** của luật, không phải bằng chứng bài là người viết. Mọi datum trước mốc "tell đầu tiên lên
  `calibrated`" chỉ dùng để hiệu chuẩn, không dùng để phán xét.
- Ba cột "đúng / trượt / oan" đếm ở mức **câu**, đối chiếu cờ của Y5 với `machine_written_spans[]`
  của `draft.meta.json` (đối với bài từ studio) hoặc với `spans[]` của manifest (đối với mixed).
- `sentence_id` phải là ID của `sentences.json` **bản cuối** (sau Y4). Trước khi task P0 "sentence_id
  ổn định xuyên chuỗi" xong, mọi ID trong sổ này là ID map bằng trích dẫn, ghi rõ ở cột ghi chú.

## 1. Datum

### Datum #1 — `cot-b-ai-baitap` (30/08/2026)

Manifest (theo `fixtures/manifest.schema.json`):

| Khoá | Giá trị |
|---|---|
| `id` | `studio-essay-001-cot-b-ai-baitap` |
| `provenance` | `ai` |
| `language` | `vi` |
| `genre` | `essay` (structure `luan_de_phan_de`, profile `duc-nguyen` trạng thái `draft`) |
| `source_date` | `2026-08-30` |
| `ground_truth_level` | `generated_and_logged` |
| `generator` | `claude-fable-5` (Claude Code) — Y2 viết, Y4 cùng model sửa 9 nhát / 8 câu |
| `prompt_family` | `studio-cot-b` = Y1 `context.json` → outline 3 tầng → Y2 áp `anti_llm_defaults` của `essay.md` §2 → Y3 → Y4 |
| `evidence` | `.work/cot-b-ai-baitap/draft.meta.json` (45 span `origin: machine`), `polish.diff.json`, `y5-codex-blind.md` |
| `split` | `dev` |
| Độ dài | 994 từ · 47 câu thật (`sentences.json` chỉ 45 — xem §1.2) |

Kết quả Y5 **mù** (Codex qua bridge, chỉ thấy `polished.md`, `sealed_before_counters: true`):

| Đo | Giá trị |
|---|---|
| S | **2 / 100** |
| C | **2,0 %** |
| Nhãn | `low_signal` |
| FLAG / NOTE | 0 / 2 |
| Lớp 0-token `counters.py` | 0 tín hiệu (`template_repeats={}`, `vague_sources=[]`) |
| **Đúng** (cờ trúng câu máy) | **2** — polished `s0022` (T05 nguồn mơ hồ, G3) · `s0032` (phân đôi tuyệt đối, G1/G3) |
| **Trượt** (câu máy không cờ) | **43** (+ 2 câu bị script nuốt) |
| **Oan** | 0 (bài không có câu người → không đo được độ đặc hiệu) |
| Tỷ lệ phát hiện mức NOTE | 2/45 = 4,4 % (2/40 câu hợp lệ theo Codex = 5 %) |
| Tỷ lệ phát hiện mức FLAG | 0 % |
| Câu Y4 chạm bị cờ | 1/8 (`s0032`, vì nội dung sẵn có, không vì nhát sửa) |

Cả 2 NOTE trùng vùng Y3 đã thấy (F01 = evidence tiêu chí *evidence* không thành finding; F02 = bản sao
kề của Y3 F2 mà Y4 sửa `s0034` nhưng bỏ sót `s0032`). Y5 mù không tìm ra lỗi mới — nó tìm phần Y3/Y4
sửa chưa hết. Phân tích đầy đủ: `docs/results/self-audit-cot-B.md`.

#### 1.1 Ba chỗ máy-mà-không-cờ (người viết biết, Y5 không thấy) — ứng viên tell cho vòng sau

| # | Tật | `sentence_id` (polished) | Vì sao tell hiện tại không bắt | Ứng viên |
|---|---|---|---|---|
| 1 | Cụ-thể-**giả-định** đọc thành cụ-thể-**đã-sống**: toàn bài mở bằng "Giả sử…", 0 quan sát cá nhân | `s0002`–`s0004` (tình huống mở), lan cả bài | Rubric trục 5 gọi đích danh "không có một trải nghiệm hay quan sát cá nhân nào" nhưng không có tell nào mô tả; Codex đọc ví dụ cụ thể = dấu vết người | tell mới G3 `vi_du_gia_dinh_thay_trai_nghiem` — phản chứng: bài phương pháp luận đúng là dùng ví dụ giả định |
| 2 | Mở đoạn bằng câu hỏi tu từ 3–5 từ rồi tự trả lời, 3/6 đoạn | 2 câu **không có ID** (bị `min_chars=15` nuốt, Đ1 · Đ2) + 1 câu Đ5 | Không tell nào mô tả; `counters.py` chỉ đếm 5 khuôn cố định; Codex xếp câu ngắn vào `SKIP` — tật bị loại khỏi phép đo ở cả hai lớp | tell mới G1 `cau_hoi_tu_tu_mo_doan` + khuôn `TEMPLATES` "câu hỏi ≤ 5 từ mở đoạn" |
| 3 | Khuôn đối xứng phân đôi "X thì A; Y thì B" lặp 3 lần / 1.000 từ | `s0016` · `s0032` · `s0034` | T10/T31 nói bộ ba và câu chốt gương, không nói đối xứng phân đôi; `template_repeats` không có khuôn này; Codex bắt 1/3 như lỗi lập luận, không thấy là khuôn lặp | tell mới G1 `doi_xung_phan_doi_lap` + khuôn `TEMPLATES` "ai … thì …; ai … thì …" / "người … thì …" |

Ghi thêm, không tính: kết bài là phép đảo châm ngôn đã lưu truyền (`s0044`–`s0045`), T32 lẽ ra bắt khi
sinh; Y2 tự kiểm "passed" — tự kiểm T32 bởi chính model sinh câu là tự kiểm mù.

#### 1.2 Lỗi đo lường phát hiện nhờ datum này (phải sửa trước datum #2)

- `vi_segment.split_sentences(min_chars=15)` nuốt câm 2 câu < 15 ký tự → "45/45 máy" là số của script,
  văn bản có 47 câu. Task P0 ở `tasks.md`.
- Ba hệ đánh số câu trong một ca (`draft.md` 43 · `sentences.json` 45 · Codex tự đếm 46); map bằng
  trích dẫn, không map bằng ID. Task P0 `sentence_id` ổn định xuyên chuỗi.
- **Hệ quả cho sổ này:** ID ở §1.1 là ID của `sentences.json` bản cuối, map tay; không trích số
  "4,4 %" ra README/ARCHITECTURE cho tới khi hai task trên xong.

#### 1.3 Điều datum #1 nói và không nói

- **Nói:** trên văn 100 % máy đã qua Y2 (áp `anti_llm_defaults`) + Y4, bộ 29 tell `candidate` + lớp
  0-token cho tín hiệu ≈ 0. Đây là hằng đẳng thức của thiết kế "một danh sách, hai chiều" (Y2 tránh
  đúng cái Y5 tìm), không phải bằng chứng Y5 hỏng — nhưng cũng nghĩa là **S/C của Y5 trên sản phẩm của
  chính studio vô nghĩa cho phán xét**.
- **Không nói:** bất cứ điều gì về độ đặc hiệu (FPR trên người) hay về bài máy **không** qua studio.
  Một điểm dữ liệu, một thể loại, một model, không có đối chứng.

## 2. Kế hoạch corpus tối thiểu — trước khi bất kỳ tell nào lên `calibrated`

Mục tiêu của đợt tối thiểu **không phải** đo FPR (cần ≥ 30 bài người/thể loại, xem "Thang bằng chứng"
ở `SKILL.md`) mà là trả lời một câu hẹp: *tell nào bắt được văn máy ở mức NOTE khi Y2 đã áp
`anti_llm_defaults`, và bắt được ở thể loại nào?* — để quyết định tell nào đáng đầu tư corpus thật.

### 2.1 Nhánh `ai` — ≥ 5 bài máy từ studio (đa thể loại, có / không qua Y4)

| # | Thể loại | Cấu hình | Mục đích so sánh |
|---|---|---|---|
| A1 | `essay` | Y1→Y2→Y3→**Y4** | = datum #1, chạy lại **sau** khi P0 `min_chars` + `sentence_id` xong → cột đối chiếu sạch |
| A2 | `essay` | Y1→Y2→Y3, **không Y4** | tách hiệu ứng Y4: Y4 có xoá tín hiệu Y5 không (datum #1 nghi ngờ ở F2) |
| A3 | `essay` | Y2 **không** đọc `anti_llm_defaults` (prompt trần, cùng đề) | đối chứng "một danh sách, hai chiều": tell có bắt được máy khi máy không được cảnh báo không |
| A4 | `research` (structure `phan_tich_chinh_sach`) | Y1→Y2→Y3→Y4 | thể loại có baseline NOMINAL/TEMPLATES rộng nhất → đo Y5 còn nhìn được gì |
| A5 | `blog` | Y1→Y2→Y3→Y4 | thể loại duy nhất bật `retention`; T04/T18 baseline → đo tell G1 còn lại |
| A6 *(nếu kịp)* | `bao-cao-thuc-tap` | Y2 viết theo mẫu khoa, **không** có đơn vị thật | thể loại tắt gần hết counter; kiểm "cân bằng" ghi ở `bao-cao-thuc-tap.md` §5: Y5 mù có thấy gì ngoài khung không |

Mỗi bài: `draft.meta.json` đủ span · `sentences.json` bản cuối · Y5 do **model khác** chấm mù qua
bridge (Codex, hoặc agy) · ghi vào sổ này một bảng như datum #1. Cùng một `prompt_family` (`studio-cot-b`)
cho A1/A2/A4/A5/A6; A3 là `prompt_family` riêng (`bare-prompt`) — chia split theo họ prompt.

### 2.2 Nhánh `human` — ≥ 5 bài chính chủ (đối chứng oan)

- 2 bài chủ repo đã chỉ ở cổng Phase 4 (`profile_build.py`, `ground_truth_level: edit_history_verified`)
  + ≥ 3 bài nữa của chủ repo trước 2022 hoặc có lịch sử sửa (Brain / blog cũ), đa thể loại (`essay`,
  `blog`, `research`). Không dùng bài học viên.
- Chấm mù bởi cùng model đã chấm nhánh `ai`, cùng phiên bản rule. Số đo duy nhất có nghĩa ở cỡ này:
  **có câu người nào bị NOTE không, và bởi tell nào** → tell nào NOTE bài người ở n=5 đã là ứng viên tắt.

### 2.3 Điều kiện tiên quyết và thứ tự

1. P0 `vi_segment` không nuốt câu + `sentence_id` ổn định xuyên chuỗi (nếu không, cột đúng/trượt/oan
   không đối chiếu được — datum #1 đã phải map tay).
2. Khoá phiên bản `vi-ai-tells.json` + `counters.py` trước khi chạy A1–A6; 3 ứng viên tell ở §1.1 đưa
   vào dưới trạng thái `candidate`, **không** tạo finding.
3. Chạy `ai` trước, `human` sau, cùng một tuần; ghi mỗi datum ngay sau khi chấm.
4. Kết quả kỳ vọng để ra quyết định: tell nào NOTE ≥ 2/5 bài máy **và** 0/5 bài người → ứng viên corpus
   thật (≥ 30 + 30 theo `docs/EVALUATION_v1.md`); tell nào NOTE bài người → tắt hoặc chuyển vào
   `genre_baseline`. Ở n=5 không kết luận gì về FPR.

### 2.4 Ghi số, không ghi văn

Mỗi datum chỉ có: manifest · bảng S/C/nhãn/FLAG/NOTE · bảng đúng-trượt-oan · danh sách `sentence_id`
bị cờ kèm `rule_id`. `shared/scripts/evaluate.py` từ chối trường chứa nguyên văn — dùng nó để tổng hợp
khi có ≥ 5 datum mỗi nhánh.
