# Danh mục lăng kính

Lăng kính là **tài sản của trục 3**. Hồ sơ thể loại chỉ bật hoặc tắt bằng `lenses[]` ở §3; nó không
được định nghĩa lăng kính mới, và trục 3 không được thêm lăng kính vì thấy bài "có vẻ cần". Danh mục
này là danh sách đóng: thêm một lăng kính là sửa file này, không phải sửa một hồ sơ thể loại.

Một lăng kính gồm đúng bốn phần, và phải đủ cả bốn mới được coi là lăng kính:

| Phần | Nghĩa |
|---|---|
| **Đầu vào** | Cần đọc gì, cần trích ra gì trước khi soi |
| **Câu hỏi** | Một câu hỏi duy nhất mà lăng kính này trả lời |
| **Bằng chứng cần** | Thứ phải trưng ra được; không có thì không có finding |
| **Đầu ra** | Ghi vào đâu trong `critique.json` |

Khung "một việc – một câu hỏi – một hợp đồng đầu ra" chưng cất từ cách `Fabric` tổ chức pattern
(MIT, xem `vendor-notes/fabric/`). Chỉ lấy nguyên lý tổ chức; toàn bộ câu hỏi dưới đây là tự soạn cho
tiếng Việt.

---

## Luật chung — đọc trước khi chạy bất kỳ lăng kính nào

1. **Chỉ chạy lăng kính mà §3 của hồ sơ thể loại bật.** Chạy thừa hay thiếu đều phải ghi vào
   `limitations[]`. Chạy thừa nguy hiểm hơn thiếu: nó tạo finding mà thể loại không yêu cầu.
2. **Không có bằng chứng thì không có finding.** Cảm giác "đoạn này yếu" chưa phải bằng chứng. Bằng
   chứng là câu trích được, đếm được hoặc đối chiếu được.
3. **Mỗi finding phải có phản chứng.** Viết cách đọc rộng lượng nhất của đoạn đó. Không nghĩ ra được
   thì bỏ finding — đây là luật của `critique.schema.json`, không phải lời khuyên.
4. **Lăng kính không phải tiêu chí.** Một lăng kính có thể đổ bằng chứng cho nhiều `criteria[]`, và
   một tiêu chí có thể nhận bằng chứng từ nhiều lăng kính. Trường `criterion_id` của finding nói
   finding này chấm vào tiêu chí nào; trường `lens` nói nó được tìm ra bằng cách nào.
5. **Lăng kính không phán về nguồn gốc văn bản.** "Đoạn này nghe như máy viết" không phải kết luận
   của trục 3. Trục 3 chấm chất lượng; nguồn gốc là việc của trục 5 và đi theo quy trình khác.
6. **Văn trơn tru không được cộng điểm cho lăng kính khác.** Một câu đẹp mà không thêm thông tin vẫn
   là câu yếu; điểm ngôn ngữ cao không được kéo điểm logic lên.

---

## 1. `fallacy_scan` — soi ngụy biện

- **Đầu vào:** các đoạn có kết luận; chuỗi tiền đề → kết luận đã viết lại thành 3–5 dòng.
- **Câu hỏi:** Bước nào trong chuỗi lập luận không được tiền đề đỡ, và nó rơi vào loại ngụy biện nào
  trong 13 loại ở [`02-nguy-bien-13-loai-vi.md`](02-nguy-bien-13-loai-vi.md)?
- **Bằng chứng cần:** câu trích chứa bước nhảy, tên loại ngụy biện, và một câu nói rõ tiền đề nào
  đang thiếu. Không đặt tên được loại thì đây là lập luận yếu, không phải ngụy biện.
- **Đầu ra:** `findings[]` với `lens: fallacy_scan`, `criterion_id` thường là tiêu chí logic của thể
  loại; `verification_question` hỏi tác giả tiền đề còn thiếu là gì.

## 2. `claim_check` — kiểm khẳng định

- **Đầu vào:** danh sách khẳng định **thực chứng** (kiểm đúng/sai được), tách khỏi khẳng định giá trị
  và khẳng định định nghĩa.
