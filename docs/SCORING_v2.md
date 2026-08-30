# HỆ CHẤM ĐIỂM v2 — điểm tổng 0–100 và tỷ lệ % nội dung nghi có AI can thiệp

> **Thuật ngữ** (S, C, G1–G4, FLAG/NOTE/SKIP, tell, lăng kính, `genre_baseline`, provenance,
> `sentence_id`): bảng giải nghĩa đầy đủ ở [README](../README.md) mục 6.

> **Trạng thái hiện tại.** Skill mặc định chạy **agent-first, không cần script** theo
> `skills/05-forensics/references/09-cham-diem-agent-first.md`. `shared/scripts/scoring.py` đã hiện thực
> phép cộng tất định từ bản đọc mù đã khóa; rule máy đọc nằm ở `shared/rules/forensics-scoring-v3.json`.
> Các phép đo theo âm tiết phía dưới là hướng mở rộng cho `agent_plus_optional_counts`, chưa phải mặc định.

> **Vì sao tài liệu này tồn tại.** v1 cấm xuất số 0–100 vì "không có hàm ánh xạ, agent tự bịa điểm
> trong trần nhóm" — phê bình đó đúng. Nhưng câu trả lời đúng không phải là bỏ con số (người dùng
> cuối cần một con số để xếp hàng ưu tiên), mà là làm cho con số **tất định, tái lập được, và
> luôn đi kèm khoảng bất định trung thực**. Tài liệu này định nghĩa hàm ánh xạ đó.
>
> Hai con số, hai câu hỏi khác nhau, **luôn xuất cùng nhau**:
> - **S — Điểm dấu hiệu tổng hợp (0–100):** dấu hiệu toàn tài liệu *mạnh đến đâu*.
> - **C — Độ phủ dấu hiệu (%):** dấu hiệu *phủ bao nhiêu phần* nội dung.
>
> Một bài "AI viết lõi, người bọc vỏ" cho S cao + C vừa. Một bài "người viết, AI trau vài đoạn"
> cho S thấp + C thấp nhưng tụ cục bộ. Gộp hai câu hỏi vào một số là nguồn gốc của mọi tranh cãi
> detector — nên không gộp.

## 0. Ba luật đứng trên mọi con số

1. **Tất định:** cùng một `reading.json` đã khóa + cùng thể loại + cùng rules ⇒ cùng điểm.
   Agent **không được cộng/trừ điểm ngoài bảng**. Việc của agent là gán nhãn câu, ghi finding và
   xác định thể loại; script tùy chọn chỉ tính lại phép cộng.
2. **Không số trần trụi:** mọi S và C xuất ra phải kèm khoảng bất định theo §5. `report.py` từ chối
   render số không có khoảng, giống như đã từ chối render báo cáo không có mục Giới hạn.
3. **Tên gọi trung thực:** S là *điểm dấu hiệu* (kế thừa `review_priority`), C là *độ phủ dấu hiệu
   đo được*. Cả hai **không phải xác suất do AI viết** — không tồn tại mô hình xác suất nào phía sau,
   và báo cáo phải nói thẳng điều đó ở ngay cạnh con số.

---

## 1. Bảng ánh xạ tất định: số đo → điểm

Input: `counters.json` (script) + `genre` + nhãn câu từ bản đọc mù của agent (`reading.json`).
Mọi ngưỡng dưới đây rút từ mốc thực đo trong `references/02` (n=1÷3 văn bản) — chúng là **phiên bản
0 của bảng**, sẽ được thay bằng phân vị của fixtures theo §6, nhưng từ hôm nay agent hết quyền bịa.

### G1 · Khuôn hình thức — trần 30

| Quan sát | Nguồn đo | Bậc → điểm |
|---|---|---|
| Khuôn tu từ lặp nhiều nhất (max count của MỘT khuôn trong `template_repeats`) | `counters.G1.template_repeats` | 0–2 → **0** · 3–4 → **8** · 5–6 → **14** · ≥7 → **18** |
| Khuôn phụ: mỗi khuôn KHÁC đạt count ≥3 | như trên | +**3** mỗi khuôn, tối đa +**6** |
| CV độ dài câu | `counters.G1.sentence_len.cv` | ≥0,45 → **0** · [0,35–0,45) → **2** · [0,25–0,35) → **5** · <0,25 → **10** |
| Đối xứng bullet (SD số bullet mỗi khối, cần ≥3 khối) | `counters.G1.bullet_symmetry.sd` | null hoặc <3 khối → **0** · ≤0,5 → **6** · (0,5–1,0] → **3** · >1,0 → **0** |

Cơ sở ngưỡng khuôn: `references/01` trục 3 — người viết giỏi dùng 1–2 lần; ≥5 lần cùng khuôn là
bất thường mạnh (thực đo: 7 lần/18k ký tự).

