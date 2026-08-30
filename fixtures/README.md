# fixtures — bộ test có nguồn gốc biết trước

**KHÔNG commit bài thật của học viên vào đây.** `.gitignore` chặn toàn bộ thư mục này
trừ chính file README. Muốn chia sẻ fixture thì phải ẩn danh hoá trước: bỏ tên, đơn vị,
tên cuộc thi, ngày tháng cụ thể, và mọi metadata file.

## Cấu trúc cần dựng

```
fixtures/
├─ human/          bài chắc chắn do người viết (ưu tiên trước 2022, hoặc viết có giám sát)
├─ ai/             bài sinh thuần bằng LLM, nhiều model + nhiều prompt style
├─ mixed-edited/   AI sinh rồi người sửa · người viết rồi AI trau chuốt
└─ adversarial/    bài đã qua humanizer / prompt "viết tự nhiên hơn"
```

## Vì sao cần ≥30 bài mỗi thể loại — và vì sao 30 vẫn chưa đủ

Ngay cả **0 lỗi trên 30 bài người** vẫn cho cận trên khoảng tin cậy 95% của FPR xấp xỉ **10%**
(quy tắc ba: 3/n). Muốn kiểm chứng vùng FPR 1% cần cỡ **300 bài người mỗi thể loại**.

Trước khi có `fixtures/`, skill vẫn xuất S/C để xếp hàng ưu tiên theo yêu cầu sản phẩm, nhưng phải
gắn nhãn **chưa hiệu chuẩn**, dùng khoảng vận hành rộng và không gọi các con số đó là xác suất AI.