- **Câu hỏi:** Mỗi khẳng định này dựa vào đâu, và mức bằng chứng có tương xứng với mức khẳng định không?
- **Bằng chứng cần:** với mỗi khẳng định, ghi ba thứ: câu trích · thứ đang đỡ nó (số liệu, nguồn,
  suy luận, hoặc không có gì) · mức chắc chắn mà câu chữ đang phát biểu.
- **Đầu ra:** `criteria_scores[]` của tiêu chí bằng chứng lấy bảng này làm `evidence`; khẳng định
  quan trọng nhất mà không có gì đỡ trở thành `findings[]` và thường vào `must_fix[]`.

## 3. `task_response` — trả lời đúng nhiệm vụ

- **Đầu vào:** đề bài hoặc barem thật (`rubric_source`), và bản viết lại luận đề thành một câu.
- **Câu hỏi:** Bài có trả lời đúng thứ nhiệm vụ hỏi, đủ mọi phần của nhiệm vụ, hay chỉ viết quanh
  chủ đề?
- **Bằng chứng cần:** ánh xạ từng phần yêu cầu của đề → đoạn đáp ứng nó; và ngược lại, đoạn nào không
  ánh xạ về phần nào.
- **Đầu ra:** `criteria_scores[]` của tiêu chí trả lời đề. Đây là lăng kính có quyền phủ quyết: bài
  lạc đề không được cứu bằng điểm ngôn ngữ. Barem thật ghi ở `rubric_source` thắng hồ sơ thể loại.

## 4. `source_reliability` — độ tin cậy của nguồn

- **Đầu vào:** danh sách nguồn được trích, kèm điều mà mỗi nguồn đang được dùng để đỡ.
- **Câu hỏi:** Nguồn này có đủ tin cậy cho **mức khẳng định** mà nó đang đỡ không?
- **Bằng chứng cần:** loại nguồn (nghiên cứu gốc, tổng quan, báo chí, trang thương mại, ý kiến cá
  nhân), năm, và khoảng cách giữa điều nguồn nói với điều bài nói. Nguồn không mở được thì ghi
  "không kiểm được", không suy đoán.
- **Đầu ra:** `findings[]` với `lens: source_reliability`; nguồn không kiểm được đi vào
  `limitations[]`, không thành finding.
- **Cạm bẫy:** nêu tên tạp chí hoặc tên tác giả **không phải** là nguồn. Nguồn là kết quả cụ thể ở vị
  trí cụ thể.

## 5. `source_independence` — nguồn có độc lập nhau không

- **Đầu vào:** danh sách nguồn của cùng một khẳng định.
- **Câu hỏi:** Ba nguồn này có thật sự là ba nguồn, hay là ba lần nhắc lại cùng một nguồn gốc?
- **Bằng chứng cần:** chuỗi truy ngược của mỗi nguồn về nơi thông tin xuất hiện lần đầu; đánh dấu
  nguồn nào chỉ dẫn lại nguồn khác.
- **Đầu ra:** `findings[]`; khi cả chùm nguồn quy về một gốc, ghi rõ mức bằng chứng thật sự chỉ bằng
  một nguồn.

## 6. `balance_check` — các bên liên quan có được nêu không

- **Đầu vào:** danh sách các bên bị ảnh hưởng bởi vấn đề bài đang bàn.
- **Câu hỏi:** Bên nào có lợi ích trong chuyện này mà bài không cho tiếng nói, và việc thiếu bên đó
  có làm kết luận đổi không?
- **Bằng chứng cần:** danh sách các bên, đánh dấu bên đã có mặt và bên vắng; với bên vắng, một câu
  nói họ sẽ phản đối điều gì, **và câu trích trong bài mà kết luận sẽ đổi nếu họ được nghe**. Danh
  sách các bên phải rút từ chính đề xuất của bài (ai bị đề xuất này tác động), không phải từ danh
  sách tổng quát về chủ đề — nếu không, người chấm sẽ tự sinh ra bên vắng để có finding.
