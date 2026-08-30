# Tích hợp với `kpim-skills:project-feedback`

`project-feedback` chấm bài học viên theo **5 trục /100** và xuất file Word cùng đoạn email.
`03-critique` chấm **chất lượng viết** theo `criteria[]` của hồ sơ thể loại và xuất `critique.json`.
Hai skill khác chủ, khác đầu ra, và **không import nhau**. Chỗ nối duy nhất là **file**.

Mô hình: `project-feedback` là người điều phối và là người ký tên vào điểm; `03-critique` là trục
chuyên môn cho phần viết, trả về bằng chứng chứ không trả về điểm tổng.

## Ranh giới sở hữu

| | `project-feedback` | `03-critique` |
|---|---|---|
| Sở hữu | Điểm tổng /100, trọng số 5 trục, tone, file Word, email | `criteria_scores[]`, `findings[]`, `must_fix[]`, `limitations[]` |
| Không được làm | Tự chấm phần lập luận mà không có bằng chứng trích được | Sinh điểm tổng, sinh Word, sinh email, quyết trọng số |
| Nguồn barem | Rubric của khoá học | Barem của nhiệm vụ, nếu không có thì §3 hồ sơ thể loại |

`critique.json` **cố ý không có điểm tổng**. Việc cộng gộp và cân trọng số thuộc về
`project-feedback`, vì chỉ nó biết khoá học này nặng về đâu.

## Hợp đồng file

Thư mục ca: `.work/<case>/` (không vào git).

**Đầu vào mà `project-feedback` phải đặt sẵn:**

| File | Bắt buộc | Nội dung |
|---|---|---|
| `draft.md` | có | Bản thảo cần chấm, đã tách khỏi mọi lời dặn |
| `case.json` | có | `{genre, rubric_source, ngon_ngu}` — `genre` là tên file trong `shared/genres/` không kèm đuôi |
| `context.json` | không | Theo `shared/schemas/context.schema.json`, nếu trục 1 đã chạy |
| `rubric.md` | không | Rubric thật của khoá học, nếu có. Có file này thì nó **thắng** §3 hồ sơ thể loại |

**Đầu ra mà `03-critique` trả về:** `critique.json`, hợp lệ theo
`shared/schemas/critique.schema.json`.

Không có tham số dòng lệnh, không có API, không có module Python chung. Đổi hợp đồng nghĩa là đổi
bảng trên và đổi schema — không phải đổi lời gọi.

## Map `criteria_scores[]` sang 5 trục

`03-critique` trả về điểm theo tiêu chí của **thể loại**, không theo 5 trục. Việc quy đổi là của
`project-feedback`, theo bảng dưới. Đây là bảng gợi ý cho bài dạng viết (essay, báo cáo, luận văn);
bài Power BI hay SQL có trục 2 nặng hơn nhiều và phần lớn không đi qua `03-critique`.

| Trục của `project-feedback` | Nhận từ `criteria_scores[]` | Nhận từ `findings[]` |
|---|---|---|
| 1 · Đáp ứng yêu cầu | `task_response`, `xac_dinh_van_de`, `research_question` | lăng kính `task_response` |
| 2 · Năng lực kỹ thuật | `method`, `citation` | `method_rigor`, `source_reliability`, `source_independence` |
| 3 · Tư duy phân tích & Insight | `logic`, `evidence`, `counterargument`, `results`, `discussion` | `fallacy_scan`, `claim_check`, `balance_check` |
| 4 · Trình bày & Truyền đạt | `cohesion`, `language`, `academic_language` | `value_density`, `retention`, `pacing_curve` |
| 5 · Hoàn thiện & Chuyên nghiệp | phần hình thức của barem: cấu trúc, dung lượng, chuẩn trích dẫn | `must_fix[]` còn tồn đọng |

Ba luật khi quy đổi:

1. **Không cho điểm trục nào mà không có `evidence` kèm theo.** `project-feedback` yêu cầu bằng
   chứng cụ thể khi trừ điểm; `criteria_scores[].evidence` chính là thứ dán thẳng vào đó.
2. **Tiêu chí không có trong `criteria_scores[]` thì không tự suy ra điểm.** Ghi vào phần hạn chế của
   bản đánh giá rằng trục đó chấm bằng nguồn khác.
3. **`limitations[]` phải đi vào bản Word**, không được nuốt. Người học có quyền biết người chấm đã
   không thấy được gì.

## Ba luật không được đảo

1. **Không đưa `draft.meta.json` cho `03-critique` trước khi nó chấm xong.** Xem
   [`03-blind-referee.md`](03-blind-referee.md). Nếu đã lỡ, `critique.json` phải ghi
   `blind_referee: false`, và bản đánh giá phải nói rõ.
2. **`critique.json` không phải bằng chứng về nguồn gốc văn bản.** Điểm `logic` thấp không có nghĩa
   bài do máy viết, và điểm `language` cao càng không. Nghi vấn nguồn gốc đi theo quy trình riêng của
   trục 5 (`05-forensics`), với ràng buộc chống báo oan của nó. Trộn hai việc là cách nhanh nhất để
   buộc tội oan một người viết trung thực.
3. **Rubric của khoá học thắng.** Có `rubric.md` thì `criteria[]` dựng theo nó và `rubric_source` ghi
   tên rubric đó; §3 hồ sơ thể loại lùi về làm mặc định. Xem [`04-barem-mau.md`](04-barem-mau.md).

## Khi bài không khớp thể loại nào

Chọn hồ sơ gần nhất và ghi lựa chọn đó vào `limitations[]`. Bài phân tích nghiệp vụ, báo cáo thực
tập, đồ án có phần viết: dùng `research` nếu bài dựa vào dữ liệu, dùng `essay` nếu bài dựa vào lập
luận. Đừng tạo hồ sơ thể loại mới giữa lúc đang chấm — thêm thể loại là một việc riêng, có test
riêng, và không được làm trong lúc một người đang chờ điểm.
