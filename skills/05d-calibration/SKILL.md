---
name: 05d-calibration
description: Use when building forensic fixtures, calibrating thresholds, evaluating false positives, adding a language profile, or changing scoring rules.
---

# Calibrating Forensics

## Tổng quan

Độ chính xác đến từ corpus có nguồn gốc biết trước, không đến từ danh sách “từ AI”. Mục tiêu ưu tiên
là giảm báo oan ở nhãn `priority_check`, sau đó mới tối ưu khả năng bắt AI/mixed.

## Corpus tối thiểu

Tách theo thể loại và gồm bốn nhóm: người viết, AI thuần, mixed-edited, adversarial. Bài người cần
bằng chứng trước 2022 hoặc phiên viết có giám sát. Chia train/dev/test theo tác giả và họ prompt để
tránh rò. Không commit văn bản thật; chỉ lưu manifest và số liệu tổng hợp.

## Quy trình

1. Khóa phiên bản skill, rubric và scoring.
2. Chạy baseline trước khi sửa ngưỡng.
3. Chỉ chỉnh trên dev; test ẩn chạy một lần sau khi đóng băng.
4. Đo FPR người thật, recall AI, precision từng finding, span overlap của mixed, abstention và độ ổn
   định qua ba lượt đọc.
5. Rule có precision dưới 50% trên bài người bị tắt hoặc chuyển vào profile thể loại.
6. Chạy paraphrase, humanizer, homoglyph, lỗi chính tả, đổi khoảng trắng và chèn đoạn người.
7. Xuất số liệu kèm cỡ mẫu và khoảng; không công bố “X% chính xác” trần trụi.

Đọc [giao thức đánh giá](../../docs/EVALUATION_v1.md) và
[chống báo oan](../05-forensics/references/03-chong-bao-oan.md). Khi thêm ngôn ngữ, bắt buộc đọc
[hướng dẫn hiệu chỉnh ngôn ngữ](../05-forensics/references/11-language-calibration.md).

## Thang bằng chứng

- 30 bài người không lỗi: cận trên FPR 95% vẫn khoảng 10%.
- 100 bài người không lỗi: mới hỗ trợ mốc khoảng 3%.
- 300 bài người không lỗi: mới kiểm được vùng khoảng 1% theo quy tắc ba.

## Thêm ngôn ngữ

Chưng cất phương pháp từ nguồn ngoại ngữ thành tài liệu tiếng Việt; giữ nguyên tên kỹ thuật, câu
trích và khóa tra cứu có chức năng. Không dịch blacklist rồi coi là language pack. Profile mới phải
có corpus người/AI/mixed riêng, thể loại riêng và test báo oan trước khi mở S/C.

## Ranh giới

Skill này không chạy trong review thường ngày và không cung cấp cách lách detector. Mọi thay đổi
ngưỡng phải tăng phiên bản, chạy lại toàn bộ fixtures và ghi rõ rule nào tăng/giảm vì dữ liệu nào.
