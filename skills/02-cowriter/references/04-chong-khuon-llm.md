# Chống khuôn LLM — áp ngay khi sinh, không đợi trục 4

Trục 4 sửa văn **sau khi đã có bản thảo**. Nhưng có một loại lỗi mà sửa sau là quá muộn: khuôn.
Một mở bài toàn cảnh, một kết bài kêu gọi chung chung, một chuỗi "Tác giả A cho rằng… Tác giả B cho
rằng…" — chúng không phải lỗi câu chữ, chúng là **chỗ đứng của cả đoạn**. Sửa chúng ở trục 4 nghĩa
là viết lại đoạn, và viết lại đoạn ở cuối dây chuyền thì bằng chứng ở tầng ba của outline thường
rơi mất trong lúc viết lại.

Nên trục 2 nhận danh sách này **trước khi gõ câu đầu tiên**, ở bước nạp hồ sơ.

---

## 1. Nguồn của danh sách

Hai nguồn, gộp lại, không có nguồn thứ ba:

1. **`anti_llm_defaults[]` ở `§2` của hồ sơ thể loại đang dùng.** Đây là nguồn chính. Danh sách khác
   nhau theo thể loại và **hồ sơ là thứ quyết định** — trục 2 không mang danh sách của thể loại này
   sang thể loại khác.
2. **Bốn họ tell chuyển sang được mọi thể loại** trong
   [`shared/rules/vi-ai-tells.json`](../../../shared/rules/vi-ai-tells.json): `T25`, `T27`, `T28`,
   `T32`. Bốn họ này khác phần còn lại của danh mục ở một điểm: chúng mô tả **một câu được đặt vào
   chỗ nào**, chứ không mô tả một cách dùng từ. Câu đặt sai chỗ thì phải không sinh ra nó, chứ không
   phải sinh ra rồi gỡ.

Danh mục tell **không phải danh sách từ cấm**. Mỗi mục là một họ tín hiệu kèm phản chứng tiếng Việt,
và mọi mục hiện vẫn ở trạng thái `candidate` — dùng để **nhận ra khuôn khi mình sắp viết nó**, không
dùng để buộc tội văn bản của ai.

## 2. Bốn họ tell áp cho mọi thể loại

| Tell | Khuôn | Thay bằng |
|---|---|---|
| `T25` — kết lạc quan chung chung | Kết bài quay về lời hứa tương lai tươi sáng không gắn với luận điểm nào phía trên | Một điều kiện kiểm được: ai làm, mốc nào, không đạt thì sao |
| `T27` — giả vờ tiết lộ chân lý | Dựng ra "sự thật ít ai dám nói" rồi tiết lộ một điều hiển nhiên | Bỏ lời dẫn. Còn lại là điều hiển nhiên thì xoá; là điều bất ngờ thật thì để nó tự đứng |
| `T28` — báo trước ý kế tiếp | Câu chỉ để báo mình sắp nói gì, không mang nội dung | Để tiêu đề mục làm việc đó. Giữ lại chỉ khi câu dẫn nêu một quy tắc đọc mà tiêu đề không nêu được |
| `T32` — châm ngôn dựng theo công thức | Câu đối xứng nghe hay, không kiểm được, không thêm thông tin | Mệnh đề nói đúng điều muốn nói. Trích tục ngữ có sẵn thì giữ và ghi rõ là trích |

## 3. Danh sách theo thể loại — năm hồ sơ đầy đủ

Chép lại ở đây để đọc một lượt; **nguồn thật vẫn là `§2` của hồ sơ**, hồ sơ đổi thì file này lỗi thời.

### `essay.md`

1. "Mở bài bằng mệnh đề toàn cảnh kiểu 'Trong bối cảnh … đang diễn ra mạnh mẽ'"
2. "Kết bài bằng lời kêu gọi chung chung không gắn với luận đề"
3. "Chuyển đoạn bằng 'Bên cạnh đó' / 'Không những vậy' khi quan hệ logic thật là đối lập hoặc nhân quả"
4. "Câu chốt cuối đoạn chỉ nhắc lại câu đầu đoạn bằng từ khác"
5. "Danh sách gạch đầu dòng có tiêu đề in đậm thay cho đoạn văn lập luận"

