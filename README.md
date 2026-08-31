# agent-writing-studio

**Một xưởng viết bằng AI agent cho chữ tiếng Việt: từ lúc chưa có chữ nào đến lúc nghiệm thu bản giao.**

Repo này không phải một ứng dụng, không có nút bấm và không chạy trên máy chủ nào. Nó là **một bộ
hướng dẫn cho AI agent** (Claude Code, Codex, Antigravity) — dạng thư mục chứa file văn bản mà agent
đọc rồi làm theo. Bạn chép các thư mục đó vào chỗ agent tìm được, sau đó nói chuyện với agent bằng
tiếng Việt bình thường.

> **Thuật ngữ ngay từ đầu.** *Agent* = trợ lý AI có thể đọc file trên máy bạn và chạy lệnh, không chỉ
> chat. *Skill* (kỹ năng) = một thư mục có file `SKILL.md` mô tả cho agent biết **khi nào** dùng và
> **làm theo trình tự nào**; agent tự nạp khi gặp đúng tình huống. Toàn bộ repo này là 9 skill cộng
> với dữ liệu dùng chung.

---

## 1. Repo này làm gì (đọc trong 5 phút)

Viết một bài tử tế có năm việc, và bốn trong năm việc đó **không phải là gõ chữ**:

| Giai đoạn | Tên trong repo | Việc thật sự làm |
|---|---|---|
| **1. Bối cảnh** | `01-context-architect` | Hỏi cho ra đề bài, luận đề, ai đọc, ai chấm, bằng chứng đang có trong tay. Chưa gỡ hết thì **dừng, không viết**. |
| **2. Viết nháp** | `02-cowriter` | Dựng dàn ý ba tầng, **chờ bạn duyệt**, rồi mới viết văn xuôi — kèm bản tự khai câu nào do máy viết. |
| **3. Phản biện** | `03-critique` | Chấm từng tiêu chí riêng theo barem của thể loại, soi ngụy biện và chỗ khẳng định không có gì đỡ. **Không có điểm tổng** — điểm tổng che mất chỗ yếu. |
| **4. Biên tập** | `04-humanizer` | Sửa văn về phía giọng của chính tác giả. Cấm thêm hay bớt số liệu, cấm đổi mức mạnh của khẳng định. |
| **5. Giám định** | `05-forensics` | Đọc bài, chỉ ra chỗ có dấu hiệu do AI viết, kèm phản chứng và câu hỏi để xác minh. |

Năm việc đó là **trục Y** (năm giai đoạn, chạy tuần tự). Nhưng một bài luận thi và một chương tiểu
thuyết không chấm giống nhau, không cấm giống nhau. Phần "khác nhau theo thể loại" nằm ở **trục X**:
mỗi thể loại là **một file dữ liệu**, không phải một skill riêng.

### Ai dùng, dùng khi nào

- **Giảng viên, biên tập viên** — cần một bản phản biện có vị trí, câu trích và câu hỏi để hỏi lại
  tác giả (giai đoạn 3), hoặc cần nhìn xem bài nộp có dấu hiệu máy viết không (giai đoạn 5).
- **Người viết** (nghiên cứu, chính luận, blog, tiểu thuyết) — cần một người đối thoại ép mình nói rõ
  luận đề trước khi viết (giai đoạn 1–2), và một biên tập viên không làm mất giọng mình (giai đoạn 4).
- **Người quản lý chương trình đào tạo** — cần một quy trình có **vết làm việc**, để nói được bài này
  đã đi qua những bước nào và ai (hay cái gì) viết phần nào.

**Không dùng repo này để** kết tội ai đó gian lận (xem mục 5), hay để "né máy chấm AI" — mục 5 giải
thích vì sao đó là ranh giới cứng chứ không phải lời khuyên.

---

## 2. Ma trận 5 trục × 9 hồ sơ thể loại — và trạng thái thật

Tài liệu tầm nhìn gốc của chủ repo (`docs/agent-writing-studio.md`) mô tả một ma trận **5 giai đoạn ×
5 loại hình = 25 giao điểm**. Bản triển khai giữ nguyên ma trận đó nhưng **không đẻ ra 25 skill**.

### Vì sao là "5 skill × dữ liệu thể loại", không phải 25 skill

