# `tests/` — hàng rào giữ tài liệu và code không trôi khỏi nhau

Bạn không cần biết lập trình để hiểu thư mục này, và nếu bạn chỉ **dùng** xưởng viết thì bạn không
cần chạy nó bao giờ.

## Test ở đây kiểm cái gì

Không kiểm "văn có hay không" — máy không làm được việc đó, và repo này cũng không hứa như vậy.

Nó kiểm **những thứ hỏng thì hỏng im lặng**. Cả repo là văn bản: skill nói một đằng, dữ liệu ghi một
nẻo, mà mọi thứ vẫn "chạy" bình thường — chỉ có kết quả là sai. Ví dụ những câu hỏi được khoá ở đây:

- Hồ sơ thể loại có đủ năm mục không, tên thể loại trong hồ sơ có khớp tên file không?
- Bảy lệnh trong `commands/` có đúng bảy cái, mỗi cái có nói rõ nó cần file gì và ai sinh ra file đó?
- Một liên kết trong tài liệu có trỏ vào chỗ không tồn tại không?
- Danh mục dấu hiệu có mục nào thiếu **phản chứng** — câu người hoàn toàn hợp lệ chứa đúng dấu hiệu ấy?
- Có dấu hiệu nào chưa hiệu chuẩn mà bị dùng để tạo nghi vấn không?

Nói gọn: test ở đây bảo đảm **luật viết trong tài liệu và hành vi trong code không trôi khỏi nhau**.
Một quy tắc đạo đức chỉ nằm trong README là một lời hứa; nằm trong test thì nó có người canh.

## Chạy thế nào

Cần Python 3 và `pip install -r requirements-dev.txt`, rồi chạy một trong hai lệnh:

```bash
python -m pytest tests/ -q
python -m unittest discover -s tests -t .
```

Hai lệnh phải cho **cùng một con số**. Con số đó đổi mỗi lần repo thêm luật mới, nên README chỉ ghi
lại số của bản phát hành; muốn biết số hiện tại thì cứ chạy — đừng tin con số chép cứng ở đâu đó.
Có test đỏ nghĩa là một luật trong tài liệu đã mất chỗ dựa; đọc tên test, nó nói bằng tiếng Việt luật
nào vừa gãy.