### `research.md`

1. "Mở đầu bằng mệnh đề toàn cảnh kiểu 'Trong bối cảnh … ngày càng phát triển mạnh mẽ' thay cho khoảng trống nghiên cứu cụ thể"
2. "Tổng quan tài liệu viết thành chuỗi 'Tác giả A cho rằng… Tác giả B cho rằng…' không có tranh luận giữa các nguồn"
3. "Đưa diễn giải, nguyên nhân hoặc đánh giá vào phần Kết quả"
4. "Bàn luận kết thúc bằng câu kêu gọi 'cần có thêm nghiên cứu trong tương lai' không nói rõ nghiên cứu nào"
5. "Mục Hạn chế liệt kê hạn chế chung chung không ảnh hưởng tới kết luận nào của chính bài"
6. "Trích dẫn nêu tên tác giả hoặc tên tạp chí thay cho kết quả cụ thể được trích"

### `novel.md`

1. "Mở truyện bằng đoạn giới thiệu bối cảnh và lai lịch nhân vật trước khi có việc gì xảy ra"
2. "Gọi tên cảm xúc thay cho cho thấy nó: 'cô cảm thấy buồn' đứng ở chỗ lẽ ra là một hành động cụ thể"
3. "Mọi nhân vật nói cùng một giọng: che tên đi thì không phân biệt được ai đang nói"
4. "Chương nào cũng kết bằng cùng một kiểu câu treo, ví dụ 'Nhưng cô không biết rằng…'"
5. "Đặt đoạn giải thích luật thế giới dài như trang từ điển vào giữa một cảnh đang diễn ra"
6. "Dùng khuôn 'không phải X mà là Y' làm nhịp tu từ mặc định thay vì dùng đúng một lần khi thật sự có tương phản"

### `journalism.md`

1. "Lead mở bằng bối cảnh chung chung kiểu 'Trong những năm gần đây…' thay cho sự việc vừa xảy ra"
2. "Cân bằng giả: đặt một phát ngôn của mỗi bên cạnh nhau rồi kết bằng 'vấn đề vẫn còn nhiều tranh cãi'"
3. "Quy nguồn mơ hồ: 'theo các chuyên gia', 'nhiều người dân cho rằng' không kèm tên và tư cách"
4. "Kết bài bằng lời khuyên hoặc lời kêu gọi thay cho việc cần theo dõi tiếp"
5. "Dùng tính từ đánh giá thay cho dữ kiện, ví dụ 'vụ việc gây bức xúc dư luận'"
6. "Đưa suy đoán về động cơ của nhân vật vào phần tường thuật như thể đó là dữ kiện"

### `blog.md`

1. "Mở bài định nghĩa lại một khái niệm người đọc đã biết trước khi vào việc"
2. "Hook giả thẳng thắn kiểu 'Nói thật nhé, hầu hết mọi người đều sai về…' rồi nói một điều hiển nhiên"
3. "Kết bài bằng lời chúc hoặc lời hứa tương lai thay cho một việc người đọc làm được ngay"
4. "Câu báo trước kiểu 'Trong bài này chúng ta sẽ cùng tìm hiểu…' chỉ nhắc lại tiêu đề"
5. "Danh sách 'X điều bạn cần biết' mà mỗi mục chỉ có một câu định nghĩa"
6. "Lời mời cuối bài không liên quan tới thứ bài vừa đưa"