Cách *chấm* một bài luận và một bài blog khác nhau ở **tiêu chí**, không khác ở **quy trình chấm**.
Nếu tách thành 25 skill thì:

- có 25 chỗ để lệch nhau: kỳ vọng thể loại của người chấm (giai đoạn 3) và của người giám định
  (giai đoạn 5) sẽ trôi mỗi nơi một kiểu;
- agent phải chọn giữa 25 mô tả cạnh tranh nhau, và sẽ chọn sai;
- thêm một thể loại mới nghĩa là viết thêm 5 skill.

Vậy nên: **thể loại là dữ liệu, skill là logic.** Mỗi thể loại là **một file Markdown** trong
`shared/genres/` có đúng năm mục đánh số — mục §1 cho giai đoạn 1, §2 cho giai đoạn 2, và cứ thế.
Giao điểm (giai đoạn *i*, thể loại *j*) = skill *i* đọc mục §*i* của file thể loại *j*. Thêm thể loại
mới = thêm **một file**, không sửa dòng code nào. Không skill nào được phép viết `if genre == "novel"`.

### Trạng thái từng trục

*(lấy từ nhật ký cổng trong `docs/plans/2026-08-30-skills-1-4-genres/tasks.md`)*

| Trục | Skill | Trạng thái | Đã chạy thật trên ca nào |
|---|---|---|---|
| Y1 | `01-context-architect` | ✅ có `SKILL.md` + 4 tài liệu tham chiếu | ca `cot-b-ai-baitap` — đề bài về AI trong bài tập về nhà |
| Y2 | `02-cowriter` | ✅ | cùng ca trên: bài 994 từ, tự khai 100% máy viết |
| Y3 | `03-critique` | ✅ | bài hội thảo thật 6.307 chữ, và ca `cot-b` |
| Y4 | `04-humanizer` | ✅ | ca `cot-b`: 9 nhát sửa trên 8 câu |
| Y5 | `05-forensics` | ✅ router + 4 skill con | ca hội thảo; ca `cot-b` chấm mù bởi model khác |
| Y5a | `05a-reading` | ✅ | đọc mù, gán nhãn từng câu, mỗi nhận định kèm phản chứng |
| Y5b | `05b-scoring` | ✅ | tính hai con số S và C sau khi bản đọc đã khoá |
| Y5c | `05c-reporting` | ✅ | báo cáo tiếng Việt: vị trí, cách sửa, câu hỏi xác minh |
| Y5d | `05d-calibration` | ✅ | quản lý bộ bài mẫu, đo báo oan, hiệu chuẩn ngưỡng |

Chín skill, **không có** router tổng — router chỉ nên xây khi năm trục đã ổn định, và hiện chưa tới lúc.

### Chín hồ sơ thể loại

`full` = có đủ năm mục, dùng được cho cả năm trục. `partial` = **chỉ có §5**, dùng riêng cho giai
đoạn giám định — đây là những thể loại đã phải giám định thật trước khi kịp soạn phần viết.

| Hồ sơ | Trạng thái | Ghi chú |
|---|---|---|
| `essay.md` — bài luận, bài thi | `full` | hồ sơ mẫu, viết đầu tiên |
| `research.md` — nghiên cứu, báo cáo chuyên sâu | `full` | có cả khung IMRAD lẫn khung phân tích chính sách |
| `blog.md` — blog, thought leadership | `full` | |
| `journalism.md` — báo chí, phân tích chuyên luận | `full` | |
| `novel.md` — tiểu thuyết, truyện dài kỳ | `full` | |
| `chinh-luan.md` — chính luận | `partial` | thể loại Việt Nam đặc thù |
| `de-cuong-nghien-cuu.md` — đề cương nghiên cứu sinh | `partial` | |
| `bao-cao-thuc-tap.md` — báo cáo thực tập | `partial` | |
| `sang-kien-kinh-nghiem.md` — sáng kiến kinh nghiệm | `partial` | |

Bốn hồ sơ cuối là **mở rộng cột**, không phá ma trận: chúng có thật trong đời sống viết tiếng Việt và
đã có ca giám định thật, nên có mặt trước khi tới lượt soạn phần viết.

Muốn thêm một thể loại? Xem `docs/GENRES.md`.

---

## 3. Cài và gọi

### Cài