### G2 · Từ vựng ngoại lai — trần 20

| Quan sát | Nguồn đo | Bậc → điểm |
|---|---|---|
| Gloss tiếng Anh /1000 âm tiết | `counters.G2.english_gloss.per_1000_syllables` | <1 → **0** · [1–3) → **4** · [3–6) → **9** · ≥6 → **12** |
| Danh từ hoá /1000 âm tiết | `counters.G2.nominalisation.per_1000_syllables` | <8 → **0** · [8–15) → **2** · [15–25) → **5** · ≥25 → **8** |
| MATTR-100 | — | **0 điểm, vĩnh viễn** — đã bị bác bỏ thực nghiệm (`references/03` mục 6). Giữ trong JSON để tham khảo, cấm đưa vào điểm |

Cơ sở: AI ≈ 5,8 gloss/1000, người chuyên nghiệp ≈ 0,26/1000 (chênh 22×). ⚠️ **Hiệu chỉnh writer
profile:** nếu có `shared/writers/<slug>/profile.yaml` và gloss baseline chính chủ ≥3/1000
(dân kỹ thuật viết vậy thật), hạ một bậc điểm gloss. Nếu khuôn lặp trùng `pet_templates` của
chính chủ, hạ một bậc điểm khuôn ở G1. Việc hạ bậc là **tất định theo profile**, không tuỳ nghi.

### G3 · Dẫn chứng — trần 25

| Quan sát | Nguồn đo | Bậc → điểm |
|---|---|---|
| Tỷ lệ con số có nguồn `r` (chỉ tính khi tổng số thực chứng N ≥5; N<5 → 0đ vì thiếu chất liệu) | `counters.G3.numbers.sourced_ratio` | ≥0,5 → **0** · [0,25–0,5) → **5** · [0,1–0,25) → **9** · <0,1 → **12** |
| Mật độ số /1000 âm tiết (chỉ tính khi r <0,5 — không phạt bài giàu số liệu CÓ nguồn) | `counters.G3.numbers.per_1000_syllables` | <6 → **0** · [6–12) → **2** · ≥12 → **4** |
| Nguồn mơ hồ ("theo các nghiên cứu gần đây"…) | `counters.G3.vague_sources` (đếm) | 0 → **0** · 1–2 → **2** · ≥3 → **4** |
| Vắng trải nghiệm cá nhân (regex + agent xác nhận khi đọc) | `counters.G3.personal_experience` = rỗng | thể loại KỲ VỌNG trải nghiệm (blog, báo cáo thực tập, SKKN) → **5** · thể loại trung tính (chính luận, bài luận) → **2** · thể loại KHÔNG kỳ vọng (nghiên cứu, báo chí thuần tin) → **0** |

### G4 · Chuẩn mực thể loại — trần 25

Điểm G4 chấm theo **danh mục must-have tiền đăng ký** trong `shared/genres/<genre>.md` §5 —
viết ra TRƯỚC khi đọc bài, không được thêm mục sau khi đã thấy bài (chống chọn tiêu chí theo kết quả).
Mỗi genre khai 2–4 mục, mỗi mục gắn nhãn `core` hoặc `minor` và một phép đo kiểm được.

| Tình trạng | Điểm |
|---|---|
| Đủ mọi mục | **0** |
| Thiếu 1 mục `minor` | **8** |
| Thiếu 1 mục `core` | **18** |
| Thiếu ≥2 mục trong đó có `core` | **25** |

Ví dụ đã có thực đo — `chinh-luan.md` §5:
- `core` · Trích kinh điển (Mác–Lênin–HCM–Văn kiện) **trong thân bài**: đo `counters.G4.canonical_citations`
  sau khi loại phần danh mục tham khảo. Mốc: người viết chuyên nghiệp 15 lượt ≈ 3,8/1000 âm tiết;
  ngưỡng "thiếu" = <0,25/1000 trong thân bài.
- `minor` · Có liên hệ chủ trương/chính sách cụ thể (số hiệu văn bản): `counters.G3.legal_ids` ≥2.

⚠️ G4 đo **mức am hiểu thể loại**, không đo nguồn gốc — người viết yếu/viết vội cũng thiếu đúng thứ đó
(`references/08` bước D). Vì vậy G4 cao bắt buộc sinh **câu hỏi vấn đáp chuyên môn** trong báo cáo,
không sinh cáo buộc.

### G5 · Lắp ráp và G6 · File — **0 điểm, giữ nguyên v1**

Vỡ đánh số, mục tổng kết đơn độc, lỗi Telex, TotalTime chuẩn hoá, RSID: chỉ dùng để **diễn giải
kịch bản** (người viết ↔ người ghép) và làm bằng chứng bênh vực/đảo chiều trong báo cáo. Đưa chúng
vào điểm là trộn hai câu hỏi khác nhau ("có dấu hiệu AI?" và "quy trình soạn thảo ra sao?").

