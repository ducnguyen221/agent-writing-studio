# Writer baseline — hồ sơ tùy chọn, lưu cục bộ

Writer baseline dùng để chống báo oan khi người viết vốn có thói quen dùng phép đối, thuật ngữ Anh,
câu dài hoặc công thức nghề nghiệp. Đây là dữ liệu có thể nhận diện cá nhân nên **nó không nằm trong
repo nữa**: thư mục này chỉ giữ schema và hướng dẫn.

## Dữ liệu nằm ở đâu

Hồ sơ và bài mẫu sống **ngoài repo**, ở một trong hai chỗ dưới đây. Repo chỉ là đường lui cuối cùng khi
không có cả hai; thứ tự tra đầy đủ ba gốc ở đoạn cuối mục này:

- **kho tri thức cá nhân** (`OPCOS_BRAIN_PATH`, mặc định `~/Brain`) — nên dùng khi có kho, vì hồ sơ
  giọng mang danh tính người viết và dùng lại được ngoài xưởng viết;
- **station** (`WRITING_STUDIO_DATA`) khi không có kho:

```
$WRITING_STUDIO_DATA/writers/<slug>/profile.yaml
$WRITING_STUDIO_DATA/writers/<slug>/samples/
```

`writer_profile_ref` của `context.json` là đường **tương đối**, phân giải theo thứ tự: (1) gốc kho tri
thức → (2) gốc station → (3) gốc repo; chuỗi không chứa `/` là slug, tìm `writers/<slug>/profile.yaml`
ở (2) rồi `shared/writers/<slug>/profile.yaml` ở (3). Luật đầy đủ ở
`skills/01-context-architect/references/03-brain-bridge.md`.

Thứ tự ưu tiên của mọi script: **tham số CLI tường minh** (`--samples-dir`, `--out`) → biến
`WRITING_STUDIO_DATA` → `shared/writers/<slug>/` trong repo. Vế cuối chỉ là lưới an toàn cho người
clone repo về mà chưa dựng station; `.gitignore` vẫn chặn `shared/writers/**` để một lần đặt nhầm
chỗ không thành một lần commit nhầm. Dựng station: xem `README.md` trong chính thư mục station.

## Hồ sơ giọng là DỮ LIỆU, không phải tri thức

Phân biệt này quyết định thứ gì vào đây. `profile.yaml` giữ **số đo**: vân tay câu chữ, khuôn tu từ
đếm được, thuật ngữ bắt buộc, mã băm bài mẫu. Nó **sinh lại được** từ bài mẫu bằng script.

Thứ **không đo được** — vai người viết được đứng, kho chất liệu được phép kể, điều cấm riêng, khuôn
trình bày của kênh đăng — là **tri thức**, và thuộc kho tri thức cá nhân ngoài repo (xem README gốc,
mục *Ba tầng, ba chỗ*). Trường `voice_notes` trong hồ sơ là **bản nén** của tri thức đó để trục 4 và
trục 5 dùng được mà không phải mở kho; bản nén thì tự khai nguồn ở dòng đầu.

## Điều kiện tạo

- Có ít nhất 3 bài đã xác nhận chính chủ, tốt hơn là 10 bài cùng thể loại.
- Bài mốc phải có provenance; không dùng văn “được cho là của tác giả”.
- Không trộn bài đã qua AI rewrite nếu mục tiêu là baseline giọng tự nhiên.
- Ghi ngôn ngữ, thể loại, thời gian và bối cảnh; không coi một profile là phổ quát.

## Hình dạng chuẩn: `writer.schema.json`

Từ 30/08/2026, **nguồn chân lý về hình dạng hồ sơ là `writer.schema.json`** trong chính thư mục này,
và chân dung độc giả là `audience.schema.json`. Hai file đó được commit; `profile.yaml` và `samples/`
thì không — chúng ở kho tri thức hoặc station. Dựng hồ sơ bằng:

```
python shared/scripts/profile_build.py --writer <slug> --genre <genre>
```

Hồ sơ và bài mẫu nằm trong kho tri thức thì chỉ rõ hai đường, và dựng lại mà giữ phần điền tay:

```
python shared/scripts/profile_build.py --writer <slug> --genre <genre> \
  --samples-dir <kho>/<thư mục bài mẫu> --out <kho>/<đường profile.yaml> --keep-manual
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
