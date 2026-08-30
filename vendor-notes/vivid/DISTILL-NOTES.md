# Ghi chú chưng cất VIVID

## Đã chưng cất

| Nguyên lý upstream | Cách chuyển hóa trong studio |
|---|---|
| Kho thành ngữ tiếng Việt kèm nghĩa | `skills/04-humanizer/assets/thanh-ngu.json`: **58 mục trên 1.636**, mỗi mục có nghĩa, ngữ cảnh dùng và thể loại phù hợp do repo này tự soạn |

## Không mang sang

- Việc nhồi toàn bộ kho vào repo: một danh sách hơn một nghìn bảy trăm mục biến trục 4 thành máy rắc thành ngữ.
- Phần mô hình và benchmark của bộ dữ liệu.
- Ý tưởng dùng mật độ thành ngữ làm dấu hiệu nguồn gốc văn bản.

## Ranh giới

MIT cho phép dùng lại kèm ghi công. Đã lấy tập con ở Phase 3 (30/08/2026): `assets/thanh-ngu.json` ghi ngay trong nội dung tên repo, license MIT, SHA commit pin ở trên và blob SHA của `dataset/VIVID_Dataset.csv` (`9d114a4e99baa2cc87d56eea511c57912a8c6704`).

**Phát hiện khi lấy, ghi lại để đợt sau không phải làm lại:** bộ dữ liệu này là kho thành ngữ **hiếm và cổ**, dựng cho bài toán đo độ khó ngôn ngữ, không phải kho thành ngữ thông dụng. Phần lớn mục đòi kiến thức nhà nông, nghề cũ hoặc phong tục cũ mới hiểu, và nhiều mục hạ thấp người theo giới hoặc tuổi. Những cụm quen thuộc nhất trong văn nghị luận Việt (`đầu voi đuôi chuột`, `thầy bói xem voi`, `ếch ngồi đáy giếng`, `có công mài sắt`, `uống nước nhớ nguồn`…) **không có trong bộ này**. Vì vậy tỷ lệ dùng được cho văn học thuật và blog rất thấp: 58/1.636. Con số đó là kết quả của phép lọc, không phải hạn ngạch — không nới tiêu chí để đạt một con số đẹp hơn.

Cột nghĩa trong `thanh-ngu.json` do repo này tự viết lại, không chép nguyên văn cột `Meaning` của bộ dữ liệu.