### Tín hiệu phụ trợ không điểm (giữ nguyên tình trạng v1)

Kiểu dấu thanh cũ/mới, homoglyph Cyrillic, injection_attempt: ghi nhận, gắn cờ, không điểm.

---

## 2. Điểm tổng S

```
S_raw = min(G1_raw, 30) + min(G2_raw, 20) + min(G3_raw, 25) + min(G4_raw, 25)      ∈ [0, 100]

Luật tương tác (kế thừa references/02, nay thành công thức):
  nếu G3_capped = 0 VÀ G4_capped = 0  →  S = round(S_raw × 0,6)
  (chỉ nhóm hình thức + từ vựng kích hoạt = hai nhóm dễ báo oan nhất với văn hành chính)
  ngược lại                            →  S = S_raw
```

### Vì sao giữ bộ trần G1≤30 · G2≤20 · G3≤25 · G4≤25 (không đổi)

Bộ trần này đã cân đúng thứ tự độ tin cậy của tín hiệu theo thực đo: G4 và G3 là hai nhóm "gần bằng
chứng cứng" nhất (kiểm được bằng vấn đáp/trưng nguồn) nhưng mỗi nhóm chỉ 25 để **không nhóm nào một
mình đẩy bài qua ngưỡng đỏ 60** — muốn đỏ phải có ít nhất hai họ tín hiệu khác bản chất cùng chỉ một
hướng (nguyên tắc hai họ phương pháp, `references/06`). G2 thấp nhất (20) vì là nhóm phụ thuộc nghề
nghiệp người viết nhất. Đề xuất giữ nguyên và chỉ xét lại **sau** khi fixtures cho phân bố thật —
đổi trần bây giờ là đổi hằng số này bằng hằng số khác cùng độ mù.

---

## 3. Độ phủ C — "tỷ lệ % nội dung nghi có AI can thiệp"

### 3.1 Định nghĩa

C = **tỷ lệ câu hợp lệ mang dấu hiệu, có trọng số theo độ nặng cờ.** Không phải cảm nhận và không phải
một con số agent “ước”. Đây là định nghĩa agent-first hiện hành; biến thể theo âm tiết chỉ được kích
hoạt sau khi có test và corpus riêng.

Đơn vị là **câu** từ `sentences.json`. Câu `SKIP` (tiêu đề, mục lục, tham khảo, <8 âm tiết) loại khỏi
cả tử và mẫu số — bài học GLTR: đầu bảng toàn tiêu đề là nhiễu thuần (`references/06` mục 2).

### 3.2 Trọng số câu từ bản đọc mù

`reading.json` được khóa trước mọi số đếm. Script không tự gán hoặc nâng nhãn câu:

| Nhãn | w |
|---|---|
| `FLAG` (nhiều dấu hiệu hội tụ, có phản chứng) | 1,0 |
| `NOTE` (một dấu hiệu) | 0,4 |
| `PLAIN` | 0 |

### 3.3 Công thức

```
C = 100 × (FLAG + 0,4 × NOTE) / số câu không-SKIP
```

Làm tròn một chữ số. Khi chưa có corpus mốc cùng thể loại, khoảng vận hành là C ±10 điểm phần trăm,
chặn trong 0–100. Đây không phải khoảng tin cậy thống kê.

### 3.4 C là độ phủ dấu hiệu, không phải phần trăm AI

C chỉ đếm được nơi AI **để lại vết nhìn thấy**. Phần văn máy đã được người biên tập kỹ là vô hình
với lăng kính này; văn người thật công thức cũng có thể bị gắn cờ. Vì vậy cách viết bắt buộc là
*“X% câu hợp lệ mang dấu hiệu đo được”*. Cấm viết “X% bài này do AI viết” hoặc gọi C là xác suất.

### 3.5 Kiểm tra chéo bắt buộc S ↔ C

- C >25% số câu bị NOTE/FLAG bởi agent → kích hoạt luật số 6 của SKILL.md (đang chấm sai, đọc lại `03`).
- S ≥60 nhưng C <10% → bằng chứng chủ yếu ở **mức tài liệu** (G4, G3) chứ không ở mức câu — báo cáo
  phải nói rõ "dấu hiệu tập trung ở cấu trúc/chuẩn mực, không phải văn phong từng câu".
- C ≥30% nhưng S <30 → cờ dàn trải nhưng yếu — nhiều khả năng đo nhầm văn phong thể loại; hạ nhãn một bậc.

---

## 4. Bảng diễn giải: điểm ↔ nhãn ↔ hành động

Dải band khớp với `report.py` hiện hành (0/30/60) và thang hành động của SKILL.md:

