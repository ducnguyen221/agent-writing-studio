# ECOSYSTEM — Agent Writing Studio trong hệ thống ACD

## 🤝 ACD Ecosystem Integration
- **Role in ACD:** Studio thuộc Nhóm 2 (Production Studio) — xưởng viết và biên tập tiếng Việt: năm trục từ bối cảnh, bản nháp, phê bình, làm tự nhiên tới kiểm chứng và bàn giao. `agent-skill-studio` là xưởng nền cấp chuẩn `SKILL.md` portable, công cụ kiểm (`validate`/`audit`/`package`) và đóng gói skill; repo này tự giữ nghiệp vụ của mình, không nhờ xưởng nền viết thay.
- **Upstream Controllers:** Repo marketing (copy, blog, PR), `agent-customer-team` (FAQ, hướng dẫn xử lý), `agent-finance-legal-team` (hợp đồng, SLA, NDA), `agent-hr-team` (JD, thư tuyển dụng) và `agent-academy-team` (giáo trình, handbook) ở mức Cốt lõi; `agent-executive-team`, `agent-sales-team`, `agent-agile-team`, `agent-operations-team` ở mức Thường xuyên. `agent-data-studio` cấp số liệu thực chứng cho bài có chiều sâu.
- **Downstream Consumers:** `agent-slide-studio` nhận chữ đã gọt; `agent-voice-studio` nhận kịch bản để đọc. `agent-skill-studio` nhận phần biên tập `description` và thân tiếng Việt của skill để kích hoạt đúng, không đổi quy tắc.
- **Recommended Bundles:** Bundle A (biên tập bài PR, blog) cùng `agent-video-studio` và `agent-voice-studio`. Không thuộc Bundle E; hỗ trợ biên tập chữ cho `agent-skill-studio` khi được nhờ.
- **Handoff Artifacts:** Đầu vào là `production-brief.md` do Team giao, rồi tệp bối cảnh của trục thứ nhất. Đầu ra là bản viết đã duyệt kèm khai báo phần máy viết, báo cáo phê bình và kiểm chứng, bản giao `.docx` khi cần, cùng biên nhận nghiệm thu.
