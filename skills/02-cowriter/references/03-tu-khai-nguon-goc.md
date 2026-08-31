# Tự khai nguồn gốc — `draft.meta.json` là bắt buộc

`draft.md` không bao giờ đi một mình. Mỗi lần trục 2 tham gia viết, nó xuất kèm
`draft.meta.json` theo [`shared/schemas/draft.schema.json`](../../../shared/schemas/draft.schema.json),
và trong đó `machine_written_spans[]` là trường **bắt buộc có mặt**.

---

## 1. Vì sao — luật `§2.5` của `KIEN-TRUC.md`

Repo này có một trục đi giám định xem văn bản của người khác có phải do máy viết không (trục 5), và
một trục đi sửa văn cho mượt hơn (trục 4). Hai việc ấy chỉ đứng vững nếu chính studio trả lời được
câu hỏi mà nó đặt cho người khác: **bài do studio viết thì phần nào là máy viết?**

Luật `§2.5` mục 3 nói thẳng: *cổng Y5 của chính studio mà không có bản tự khai thì mất tư cách nói
về liêm chính*. Đây không phải một dòng thủ tục. Ba hệ quả cụ thể:

1. **Không có bản tự khai thì không đo được trục 5.** Bản tự khai là **ground truth** duy nhất repo
   này tự tạo ra được. Trục 5 chấm mù `polished.md`, rồi đối chiếu finding với
   `machine_written_spans[]`: chỗ nào bắt đúng, chỗ nào trượt, chỗ nào báo oan. Không có nó, mọi con
   số của `CHAM-DIEM.md` chỉ là ý kiến.
2. **Người dùng phải biết mình đang nộp cái gì.** Một bản thảo có 40 câu máy viết và một bản có 3
   câu máy viết là hai thứ khác nhau về mặt trách nhiệm học thuật, dù đọc giống nhau.
3. **Tự khai chặn đúng cái cám dỗ mà repo này tồn tại để chống.** Studio vừa viết hộ vừa xoá dấu vết
   là dịch vụ né máy chấm. Ranh giới ấy được giữ bằng một file, không bằng một lời hứa.

**Trường bắt buộc, được phép rỗng.** Mảng rỗng nghĩa là *"không câu nào do máy viết"* — một khẳng
định, không phải một chỗ trống. Bỏ hẳn trường đi thì file không hợp lệ theo schema, và đó là chủ ý.

## 2. Ghi thế nào

`machine_written_spans[]` khai theo **câu**, không theo đoạn hay theo dòng — một đoạn thường có câu
của người và câu của máy nằm cạnh nhau.

```json
{ "sentence_id": "s0042", "origin": "machine",
  "note": "Câu chuyển đoạn, máy viết theo quan hệ đối lập đã khai ở tầng hai outline" }
```

- **`sentence_id` phải khớp `sentences.json`.** File đó do
  `python skills/05-forensics/scripts/extract.py` sinh ra từ chính `draft.md`, dùng bộ tách câu
  `vi_segment.py` (biết `et al.`, `TS.`, `v.v.` không kết câu). Đánh số tay là cách chắc chắn để bản
  tự khai lệch khỏi văn bản: **chạy extract trên bản cuối cùng**, sau lần sửa cuối.
- **Ba giá trị `origin`, chọn theo ai chạm sau cùng:**

  | `origin` | Nghĩa | Ca điển hình |
  |---|---|---|
  | `machine` | Máy viết, người không sửa chữ nào | Câu nối, câu tóm ý, câu mở đoạn theo dàn ý đã duyệt |
  | `machine_edited_by_human` | Máy viết trước, người sửa sau | Người đổi từ, cắt vế, thêm số liệu vào câu máy |
  | `human_edited_by_machine` | Người viết trước, máy sửa sau | Trục 2 gọn lại một câu người viết trong lúc dựng đoạn |

- Câu người viết mà máy không chạm vào thì **không có mặt** trong mảng. Mảng này chỉ liệt kê chỗ máy
  có tay vào.
- `outline_approved`, `structure_id`, `profile_used`, `model` khai cùng lúc, không khai sau. Chúng
  trả lời "bản này được sinh ra trong điều kiện nào" — thiếu chúng thì bản tự khai không tái lập được.

## 3. Ba chỗ dễ quên nhất

Đây là ba chỗ mà bản tự khai âm thầm sai, xếp theo mức hay gặp:

1. **Sửa sau khi đã ghi meta.** Người dùng đọc bản thảo, xin đổi hai đoạn, trục 2 viết lại — và
   `sentence_id` từ chỗ sửa trở đi **dịch hết**. Bản tự khai vẫn hợp lệ theo schema, vẫn trỏ đúng
   định dạng, và trỏ sai câu. Luật: **mỗi lần `draft.md` đổi, chạy lại extract và soát lại mảng**;
   không đủ thời gian soát thì ghi `outline_approved` và mảng theo bản mới, đừng bê mảng cũ sang.
2. **Câu máy viết rồi người sửa nhẹ.** Người dùng đổi hai từ, và câu đó rất dễ bị bỏ khỏi mảng vì
   "người có sửa mà". Sai: giá trị đúng là `machine_edited_by_human`, và nó vẫn nằm trong mảng.
   Người chạm sau cùng không xoá được việc máy viết câu ấy đầu tiên.
3. **Câu nối, câu chuyển đoạn, câu chốt đoạn.** Đây là loại câu máy viết nhiều nhất và bị khai
   thiếu nhiều nhất, vì nó "không chứa nội dung nào của người dùng". Nhưng đó chính là loại câu mà
   trục 5 bắt được nhiều nhất — khai thiếu đúng chỗ này làm hỏng phép đo mà bản tự khai sinh ra để
   phục vụ.

## 4. Không dùng bản tự khai để đi đường tắt

- **Trục 3 không xem `draft.meta.json` trước khi chấm xong.** Biết câu nào máy viết thì phiếu chấm
  không còn mù nữa.
- **Trục 5 chạy mù**, không nhận file này. Đối chiếu chỉ xảy ra **sau khi** trục 5 đã khoá kết quả.
- **Trục 2 không được sửa văn cho khớp bản tự khai.** Bản tự khai mô tả bài; bài không phục vụ bản
  tự khai.
- Kết quả đối chiếu là **dữ liệu hiệu chỉnh cho trục 5**, không phải điểm số của tác giả. Trục 5
  trượt một câu máy viết thì đó là con số về trục 5, không phải lời khen dành cho bài.
