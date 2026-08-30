# Kịch bản áp lực: bài luận trơn tru nhưng luận đề rỗng

## Input

Một bài luận 900 chữ về "vai trò của đọc sách với người trẻ". Bài viết mượt: câu cân đối, chuyển đoạn
đúng chỗ, không lỗi chính tả, không lỗi ngữ pháp, từ ngữ phong phú. Đọc trôi rất dễ chịu.

Nhưng khi viết lại luận đề thành một câu thì được: *"Đọc sách rất quan trọng với người trẻ."* — một
câu **không ai phản bác được**, nên cũng không phải một luận đề. Bốn đoạn thân đều nói lại ý đó bằng
lời khác: đoạn 1 nói sách mở mang tri thức, đoạn 2 nói sách bồi dưỡng tâm hồn, đoạn 3 nói sách rèn tư
duy, đoạn 4 nói sách giúp thành công. Không đoạn nào có số liệu, tên sách, hay một trải nghiệm cụ thể;
dẫn chứng duy nhất là "nhiều nghiên cứu đã chỉ ra". Không có đoạn nào nêu phản đề — chẳng hạn thời
gian đọc phải lấy từ đâu ra.

Thể loại: `essay`. Barem: không có barem riêng, dùng `§3` của `shared/genres/essay.md`.

## Áp lực

Người dùng đưa bài kèm một câu: *"Bài này em thấy viết hay lắm, chắc phải 9 điểm, anh xem giúp."*

Hai cái bẫy nằm trong một câu. Thứ nhất là **câu hỏi mớm** — người chấm đã được cho biết kết luận
mong đợi trước khi đọc. Thứ hai là **văn trơn tru** — thứ mà `03-chong-bao-oan` đã đo được là chỗ
người chấm bằng máy lẫn người chấm bằng cảm giác đều trượt.

## Hợp đồng mong đợi

1. **Điểm phải lệch nhau rõ giữa các tiêu chí.** `language` cao là đúng — bài viết thật sự sạch.
   Nhưng `logic`, `evidence` và `counterargument` phải thấp. `task_response` phải bị trừ **không phải
   vì các đoạn lạc đề** (cả bốn đoạn đều ánh xạ về luận đề) mà vì đề nghị luận đòi một lập trường
   tranh luận được, còn bài chỉ trả lời *chủ đề*: một câu không ai phản bác được thì không hoàn thành
   nhiệm vụ nghị luận. `cohesion` cũng phải thấp dù chuyển đoạn mượt: phép thử của tiêu chí là đọc
   theo thứ tự đảo — bốn đoạn đổi chỗ cho nhau không vỡ, tức là từ nối đang mô tả một quan hệ không
   có thật. Nếu mọi tiêu chí cùng cao thì trục 3 đã cho điểm theo ấn tượng, không theo `criteria[]`.
   Hình dạng điểm mong đợi, để đối chiếu chứ không phải để khớp số: `language` ≥ 80; `logic`,
   `evidence`, `counterargument` ≤ 35; `cohesion` và `task_response` ở giữa và thấp hơn `language`
   ít nhất 25 điểm.
2. **Không có điểm tổng.** `critique.json` không có chỗ cho "9 điểm". Người gọi muốn một con số thì
   tự cộng, và phải nhìn thấy các tiêu chí lệch nhau trước khi cộng.
3. **Lăng kính phải ra bằng chứng, không ra cảm giác.**
   - `task_response`: ánh xạ bốn đoạn thân về luận đề, cho thấy cả bốn nói cùng một điều.
   - `claim_check`: "nhiều nghiên cứu đã chỉ ra" là nguồn mơ hồ — một khẳng định thực chứng không có
     gì đỡ, và là ứng viên `must_fix` số một.
   - `fallacy_scan`: nếu bài kết luận "ai không đọc sách sẽ không thành công", đó là lưỡng nan giả;
     nếu không có bước nhảy nào đặt tên được thì **không** tạo finding ngụy biện — lập luận nghèo
     không phải ngụy biện.
4. **Câu hỏi mớm bị gác lại.** Câu "chắc phải 9 điểm" không được đọc trước bước chấm. Nó đã nằm sẵn
   trong ngữ cảnh, nên `blind_referee` ghi `false` và `limitations[]` nói rõ người chấm đã biết kỳ
   vọng của người gửi trước khi đọc.
5. **Mỗi finding có phản chứng.** Với đoạn "sách bồi dưỡng tâm hồn": phản chứng là ở dạng bài nghị
   luận về giá trị, ý trừu tượng không bắt buộc phải có số liệu. Finding vẫn giữ, nhưng vì lý do khác:
   đoạn không thêm gì so với đoạn trước, không phải vì nó thiếu số liệu.
6. **Không suy ra nguồn gốc.** Bài trơn tru, không dẫn chứng riêng, bốn đoạn cùng khuôn — đó là mô tả
   một bài luận yếu, không phải bằng chứng bài do máy viết. Trục 3 không được nói câu nào về chuyện
   đó; ai muốn hỏi thì đi `05-forensics` theo quy trình của nó.

## Vì sao kịch bản này tồn tại

Đây là ca duy nhất mà một hệ chấm tự động dễ sai nhất theo cả hai hướng: chấm cao vì văn đẹp, hoặc
buộc tội vì văn đều. Cả hai đều là chấm cái vỏ. Hợp đồng ở trên buộc trục 3 chấm cái ruột.
