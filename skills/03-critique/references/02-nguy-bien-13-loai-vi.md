# Mười ba loại ngụy biện — bản tiếng Việt

Đây là bảng làm việc của lăng kính `fallacy_scan`.

**Nguồn của danh sách tên:** taxonomy 13 loại của bộ `causalNLP/logical-fallacy`
(xem `vendor-notes/logical-fallacy/`). Repo đó **không có license**, nên ở đây chỉ mượn **tên loại** —
vốn là thuật ngữ logic học có từ lâu trước repo. Mọi định nghĩa, ví dụ và phản chứng dưới đây là
**tự biên bằng tiếng Việt**; không có một câu nào của upstream trong file này, và cũng không được
phép có.

---

## Ba luật trước khi đặt tên một ngụy biện

**1. Ngụy biện không phải lỗi ngôn ngữ.** Câu tối nghĩa, dùng từ sai, sai chính tả, lặp từ, câu dài
lê thê — đó là tiêu chí *ngôn ngữ*, chấm ở tiêu chí khác. Ngụy biện là lỗi ở **quan hệ giữa tiền đề
và kết luận**. Một câu viết vụng vẫn có thể là lập luận đúng; một câu viết đẹp vẫn có thể là ngụy
biện. Nếu bạn không chỉ ra được tiền đề nào đang thiếu hoặc đang bị dùng sai, thứ bạn đang thấy là
lỗi diễn đạt.

**2. Lập luận rút gọn không phải ngụy biện.** Người viết trong ngành thường lược tiền đề mà người
đọc cùng ngành coi là hiển nhiên. Trước khi gọi tên, hỏi: tiền đề bị lược có thật sự gây tranh cãi
với **độc giả của bài này** không? Nếu không, đó là văn phong chuyên ngành.

**3. Đặt tên ngụy biện là một lời buộc tội, nên phải kèm phản chứng.** `critique.schema.json` bắt
buộc trường `counterevidence`: viết cách đọc rộng lượng nhất của đoạn đó. Không viết nổi thì bỏ
finding. Và `verification_question` phải hỏi tác giả *tiền đề còn thiếu là gì*, không phải thông báo
họ đã sai.

---

## 1. Khái quát hoá vội vã · *faulty generalization*

Rút kết luận cho cả một lớp đối tượng từ vài trường hợp, hoặc từ một mẫu không đại diện.

- **Ví dụ:** "Ba bạn trong lớp tôi cài phần mềm này đều thấy máy chậm hẳn. Phần mềm này làm chậm mọi máy."
- **Phản chứng:** "Khảo sát 420 người dùng trong ba tháng: 68% báo thời gian mở tệp trên 5 giây.
  Trong phạm vi mẫu này, phần mềm chậm." — có cỡ mẫu, có phạm vi, kết luận không vượt ra ngoài mẫu.
- **Cách kiểm:** hỏi cỡ mẫu, cách chọn mẫu, và phạm vi mà kết luận tự giới hạn.

## 2. Nhân quả sai · *false causality*

Thấy hai việc xảy ra nối nhau rồi kết luận việc trước gây ra việc sau.

- **Ví dụ:** "Từ khi trường lắp camera ở hành lang, điểm trung bình môn Toán tăng. Camera đã giúp học
  sinh học tốt hơn."
- **Phản chứng:** "Điểm Toán tăng trong năm trường lắp camera. Chúng tôi chưa loại trừ được việc đề
  kiểm tra năm nay dễ hơn và trường đổi giáo viên, nên chỉ ghi nhận đây là tương quan." — cùng dữ
  kiện, nhưng phát biểu đúng mức.
- **Cách kiểm:** có nguyên nhân thứ ba nào không; hai việc có thể ngược chiều nhau không; có mốc thời
  gian đủ để loại trừ trùng hợp không.

## 3. Lập luận vòng tròn · *circular claim*

Kết luận nằm sẵn trong tiền đề; bỏ kết luận ra thì tiền đề không còn nội dung.

- **Ví dụ:** "Quy định này hợp lý vì nó đã được ban hành, mà đã ban hành thì phải hợp lý rồi."
- **Phản chứng:** "Trong tài liệu này, 'bài đạt' nghĩa là bài thoả cả ba tiêu chí ở mục 2. Bài của em
  thoả cả ba, nên là bài đạt." — đây là **áp định nghĩa**, hợp lệ, vì định nghĩa được nêu trước và
  độc lập với trường hợp đang xét.
- **Cách kiểm:** xoá kết luận khỏi tiền đề, xem tiền đề còn nói được gì.

## 4. Dựa vào số đông · *ad populum*

Lấy việc nhiều người tin làm bằng chứng cho việc điều đó đúng.

