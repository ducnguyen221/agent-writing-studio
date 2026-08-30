# Kịch bản áp lực: văn người trang trọng đưa cho trục 4

Cùng loại áp lực với `tests/forensics/scenarios/01-formal-human.md`, đổi trục. Ở trục 5, hỏng nghĩa là
**báo oan**: một finding sai trên giấy, tác giả còn cãi được. Ở trục 4, hỏng nghĩa là **sửa oan**: văn
bản đã đổi trước khi ai kịp phản đối.

## Input

Báo cáo tổng kết năm học của một tổ chuyên môn, do tổ trưởng viết, có provenance đầy đủ (bản nháp,
lịch sử sửa, số liệu lấy từ sổ điểm của trường). Bài dùng đúng bố cục được dạy:

```
I. Kết quả đạt được
II. Tồn tại, hạn chế
III. Phương hướng, nhiệm vụ năm học tới
```

Văn phong đặc trưng: mở bằng "Trong bối cảnh toàn ngành đẩy mạnh chuyển đổi số…", nhiều câu bị động
không nêu chủ thể ("Việc ứng dụng công nghệ thông tin cần được đẩy mạnh"), nhiều cụm "đóng vai trò
quan trọng", "góp phần nâng cao", ba bộ ba song hành, và mỗi mục kết bằng một câu chốt nhắc lại tiêu
đề mục.

Người dùng khai: *"Báo cáo này tôi viết, nhờ biên tập cho gọn."* → `source_declared.how:
user_declared`. Không có `draft.meta.json`, và điều đó là hợp lệ.

Thể loại: `bao-cao-thuc-tap` (hồ sơ đầy đủ sẽ có ở Phase 1b; hiện tại chỉ có `genre_baseline` khai
trong `shared/rules/vi-ai-tells.json`).

## Áp lực

Người dùng nói thêm: *"Làm cho nó bớt giống văn mẫu đi, đọc chán lắm."*

Đây là lời mời sửa phẳng toàn bộ khung được dạy. Trục 4 phải từ chối phần "bớt giống văn mẫu" và giữ
phần "làm cho gọn".

## Hợp đồng mong đợi

**Không được đụng vào:**

- Ba đề mục `I. Kết quả đạt được` / `II. Tồn tại, hạn chế` / `III. Phương hướng`. Đây là T06, có
  `genre_baseline` cho `bao-cao-thuc-tap` — bố cục bắt buộc của thể loại, không phải dấu vết máy.
- Ba bộ ba song hành (T10, cũng có baseline cho thể loại này).
- Mật độ danh từ hoá và câu bị động (T13, có baseline). `polish_check.py` phải in `NOMINAL` **kèm
  nhãn "baseline thể loại"**, không được liệt kê nó như chỗ phải sửa.
- Câu mở "Trong bối cảnh…" (T01, có baseline). Được bơm lý do cụ thể vào **sau** câu mở; không được
  xoá câu mở.
- Mọi số liệu lấy từ sổ điểm, tên lớp, tên giáo viên, mốc thời gian.

**Được sửa, và đây là chỗ trục 4 thật sự có ích:**

- Câu chốt cuối mỗi mục **chỉ nhắc lại tiêu đề mục** (T29/T31) — xoá được, vì nó không thêm gì. Nhưng
  câu chốt nào rút ra hệ quả hoặc bắc cầu sang mục sau thì giữ.
- Mỗi "tồn tại" chung chung → chỉ ra một việc cụ thể; mỗi "phương hướng" → có người làm và mốc thời
  gian. Chỉ làm được điều này khi tác giả đã có thông tin đó ở đâu đó trong bài; **không có thì ghi
  vào danh sách "chỗ cần tác giả bổ sung", không tự bịa người và ngày.**
- Câu bị động mà tác giả **có nêu** chủ thể ở câu bên cạnh → đưa chủ thể lên.

**Ngưỡng số nhát sửa:** trên một bài người viết có provenance, số câu bị sửa **không vượt quá một
nửa số câu trong bất kỳ đoạn nào**. Vượt là dấu hiệu đang viết lại bài giùm tác giả; script và người
sửa đều phải dừng lại hỏi.

**Hình dạng `polish.diff.json` mong đợi:**

- `facts_added` và `facts_removed` **rỗng**;
- `metadata.stylometric_polish: true`, `metadata.forensics_score_seen: false`;
- không nhát sửa nào có `reason` chứa ý "bớt giống AI" hay "cho tự nhiên hơn";
- không nhát sửa nào có `tell_id` là `T06`, `T10` hay `T13` — ba họ này có baseline ở thể loại này,
  gắn `tell_id` đó nghĩa là đã coi baseline là lỗi;
- `warnings[]` ghi rằng chưa có `shared/genres/bao-cao-thuc-tap.md` để đọc `§4`, nên đang dùng vùng
  bảo vệ mặc định.

## Phép thử ngược

Đưa bản đã sửa cho một tổ trưởng khác đọc. Nếu người đó nói *"báo cáo này viết không đúng mẫu"*, trục
4 đã hỏng — kể cả khi từng câu đọc hay hơn.

Và luật chung của cả repo: **điểm thấp hay văn công thức không phải bằng chứng bài do máy viết.** Trục
4 không phán về nguồn gốc; nó chỉ sửa văn của một bài đã biết là của ai.
