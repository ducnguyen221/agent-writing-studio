# Rà dẫn nguồn — bước bắt buộc của trục 3

Bước 4 trong *Quy trình* của `SKILL.md`; bản đầy đủ ở đây để SKILL.md giữ được trần 550 từ. Bước này
**không phụ thuộc `lenses[]`**: hồ sơ thể loại có bật `claim_check` hay không, nó vẫn chạy. Nó đi cặp
với luật *không gán nhận định cho nguồn* của trục 2
([`02-cowriter/references/05-source-attribution.md`](../../02-cowriter/references/05-source-attribution.md)).

---

## Cách rà

1. Liệt kê **mọi** câu gán cho một nguồn: "Theo X…", "X cho biết…", mọi ngoặc kép có chủ thể.
2. Đối chiếu từng câu với tư liệu bài dựa vào.
3. Câu nào không tìm thấy trong tư liệu → một `finding` riêng:
   - **trích nguyên văn câu đó**;
   - nêu đích danh nguồn bị gán;
   - nói rõ tư liệu không có ý ấy;
   - xếp **mức thiệt hại cao nhất** nếu bài sẽ đăng công khai.

   Đây là thứ đối chiếu được, nên nó là bằng chứng đủ theo luật *không có bằng chứng thì không có
   finding*.
4. Không được cấp tư liệu để đối chiếu thì **không suy đoán** — ghi vào `limitations[]`.

## Kết quả phải nói ra

Kết quả rà dẫn nguồn **được nói ra** trong `critique.json`: hoặc một `finding` cho mỗi câu gán sai,
hoặc một câu khẳng định đã rà hết và không thấy câu nào lệch tư liệu — **im lặng không tính là đã
rà**.

## Ví dụ

❌ *Theo hãng tin A, đây mới là tuyên bố chứ chưa phải kế hoạch.* — tư liệu chỉ có đường dẫn bài của
hãng tin A, không có câu nào như vậy ⇒ nhận định của người viết đang mượn danh nguồn.

✅ *Hãng tin A ghi nhận chưa có ngân sách và lộ trình.* — khớp tư liệu; phần đánh giá đi kèm được khai
là của người viết.

"Hãng tin A" là nguồn giả định — repo public không dùng tên nguồn thật trong ví dụ.
