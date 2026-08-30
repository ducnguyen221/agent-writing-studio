# Forensics file — bằng chứng ngoài văn bản

Tầng này **không phụ thuộc ngôn ngữ**, nên hiệu lực đầy đủ với bài tiếng Việt và **không mang bias ESL**.
Nó cũng là tầng được Thông tư 49/2026 chống lưng (yêu cầu "lưu vết quá trình học tập, truy xuất, kiểm chứng").

Nhưng nó **không bao giờ đủ để kết luận một mình**.

---

## `.docx` là file ZIP — hai chỗ phải mở

### `docProps/core.xml` — đọc bằng `python-docx`

| Trường | Đáng chú ý khi |
|---|---|
| `creator` / `last_modified_by` | Khác tên người nộp, hoặc là tên chung chung (`Windows User`, `Admin`, `User`) |
| `revision` | Rất thấp (1–2) cho một tài liệu dài |
| `created` → `modified` | Cách nhau vài chục phút cho một tài liệu lớn; hoặc `created` sau ngày giao đề chỉ vài giờ |

### `docProps/app.xml` — **`python-docx` KHÔNG expose**, phải mở ZIP bằng `zipfile` + `lxml`

Chứa `TotalTime` (Total Editing Time), `Words`, `Pages`, `Application`, `AppVersion`, `Company`, `Template`.

---

## `TotalTime` — trường dễ đọc sai nhất

Word chỉ tăng `TotalTime` **khi tài liệu đang mở trong Word, đang có focus, và người dùng vừa thao tác**.

> 🔴 **`TotalTime` thấp KHÔNG phải bằng chứng gian lận.** Nó bằng 0 hoặc gần 0 một cách **hoàn toàn vô tội**
> nếu: soạn trên Google Docs rồi export · dùng LibreOffice/WPS · dùng Word Online · file sinh bởi script.

**Phải chuẩn hoá theo độ dài, không dùng ngưỡng tuyệt đối.** Chỉ số dùng được:

```
phút_trên_100_từ = TotalTime / (Words / 100)
```

Mốc tham chiếu thô cho văn học thuật nguyên gốc: **≥8–10 phút/100 từ** là hợp lý cho sáng tác;
**≤5 phút/100 từ** nghiêng về biên tập/lắp ráp hơn là sáng tác.

*Ca 2026-08-29:* `TotalTime` 130 phút · `Words` 2707 → **4,8 phút/100 từ** cho một bài lý luận chính trị
12 trang. Ban đầu bị đọc nhầm là bằng chứng bênh vực; thực ra nghiêng về lắp ráp.

**Chiều ngược lại thì mạnh hơn:** `TotalTime` **cao** là bằng chứng **bênh vực** tác giả.

---

## `Company` và `Template` — dấu vết bản cài

Trường `Company` thường chứa tên tổ chức đăng ký bản Word. Nếu nó chứa **email/số điện thoại cá nhân
của người khác**, đó là dấu vết bản cài Word không thuộc về tác giả — thường gặp khi dùng máy chung,
tiệm đánh máy, hoặc file được truyền tay.

⚠️ Đây là **PII của bên thứ ba**. Ghi nhận trong `evidence.json` ở dạng đã che một phần, không đưa
nguyên văn vào báo cáo gửi hội đồng. Và nó **không phải** dấu hiệu AI.

---

## RSID — có nghiên cứu forensic thật, và có giới hạn cứng

Word 2007+ gán **revision save identifier** cho mỗi phiên chỉnh sửa kết thúc bằng một lần Save.
Nằm ở `word/settings.xml` (`<w:rsids>`) và bám vào từng run/paragraph (`w:rsidR`, `w:rsidRDefault`).

Tài liệu học thuật: *Examining and detecting academic misconduct in written documents using revision
save identifier numbers in MS Word* — FSI: Digital Investigation, 2024
([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666281724001458)).

Copy/paste/chèn khối text từ tài liệu khác **đều để lại dấu** trong mã hoá RSID.

> 🔴 **Giới hạn phải nói ra trong mọi báo cáo:** cài đặt OOXML của Microsoft **không tuân chuẩn**, nên RSID
> **KHÔNG cho phép phục dựng thứ tự thời gian** của các lần sửa. RSID gắn với *sự kiện sửa*, không phải
> *dấu thời gian*. Ai nói "RSID chứng minh anh ta paste lúc 2h sáng" là nói sai.

**Heuristic dùng được:** rất ít RSID distinct + văn bản rất dài + `revision` thấp = soạn trong một hoặc
hai phiên, khối lớn xuất hiện cùng lúc. Đó là **chỉ dấu để hỏi**, không phải kết luận.

---

## Provenance chủ động — mạnh hơn nhiều, nhưng phải yêu cầu TRƯỚC

| Công cụ | Cơ chế | Hạn chế |
|---|---|---|
| Google Docs Version History | Timeline bản nháp; khối text lớn xuất hiện trong thời gian ngắn = paste | Chỉ khi soạn *trong* Docs |
| [Draftback](https://draftback.com/) | Replay toàn bộ revision history như quay video quá trình gõ | Chỉ Google Docs |
| Grammarly Authorship | Phân loại từng phần: gõ tay / dán / sinh bởi AI | Sản phẩm thương mại; số liệu hiệu quả là marketing của chính họ |

**Không áp ngược được.** Phải yêu cầu từ đầu học kỳ. Nhưng Thông tư 49/2026 đã đứng sẵn về phía cách làm này.

Và lưu ý quan trọng để "bán" cho học viên: **đã có tiền lệ sinh viên dùng chính version history để tự minh oan.**
Khung này bảo vệ cả hai phía — hãy trình bày theo hướng đó, không phải hướng giám sát.

---

## Ký tự lạ — phần lớn đã bị bác bỏ cho tiếng Việt

Quét vẫn rẻ nên cứ quét, nhưng **kỳ vọng thấp**: trong ca thật, NBSP · ZWSP · narrow-NBSP · em-dash ·
curly quotes · soft hyphen đều **bằng 0** ở cả bài AI lẫn bài người. Đây là tín hiệu tiếng Anh,
không chuyển sang tiếng Việt qua `.docx`.

**Chuẩn hoá NFC/NFD: đã bị bác bỏ hoàn toàn** — Word tự chuẩn hoá NFC khi lưu, nên mọi `.docx` đều thuần NFC.

Còn dùng được: **homoglyph Cyrillic** (`а е о р с х` trông y hệt Latin) — hiếm nhưng khi có thì rất đáng ngờ.
