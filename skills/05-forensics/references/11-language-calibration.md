# Hiệu chỉnh theo ngôn ngữ và chuyển hóa tri thức ngoại ngữ

Mục tiêu là mang **phương pháp** về cho agent, không mang nguyên danh sách từ hoặc ngưỡng của một
ngôn ngữ sang ngôn ngữ khác. Ngôn ngữ thay đổi cách tách từ, nhịp câu, công thức lịch sự, cấu trúc
lập luận và chuẩn thể loại; vì vậy **không chép ngưỡng** từ corpus tiếng Anh sang tiếng Việt.

## 1. Khi nhận tài liệu không phải tiếng Việt

1. Nhận diện ngôn ngữ chính, các đoạn chuyển mã và phần trích dẫn.
2. Giữ nguyên trích dẫn gốc làm bằng chứng; diễn giải ý nghĩa bằng tiếng Việt ngay bên dưới.
3. Áp dụng các họ dấu hiệu bền qua ngôn ngữ: khẳng định rỗng, nguồn mơ hồ, đổi giọng, lặp khuôn,
   thiếu chuẩn thể loại và mâu thuẫn lập luận.
4. Tạm ngưng tiêu chí phụ thuộc từ vựng, tokenizer hoặc thành ngữ nếu chưa có baseline phù hợp.
5. Báo cáo bằng tiếng Việt. Không dịch câu rồi dùng bản dịch để kết luận về văn phong nguyên bản.

Nếu chưa có profile ngôn ngữ/thể loại, trả `insufficient_calibration`, `S=null`, `C=null` và không tạo
action band. Vẫn được nêu finding định tính có trích dẫn và phản chứng, nhưng không xuất khoảng điểm
hoặc tuyên bố độ chính xác.

## 2. Cách chuyển hóa phương pháp từ nguồn ngoại ngữ

Với mỗi rule upstream, lập thẻ bốn dòng:

- **Ý định:** hiện tượng nào cần phát hiện?
- **Phần bền:** điều gì không phụ thuộc ngôn ngữ?
- **Phần cần bản địa hóa:** tokenizer, từ điển, cấu trúc câu, chuẩn thể loại hay ngưỡng nào?
- **Phép bác bỏ:** ví dụ vô tội nào khiến rule phải im lặng?

Chỉ đưa rule vào skill khi agent có thể đọc, trích đúng vị trí, nêu phản chứng và đề xuất cách xác minh.
Danh sách “AI words” ngoại ngữ không đạt cổng này.

## 3. Hiệu chỉnh tối thiểu

- Tách corpus theo **ngôn ngữ × thể loại × bối cảnh người viết**, không gộp thành một mốc chung.
- Human fixture phải có bằng chứng nguồn gốc; AI fixture phải ghi model/prompt; mixed fixture phải có
  thao tác biên tập và span.
- Đo false positive trước: nếu rule thường xuyên gắn cờ văn người thật, hạ trọng số hoặc loại rule.
- Chỉ thu hẹp khoảng S/C theo [giao thức đánh giá](../../../docs/CHAM-DIEM.md), không theo cảm giác.

## 4. Ranh giới ngôn ngữ báo cáo

Tên rule và metadata có thể giữ tiếng Anh để agent định tuyến ổn định. Phần giải thích, phản chứng,
cách sửa và câu hỏi xác minh phải bằng tiếng Việt. Thuật ngữ chuyên môn giữ nguyên ở lần đầu kèm
giải nghĩa; không “Việt hóa” đến mức làm sai khái niệm gốc.
