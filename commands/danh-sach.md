---
description: List every agent-writing-studio command with its axis, inputs and output artifacts, read live from the command files
argument-hint: [để trống, hoặc tên một lệnh muốn xem kỹ]
---

Người dùng muốn xem **danh sách lệnh** của agent-writing-studio: **$ARGUMENTS**

## Cách dựng bảng — đọc động, KHÔNG chép cứng

Bảng dưới đây **không được viết sẵn trong file này**. Một bảng chép cứng và bảy file lệnh là hai
nguồn sự thật, và chúng sẽ lệch nhau ngay lần sửa đầu tiên.

1. Liệt kê mọi file `*.md` **trong cùng thư mục với chính file lệnh này** (thư mục `commands/` của
   repo/plugin; dạng plugin là `${CLAUDE_PLUGIN_ROOT}/commands/`), **bỏ `danh-sach.md`**.
2. Với mỗi file, đọc:
   - `description:` trong frontmatter — mô tả tiếng Anh, dùng để định tuyến;
   - mục **`## Tóm tắt cho /agent-writing-studio:danh-sach`** ở cuối file — bốn dòng
     `Trục` · `Làm gì` · `Cần đầu vào` · `Ra file`.
3. Sắp theo thứ tự chuỗi công việc — số đầu tên file chính là số trục: `01-boi-canh` →
   `02-viet-nhap` → `03-phan-bien` → `04-bien-tap` → `05-giam-dinh` → `giao-docx`. File nào không
   nằm trong thứ tự đó thì xếp cuối theo tên.
4. In một bảng Markdown năm cột: **Lệnh · Trục · Làm gì · Cần đầu vào · Ra file gì**. Cột *Lệnh* ghi
   đủ namespace: `/agent-writing-studio:<tên>`.

File nào thiếu mục tóm tắt: vẫn liệt kê, điền `—` vào ô thiếu và **nói rõ file nào thiếu** thay vì
tự nghĩ hộ nội dung.

`$ARGUMENTS` có tên một lệnh: in bảng như trên, rồi đọc trọn file lệnh đó và tóm tắt kỹ phần
*Đầu vào* và *Chỉ làm đúng bước này*.

## Nói kèm ba điều, mỗi điều một dòng

- **Mỗi lệnh chạy độc lập được giữa chừng.** Thiếu artifact của bước trước thì lệnh đó nói rõ thiếu
  gì và lệnh nào sinh ra nó — **không** tự chạy lại cả chuỗi.
- **Chuỗi nối nhau bằng file**, trong thư mục ca `$WRITING_STUDIO_DATA/work/<slug>/` (không đặt biến
  thì `./.work/<slug>/`), không nối bằng trí nhớ hội thoại.
- **Bản giao cho người đọc mặc định là `.docx`**, đặt trong thư mục người dùng đang làm việc — station
  `.writing` là xưởng của agent, không phải chỗ người dùng phải vào lấy bài.

## Không làm gì khác

Lệnh này chỉ in bảng. Không tạo thư mục ca, không đọc bài của người dùng, không chạy trục nào.
