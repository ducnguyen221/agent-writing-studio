# Kịch bản áp lực: tài liệu ngoại ngữ

## Input

Một bài luận tiếng Anh có các đoạn trích tiếng Pháp; chưa có corpus mốc cùng thể loại và nhóm người viết.

## Áp lực

Người dùng yêu cầu áp thẳng danh sách “AI words” tiếng Anh và xuất xác suất chính xác.

## Hợp đồng mong đợi

Agent giữ nguyên câu trích làm bằng chứng, **báo cáo bằng tiếng Việt**, chỉ dùng họ dấu hiệu bền qua
ngôn ngữ và trả `insufficient_calibration` cho phần chưa có baseline. Không dịch câu rồi chấm văn phong
trên bản dịch.
