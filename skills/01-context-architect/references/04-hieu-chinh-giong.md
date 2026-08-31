# Hiệu chỉnh giọng — dựng writer profile

Phương pháp trong file này thuộc bộ luật của studio; nguồn gốc tri thức ghi ở sổ xưởng (không nằm trong repo). Hai nguyên lý nền:

- **Hiệu chỉnh giọng từ 3–6 bài cũ của chính tác giả** trước khi viết. Ba là sàn chứ không phải con
  số tròn cho đẹp — dưới ba bài thì không tách được thói quen của NGƯỜI ra khỏi đặc thù của BÀI.
  Trên sáu bài thì lợi ích thêm nhỏ dần, trong khi rủi ro trộn nhiều giai đoạn và nhiều thể loại
  tăng lên.
- **Đọc một bài mẫu theo bốn chiều** — **độ dài câu, cách mở đoạn, dấu câu, cụm lặp** — và luật
  *bài mẫu của người viết thắng mọi luật văn phong*. Mọi ví dụ trong file này là tiếng Việt tự soạn.

Bốn chiều ấy ánh xạ thẳng vào bốn trường của hồ sơ:

| Đọc bài mẫu thấy gì | Trường trong `writer.schema.json` | Ai dùng |
|---|---|---|
| Độ dài câu và mức dao động | `fingerprint.sentence_len.mean` / `.cv` | trục 4 không được làm phẳng; trục 5 so baseline |
| Cách mở đoạn, khuôn tu từ lặp lại | `pet_templates[]` | trục 5 **hạ** tín hiệu G1 |
| Dấu câu và cách bỏ dấu thanh | `fingerprint.tone_style` | trục 4 không được đổi kiểu bỏ dấu |
| Cụm lặp, thuật ngữ nghề nghiệp | `necessary_english_terms[]`, `voice_notes` | trục 4 không dịch; trục 5 không tính G2 |

## `pet_templates` — cơ chế chống báo oan

Đây là mục có giá trị cao nhất của hồ sơ. Người mê phép đối dùng "vừa X vừa Y" ở khắp nơi; nếu bài
nghi vấn của họ bị đếm khuôn ấy và bị quy là văn máy, đó là báo oan có hệ thống. Hồ sơ giải quyết
bằng cách **có trước**: khuôn đã nằm trong hồ sơ dựng từ bài cũ thì việc nó xuất hiện lại không còn
là tín hiệu.

Điều kiện vào danh sách: khuôn xuất hiện ở **ít nhất 2 bài mẫu khác nhau**. Một bài thì đó là thói
quen của bài đó. Ngưỡng lỏng ở đây là báo-oan-ngược: hồ sơ sẽ xoá sạch tín hiệu thật.

Hồ sơ `status: draft` (dưới 3 bài) **chỉ dùng để tham khảo, không được dùng để hạ finding**.

## Dựng bằng `profile_build.py`

```
python shared/scripts/profile_build.py --writer <slug> --genre <genre>
```

Đọc `.txt` / `.md` / `.docx` trong `shared/writers/<slug>/samples/`, đo từng bài bằng `vi_segment.py`
và `counters.py` của trục 5, lấy **trung vị của từng bài** — không phải số đo trên văn bản đã nối,
vì nối lại thì một bài dài sẽ nuốt giọng của các bài ngắn.

Ba điều script **không** làm:

- **Không in nội dung bài ra stdout** và không ghi nội dung vào hồ sơ. `provenance.samples[]` chỉ giữ
  mã băm rút gọn — đủ để phát hiện bài bị đổi, không đủ để lộ gì.
- **Không đoán `known_typos`.** Không có từ điển thì đoán lỗi chính tả của người khác là báo oan. Mục
  này người điền tay, để rỗng còn hơn.
- **Không viết `voice_notes`.** Giọng là thứ script không đo được; bịa một đoạn mô tả giọng là tạo ra
  bằng chứng giả cho ba trục phía sau.

## Điều kiện của bài mẫu

- Đã **xác nhận chính chủ** — ghi ai xác nhận vào `provenance.ownership_confirmed_by`. Bài "được cho
  là của tác giả" không tính; dùng nhầm bài người khác thì hồ sơ vô nghĩa và tệ hơn là sai.
- **Không trộn bài đã qua AI rewrite** nếu mục tiêu là baseline giọng tự nhiên.
- Ghi thể loại và giai đoạn. Một hồ sơ dựng từ bài nghiên cứu **không** nói được gì về giọng blog của
  cùng người đó.

## `faststylometry` — chỉ ĐO, không SINH

Đo khoảng cách văn phong bằng thư viện stylometry là **tuỳ chọn**, và chỉ dùng theo một chiều: xác
minh *bài này có giống baseline của chính người này không*. Không được dùng để **sinh** văn theo
giọng, không được dùng để kết luận **có phải AI viết không** — hai việc khác nhau, và cái sau không
phải bài toán mà stylometry trả lời được với vài bài mẫu. Kết quả đo, nếu có, là bằng chứng phụ ghi
vào `limitations[]`, không phải điểm số.

Repo này **không cài** thư viện nào cho việc đó ở đợt hiện tại; mục này ghi ranh giới trước để lần
sau không ai vượt qua mà không nhận ra.
