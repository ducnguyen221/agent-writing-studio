# Bắt đầu ở đây

Bạn đã cài xong (chưa thì dán prompt trong [`INSTALL.md`](INSTALL.md#prompt-copy-dán) vào ứng dụng AI).
Trang này đưa bạn qua **bài thực hành đầu tiên**, mười phút, không cần bài của chính bạn.

## 1. Mở đúng chỗ

- **Claude Code đã cài plugin:** mở phiên mới ở thư mục bạn muốn làm việc. Gõ `/agent-writing-studio:list`.
- **Codex, Antigravity, hoặc bản clone:** mở **chính thư mục repo**. Agent đọc `AGENTS.md` trước.

Ca viết của bạn nằm ở `.work/<tên-ca>/` trong thư mục đang mở (Git bỏ qua), hoặc ở station
`WRITING_STUDIO_DATA` nếu bạn đã đặt.

## 2. Bài mẫu: chấm một bài luận ngắn

[`samples/bai-mau.md`](samples/bai-mau.md) là một bài luận tự soạn, có **một** chỗ yếu cố ý. Nói với agent:

> *"Chấm `samples/bai-mau.md` theo hồ sơ `essay`, dùng bối cảnh `samples/context.json`. Ghi
> `critique.json` vào `.work/mau/`. Đừng mở `samples/critique.expected.json` trước khi chấm xong."*

Chấm xong, mở [`samples/critique.expected.json`](samples/critique.expected.json) mà so. Điểm từng tiêu chí
được phép lệch. Không được lệch: bắt được câu *"Hầu hết người đi làm…"* thiếu bằng chứng, không có điểm
tổng, có dòng nói kết quả rà dẫn nguồn.

## 3. Viết bài của bạn

Nói bằng tiếng Việt bình thường — agent tự chọn trục:

| Muốn gì | Nói với agent |
|---|---|
| Chuẩn bị viết | *"Tôi cần viết một bài luận về X. Dựng bối cảnh giúp tôi trước đã."* |
| Viết nháp | *"Đã có `context.json` ở ca `bai-x`. Dựng dàn ý rồi viết nháp."* |
| Phản biện | *"Chấm giúp bài này theo hồ sơ `research`, chỉ chỗ lập luận hổng."* |
| Biên tập | *"Biên tập bản nháp này, giữ nguyên số liệu và trích dẫn."* |
| Giao bản Word | *"Giao bản docx vào thư mục D:/thu-muc-cua-toi."* |

Thể loại có sẵn: `essay`, `research`, `blog`, `journalism`, `novel`, `commentary`, `thesis-proposal`,
`internship-report`, `teaching-initiative`.

## 4. Khi có trục trặc

Chạy `python studio.py doctor` trong thư mục repo và đọc dòng `FAIL` / `WARN`. Bảng lỗi hay gặp ở cuối
[`INSTALL.md`](INSTALL.md#lỗi-hay-gặp). Ranh giới đạo đức của xưởng — vì sao không dùng nó để kết tội
hay "né máy chấm AI" — ở [README mục 5](README.md#5-ranh-giới-đạo-đức--phần-quan-trọng-nhất-của-repo-này).
