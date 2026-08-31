# Vòng sửa – đánh giá – giữ

Sơ đồ ba bước này là kiến thức chung của ngành, và ở đây được viết lại **hoàn toàn bằng lời của
repo này**. Phương pháp trong file này thuộc bộ luật của studio; nguồn gốc tri thức ghi ở sổ xưởng (không nằm trong repo).

---

## 1. Ba bước, chạy trên đơn vị nhỏ

Đơn vị của vòng lặp là **một đoạn** (văn xuôi) hoặc **một chương** (truyện dài), không phải cả bài.
Chạy trên cả bài thì lúc thước đo kêu, không ai biết chỗ nào kêu.

1. **Sửa** — viết đoạn, hoặc viết lại đoạn vừa có theo một hướng khác. "Hướng khác" nghĩa là đổi
   thứ tự lập luận, đổi chỗ đặt bằng chứng, đổi độ dài câu chủ đề — không phải đổi vài từ.
2. **Đánh giá** — chạy đúng hai thước, không hơn:
   - `python skills/05-forensics/scripts/counters.py` trên đoạn vừa viết, để có số;
   - **một hoặc hai lăng kính** của trục 3, chọn từ `lenses[]` mà `§3` hồ sơ thể loại đã bật.
     Một hai, không phải tất cả: chạy đủ bộ là làm việc của trục 3, và trục 2 chấm bài của chính
     mình đủ bộ thì cái phiếu ấy không dùng được cho ai.
3. **Giữ hay bỏ** — so bản mới với bản cũ theo tiêu chí ở mục 3 dưới đây, rồi quyết. Không quyết
   được thì **giữ bản cũ**: bản cũ đã có, bản mới chỉ là ứng viên.

Ghi kết quả từng vòng vào `self_checks[]` của `draft.meta.json`: tên thước, `passed`, và một dòng
`detail` nói thước ấy nói gì. Vòng không ghi lại là vòng không xảy ra.

## 2. Chọn lăng kính nào

Chọn theo **chỗ đoạn ấy dễ hỏng nhất**, không chọn theo chỗ dễ chạy nhất:

| Đoạn đang viết | Lăng kính nên chạy |
|---|---|
| Đoạn nêu luận điểm trung tâm | `task_response` — đoạn này phục vụ luận đề ở chỗ nào |
| Đoạn có suy luận nhiều bước | `fallacy_scan` — bước nào thiếu tiền đề |
| Đoạn có số liệu, nguồn, khẳng định thực chứng | `claim_check` |
| Đoạn tổng quan tài liệu, đoạn dẫn nguồn thứ cấp | `source_reliability` |
| Đoạn mô tả cách làm, cỡ mẫu, phạm vi | `method_rigor` |

Danh mục đầy đủ và đầu ra của từng lăng kính:
[`03-critique/references/01-lang-kinh.md`](../../03-critique/references/01-lang-kinh.md). Lăng kính
không nằm trong `lenses[]` của hồ sơ thì **không chạy** — hồ sơ thể loại là thứ quyết định, không
phải cảm giác của trục 2.

## 3. Giữ bản nào — bốn cửa, theo thứ tự

Bản mới chỉ thắng khi qua được cả bốn, theo đúng thứ tự này:

1. **Nội dung.** Bản mới nói được điều bản cũ nói, và nói thêm hoặc nói rõ hơn chỗ nào? Không nói
   thêm gì thì thua, dù đọc mượt hơn.
2. **Bằng chứng.** Bản mới có bỏ rơi bằng chứng nào ở tầng ba của outline không? Bỏ rơi là thua
   ngay, không cần xét tiếp.
3. **Khuôn.** Bản mới có kéo vào khuôn nào trong `anti_llm_defaults[]` của `§2` không? Xem
   [`04-chong-khuon-llm.md`](04-chong-khuon-llm.md).
4. **Số.** Chỉ đến đây mới nhìn `counters.py`. Số là thứ **mô tả**, không phải thứ để tối ưu.

## 4. Luật chống Goodhart — thước không phải đích

Đây là chỗ vòng lặp này dễ hỏng nhất, và cũng là lý do luật `§2.5` của `ARCHITECTURE_v2.md` tồn tại.

- **Không sửa để con số đẹp lên.** Không có ngưỡng nào ở đây cả: `counters.py` chỉ ra chỗ để nhìn,
  không ra điểm đỗ. Sửa một câu vì `NOMINAL` cao là đã lấy thước làm đích.
- **Thể loại nào khai baseline thì con số ấy không phải chỗ phải sửa.** `§5` của hồ sơ khai
  `genre_baseline.normal_signals`; `research.md` khai đích danh danh từ hoá và mật độ thuật ngữ cao
  là bình thường. Trục 4 có cả một file cho chuyện này
  ([`04-humanizer/references/03-chong-sua-oan.md`](../../04-humanizer/references/03-chong-sua-oan.md));
  trục 2 chịu chung luật, vì sửa oan lúc sinh cũng là sửa oan.
- **Không xem điểm trục 5.** Trục 2 không chạy `05-forensics` trên bản của chính mình và không nhận
  điểm ấy nếu ai đó đưa. Viết để qua máy giám định là đích sai; bản tự khai ở
  [`03-tu-khai-nguon-goc.md`](03-tu-khai-nguon-goc.md) mới là cách studio đối diện chuyện nguồn gốc.
- **Nhiều nhất hai vòng cho một đoạn.** Vòng thứ ba mà vẫn không quyết được thì vấn đề nằm ở outline
  chứ không ở câu chữ: quay lại tầng hai, đừng mài tiếp.

## 5. Tự kiểm theo cụm ba chương — cho truyện dài

Phương pháp trong file này thuộc bộ luật của studio; nguồn gốc tri thức ghi ở sổ xưởng (không nằm trong repo). **Đây là luật đang chạy**: `shared/genres/novel.md`
khai `three_chapter_selfcheck` trong `lenses[]` ở `§3`, nên với thể loại truyện dài trục 2 phải chạy
mục này, không phải chỉ đọc để biết.

Truyện dài hỏng theo cách mà vòng lặp một-đoạn không thấy: nhân vật đổi tính giữa các chương, một
manh mối được cài rồi bỏ quên, nhịp thắt–mở phẳng dần. Nên ngoài vòng lặp cấp đoạn, cứ **ba chương**
dừng lại một lần và đọc cụm ba chương ấy như một khối:

- nhân vật ở chương sau có làm điều mà chương trước đã loại trừ không;
- manh mối cài ở chương trước đã được nhắc lại hay đã rơi mất;
- ba chương có cùng một hình nhịp không — cả ba cùng lên đều rồi hạ ở câu cuối là dấu hiệu đang
  viết theo khuôn, không theo truyện.

Ba câu hỏi này ứng với ba lăng kính `character_consistency`, `plot_consistency`, `pacing_curve`;
`novel.md` bật cả ba cộng `three_chapter_selfcheck` qua `lenses[]` ở `§3` — trục 2 đọc `lenses[]` của
hồ sơ, không tự bịa ra chúng cho thể loại không khai.
