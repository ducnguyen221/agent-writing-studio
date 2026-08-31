# Writer baseline — hồ sơ tùy chọn, lưu cục bộ

Writer baseline dùng để chống báo oan khi người viết vốn có thói quen dùng phép đối, thuật ngữ Anh,
câu dài hoặc công thức nghề nghiệp. Đây là dữ liệu có thể nhận diện cá nhân nên **nó không nằm trong
repo nữa**: thư mục này chỉ giữ schema và hướng dẫn.

## Dữ liệu nằm ở đâu (từ 31/08/2026)

Hồ sơ và bài mẫu sống ở **station** ngoài repo, trỏ bằng biến môi trường `WRITING_STUDIO_DATA`:

```
$WRITING_STUDIO_DATA/writers/<slug>/profile.yaml
$WRITING_STUDIO_DATA/writers/<slug>/samples/
```

Thứ tự ưu tiên của mọi script: **tham số CLI tường minh** (`--samples-dir`, `--out`) → biến
`WRITING_STUDIO_DATA` → `shared/writers/<slug>/` trong repo. Vế cuối chỉ là lưới an toàn cho người
clone repo về mà chưa dựng station; `.gitignore` vẫn chặn `shared/writers/**` để một lần đặt nhầm
chỗ không thành một lần commit nhầm. Dựng station: xem `README.md` trong chính thư mục station.

## Điều kiện tạo

- Có ít nhất 3 bài đã xác nhận chính chủ, tốt hơn là 10 bài cùng thể loại.
- Bài mốc phải có provenance; không dùng văn “được cho là của tác giả”.
- Không trộn bài đã qua AI rewrite nếu mục tiêu là baseline giọng tự nhiên.
- Ghi ngôn ngữ, thể loại, thời gian và bối cảnh; không coi một profile là phổ quát.

## Hình dạng chuẩn: `writer.schema.json`

Từ 30/08/2026, **nguồn chân lý về hình dạng hồ sơ là `writer.schema.json`** trong chính thư mục này,
và chân dung độc giả là `audience.schema.json`. Hai file đó được commit; `profile.yaml` và `samples/`
thì không — chúng ở station. Dựng hồ sơ bằng:

```
python shared/scripts/profile_build.py --writer <slug> --genre <genre>
```

Ba khác biệt so với phác thảo bên dưới, ghi ra để không ai đọc nhầm bản cũ:

- `observed.repeated_frames` đổi tên thành **`pet_templates[]`** và không còn là mảng chuỗi: mỗi khuôn
  phải mang bằng chứng `seen_in_samples` (≥2 bài khác nhau) và `total_hits`. Đây là mục để trục 5
  **hạ** finding, nên nó phải chứng minh được chứ không chỉ khai.
- `fingerprint` là **số đo**, tách khỏi `voice_notes` là **nhận xét của người**. Script điền phần
  đầu và để trống phần sau; nó không đo được giọng và không được bịa.
- `built_from < 3` ⇒ **`status: draft`**, schema chặn cứng. Hồ sơ draft chỉ để tham khảo.

## Trường nên có *(phác thảo ban đầu — hình dạng thi hành được ở `writer.schema.json`)*

```yaml
profile_version: "1.0"
language: vi
genre: essay
built_from: 5
observed:
  repeated_frames: ["vua_X_vua_Y"]
  necessary_english_terms: ["semantic model"]
  sentence_length_notes: "Câu dài ở phần giải thích kỹ thuật."
  voice_notes: "Thường nêu ví dụ dự án trước kết luận."
provenance: "local-only manifest path"
```

## Cách dùng trong review

Không mở profile ở lượt đọc mù đầu tiên. Mở ở lượt chống báo oan sau khi findings sơ bộ đã ghi.
Baseline chỉ được **hạ hoặc loại G1/G2** nếu dấu hiệu trùng thói quen đã chứng minh; không được tạo
finding mới và không được xóa vấn đề nguồn/dữ kiện ở G3. Ghi rõ finding nào đã được hạ nhờ baseline.

Không đưa tên, email, tổ chức, bài mẫu hoặc trích dẫn dài vào báo cáo tổng hợp.