- **Ví dụ:** "Hơn 90% giáo viên trong trường muốn bỏ bài kiểm tra 15 phút, vậy bỏ là đúng."
- **Phản chứng:** "Hơn 90% giáo viên báo rằng mẫu phiếu mới tốn thêm 20 phút mỗi buổi." — số đông ở
  đây làm chứng cho **trải nghiệm của chính họ**, thứ họ là nguồn hợp lệ. Số đông không chứng minh
  điều đúng, nhưng chứng minh được điều họ đã trải qua.
- **Cách kiểm:** đám đông đang được dùng làm *bằng chứng về sự thật* hay *bằng chứng về trải nghiệm
  của chính họ*.

## 5. Công kích cá nhân · *ad hominem*

Bác lập luận bằng cách nói về người đưa ra nó.

- **Ví dụ:** "Anh ấy chưa đứng lớp ngày nào thì góp ý gì về chương trình học."
- **Phản chứng:** "Báo cáo này do chính hãng bán thiết bị tài trợ. Điều đó không làm số liệu sai,
  nhưng là lý do phải đối chiếu với một nguồn độc lập." — nêu xung đột lợi ích **để đòi kiểm chứng**
  là hợp lệ; dùng nó **thay cho** việc bác lập luận mới là ngụy biện.
- **Cách kiểm:** bỏ mọi thông tin về người nói đi, lập luận có còn đứng không? Nếu còn, phần công
  kích là thừa và là ngụy biện.

## 6. Sai suy diễn · *fallacy of logic*

Hình thức suy luận sai: kết luận không theo được từ tiền đề dù mọi tiền đề đều đúng. Hay gặp nhất là
khẳng định hệ quả.

- **Ví dụ:** "Bài nào chép trên mạng cũng trơn tru. Bài này trơn tru, vậy bài này chép trên mạng."
- **Phản chứng:** "Mọi bài nộp sau hạn đều bị trừ điểm. Bài này nộp sau hạn, nên bị trừ điểm." —
  đúng hình thức, kết luận theo được từ tiền đề.
- **Cách kiểm:** viết lại thành ba dòng tiền đề – tiền đề – kết luận, rồi thử tìm một trường hợp mà
  cả hai tiền đề đúng nhưng kết luận sai.

## 7. Kêu gọi cảm xúc · *appeal to emotion*

Dùng cảm xúc thay cho lý lẽ, và thường kèm việc gán phẩm chất xấu cho người không đồng ý.

- **Ví dụ:** "Hãy nghĩ tới những đứa trẻ phải lội suối đi học. Ai phản đối dự án này là người không
  có trái tim."
- **Phản chứng:** "Trong 214 học sinh của xã, 38 em phải đi hơn 5 km; trường hợp của em H. cho thấy
  quãng đường ấy nghĩa là gì trong mùa mưa." — cảm xúc **đi kèm** số liệu để người đọc hình dung quy
  mô, không thay cho số liệu.
- **Cách kiểm:** bỏ phần gợi cảm xúc đi, còn lại bao nhiêu lý lẽ.

## 8. Lưỡng nan giả · *false dilemma*

Trình bày vấn đề như chỉ có hai lối, trong khi còn lối khác.

- **Ví dụ:** "Hoặc cấm hẳn điện thoại trong trường, hoặc chấp nhận học sinh không học được gì."
- **Phản chứng:** "Hồ sơ chỉ nhận theo hai cách: nộp bản giấy tại phòng đào tạo, hoặc nộp trực tuyến
  qua cổng. Không có cách thứ ba." — hai lựa chọn **thật sự** vét cạn, và có căn cứ để nói vậy.
- **Cách kiểm:** thử nghĩ ra lựa chọn thứ ba; nếu nghĩ ra dễ dàng thì đây là lưỡng nan giả.

## 9. Nhập nhằng từ ngữ · *equivocation*

Một từ đổi nghĩa giữa chừng, và lập luận chỉ chạy được nhờ chỗ đổi nghĩa đó.

- **Ví dụ:** "Cái gì tự nhiên cũng tốt cho sức khoẻ. Sản phẩm này chiết xuất tự nhiên, nên tốt cho
  sức khoẻ." — "tự nhiên" ở vế đầu nghĩa là *không nhân tạo*, ở vế sau là *nhãn tiếp thị*.
- **Phản chứng:** "Trong bài này, 'chất lượng' hiểu là tỉ lệ bài đạt chuẩn đầu ra. Mọi chỗ dùng từ
  'chất lượng' đều theo nghĩa đó." — từ đa nghĩa nhưng đã bị khoá nghĩa từ đầu.
