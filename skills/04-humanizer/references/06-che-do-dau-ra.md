# Ba chế độ đầu ra

Cùng một bản sửa, ba cách giao. Chế độ **không** đổi luật biên tập: vùng bảo vệ, `facts_added`/
`facts_removed` rỗng, `metadata.stylometric_polish: true` giữ nguyên ở cả ba. Nó chỉ đổi **những gì
được in ra** và **những gì được ghi xuống đĩa**.

Chọn chế độ ở đầu lượt, không đổi giữa chừng. Không đoán: người dùng dán một đoạn vào khung chat thì
là *dán-text*; chỉ một đường dẫn file thì là *file*; trục 4 đang được một quy trình khác gọi vào thì
là *nhúng-trong-task*. Còn phân vân thì hỏi một câu.

---

## 1. Dán-text — người dùng dán văn bản thẳng vào lượt

**Trả ba phần, đúng thứ tự này:**

1. **Danh sách tín hiệu tìm thấy**, mỗi dòng một `sentence_id` + tên họ tín hiệu + trích đúng cụm bị
   nêu. Chưa sửa gì cả — đây là bước nhận diện, để người dùng thấy trước khi thấy bản mới. Không
   liệt kê được `sentence_id` thì không được nêu tín hiệu đó.
2. **Bản đã sửa**, đầy đủ, không cắt đoạn, không thay đoạn giữa bằng dấu ba chấm.
3. **`polish.diff.json`** in ra ngay trong lượt, theo `shared/schemas/polish.schema.json`.

Không được im lặng giao mỗi bản mới. Ở chế độ này người dùng không có file để mở đối chiếu, nên phần
diff là thứ duy nhất chứng minh trục 4 đã sửa gì; giấu nó đi là biến biên tập thành phép màu.

Văn bản dán vào không có `sentences.json`: sinh `sentence_id` cho lượt đó và **in kèm bảng số câu**,
để người dùng tra được. Không tự đếm câu trong đầu rồi ghi một con số không ai kiểm được.

---

## 2. File — người dùng đưa đường dẫn

**Ghi bản cuối vào file đích, chỉ vậy.**

- **Tuyệt đối không đụng** vào code block, khối số liệu, bảng, frontmatter, chú thích nguồn, liên kết,
  và bất cứ gì nằm trong vùng bảo vệ (`02-vung-bao-ve.md`). Nếu một đoạn cần sửa nằm lẫn trong bảng
  hoặc trong code, **bỏ qua đoạn đó** và ghi vào `warnings[]` thay vì sửa khéo.
- Không chèn bình luận, không chèn dấu vết sửa, không đổi cách xuống dòng của phần không sửa. File
  sau khi ghi phải `diff` được với file trước và chỉ hiện đúng những dòng văn xuôi đã sửa.
- `polish.diff.json` và `polished.provenance.json` ghi **cạnh** file đích, không chèn vào trong nó.
  Trường hợp không được phép tạo file phụ: chèn provenance dưới dạng HTML-comment ở cuối file.
- Ghi đè file gốc chỉ khi người dùng nói rõ. Mặc định ghi sang `<tên>.polished.<đuôi>`.
- **Đích giao vs kho gốc.** Người dùng chỉ định thư mục làm việc của họ thì **bản giao** (file đích
  + sidecar) ghi thẳng vào đó — đó là nơi họ đọc và quản lý. Toàn bộ **file làm việc** của ca
  (`polish.diff.json`, meta, bản trung gian) vẫn nằm trong thư mục ca ở station
  (`$WRITING_STUDIO_DATA/work/<slug>/`, fallback `./.work/<slug>/`): station là nơi làm việc gốc
  của agent, bản trong thư mục người dùng là bản chép để giao. Sửa tiếp thì sửa từ ca trong station
  rồi giao lại, không biến bản chép thành nguồn thứ hai.

---

## 3. Nhúng-trong-task — trục 4 là một bước trong quy trình lớn hơn

**Chỉ trả bản cuối. Không diễn giải.**

Không lời dẫn, không "tôi đã sửa những chỗ sau", không bảng tín hiệu, không tóm tắt. Bên gọi đang chờ
một chuỗi văn bản để đưa sang bước sau; mọi câu thừa của trục 4 sẽ đi thẳng vào sản phẩm cuối.

`polish.diff.json` **vẫn phải sinh** — ghi ra file hoặc trả về trong trường dữ liệu mà bên gọi quy
định, không in vào phần văn bản. Im lặng ở đây là im lặng với người đọc cuối, không phải im lặng với
sổ ghi.

Fail-closed vẫn nguyên: `facts_added`/`facts_removed` khác rỗng thì **trả bản gốc** và trả kèm một
dòng lỗi, chứ không trả bản sửa. Bên gọi thà nhận bản gốc còn hơn nhận một bản đã lệch sự kiện mà
không ai đọc lại.

---

## 4. Voice-matching ad-hoc — chưa có hồ sơ người viết

Không có `shared/writers/<slug>/`, người dùng vẫn có thể đưa **1–2 bài mẫu ngay trong lượt**. Được
dùng, với đúng ba ràng buộc:

- **Dùng như hồ sơ `status: draft`.** Một hai bài không tách được thói quen của người ra khỏi đặc thù
  của bài — luật này đã có ở `shared/writers/README.md` và `writer.schema.json` chặn cứng ở
  `built_from < 3`. Bài mẫu ad-hoc ở đây cũng vậy.
- **Chỉ gợi ý, không ép `fingerprint`.** Được đọc bài mẫu để chọn cách gọi khái niệm, độ trang trọng,
  thói quen mở câu. **Không** lấy số đo của một hai bài (độ dài câu trung bình, `gloss_per_1000`,
  `nominal_per_1000`) rồi kéo bản sửa về khớp con số đó. Ép fingerprint từ mẫu quá nhỏ là bắt chước
  đặc thù của đúng hai bài, không phải giọng của người.
- **Khai đúng trong sổ.** `polish.diff.json` ghi
  `profile_used: "ad-hoc (n bài, chưa xác nhận chính chủ)"` với `n` là số bài thật đã đọc. Không ghi
  `null` (đã dùng bài mẫu thì đó là sai sự thật), không ghi tên slug (chưa có hồ sơ nào cả).

Bài mẫu ad-hoc **không** được dùng để hạ finding của trục 5 — đó là việc của hồ sơ `ready`, xem
`shared/writers/README.md`. Ở trục 4 nó chỉ là nguồn tham khảo về giọng.

Người dùng đưa ≥3 bài và xác nhận chính chủ: dừng lại đề nghị dựng hồ sơ thật bằng
`shared/scripts/profile_build.py`. Một hồ sơ dùng được nhiều lần tốt hơn ba bài đọc một lần rồi quên.