Chép thư mục `skills/` vào nơi agent tìm skill. Chép cả chín, vì các skill gọi lẫn nhau.

```bash
# Claude Code
cp -r skills/* ~/.claude/skills/

# Codex
cp -r skills/* ~/.codex/skills/
```

```powershell
# Windows PowerShell — Claude Code
Copy-Item -Recurse skills\* $HOME\.claude\skills\
```

Thư viện Python phụ trợ (**đều tuỳ chọn**, đều nhẹ, đều chạy CPU — không cần card đồ hoạ):

```bash
pip install underthesea python-docx pymupdf jsonschema pyyaml
```

`underthesea` quan trọng nhất: tiếng Việt không tách từ bằng khoảng trắng, thiếu nó thì các bộ đếm tự
hạ độ tin cậy của chính mình. Không cài gì cả thì agent vẫn đọc, vẫn chấm, vẫn báo cáo được — script
trong repo chỉ là **lớp kiểm chứng**, không phải bộ não.

⚠️ **Repo cần nằm trên máy, không chỉ nằm trong `~/.claude/skills/`.** Các skill đọc dữ liệu dùng
chung ở `shared/` (hồ sơ thể loại, quy tắc, schema). Hãy nói cho agent biết repo nằm ở đâu, ví dụ:
*"repo agent-writing-studio ở `C:\Users\...\Code\agent-writing-studio`"*.

### Gọi từng trục

Không có cú pháp lệnh riêng. Nói bằng tiếng Việt, agent tự chọn skill:

| Muốn gì | Nói với agent | Trục chạy |
|---|---|---|
| Chuẩn bị viết | *"Tôi cần viết một bài luận về X. Dựng bối cảnh giúp tôi trước đã."* | Y1 |
| Viết nháp | *"Đã có `context.json` ở `.work/bai-x/`. Dựng dàn ý rồi viết nháp."* | Y2 |
| Phản biện | *"Chấm giúp bài này theo hồ sơ `research`, chỉ chỗ lập luận hổng."* | Y3 |
| Biên tập | *"Biên tập bản nháp này, giữ nguyên số liệu và trích dẫn."* | Y4 |
| Giám định | *"Bài nộp này có dấu hiệu AI viết không? Đọc và báo cáo."* | Y5 |

Nói rõ **thể loại** thì tốt (`essay`, `research`, `blog`, `journalism`, `novel`, `chinh-luan`,
`de-cuong-nghien-cuu`, `bao-cao-thuc-tap`, `sang-kien-kinh-nghiem`); không nói thì agent sẽ hỏi.

### Chạy trọn chuỗi Y1 → Y5

Năm trục nối với nhau bằng **file**, không bằng trí nhớ hội thoại. Mỗi bài một thư mục
`.work/<tên-ca>/`, mỗi giai đoạn đọc sản phẩm của giai đoạn trước:

```
.work/bai-cua-toi/
├─ context.json                 Y1 → đề bài, luận đề, chân dung độc giả, con trỏ tài liệu nền
├─ draft.md                     Y2 → bản nháp
├─ draft.meta.json              Y2 → tự khai: câu nào máy viết, dàn ý đã duyệt chưa
├─ sentences.json               hệ đánh số câu dùng chung cho cả chuỗi (Y3/Y4/Y5 không tự đếm câu)
├─ critique.json                Y3 → điểm từng tiêu chí + danh sách việc phải sửa
├─ polished.md                  Y4 → bản đã biên tập
├─ polished.provenance.json     Y4 → bản tự khai nguồn gốc ĐI KÈM bản giao (xem mục 5)
├─ polish.diff.json             Y4 → từng nhát sửa: vị trí, lý do, trước và sau
├─ evidence.json                Y5 → gói bằng chứng giám định
└─ report.md                    báo cáo cho người đọc
```

`.work/` **không bao giờ được commit** — nó chứa bài của người thật. `.gitignore` đã chặn sẵn.

Ba cổng cứng trong chuỗi, qua được mới đi tiếp:

1. Y1 còn điều kiện chưa gỡ được → **dừng và hỏi**, không chuyển sang Y2.
2. Y2 chưa được duyệt dàn ý → **không viết văn xuôi**.
3. Y4 phát hiện mình đã thêm hoặc bớt một dữ kiện → **trả lại bản gốc**, không sửa tiếp.

---