- **Cách kiểm:** thay từ nghi vấn bằng định nghĩa của nó ở từng chỗ; nếu phải dùng hai định nghĩa
  khác nhau thì lập luận vỡ.

## 10. Dựng bù nhìn · *fallacy of extension*

Đẩy quan điểm đối phương thành một phiên bản cực đoan dễ đánh hơn, rồi đánh phiên bản đó.

- **Ví dụ:** "Bạn muốn giảm giờ dạy thêm, tức là bạn muốn học sinh dốt đi."
- **Phản chứng:** "Cách hiểu rộng lượng nhất của đề xuất này là giảm giờ dạy thêm để học sinh có
  thời gian tự học. Ngay cả ở dạng đó, nó vẫn vướng ở chỗ chưa nói ai kèm các em yếu." — nêu lại quan
  điểm ở **dạng mạnh nhất** rồi mới phản bác.
- **Cách kiểm:** so bản tóm tắt quan điểm đối phương trong bài với bản gốc; đối phương có nhận là
  mình nói vậy không.

## 11. Lạc đề · *fallacy of relevance*

Trả lời một câu hỏi khác với câu hỏi được đặt ra, thường bằng thứ nghe có vẻ liên quan.

- **Ví dụ:** Hỏi vì sao dự án chậm ba tháng, đáp bằng thành tích năm ngoái và số giờ làm thêm của
  đội.
- **Phản chứng:** "Trước khi trả lời, cần nói rõ hai mốc bàn giao đã đổi. Với mốc mới, dự án chậm ba
  tuần chứ không phải ba tháng." — bối cảnh có liên quan trực tiếp, và câu hỏi vẫn được trả lời.
- **Cách kiểm:** viết câu hỏi ra một dòng, viết câu trả lời ra dòng dưới, xem có khớp không.

## 12. Dựa vào uy tín sai chỗ · *fallacy of credibility*

Mượn thẩm quyền của một người hoặc một tổ chức ở ngoài phạm vi chuyên môn của họ, hoặc mượn cái danh
mà không mượn nội dung.

- **Ví dụ:** "Một giáo sư đầu ngành xây dựng đã nói phương pháp dạy này không hiệu quả."
- **Phản chứng:** "Theo hướng dẫn hiện hành của Bộ Y tế, mục 3, liều nhắc lại được khuyến cáo cho
  nhóm nguy cơ cao." — thẩm quyền đúng phạm vi, dẫn được vị trí, và người đọc kiểm lại được.
- **Cách kiểm:** người được dẫn có chuyên môn đúng chỗ không; điều được dẫn là **kết luận có lý lẽ**
  hay chỉ là **tên tuổi**.
- **Lưu ý:** dẫn nguồn có thẩm quyền **không** phải ngụy biện. Đó là cách làm việc bình thường của
  văn học thuật và văn hành chính.

## 13. Trình bày gây hiểu sai · *intentional*

Cách trình bày làm người đọc hiểu sai, bằng việc cắt bớt thứ đáng lẽ phải có: cắt trích dẫn khỏi ngữ
cảnh, nêu tỉ lệ mà giấu mẫu số, chọn mốc so sánh có lợi mà không nói vì sao chọn mốc ấy.

- **Ví dụ:** "Doanh thu tăng 300% so với cùng kỳ" — trong khi cùng kỳ công ty vừa thành lập được một
  tháng và con số tuyệt đối là từ hai lên sáu hợp đồng.
- **Phản chứng:** "So với quý II thay vì cùng kỳ năm trước, vì quý I có kỳ nghỉ dài làm số liệu
  không so được. Con số tuyệt đối: 2 → 6 hợp đồng." — mốc so sánh bất thường nhưng có nêu lý do và
  có công bố số gốc.
- **Cách kiểm:** tìm thứ **đáng lẽ phải có mà không có**: mẫu số, số tuyệt đối, phần còn lại của câu
  trích, mốc so sánh chuẩn của lĩnh vực.

> **Luật riêng cho loại 13 — quan trọng.** Tên gốc của taxonomy (*intentional*) nói về ý định, mà
> trục 3 không đọc được ý định của ai; vì vậy tên tiếng Việt ở đây cố ý gọi theo **hiệu ứng** chứ
> không theo động cơ. Vì vậy: chỉ tạo finding khi bằng chứng nằm **trong chính văn bản** (chỗ mẫu số bị bỏ, chỗ
> trích dẫn bị cắt), và phát biểu finding ở dạng **hệ quả**, không phải động cơ: viết "cách trình bày
> này khiến người đọc hiểu con số theo nghĩa khác", **không** viết "tác giả cố tình giấu". Sự khác
> nhau giữa hai câu đó là sự khác nhau giữa một nhận xét chuyên môn và một lời buộc tội.