Hai mươi chín mục trên cộng bốn họ tell ở mục 2 là **ba mươi ba** thứ trục 2 phải cầm trong đầu khi
sinh — nhưng không phải cùng lúc: trục 2 chỉ nạp danh sách của **một** thể loại đang viết, cộng bốn
họ tell luôn bật. Ba hồ sơ mới của Phase 1b cho thấy rõ vì sao danh sách không được trộn: khuôn
"mọi nhân vật nói cùng một giọng" chỉ có nghĩa ở tiểu thuyết, còn "quy nguồn mơ hồ" mà mang sang
tiểu thuyết thì thành lệnh cấm hư cấu.

**Bốn thể loại VN đặc thù không có mặt ở đây.** `chinh-luan`, `de-cuong-nghien-cuu`,
`bao-cao-thuc-tap`, `sang-kien-kinh-nghiem` là hồ sơ `partial` — chỉ có §5, dựng cho trục 5. Trục 2
không đọc chúng và không được tự suy ra danh sách khuôn cho chúng; muốn viết bốn thể loại đó thì
dùng hồ sơ đầy đủ gần nhất (`essay.md` hoặc `research.md`) và ghi rõ trong phạm vi.

## 4. Áp ở tầng nào

Khuôn không sống ở tầng câu, nên đừng đợi tới tầng câu mới gỡ:

| Tầng | Áp cái gì |
|---|---|
| **Tầng 1 outline** — luận đề, ý chính | Ý chính nào chỉ là một chủ đề chứ không phải mệnh đề cãi được → khuôn mở bài toàn cảnh sẽ mọc ra từ chính chỗ ấy |
| **Tầng 2 outline** — đoạn | Quan hệ thật giữa hai đoạn phải được khai. Khai rồi thì không có chỗ cho "Bên cạnh đó" khi quan hệ thật là đối lập. Đoạn kết khai "trả lời đề bằng gì" thì `T25` không mọc được |
| **Tầng 3 outline** — bằng chứng | Chỗ trống ở tầng ba là nơi sinh ra "nhiều nghiên cứu đã chỉ ra" và khuôn "cần có thêm nghiên cứu trong tương lai". Hạ mức khẳng định hoặc báo lên, đừng lấp bằng câu |
| **Khi viết prose** | `T27`, `T28`, `T32` — ba họ này chỉ xuất hiện ở tầng câu, và ba câu hỏi để bắt chúng: *câu này có nội dung không? bỏ đi bài có mất gì không? nó nói được điều gì mà tiêu đề chưa nói?* |
| **Vòng đánh giá** | Cửa số 3 của [`02-vong-sua-danh-gia-giu.md`](02-vong-sua-danh-gia-giu.md): bản mới kéo khuôn nào vào thì thua bản cũ |

## 5. Ba luật giữ cho việc này không thành báo oan

1. **`genre_baseline` thắng danh sách này.** `§5` của hồ sơ khai tín hiệu nào là bình thường ở thể
   loại đó thì tín hiệu ấy **không phải khuôn cấm**. Báo cáo thực tập có mục "kết quả – tồn tại –
   phương hướng" là khung được dạy, không phải khuôn máy: giữ mục, chỉ thay nội dung rỗng bằng nội
   dung thật. Trục 4 đã trả giá một ca giám định để rút ra luật này
   ([`04-humanizer/references/03-chong-sua-oan.md`](../../04-humanizer/references/03-chong-sua-oan.md));
   trục 2 không được phạm lại nó ở đầu dây chuyền.
2. **Cụm quy ước của thể loại không phải khuôn.** "Nghiên cứu này nhằm", "Kết quả cho thấy",
   "Bảng 1 trình bày" là cách viết chuẩn của bài nghiên cứu tiếng Việt. `research.md` `§5` khai
   chúng là bình thường.
3. **Bài mẫu của người viết thắng cả hai.** `writer_profile_ref` trỏ tới hồ sơ có `pet_templates[]`:
   khuôn nào là thói quen thật của tác giả, thấy ở từ hai bài trở lên, thì đó là **giọng**, không
   phải khuôn máy. Thứ tự ưu tiên nằm ở `voice_priority` trong `§4` của hồ sơ thể loại.