## 4. Cây thư mục

```
agent-writing-studio/
├─ README.md                    file bạn đang đọc — bản triển khai
├─ requirements-dev.txt         thư viện để chạy test
│
├─ skills/                      CHÍN SKILL — thứ được chép sang ~/.claude/skills/
│  ├─ 01-context-architect/       Y1 · phỏng vấn bối cảnh, chân dung người viết và độc giả
│  ├─ 02-cowriter/                Y2 · dàn ý ba tầng → duyệt → viết → tự khai nguồn gốc
│  ├─ 03-critique/                Y3 · chấm từng tiêu chí, 13 lăng kính, 13 loại ngụy biện
│  ├─ 04-humanizer/               Y4 · biên tập về phía giọng tác giả, có vùng cấm sửa
│  ├─ 05-forensics/               Y5 · router giám định + tài liệu chống báo oan
│  ├─ 05a-reading/                  đọc mù, gán nhãn từng câu, mỗi nhận định kèm phản chứng
│  ├─ 05b-scoring/                  tính S và C sau khi bản đọc đã khoá
│  ├─ 05c-reporting/                viết báo cáo: vị trí, cách sửa, câu hỏi xác minh
│  └─ 05d-calibration/              dựng bộ bài mẫu, đo tỷ lệ báo oan, chỉnh ngưỡng
│     (mỗi skill: SKILL.md ≤550 từ + references/ tài liệu dài + scripts/ + assets/)
│
├─ shared/                      DỮ LIỆU DÙNG CHUNG — nhiều skill cùng đọc một nguồn
│  ├─ genres/                     9 hồ sơ thể loại + _schema.md (hợp đồng hình dạng file)
│  ├─ schemas/                    5 schema JSON: context · draft · critique · polish · provenance
│  ├─ rules/                      quy tắc máy đọc được: 33 dấu hiệu tiếng Việt, bảng chấm điểm
│  ├─ scripts/                    script dùng lại: đo, đối chiếu, dựng hồ sơ người viết
│  └─ writers/                    hồ sơ giọng văn của người thật — GITIGNORED, chỉ commit hướng dẫn
│
├─ tests/                       314 test — canh cấu trúc skill, hình dạng dữ liệu, liên kết
│  ├─ forensics/                  hành vi trục 5 (có từ bản v1)
│  ├─ genres/                     hồ sơ thể loại đúng schema, slug khớp hai chiều
│  ├─ shared/                     schema, quy tắc, hàng rào de-name
│  └─ skills/                     bốn trục viết + kịch bản nghiệm thu dạng văn bản
│
├─ docs/
│  ├─ ARCHITECTURE_v2.md          kiến trúc: vì sao 5 skill chứ không 25, ai đọc gì của ai
│  ├─ GENRES.md                   cách soạn một hồ sơ thể loại mới
│  ├─ SCORING_v2.md               hệ chấm điểm S và C, bảng ánh xạ số đo → điểm
│  ├─ REPORT_TEMPLATE_v2.md       mẫu báo cáo giám định
│  ├─ EVALUATION_v1.md            cách đo độ chính xác khi đã có bộ bài mẫu
│  ├─ agent-writing-studio.md     tầm nhìn gốc của chủ repo (ma trận 5×5)
│  ├─ results/                    kết quả đo có thật, không phải ví dụ minh hoạ
│  └─ plans/                      hồ sơ từng đợt làm: spec, task, nhật ký cổng
│
├─ fixtures/                    bộ bài mẫu để hiệu chuẩn — GITIGNORED, hiện còn rỗng
└─ .work/                       thư mục làm việc từng ca — GITIGNORED, chứa bài người thật
```

---

## 5. Ranh giới đạo đức — phần quan trọng nhất của repo này

Repo này vừa **viết** (trục 2, trục 4) vừa **giám định nguồn gốc** (trục 5), bằng **cùng một danh mục
dấu hiệu**. Đó là một xung đột lợi ích có thật, và chúng tôi đã đo nó thay vì hứa suông.

### Phép thử: cho studio viết một bài 100% bằng máy, rồi bắt chính studio chấm mù

Ca `cot-b-ai-baitap`, ngày 30/08/2026 — số liệu đầy đủ ở `docs/results/self-audit-cot-B.md`:

