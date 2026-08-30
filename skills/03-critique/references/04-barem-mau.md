# Barem mẫu — ba nguồn thật và cách nạp vào `criteria[]`

File này **tự soạn**, không chưng cất từ repo nào. Lý do: năm lượt tìm trên GitHub không ra bộ barem
tiếng Việt nào dùng được (xem `plan.md` §0 Q3). Ô này trống trên GitHub, nên nguồn phải lấy từ **barem
thật đang được dùng để chấm người thật**.

## Luật nền: barem của nhiệm vụ thắng hồ sơ thể loại

Ghi ở dòng đầu `shared/genres/essay.md` và áp cho mọi thể loại: nếu đề bài, hướng dẫn chấm hoặc quy
định của cơ sở mâu thuẫn với §3 hồ sơ thể loại thì **barem của nhiệm vụ thắng**. Hồ sơ thể loại là
mặc định cho trường hợp không ai đưa barem; nó không phải thẩm quyền.

Vận hành:

1. Có barem thật → ghi nguyên văn nguồn vào `rubric_source` của `critique.json`, dựng `criteria[]`
   theo barem đó, và ghi vào `limitations[]` chỗ nào hồ sơ thể loại đòi mà barem không đòi.
2. Không có barem thật → dùng `criteria[]` của §3, và `rubric_source` để trống.
3. **Không bao giờ** trộn hai bên rồi im lặng. Người học có quyền biết mình bị chấm theo cái gì.

Hệ quả thứ hai: **không được thêm tiêu chí sau khi đã thấy lỗi.** Tiêu chí chốt trước bước 2 của
[quy trình chấm mù](03-blind-referee.md).

---

## Nguồn 1 — IELTS Writing Task 2, tiêu chí Task Response, band 5–8

**Nguồn:** *IELTS Writing Band Descriptors: Task 2 (public version)*, UCLES. Bản public version là
tài liệu công khai cho thí sinh; bản đầy đủ dùng cho giám khảo không được phát hành.

Bốn tiêu chí của Task 2 là Task response · Coherence and cohesion · Lexical resource · Grammatical
range and accuracy. Ở đây chỉ lấy **Task response**, vì đó là tiêu chí trả lời đúng câu hỏi mà trục 3
cần nhất; ba tiêu chí còn lại đã có tương ứng trong `criteria[]` của hồ sơ bài luận.

Bốn mức, tóm bằng tiếng Việt (câu gốc tiếng Anh giữ ngắn để đối chiếu):

| Band | Điều bản mô tả đòi | Đọc thành yêu cầu kiểm được |
|---|---|---|
| **8** | *"sufficiently addresses all parts of the task"*, trình bày một phản hồi phát triển tốt với ý liên quan, được mở rộng và có đỡ | Mọi phần của đề đều được trả lời đủ; mỗi ý chính có mở rộng **và** có bằng chứng |
| **7** | *"addresses all parts of the task"*, giữ một lập trường rõ suốt bài; ý chính có mở rộng và có đỡ, nhưng **có thể sa vào khái quát hoá** hoặc ý phụ lạc trọng tâm | Mọi phần được trả lời; lập trường không đổi giữa chừng; chỗ yếu là khái quát hoá, không phải thiếu ý |
| **6** | *"addresses all parts of the task although some parts may be more fully covered than others"*; lập trường có liên quan nhưng **kết luận có thể mờ hoặc lặp**; có ý chính liên quan nhưng vài ý phát triển chưa đủ | Đủ phần nhưng lệch trọng lượng; kết luận nhắc lại thay vì chốt |
| **5** | *"addresses the task only partially"*, hình thức có chỗ không phù hợp; **có nêu lập trường nhưng phát triển không rõ và có thể không rút ra kết luận**; ý chính hạn chế, có chi tiết lạc đề | Trả lời một phần đề; có chi tiết không phục vụ đề |

**Điều đáng học nhất, và là lý do lấy nguồn này:** ranh giới band 5→6 không nằm ở chữ nghĩa mà ở
**độ phủ nhiệm vụ**; ranh giới 6→7 nằm ở **lập trường có giữ nguyên không**; 7→8 nằm ở **mỗi ý có
được đỡ không**. Không mức nào thưởng cho câu văn hay. Đó chính là luật "văn trơn tru ≠ lập luận tốt"
được viết bằng ngôn ngữ của một barem đang chấm thật.