- **Đầu ra:** `findings[]`. **Không** chấm thiên vị chính trị: lăng kính này hỏi bài có nêu đủ bên
  không, không hỏi bài nên đứng về bên nào. Bài có lập trường rõ ràng không phải là bài mất cân bằng.
  Bên vắng mà việc vắng không đổi kết luận nào thì ghi vào `limitations[]`, không thành finding.

## 7. `method_rigor` — phương pháp có đỡ nổi kết luận không

- **Đầu vào:** mục phương pháp (hoặc phần mô tả cách tác giả biết điều mình nói), và danh sách kết luận.
- **Câu hỏi:** Thiết kế nghiên cứu này cho phép phát biểu tới mức nào, và kết luận có vượt quá mức đó
  không?
- **Bằng chứng cần:** với mỗi kết luận, ghi thiết kế đỡ nó (cỡ mẫu, cách chọn mẫu, có nhóm đối chứng
  không, đo một thời điểm hay theo dõi dọc) và động từ dùng để phát biểu.
- **Đầu ra:** `findings[]`; chỗ tương quan được phát biểu thành nhân quả gần như luôn vào `must_fix[]`.

## 8. `plot_consistency` — tình tiết có mâu thuẫn nhau không

- **Đầu vào:** dòng thời gian sự kiện và danh sách ràng buộc mà truyện đã tự đặt ra (luật của thế
  giới, khoảng cách, thời gian, thứ nhân vật biết và chưa biết).
- **Câu hỏi:** Có sự kiện nào chỉ xảy ra được khi vi phạm một ràng buộc mà chính truyện đã dựng không?
- **Bằng chứng cần:** hai vị trí trở lên, một chỗ dựng ràng buộc và một chỗ phá nó.
- **Đầu ra:** `findings[]` với hai `location` — chỗ dựng ghi ở `evidence`, chỗ phá ghi ở `location`.

## 9. `character_consistency` — nhân vật có làm điều đã bị loại trừ không

- **Đầu vào:** hồ sơ nhân vật rút từ chính văn bản: điều họ muốn, điều họ sợ, cách họ nói.
- **Câu hỏi:** Nhân vật này có làm điều mà những chương trước đã loại trừ, mà truyện không cho thấy
  vì sao họ đổi?
- **Bằng chứng cần:** chỗ thiết lập tính cách, chỗ hành động lệch, và khoảng trống giữa hai chỗ.
- **Đầu ra:** `findings[]`. Nhân vật thay đổi **không** là lỗi; thay đổi **không có nguyên nhân trong
  truyện** mới là lỗi. Phản chứng bắt buộc phải cân nhắc khả năng đây là chủ ý nghệ thuật.

## 10. `pacing_curve` — nhịp thắt mở

- **Đầu vào:** bản đồ độ dài từng phần kèm chuyện gì thay đổi trong mỗi phần.
- **Câu hỏi:** Đoạn nào dài mà không có gì thay đổi, và đoạn nào ngắn tới mức thay đổi lớn xảy ra
  không kịp cảm nhận?
- **Bằng chứng cần:** với mỗi phần, một câu "sau phần này, điều gì khác trước". Phần không trả lời
  được là phần chùng.
- **Đầu ra:** `criteria_scores[]` của tiêu chí nhịp; các đoạn chùng liệt kê trong `evidence`.

## 11. `value_density` — mỗi đoạn có thêm gì mới không

- **Đầu vào:** toàn bài, đọc theo đoạn.
- **Câu hỏi:** Xoá đoạn này đi thì người đọc mất thông tin gì — **hoặc mất chức năng gì** (định vị,
  chốt, chuyển)?
- **Bằng chứng cần:** danh sách đoạn kèm một câu "cái mới của đoạn" hoặc "chức năng của đoạn"; đoạn
  không viết được câu nào trong hai câu đó là đoạn rỗng.
