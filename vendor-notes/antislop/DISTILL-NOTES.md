# Ghi chú chưng cất antislop

## Đã chưng cất

| Nguyên lý upstream | Cách chuyển hóa trong studio |
|---|---|
| Một spec dùng chung | Một schema finding cho đọc, chấm và báo cáo |
| Tầng đếm tất định và tầng phán đoán | Agent đọc mù trước; script kiểm chứng sau |
| Finding có category, vị trí, quote | Thêm phản chứng, cách sửa và câu hỏi xác minh |
| `stable/unstable` | Phân biệt số đo byte-stable với nhận định agent |
| Allow-list thắng | Baseline nghề nghiệp/thể loại có quyền hạ tín hiệu từ vựng |
| Progressive disclosure | Router `05-forensics` nối bốn skill nhỏ |
| Hai tầng test | Unit test cho phần tất định; scenario fixture cho hành vi agent |

## Không mang sang

- Danh sách từ tiếng Anh và regex tiếng Anh.
- Thứ tự script-first; studio bắt buộc agent đọc mù trước.
- Kết luận “không có tell = người viết”.
- Severity cố định không xét thể loại hoặc writer baseline.
- Lens rewrite/humanize và cách đóng gói Claude-only.
- Chính sách không có điểm tổng; sản phẩm cần S/C nhưng luôn có giới hạn và bằng chứng.

## Ranh giới

Đây là **DERIVED về kiến trúc**, không phải bản sao detector. Không dùng antislop làm ground truth về
nguồn gốc văn bản; độ chính xác chỉ được xác lập bằng corpus tiếng Việt có provenance.