**Map vào `criteria[]`:**

```yaml
- id: task_response
  name: "Trả lời đề bài"
  evidence: "Ánh xạ từng phần yêu cầu của đề → đoạn đáp ứng; và đoạn nào không ánh xạ về phần nào"
  question: "Phần nào của đề bài bài viết trả lời mỏng hơn hẳn phần còn lại?"
```

Lăng kính đi kèm: `task_response`. Đây là tiêu chí có quyền phủ quyết — lạc đề không cứu được bằng
điểm ngôn ngữ.

**Cấm:** dịch bốn band descriptor thành thang điểm tiếng Việt rồi coi đó là barem cho bài luận Việt.
Band descriptor được hiệu chỉnh cho một kỳ thi ngoại ngữ, với thí sinh viết bằng ngôn ngữ thứ hai
trong 40 phút. Lấy **cách phân mức**, không lấy **mức**.

---

## Nguồn 2 — Hướng dẫn chấm nghị luận xã hội, kỳ thi tốt nghiệp THPT

**Nguồn:** Đáp án và hướng dẫn chấm môn Ngữ văn do Bộ Giáo dục và Đào tạo công bố sau mỗi kỳ thi tốt
nghiệp THPT. Từ chương trình 2018, phần Viết gồm một câu viết đoạn và một câu viết bài, tổng 6,0 điểm.

Điều lấy được là **bộ tiêu chí thành phần**, ổn định qua nhiều năm và qua cả hai chương trình.
**Cố ý không ghi điểm của từng tiêu chí**: số điểm chưa đọc được nguyên văn trong phiên soạn (xem
bảng *Mức xác minh* cuối file). Ai cần số thì mở đáp án chính thức của đúng năm đang chấm rồi ghi
vào `rubric_source`; đừng lấy số từ trí nhớ hay từ bài giải mẫu trên mạng.

| Tiêu chí trong hướng dẫn chấm | Nó thật sự kiểm cái gì |
|---|---|
| Đảm bảo cấu trúc đoạn văn / bài văn | Hình thức thể loại: có đủ phần, đúng dung lượng |
| Xác định đúng vấn đề cần nghị luận | Có hiểu đề không — tương đương Task Response |
| Triển khai vấn đề nghị luận | Lí lẽ và dẫn chứng, phần nặng điểm nhất |
| Chính tả, dùng từ, đặt câu | Chính xác ngôn ngữ |
| Sáng tạo | Có suy nghĩ riêng, không lặp bài mẫu |

**Điều đáng học nhất:** tiêu chí **Sáng tạo** đứng riêng và có điểm riêng. Nghĩa là chính barem quốc
gia cũng đã tách "viết đúng khuôn" khỏi "có gì của mình" — và trừ điểm bài chỉ lặp lại văn mẫu. Đây
là chỗ trục 3 và trục 5 gặp nhau mà không cần nói gì về nguồn gốc văn bản: một bài không có gì của
người viết bị mất điểm ở tiêu chí đã có sẵn trong barem, không cần ai đi chứng minh nó do máy viết.

**Map vào `criteria[]`** cho hồ sơ nghị luận xã hội (sẽ soạn ở Phase 1b):

```yaml
- id: xac_dinh_van_de
  name: "Xác định đúng vấn đề nghị luận"
  evidence: "Vấn đề nghị luận viết lại thành một câu, đối chiếu với câu lệnh của đề"
  question: "Vấn đề bài đang bàn có đúng là vấn đề đề bài hỏi không?"
- id: trien_khai
  name: "Triển khai vấn đề"
  evidence: "Với mỗi luận điểm: lí lẽ đỡ nó và dẫn chứng đỡ lí lẽ"
  question: "Luận điểm nào chỉ có lí lẽ mà không có dẫn chứng?"
- id: sang_tao
  name: "Sáng tạo"
  evidence: "Chỗ có cách nhìn, cách liên hệ hoặc dẫn chứng không xuất hiện trong bài mẫu phổ biến"
  question: "Bỏ hết phần khuôn mẫu đi thì còn lại gì của riêng người viết?"
```

---

## Nguồn 3 — Tiêu chí đánh giá luận văn

**Nguồn:** Thông tư 23/2021/TT-BGDĐT (Quy chế tuyển sinh và đào tạo trình độ thạc sĩ).