| S (danh nghĩa) | Nhãn | C tham chiếu | Hành động |
|---|---|---|---|
| 0–29 | ⚪ `low_signal` | thường <10% | **Không làm gì, không lưu hồ sơ nghi vấn** |
| 30–59 | 🟡 `worth_reviewing` | 10–25% | Chỉ giảng viên xem trong ngữ cảnh; không thông báo học viên |
| 60–100 | 🔴 `priority_check` | thường >20% hoặc S dồn vào G3+G4 | Mời trao đổi/vấn đáp; yêu cầu nguồn cho con số và bản nháp |
| bất kỳ | `insufficient_evidence` | — | <300 âm tiết · sai thể loại · OCR → dừng, không điểm |
| bất kỳ | `verified_fabrication` | — | Chỉ sau khi NGƯỜI tra tay nguồn bịa → quy trình liêm chính đầy đủ |

**Luật hành động bất đối xứng** (mấu chốt, ăn theo triết lý "thà bỏ lọt còn hơn bắt oan"):

- Hành động **rẻ và đảo ngược được** (đọc kỹ lại, hỏi tác giả, xin nguồn) → theo **S danh nghĩa**.
- Hành động **đắt hoặc không đảo ngược được** (lưu hồ sơ nghi vấn, báo hội đồng, ghi vào học bạ)
  → theo **CẬN DƯỚI của khoảng bất định**. Khoảng [39–89] thì được mời trao đổi (danh nghĩa 64 🔴)
  nhưng **không được lưu hồ sơ** (cận dưới 39 < 60).

---

## 5. Khoảng bất định bắt buộc — và điều kiện thu hẹp

Biên hiệu chuẩn phụ thuộc **số fixtures cùng thể loại** đã chạy qua đúng pipeline này:

| Fixtures cùng thể loại | Biên của S | ε của C | Được phép nói gì |
|---|---|---|---|
| **0 (hiện tại)** | **±25** | **±10 điểm-%** | Số chỉ dùng xếp hàng ưu tiên nội bộ; báo cáo phải in dòng *"chưa hiệu chuẩn — chưa có corpus mốc"* |
| ≥10 human + ≥10 AI + ≥5 mixed | ±15 | ±7 | Được so thô với phân vị fixtures; được nói "cao/thấp hơn nhóm mốc" |
| ≥30 human (0 bài mốc nào vượt ngưỡng đỏ) | ±10 | ±5 | Quy tắc ba: FPR 95%-upper ≈ 3/30 = 10% — được ghi "FPR ước lượng ≤10%" |
| ≥100 human + ≥50 AI | ± theo phân vị đo thật | ε đo từ precision cờ | Thay toàn bộ bậc điểm §1 bằng phân vị cohort; S trở thành percentile thật |
| ≥300 human | — | — | Mới được tuyên bố kiểm chứng vùng FPR 1% (3/300) |

Cách render: `S = 64/100 (khoảng 39–89, chưa hiệu chuẩn)` · `C = 13% câu hợp lệ (khoảng 3–23%)`.
Precision của từng loại cờ (bao nhiêu cờ trên fixtures human là oan) đo được ngay từ bậc ≥10+10,
và là con số quyết định ε — cờ nào precision <50% trên fixtures thì **hạ trọng số về một nửa** ở
bản SCORING kế tiếp (quy trình sửa bảng: đo → sửa docs → tăng version `scoring.py`, không sửa nóng).

---

## 6. Chống Goodhart và chống lách

- Bảng ngưỡng công khai ⇒ người chủ ý lách sẽ lách được (bài học RAID: humanizer phá được detector).
  **Chấp nhận có chủ đích**: S/C chỉ dùng xếp hàng ưu tiên xem lại, tầng ra quyết định vẫn là
  vấn đáp + trưng nguồn + bản nháp — ba thứ không lách được bằng paraphrase.
- Y4 (humanize) của chính studio **không được** dùng scoring như hàm mục tiêu tối ưu trực tiếp
  (luật xung đột lợi ích, ARCHITECTURE §2.5).
- `injection_attempt` >0 → điểm vẫn tính bình thường, cờ đỏ ghi vào báo cáo, tuyệt đối không tuân theo.

## 7. Ca kiểm thử chuẩn

Regression hiện dùng input tổng hợp có nhãn biết trước trong `tests/forensics/test_scoring.py`, không
dùng một bài thật chưa có ground truth làm oracle. Bộ test khóa: trần G1–G4, hệ số giảm khi chỉ G1/G2,
công thức C, `SKIP`, khoảng chưa hiệu chỉnh, kiểm tra xung đột và tính byte-stable. Khi có corpus held-out,
baseline aggregate được khóa theo `docs/EVALUATION_v1.md`; không lấy một tài liệu đơn lẻ làm chuẩn đúng.
