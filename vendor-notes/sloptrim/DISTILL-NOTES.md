# Ghi chú chưng cất sloptrim

## Đã chưng cất

| Nguyên lý upstream | Cách chuyển hóa trong studio |
|---|---|
| Cổng chạy khi lưu, không gọi mô hình | `scripts/polish_check.py`: chạy `counters.py` trước và sau, 0 lượt gọi mô hình |
| Chỉ sửa câu bị chạm, giữ nguyên phần còn lại | `moves_allowed` ở §4 và luật ghi từng nhát sửa vào `polish.diff.json` |

## Không mang sang

- Toàn bộ mẫu nhận diện tiếng Anh.
- Việc quy điểm số thành phán quyết về nguồn gốc văn bản.
- Tích hợp vào vòng lưu file của một trình soạn thảo cụ thể.

## Ranh giới

Apache-2.0 buộc giữ NOTICE khi phân phối lại mã. Repo này KHÔNG vendor dòng nào nên không phát sinh nghĩa vụ; nếu về sau có chép mã, phải thêm NOTICE trước khi commit.
