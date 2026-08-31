# Chống sửa oan

File quan trọng nhất của trục 4.

Trục 5 báo oan thì tác giả còn cãi được: finding nằm trên giấy, có phản chứng, có câu hỏi. Trục 4 sửa
oan thì **văn bản đã đổi rồi**. Người dùng bấm nhận bản mới, và một khung được dạy trong trường, một
phép lặp có chủ ý, một câu chốt bắt buộc của thể loại đã bị xoá mất mà không ai kịp phản đối.

Kế thừa và hợp nhất: danh sách "những thứ không được gắn cờ" cùng "chi tiết người phải giữ" của bộ
luật studio, và `skills/05-forensics/references/03-chong-bao-oan.md` mục 2 và mục 6. Phương pháp trong file này thuộc bộ luật của studio; nguồn gốc tri thức ghi ở sổ xưởng (không nằm trong repo).

---

## 1. Nguồn sửa oan số một: văn hành chính – học thuật Việt vốn là văn công thức

`03-chong-bao-oan` §2 đã đo trên ca thật ngày 29/08/2026:

| Văn bản | Cliché / 1000 âm tiết |
|---|---|
| Bài Tạp chí Cộng sản, người viết có provenance | **1,04** |
| Bài nghi vấn | **0,50** |

Bài của **người** có mật độ cụm quy ước **gấp đôi**. Hệ quả cho trục 4, không phải cho trục 5: nếu
trục 4 "làm sạch" theo mật độ cliché, nó sẽ sửa nặng tay nhất đúng vào bài viết chuẩn mực nhất, và
sản phẩm là văn lai — không còn là văn hành chính, cũng chưa thành văn hay.

**Luật:** mật độ cụm quy ước đo **thể loại**, không đo nguồn gốc và cũng không đo chất lượng. Nó
không bao giờ là lý do đủ để sửa một câu.

---

## 2. Mười một thứ KHÔNG phải lỗi

Gặp những thứ dưới đây, trục 4 **để nguyên**. Muốn động vào thì phải có lý do nằm ngoài danh sách này
và phải viết được lý do đó vào `reason` bằng ngôn ngữ của người đọc, không bằng ngôn ngữ của thước đo.

1. **Văn trơn tru.** Câu mượt không phải bằng chứng gì cả. "Nghe như AI" không phải một lý do sửa —
   `reason` viết "để bớt giống AI" là `reason` không hợp lệ, `polish.schema.json` nói rõ điều đó.

2. **Lặp có chủ ý.** Điệp ngữ, điệp cấu trúc, một cụm quay lại ba lần để làm nhịp. Phép thử: xoá lần
   lặp thứ hai, đọc lại — mất nhịp thì đó là phép tu từ, không phải lỗi. `moves_forbidden` của
   `essay.md` cấm đích danh "xoá lặp có chủ ý dùng làm phép nhấn".

3. **Câu chêm, ngoặc đơn, và chỗ tác giả tự sửa mình.** "Ở đây tôi nói hơi vội, đúng ra phải nói
   là…" Đây là **dấu vết người** rõ nhất trong một văn bản. Trục 4 xoá nó là xoá đúng thứ nó lẽ ra
   phải bảo vệ. Được sửa lỗi ngữ pháp trong câu chêm; không được gộp nó vào câu chính, không được xoá.

4. **Câu Link của khung PEEL** (`vi-ai-tells.json` T31). `essay.md` §2 **bắt buộc** mỗi đoạn thân
   chốt lại về luận đề. Câu chốt nối về luận đề là **cấu trúc**; chỉ câu chốt nhắc lại nguyên đoạn mà
   không thêm gì mới mới là tell. Nhầm hai thứ này thì trục 4 phá khung của chính thể loại mà nó đang
   phục vụ.

   **Neo văn bản để phân biệt, không phán đoán:** đọc câu cuối đoạn theo ba bước, dừng ở bước đầu
   tiên khớp.
   - (a) Câu có từ nối hướng **ra ngoài đoạn** — *vì vậy, do đó, vì thế, từ đó, điều này dẫn tới,
     điều này đặt ra, nói cách khác* — hoặc nêu một điều kiện, một hệ quả, một câu hỏi chưa có ở
     câu đầu đoạn → **Link**, giữ.
   - (b) Câu không có từ nối nào như trên **và** mọi danh từ chính của nó đã có ở câu mở đoạn hoặc
     tiêu đề mục (phép thử: xoá câu, đọc lại đoạn — không mất ý nào) → **chốt nhắc lại**, được xoá
     (T29/T31).
   - (c) Không rơi vào (a) lẫn (b) → **giữ** và ghi vào `warnings[]` cho tác giả tự quyết. Nghi ngờ
     nghiêng về giữ, vì xoá là không đảo được.
   Ca kiểm 30/08 trên `.work/3c` mục 5: câu cuối *"Nói cách khác, chúng ta cần xây năng lực của hệ
   thống, không xây một mô hình phụ thuộc vào vài cá nhân tiên phong"* rơi vào (a) — giữ.