- **Đầu ra:** `findings[]` cho đoạn rỗng, `suggested_fix` là gộp hoặc xoá.
- **Cạm bẫy — vùng không được chạm:** (1) mọi phần mà `structures[]` ở §2 của hồ sơ thể loại đặt tên
  là tóm tắt, kết luận, chốt hay kiến nghị — lặp là **chức năng** của các phần đó; (2) câu chốt cuối
  đoạn (Link trong PEEL, xem `vi-ai-tells.json` T31/T34); (3) lặp mà `genre_baseline` ở §5 khai là
  bình thường — ví dụ tóm tắt bài nghiên cứu lặp gần nguyên văn thân bài; (4) đoạn nhắc lại **có chủ
  ý** để nhấn. Lăng kính này chỉ được đề nghị xoá **đoạn thân**, không bao giờ đề nghị xoá phần kết cấu
  của thể loại. Đối chiếu `05-forensics/references/03-chong-bao-oan.md` §2, §6.

## 12. `retention` — người đọc bỏ đọc ở đâu

- **Đầu vào:** chân dung độc giả từ `context.json` nếu có; nếu không, giả định độc giả mặc định của
  thể loại.
- **Câu hỏi:** Nếu độc giả này bỏ đọc, họ bỏ ở câu nào và vì sao?
- **Bằng chứng cần:** vị trí cụ thể + lý do thuộc một trong bốn nhóm: chưa thấy lý do đọc tiếp · gặp
  thuật ngữ chưa được giải thích · đã đoán được phần còn lại · mất niềm tin vào tác giả.
- **Đầu ra:** `findings[]`, **và chỉ đến đó**. Đây là lăng kính chủ quan nhất trong danh mục, nên
  nó chạy ở chế độ **tư vấn**: finding của nó không được đổi `criteria_scores[]` và không được vào
  `must_fix[]`. Mức `severity`: `medium` chỉ khi lý do thuộc hai nhóm có neo văn bản (thuật ngữ chưa
  giải thích tại vị trí X; câu làm mất niềm tin — mâu thuẫn với chỗ đã nói trước đó); hai nhóm còn lại
  (chưa thấy lý do đọc tiếp, đã đoán được phần còn lại) là mô phỏng độc giả, luôn `low`. Luôn ghi giả
  định về độc giả vào `limitations[]`.

## 13. `three_chapter_selfcheck` — tự kiểm theo cụm ba chương

Lăng kính thứ 13, dành riêng cho truyện dài kỳ; danh mục lõi ở trên là 12. Chưng cất từ luật tự kiểm
theo cụm chương của `novel-writing-framework` (MIT, xem `vendor-notes/novel-writing-framework/`).

- **Đầu vào:** ba chương gần nhất, đọc liền một mạch.
- **Câu hỏi:** Ba chương này có tự mâu thuẫn, lặp cùng một nước cờ, hay để rơi một tuyến đã mở không?
- **Bằng chứng cần:** danh sách thứ đã hứa với người đọc trong ba chương và trạng thái của từng thứ
  (đã trả · đang treo · bị bỏ quên).
- **Đầu ra:** `findings[]`; tuyến bị bỏ quên vào `must_fix[]` khi nó đã được hứa tường minh.

---

## Lăng kính nào đổ vào tiêu chí nào

Bảng gợi ý, không phải ràng buộc — `criterion_id` do §3 của thể loại quyết định.

| Lăng kính | Tiêu chí thường nhận bằng chứng |
|---|---|
| `fallacy_scan` | logic, mạch lập luận |
| `claim_check` | bằng chứng, kết quả |
| `task_response` | trả lời đề bài |
| `source_reliability`, `source_independence` | bằng chứng, trích dẫn và nguồn |
| `balance_check` | phản biện, cân bằng |
| `method_rigor` | phương pháp, bàn luận và giới hạn |
| `plot_consistency`, `character_consistency`, `three_chapter_selfcheck` | nhất quán |
| `pacing_curve`, `retention` | nhịp, sức giữ người đọc |
| `value_density` | liên kết, mật độ thông tin |