- Trục 2 viết trọn bài, **không một chữ nào của người**, và tự khai đúng như vậy.
- Trục 5 chấm **mù**, do một model khác (Codex, không phải model đã viết), chỉ nhìn thấy bản văn chứ
  không nhìn thấy bản tự khai.

Kết quả:

| Đo cái gì | Con số |
|---|---|
| Điểm dấu hiệu S | **2/100** → nhãn `low_signal`, nghĩa là *không làm gì, không lưu hồ sơ nghi vấn* |
| Câu bị đánh dấu ở mức **NOTE** (đáng ghi chú) | **2/45 = 4,4%** |
| Câu bị đánh dấu ở mức **FLAG** (đáng nghi) | **0 = 0%** |
| Bắt oan câu của người | 0 — nhưng bài không có câu nào của người để mà oan |
| Lớp đếm tự động (0 gọi mô hình) | **0 tín hiệu** |

*(Con số 4,4% tính trên 45 câu — cách đếm câu tại thời điểm đo. Sau đó một lỗi nuốt câu ngắn đã được
sửa và bài có 47 câu; tính lại là 2/47 = 4,3%. Chúng tôi giữ con số gốc kèm ghi chú thay vì làm tròn
cho đẹp.)*

### Đọc con số này cho đúng

Một bài **100% do máy viết**, đi qua đúng quy trình của studio, được chính studio chấm mù, cho kết quả
**"không có dấu hiệu"**. Đó **không** phải lỗi cài đặt. Trục 2 tránh đúng danh mục mà trục 5 dùng để
soi — cùng một file `vi-ai-tells.json`, một danh sách dùng theo hai chiều. Văn viết bằng cách tránh
danh sách thì danh sách ấy không thấy nó. Đây là **hằng đẳng thức, không phải một lỗ hổng bị lợi dụng**.

Vậy nên hai luật:

> **Trên văn đã đi qua studio này, `low_signal` khi chấm mù là KẾT QUẢ KỲ VỌNG, không phải bằng chứng.**
> Ai đọc điểm thấp thành "bài này do người viết" là đọc sai.

> **Liêm chính đến từ provenance đi theo sản phẩm — `draft.meta.json` và sidecar
> `polished.provenance.json` — chứ không đến từ điểm của máy giám định.**
> *Provenance* = bản tự khai nguồn gốc: câu nào máy viết, câu nào người viết, bài đã qua biên tập máy
> hay chưa. *Sidecar* = file đi kèm bản giao, nằm cạnh nó, không phải thứ ở lại trong máy người viết.

Vì thế trục 5 có **hai chế độ**, và chọn nhầm chế độ là đọc nhầm kết quả:

| Chế độ | Nhìn thấy gì | Dùng khi nào |
|---|---|---|
| `blind` (mặc định) | chỉ bản văn và hệ đánh số câu | tài liệu **từ ngoài** vào; hiệu chuẩn; đối chứng độc lập |
| `audit` | thêm `draft.meta.json` — **sau khi** bản đọc mù đã khoá | văn **từ chính studio**: đối chiếu bản tự khai với văn bản, báo câu máy viết mà chưa khai |

Chế độ `audit` trả về **báo cáo liêm chính**, không trả về điểm. Đó mới là câu hỏi đúng: *bản tự khai
có khớp với bản văn không*, chứ không phải *máy có đoán ra được không*.

### Bốn luật còn lại, không thương lượng

| | |
|---|---|
| **Không đầu ra nào đủ để kỷ luật một người** | Mọi kết quả là đầu vào cho một cuộc trao đổi, không phải một phán quyết |
| **Mọi nhận định phải kèm phản chứng** | Không nghĩ ra được một lời giải thích vô tội cho câu đó thì bỏ nhận định đi |
| **Văn hành chính Việt Nam vốn công thức** | "Trong bối cảnh…", "đóng vai trò quan trọng", bố cục "kết quả – tồn tại – phương hướng" là **văn phong được dạy trong trường**, có trước khi có mô hình ngôn ngữ. Mật độ sáo ngữ đo *thể loại*, không đo *nguồn gốc* |
| **Trục 4 không phải dịch vụ né máy chấm** | Nó chỉ chạy trên bản thảo đã biết nguồn gốc, và mọi bản giao đều mang theo ghi chú "đã qua biên tập máy" |