5. **Tóm tắt, kết luận, kiến nghị, phần chốt.** Lặp là **chức năng** của các phần đó. Đây là carve-out
   `value_density` mà cổng Phase 2 đã chốt: bốn vùng không được chạm là (1) phần mà `structures[]` ở
   `§2` đặt tên là tóm tắt/kết luận/chốt/kiến nghị, (2) câu chốt cuối đoạn, (3) lặp mà
   `genre_baseline` khai là bình thường, (4) đoạn nhắc lại có chủ ý. Trục 3 chỉ được đề nghị xoá
   **đoạn thân**; trục 4 chỉ được thi hành đề nghị đó, không được tự mở rộng.

6. **Mục "kết quả – tồn tại – phương hướng"** (T06). Đây là bố cục **bắt buộc** của báo cáo, tờ trình
   và sáng kiến kinh nghiệm ở Việt Nam, có trước mô hình ngôn ngữ. Giữ nguyên khung. Chỉ được bơm nội
   dung vào trong: mỗi "tồn tại" chỉ ra một việc cụ thể, mỗi "phương hướng" có người làm và mốc thời
   gian.

7. **Bộ ba song hành** (T10). Phép tu từ được dạy trong văn nghị luận và diễn văn tiếng Việt. Phép
   thử: bỏ phần tử thứ ba, câu nghèo đi thì giữ.

8. **Danh từ hoá và câu bị động không nêu chủ thể** (T13) ở văn bản hành chính, tờ trình, nghị quyết,
   và ở mục Phương pháp của bài nghiên cứu. `research.md` §5 khai đích danh đây là tín hiệu bình
   thường. Counter `NOMINAL` ở các thể loại này chỉ được in kèm nhãn baseline — xem mục 5 dưới.

9. **Cụm dẫn quy ước** (T23): "có thể nói rằng", "nhìn chung", "tóm lại", "trước hết", "thứ hai".
   Được dạy trong văn nghị luận. Chỉ sửa khi cụm đứng thay cho một phép đối lập mà tác giả không nêu.

10. **Thuật ngữ tiếng Anh cần thiết và phần chú giải lần đầu.** "học máy (machine learning)" ở lần
    đầu là đúng chuẩn viết. Chỉ bỏ những lần chú giải lặp lại từ lần thứ hai.

11. **Câu dài nhiều mệnh đề.** Ở bài học thuật, mệnh đề phụ là chỗ đặt điều kiện. Cắt cho ngắn thường
    đánh rơi điều kiện. Chỉ tách khi chủ thể của hành động bị chôn, và tách xong phải kiểm lại điều
    kiện còn nguyên.

Cộng thêm một luật về người viết, lấy từ `03-chong-bao-oan` §3: **người viết không phải bản ngữ, học
viên, người viết theo mẫu được phát** đều tạo ra văn đều đặn và công thức. Đó là hoàn cảnh viết,
không phải khuyết điểm cần chữa.

---

## 3. Chi tiết người — phải giữ, thậm chí phải bênh

Những thứ dưới đây thường bị người biên tập "làm sạch" đầu tiên vì trông lệch chuẩn. Chúng chính là
chỗ chứng minh có người ngồi viết.

- **Số lẻ không tròn:** "37 học viên", "2,7 triệu đồng". Không làm tròn thành "gần 40", "khoảng 3
  triệu". Làm tròn là sửa số liệu, thuộc vùng bảo vệ.
- **Tên đơn vị, tên lớp, tên phòng ban cụ thể** và ngày tháng cụ thể. Không thay bằng "một đơn vị",
  "thời gian qua".
- **Cách xưng hô của tác giả:** học viên Việt Nam xưng "em" với giảng viên; tác giả xưng "tôi",
  "chúng tôi", "người viết". Giữ nguyên cách xưng, giữ nguyên xuyên bài.
- **Lỗi nhỏ lặp lại nhất quán** — thói quen gõ của tác giả. Nếu writer profile có `known_typos[]`,
  đây là dữ liệu nhận dạng. Sửa được, nhưng phải liệt kê ra cho tác giả biết, không sửa lặng lẽ.