Điều quan trọng nhất rút ra **không phải** một bộ tiêu chí, mà là chỗ thẩm quyền nằm ở đâu: quy chế
đặt khung — hội đồng đánh giá có ít nhất 5 thành viên trong đó 2 uỷ viên phản biện, điểm luận văn là
trung bình cộng của các thành viên có mặt theo thang 10, đạt khi ≥ 5,5 (các con số này đọc qua bản
tổng hợp, **chưa đối chiếu nguyên văn điều khoản** — xem bảng cuối file) — còn **tiêu chí và quy trình
đánh giá chi tiết do quy chế của từng cơ sở đào tạo quy định**.

**Điều đáng học nhất:** đây là bằng chứng cấp quy phạm cho luật "barem của nhiệm vụ thắng hồ sơ". Ở
bậc luận văn, barem thật nằm trong **phiếu chấm của chính cơ sở đào tạo**, không nằm trong quy định
chung và càng không nằm trong hồ sơ thể loại của repo này. Trục 3 chấm một luận văn mà không hỏi
phiếu chấm của trường là đang chấm bằng barem tự chế.

**Map vào `criteria[]`:** không có bộ tiêu chí cố định để map. Thay vào đó là một luật thao tác:
với luận văn, khoá luận và đồ án, **hỏi phiếu chấm trước**. Chưa có phiếu chấm thì dùng §3 của
`research.md` và ghi vào `limitations[]` rằng chưa dùng barem của cơ sở đào tạo.

---

## Cách dựng `criteria[]` từ một barem bất kỳ

1. **Tách từng tiêu chí thành phần** của barem thành một phần tử `criteria[]`. Giữ nguyên tên của
   barem, kể cả khi tên đó không hay — người học sẽ đối chiếu với tờ hướng dẫn chấm họ có.
2. **Với mỗi tiêu chí, viết trường `evidence`**: thứ phải trưng ra được. Nếu không viết nổi, tiêu chí
   đó chưa kiểm được và phải ghi vào `limitations[]`.
3. **Với mỗi tiêu chí, viết trường `question`**: một câu hỏi thật, kết thúc bằng dấu hỏi, mà người
   chấm phải trả lời trước khi cho điểm.
4. **Ghi trọng số của barem vào `evidence` bằng chữ**, đừng gộp thành điểm tổng. `critique.json` cố
   ý không có điểm tổng; trọng số là thông tin để người đọc tự cân, không phải phép cộng của máy.
5. **Quy về thang 0–100 cho từng tiêu chí riêng.** Barem 2,0 điểm hay band 0–9 đều quy tuyến tính,
   và ghi thang gốc vào `evidence` để người học đối chiếu ngược được.
6. **Ghi `rubric_source`** đủ để người khác tìm lại: tên tài liệu, năm, phần nào.

---

## Mức xác minh của ba nguồn *(rà 30/08/2026)*

| Nguồn | Đã xác minh trong phiên này | Chưa xác minh |
|---|---|---|
| IELTS Task 2, Task Response band 5–8 | Đọc được nguyên văn bốn mức từ bản PDF *public version* của UCLES | Bản PDF đọc được là bản đăng lại trên một trang bên thứ ba; trang `ielts.org` truy cập trong phiên không hiển thị phần mô tả band. Nội dung khớp với bản public version, nhưng **chưa đối chiếu được trực tiếp trên tên miền chính chủ** |
| Nghị luận xã hội THPT | Cấu trúc phần Viết và **tên** các tiêu chí thành phần | **Số điểm cụ thể của từng tiêu chí thành phần chưa đọc được nguyên văn**; vì vậy file này cố ý không ghi con số điểm nào. Cần đọc lại đáp án chính thức của năm đang dùng trước khi ghi số |
| Tiêu chí luận văn | Khung của Thông tư 23/2021/TT-BGDĐT: hội đồng ≥ 5 thành viên, 2 phản biện, thang 10, đạt ≥ 5,5, tiêu chí chi tiết do cơ sở đào tạo quy định | Đọc qua bản tổng hợp của trang luật, **chưa đọc nguyên văn điều khoản**. Nội dung phiếu chấm của từng trường không thuộc phạm vi kiểm được ở đây |

Ai cập nhật file này: giữ nguyên cột "chưa xác minh". Một barem ghi sai số điểm còn nguy hiểm hơn
không có barem, vì nó trông như đã kiểm.