Hai con số nên nhớ trước khi tin bất kỳ máy dò AI nào:

> GPT-4 khi được bảo làm giám định viên: nhận đúng 97–100% văn AI, nhưng **gắn nhầm hơn 95% văn NGƯỜI
> thành AI** (arXiv 2308.01284, SIGKDD Explorations 2024).
>
> Bảy công cụ dò AI thương mại phân loại nhầm **61,22%** bài TOEFL của người không nói tiếng Anh bản
> ngữ thành AI (arXiv 2304.02819, *Patterns* 2023).

Cả repo này được thiết kế xung quanh hai con số đó.

---

## 6. Bảng thuật ngữ

| Thuật ngữ | Nghĩa |
|---|---|
| **trục** (Y1…Y5) | một trong năm giai đoạn quy trình; mỗi trục là một skill |
| **hồ sơ thể loại** | file `shared/genres/<slug>.md` có 5 mục — dữ liệu về một loại hình viết |
| **`full` / `partial`** | hồ sơ có đủ 5 mục / chỉ có §5 (dùng riêng cho giám định) |
| **S** | *điểm dấu hiệu*, thang 0–100: dấu hiệu trong bài **mạnh** đến đâu. **Không phải xác suất bài do AI viết** — không có mô hình xác suất nào phía sau |
| **C** | *độ phủ*, tính bằng phần trăm: dấu hiệu **phủ bao nhiêu phần** nội dung. S cao C thấp = dấu hiệu dồn một chỗ; S thấp C cao = nhiều khả năng đang đo văn phong thể loại |
| **`low_signal` / `worth_reviewing` / `priority_check`** | ba nhãn hành động theo S: không làm gì / giảng viên xem lại trong ngữ cảnh / mời trao đổi và xin bản nháp |
| **G1 · G2 · G3 · G4** | bốn **họ dấu hiệu**. G1 khuôn hình thức (cấu trúc câu, đoạn, danh sách dựng sẵn) · G2 từ vựng và cú pháp (cụm đệm, danh từ hoá) · G3 dẫn chứng (nguồn, số liệu, phản đối) · G4 giọng và lập trường (thổi phồng, hứa hẹn, giả thẳng thắn) |
| **FLAG / NOTE / PLAIN / SKIP** | bốn nhãn gán cho **từng câu** khi đọc mù: đáng nghi / đáng ghi chú / bình thường / không xét (câu quá ngắn, trích dẫn, tiêu đề) |
| **tell** | một **dấu hiệu** cụ thể có tên và mã (T01…T38), kèm ví dụ tiếng Việt **và** phản chứng — một câu văn người hoàn toàn hợp lệ chứa đúng dấu hiệu đó. Danh mục ở `shared/rules/vi-ai-tells.json` |
| **`candidate` / `calibrated`** | trạng thái của một tell. `candidate` = đã có ví dụ và phản chứng, dùng được cho trục 4 nhưng **cấm** dùng để tạo nghi vấn ở trục 5. `calibrated` = đã đo trên bộ bài có nguồn gốc biết trước |
| **lăng kính** | một cách đọc bài có tên, có câu hỏi và có bằng chứng bắt buộc phải trưng ra. 13 lăng kính, ví dụ `fallacy_scan` (soi ngụy biện), `pacing_curve` (nhịp truyện), `balance_check` (đã hỏi đủ các bên chưa) |
| **`genre_baseline`** | danh sách tín hiệu **bình thường ở thể loại này**. Nó chỉ dùng để **hạ** nghi vấn, không bao giờ để tạo thêm. Đây là hàng rào chống báo oan quan trọng nhất trong repo |
| **provenance** | bản tự khai nguồn gốc đi theo bản giao: câu nào máy viết, có qua biên tập máy không |
| **`sentence_id`** | mã câu (`s0001`, `s0002`…) do studio sinh một lần vào `sentences.json`. Cả ba giai đoạn sau dùng chung mã đó; **tự đếm câu lại là sai** — ba hệ đánh số khác nhau đã từng làm hỏng một lần đối chiếu |
| **chấm mù** | người chấm không được xem bản tự khai và không được nhận câu hỏi mớm, cho tới khi đã khoá kết quả |

---

## 7. Ghi nhận nguồn

