# Ca nội bộ đã ẩn danh — hai nhánh bất đồng, và bài học

Đọc một lần trước khi dùng skill. Đây là ca đã chạy thật, không phải ví dụ minh hoạ.

---

## Đối tượng

Một bài chính luận dài về công nghệ và xã hội. 18.108 ký tự · 3.972 âm tiết · 12 trang · `.docx`.

## Hai nhánh chạy mù với nhau

| | **Nhánh B — thống kê** (mô hình nhỏ, GLTR + Binoculars, CPU) | **Nhánh A — agent đọc mù** |
|---|---|---|
| Kết luận lúc chạy | **Người viết** | **ưu tiên kiểm tra cao** *(agent từng tự ước ~85%, con số này không còn được dùng)* |
| Tin cậy tự khai | Khá cao | Cao |
| Nhìn thấy | Phân bố xác suất từng token | Cấu trúc, tu từ, chuẩn mực thể loại |

### Nhánh B đo được gì

| Chỉ số | AI thuần | Mốc TCCS (người) | Bài nghi vấn |
|---|---|---|---|
| Binoculars *(thấp = máy)* | 0,8347 | 0,9064 | **0,9650** |
| Perplexity | 5,3 | 8,7 | **12,7** |
| GLTR top-10 | 87,9% | 80,0% | **76,0%** |

Cả ba xếp bài nghi vấn ở **đầu "người"**, thậm chí "người" hơn bài mốc đã biết nguồn gốc.
Nhánh B kết luận: trong sạch.

### Nhánh A tìm được gì — các quan sát đếm được, không phải nguồn gốc được chứng minh

| Khẳng định | Kiểm chứng bằng script |
|---|---|
| Khuôn `không còn X mà là Y` lặp nhiều | **7 lần** trong 18k ký tự |
| Gloss tiếng Anh dày bất thường | **23 lần** vs **1 lần** ở bài mốc — gấp **22×** |
| Số liệu rắc đều, không nguồn | **74 con số** vs 31; hầu như không con số nào có nguồn |
| Vỡ hệ đánh số chương | `I, II, III, 4, 5` |
| Mục "Tổng kết Chương 4" đơn độc | Đúng, chỉ chương 4 có |
| Lỗi gõ `"biến thế"` | Có, 1 lần |
| **Thân bài không trích kinh điển** | **2 lượt** vs **15 lượt** ở bài mốc cùng thể loại |

---

## Điều tra bất đồng — và hai sai lầm bị lộ ra

Theo luật của skill: bất đồng mạnh **không lấy trung bình**, phải điều tra.

**Giả thuyết 1 (bào chữa cho nhánh B): perplexity cao vì bài nhiều thuật ngữ tiếng Anh và con số,
thứ model 0.5B không biết.**
→ Đã kiểm: loại hết gloss tiếng Anh và con số rồi đo lại. Khoảng cách **nới rộng** (PPL 12,7 → 16,2),
không thu hẹp. **Giả thuyết SAI.**

**Sai lầm thật nằm ở bài mốc.** Bài mốc trích tài liệu kinh điển và văn kiện **15 lần** — một phần
lớn là **trích nguyên văn tài liệu chính thống**, thứ mà mọi mô hình ngôn ngữ thấy **cực kỳ dễ đoán**.
Perplexity thấp của bài mốc phản ánh *mật độ trích dẫn*, không phản ánh *do người viết*.
Control tồi làm bài nghi vấn trông "người" hơn thực tế.

**Sai lầm thứ hai: đọc sai `TotalTime`.** 130 phút cho 12 trang lý luận chính trị nguyên gốc là **NHANH**,
khớp với *biên tập và lắp ráp* hơn là *sáng tác*. Ban đầu nó bị trình bày như bằng chứng bênh vực;
thực ra nó mơ hồ, hơi nghiêng về lắp ráp.

---

## Giả thuyết làm việc lúc đó — không phải ground truth

Giả thuyết khớp nhiều quan sát nhất lúc đó là *"AI hỗ trợ phần lõi, người biên tập và lắp ráp"*.
Nhưng ca này **không có ground truth** và không có vấn đáp tác giả, lịch sử bản nháp hay nguồn xác nhận;
vì vậy không được dùng nó để tuyên bố nhánh nào đúng. Hành động hợp lý chỉ là **trao đổi với tác giả,
kiểm nguồn và xem bản nháp**, không kết luận kỷ luật.

Ba trụ:
1. **Lập luận thể loại mạnh nhất** — bài dự thi bảo vệ nền tảng tư tưởng mà thân bài gần như không trích
   kinh điển là bất thường khó giải thích. Người dự thi thật **biết** đó là yêu cầu; LLM thì không.
   *Perplexity không bao giờ nhìn thấy được điều này.*
2. **Dấu vết lắp ráp là dấu tay người ghép, không phải người viết.**
3. **74 con số hầu như không nguồn** — đây là đường điều tra rẻ nhất, và thuộc tầng bằng chứng cứng.

---

## Bài học đã đưa vào thiết kế skill

1. **Đọc mù trước mọi số đếm là bắt buộc.** Chỉ chạy nhánh B dễ bỏ sót chuẩn mực thể loại. Chỉ chạy
   nhánh A dễ tạo một con số không kiểm chứng được. Script/model đối chứng là tùy chọn và không thay
   được nguồn, bản nháp hoặc vấn đáp.
2. **Bất đồng mạnh là tài sản, không phải phiền toái** — chính nó dẫn tới việc phát hiện control hỏng.
3. **Bài mốc phải loại/chuẩn hoá phần trích dẫn nguyên văn** trước khi so sánh.
4. **`TotalTime` diễn giải theo tỷ lệ với độ dài**, không theo ngưỡng tuyệt đối.
5. **Mật độ trích dẫn kinh điển là feature riêng cho thể loại chính luận** — thiếu nó là tín hiệu mạnh.
6. **Agent bắt được thứ thống kê không thấy**, và ngược lại. Nhưng hai nhánh chưa đủ độc lập để biến
   đồng thuận thành ground truth; bằng chứng quy trình vẫn quan trọng hơn.

⚠️ **Giới hạn của ca này:** n = 1. Agent đọc có thể thiên lệch về phía gắn cờ AI
(xem `03-chong-bao-oan.md` mục 1). Việc giả thuyết của nó khớp nhiều quan sát hơn trong ca này
**không chứng minh** nó đúng hoặc sẽ luôn đúng.
Đó là lý do skill bắt buộc phản chứng và chỉ dùng script/model như lớp đối chứng tùy chọn.
