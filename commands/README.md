# `commands/` — bảy lệnh chạy lẻ từng bước

Cách thường dùng xưởng viết là **nói bằng tiếng Việt**, agent tự chọn trục. Bảy lệnh dưới đây dành
cho lúc bạn muốn chạy **đúng một bước**, không muốn agent tự ý làm tiếp.

Gõ theo dạng `/agent-writing-studio:<tên-lệnh>`. Số đầu tên chính là **số trục**, nên thứ tự chạy đọc
được ngay từ danh sách file.

| Lệnh | Trục | Làm gì |
|---|---|---|
| `/agent-writing-studio:01-boi-canh` | Y1 | Phỏng vấn ý đồ, luận đề, độc giả, ràng buộc |
| `/agent-writing-studio:02-viet-nhap` | Y2 | Dàn ý ba tầng → chờ bạn duyệt → viết văn xuôi |
| `/agent-writing-studio:03-phan-bien` | Y3 | Chấm từng tiêu chí theo barem thể loại |
| `/agent-writing-studio:04-bien-tap` | Y4 | Sửa về phía giọng tác giả, ba chế độ đầu ra |
| `/agent-writing-studio:05-giam-dinh` | Y5 | Đọc bài tìm dấu hiệu máy viết, kèm phản chứng |
| `/agent-writing-studio:giao-docx` | — | Xuất bản giao ra `.docx` đúng quy cách văn bản Việt |
| `/agent-writing-studio:danh-sach` | — | In chính bảng này, đọc thẳng từ các file lệnh |

Hai lệnh cuối không mang số vì chúng **không thuộc trục nào**: `giao-docx` là bàn giao thành phẩm,
`danh-sach` là tra cứu.

## Luật của mọi lệnh: chỉ làm đúng bước của nó

Năm trục nối với nhau bằng **file**, không bằng trí nhớ hội thoại. Thiếu sản phẩm của bước trước,
lệnh sẽ nói thẳng nó thiếu file gì và lệnh nào sinh ra file đó — rồi **dừng**. Nó không tự chạy lại
cả chuỗi, vì chạy lại nghĩa là phỏng vấn lại bạn từ đầu hoặc tự bịa ra bối cảnh.

Bảng trên là bản chép cho người đọc. **Nguồn thật là bảy file `.md` trong thư mục này** — lệnh
`danh-sach` đọc thẳng từ đó, nên nếu hai chỗ lệch nhau thì tin `danh-sach`.