Repo này **không vendor, không chép code** từ nguồn nào. Nó *đọc để chưng cất phương pháp*, rồi tự
viết lại bằng tiếng Việt với ví dụ tiếng Việt — có tham khảo ý tưởng từ cộng đồng mã nguồn mở, và sổ
nguồn chi tiết (lấy gì, không lấy gì, SHA đã ghim) giữ ở xưởng, không nằm trong repo này.

Một ngoại lệ có nghĩa vụ pháp lý: kho thành ngữ `skills/04-humanizer/assets/thanh-ngu.json` **dùng dữ
liệu cấp phép MIT**, nên copyright notice và permission notice của nguồn nằm ngay trong file đó và
**không được gỡ**.

---

## 8. Trạng thái trung thực — những gì repo này CHƯA làm được

Bốn điều dưới đây không phải "việc còn lại trong backlog". Chúng là **giới hạn cần biết trước khi tin
bất cứ con số nào** ở trên.

1. **Chưa có bộ bài mẫu để hiệu chuẩn — 0/33 dấu hiệu ở trạng thái `calibrated`.**
   `shared/rules/vi-ai-tells.json` có 33 mục: 32 `candidate` (đã có ví dụ và phản chứng, nhưng chưa
   đo trên bài có nguồn gốc biết trước) và 1 `needs_corpus` (chưa đủ cơ sở để viết cả ví dụ). Theo
   luật của chính repo, **trục 5 không được dùng dấu hiệu `candidate` để tạo nghi vấn** — nên khi
   chưa có bộ mẫu, trục 5 chỉ ghi chú chứ không kết luận. `fixtures/` hiện còn rỗng, và ngưỡng trong
   `SCORING_v2.md` là **mốc tham chiếu với n rất nhỏ (1–3 văn bản)**, không phải phân vị của một
   cohort thật.

2. **Hồ sơ giọng người viết chưa dựng xong.** `profile_build.py` cần **≥3 bài đã xác nhận chính chủ**
   mới cho ra một hồ sơ dùng được; hiện chủ repo mới cung cấp 2 bài, nên hồ sơ ở trạng thái `draft` —
   trục 2 và trục 4 chỉ được dùng nó **như gợi ý**, không được ép câu theo nó.

3. **Con số 83% / 58% là bằng chứng đầu tiên, không phải bằng chứng thống kê.** Trục 3 chấm một bài
   hội thảo thật rồi đối chiếu với phiếu phản biện của hội đồng: trong 6 điểm hội đồng nêu mà tác giả
   chưa sửa, trục 3 bắt trọn 2, bắt một phần 3, sót 1 → **5/6 = 83%** nếu tính bắt-một-phần,
   **3,5/6 = 58%** nếu tính nửa. Qua ngưỡng 50% ở cả hai cách tính, và trục 3 còn tìm thêm 4 điểm hội
   đồng không nêu. Nhưng đó là **một ca, một người chấm, không mù** — n = 1.

4. **Provenance là tự khai, chưa được cưỡng chế.** Không có test nào đỏ khi ai đó bỏ
   `draft.meta.json` ra khỏi bản giao. Ở ca đầu tiên, bản tự khai đã lệch 2 câu vì một lỗi nuốt câu
   ngắn — lỗi đã sửa, nhưng dạng lỗi thì vẫn còn đó. Toàn bộ ranh giới đạo đức ở mục 5 đứng trên một
   quy ước, và quy ước thì cần người giữ.

---

## 9. Chạy test

```bash
python -m pytest tests/ -q
python -m unittest discover -s tests -t .
```

Cả hai cùng cho **314 passed**. Test không kiểm "văn hay"; nó kiểm những thứ hỏng thì im lặng: skill
có đúng tên và ≤550 từ không, hồ sơ thể loại có đủ mục không, slug thể loại có khớp hai chiều không,
liên kết nội bộ có gãy không, nguồn ngoài có bị ghi sai license không.

---

**License:** dự kiến **MIT**, cùng chuẩn với hai repo anh em `agent-design-studio` (hình ảnh) và
`agent-voice-studio` (giọng nói) — ba repo nối với nhau bằng **file**, không import code chéo nhau.
⚠️ File `LICENSE` **chưa được thêm** vào repo; chừng nào chưa có, đây mới là dự định của chủ repo chứ
chưa phải một giấy phép có hiệu lực.