- **Ví dụ đời thường, chuyện lớp học, chuyện cơ quan.** Được rút gọn, không được thay bằng ví dụ
  "chuyên nghiệp hơn".
- **Câu ngắn cụt đứng một mình làm nhịp.** "Không. Không phải vậy." Đây là nhịp, không phải câu thiếu.
- **Thán từ, câu hỏi tu từ, chỗ ngập ngừng** ở thể loại cho phép: blog, tản văn, bài giảng.
- **Đơn vị đo và cách gọi địa phương:** "một sào", "một buổi", "khối 12". Không quy đổi.
- **Giọng đổi giữa các phần** khi bài do nhiều người viết chung và điều đó là thật. Làm phẳng cả bài
  thành một giọng "chuẩn" là xoá dấu vết cộng tác. `05-forensics/references/10-mau-bao-cao-va-cach-sua.md`
  §3 ghi đúng luật này: chọn baseline của tác giả, sửa riêng khối lệch, không san phẳng.

---

## 4. Năm mẫu bị loại khỏi danh mục

Danh mục tell của studio (`shared/rules/vi-ai-tells.json`) đã loại năm mẫu dưới đây — xem
`excluded_patterns[]` ở file đó. Lý do phải được nhắc lại ở đây vì chúng rất dễ bò ngược vào qua một
lần "cải tiến" sau này.

| Mẫu bị loại | Vì sao loại |
|---|---|
| **Em dash / en dash** (#14) | Tín hiệu tiếng Anh. Thực đo trong ca giám định: **0 lần** ở cả bài người lẫn bài máy tiếng Việt. `03-chong-bao-oan` §6 đã bác. Cấm em dash như một luật văn phong không có cơ sở trong tiếng Việt |
| **Ngoặc kép cong** (#19) | Word **tự chuẩn hoá** dấu nháy khi lưu. Đo được là đo trình soạn thảo, không đo người viết. Đã bác bằng thực đo |
| **Title Case** (#17) | Tiếng Việt không có khái niệm Title Case. Không chuyển được |
| **In đậm quá tay ở dạng mật độ thuần** (#15) | Mật độ chữ đậm không phân biệt được người với máy. Chỉ giữ phần có nghĩa: danh sách tiêu đề đậm **thay cho** đoạn văn, tức T16 |
| **Cặp gạch nối** (#26) | Không có tương đương trong chính tả tiếng Việt |

Và một mẫu bị **treo**, không bị loại: **danh sách từ mà mô hình hay dùng** (#7) nằm ở
`vi-ai-tells.json` với `status: needs_corpus`, ba trường ví dụ / phản chứng / cách sửa **để rỗng**.
Chỗ trống đó là câu trả lời trung thực. Dịch một danh sách từ tiếng Anh sang tiếng Việt rồi gọi nó là
language pack đúng là thứ `05d-calibration` cấm. **Không ai được điền vào ô đó bằng trực giác.**

---

## 5. Khi counter mâu thuẫn với baseline thể loại: baseline thắng

`skills/05-forensics/scripts/counters.py` không biết `genre_baseline`. Nó đếm `NOMINAL` và
`TEMPLATES` như nhau ở mọi thể loại. Vì vậy `scripts/polish_check.py` phải đọc `genre_baseline` của
`vi-ai-tells.json` và `§5` của hồ sơ thể loại **trước khi** in cột counter.

Ở thể loại có baseline khai tín hiệu đó là bình thường, cột counter được in kèm nhãn
**"baseline thể loại"** và **không được coi là chỗ phải sửa**. Con số vẫn hiện, vì che số đi là nói
dối, nhưng nó là mô tả chứ không phải việc cần làm.

Nguồn của luật này: cổng Phase 0, ghi trong `docs/plans/2026-08-30-skills-1-4-genres/tasks.md`.

---

## 6. Ba câu hỏi trước mỗi nhát sửa, và một quy tắc dừng

1. **Bản sau tốt hơn cho người đọc ở chỗ nào?** Viết được thành câu thì sửa. Không viết được, chỉ nói
   được "bớt giống máy", thì không sửa.
2. **Tác giả đọc bản sau có thể nói "tôi không viết thế" không?** Có lý thì hoàn tác.
3. **Chỗ này có nằm trong `preserve[]` hoặc trong mục 2 và mục 3 ở trên không?** Có thì dừng.

**Quy tắc dừng:** trong một đoạn, đếm số nhát sửa. Sửa quá nửa số câu trong một đoạn của bài do người
viết có provenance nghĩa là đang viết lại bài giùm người ta, không phải biên tập. Ghi cảnh báo vào
`warnings[]` và hỏi tác giả trước khi đi tiếp.
