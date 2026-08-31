> **Vision gốc của chủ repo — giữ nguyên làm nguồn tham chiếu. Bản triển khai thật xem `README.md`**
> (và `KIEN-TRUC.md` cho phần kiến trúc): repo hiện thực ma trận này bằng **5 skill × 9 hồ sơ
> thể loại**, không phải 25 skill; `studio_engine.py` ở mục V dưới đây là **phác thảo minh hoạ**,
> chưa bao giờ là code đang chạy trong repo.

# ✍️ AGENT WRITING STUDIO — THE 2D ARCHITECTURAL MATRIX
> **The Next-Gen Agentic Workspace for Multi-Archetype Writing, Cognitive Profiling, AI Forensics & Stylometric Polish.**  
> *Hệ sinh thái AI Agent toàn diện cho chữ viết tiếng Việt: Chuẩn hóa theo Ma trận 2 Chiều (5 Giai đoạn Quy trình × 5 Loại hình Nội dung), tích hợp Hệ thống Profile Tư duy chuyên biệt và Khả năng đồng bộ với Brain.*

---

## 🧭 I. ĐỊNH VỊ HỆ SINH THÁI & BỘ 3 STUDIO (CREATIVE SUITE)

`agent-writing-studio` hoàn thiện **Bộ 3 Tam Mã Sáng Tạo (The Creative Suite)**:
* 🎨 **`agent-design-studio`** ➔ Xử lý Hình ảnh / Thiết kế Visual / Banner / UI / Illustration.
* 🎙️ **`agent-voice-studio`** ➔ Xử lý Âm thanh / Giọng nói / Voice Clone / Podcast / Audio Drama.
* ✍️ **`agent-writing-studio`** ➔ Xử lý toàn diện Chữ viết theo **Ma trận 2 Chiều (2D Studio Matrix)** từ Tư duy khởi tạo ➔ Xuất bản.

---

## 🧩 II. MA TRẬN 2 CHIỀU TỔNG THỂ (THE 2D STUDIO MATRIX)

Hệ thống được thiết kế như một **Ma trận 5 × 5 (25 Giao điểm chức năng)**:
* **Trục Tung (Y-Axis):** 5 Giai đoạn quy trình tuần tự *(Tư duy/Bối cảnh ➔ Viết nháp ➔ Phản biện ➔ Tối ưu ➔ Giám định)*.
* **Trục Hoành (X-Axis):** 5 Loại hình nội dung chuyên biệt *(Blog, Bài luận, Nghiên cứu, Báo chí, Tiểu thuyết)*.

```
┌──────────────────────────────────────┬────────────────────────┬────────────────────────┬────────────────────────┬────────────────────────┬────────────────────────┐
│  QUY TRÌNH (Y) \ LOẠI HÌNH (X)       │ A. BLOG & THOUGHT LEAD │ B. BÀI LUẬN & THI CỬ   │ C. NGHIÊN CỨU & BÁO CÁO│ D. BÁO CHÍ & PHÂN TÍCH │ E. TIỂU THUYẾT & NARR. │
├──────────────────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┤
│ 1. INTENT, PERSONA & CONTEXT        │ • Search Intent & Niche│ • Đề bài & Luận đề gốc │ • Khoảng trống (Gap)   │ • Góc nhìn sự kiện     │ • Character 3D Forge   │
│    (Định vị Tư duy, Profile, Bối cảnh)│ • Chân dung độc giả    │ • Barem thi chuẩn      │ • Khung lý thuyết/Brain│ • Bối cảnh thời sự     │ • World-Building Matrix│
├──────────────────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┤
│ 2. CO-WRITER & DRAFTING              │ • Hook mở đầu lôi cuốn │ • Cấu trúc luận điểm   │ • Phương pháp luận     │ • Cấu trúc Tháp ngược  │ • Cấu trúc 3 Hồi       │
│    (Đồng sáng tác & Khởi tạo bản thảo)│ • CTA chuyển đổi rõ    │ • Phản đề sắc bén      │ • Phân tích dữ liệu    │ • Trích dẫn nhân chứng │ • Hội thoại có cá tính │
├──────────────────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┤
│ 3. CRITIQUE & LOGIC AUDIT            │ • Độ giữ chân & Hấp dẫn│ • Soi ngụy biện logic  │ • Độ tin cậy trích dẫn │ • Tính khách quan      │ • Soi Plot Holes       │
│    (Phản biện, Chấm điểm Barem)     │ • Tính thực tiễn       │ • Chấm điểm Barem thi  │ • Kiểm chứng chéo data │ • Kiểm tra nguồn tin   │ • Nhịp thắt/mở nút     │
├──────────────────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┤
│ 4. HUMANIZE & POLISH                 │ • Giọng đàm thoại gần gũi│ • Xóa danh từ hóa thô │ • Chuẩn hóa thuật ngữ  │ • Đanh thép, gọn gàng  │ • Tăng nhạc tính/Văn học│
│    (Tối ưu hóa & Bơm nhịp điệu)     │ • Bơm nhịp điệu câu    │ • Tự nhiên hóa liên từ │ • Tinh chỉnh mạch lạc  │ • Xóa sáo rỗng báo chí │ • Đậm chất thơ/Cảm xúc │
├──────────────────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┼────────────────────────┤
│ 5. FORENSICS & INTEGRITY GATE        │ • Quét Cliché AI mạng  │ • Quét % AI luận văn   │ • Quét liêm chính data │ • Kiểm soát trích dẫn  │ • Giữ dấu ấn tác giả   │
│    (Giám định pháp y & Nghiệm thu)   │ • Cam kết nguyên bản   │ • Báo cáo nộp hội đồng │ • Xác nhận học thuật   │ • Báo cáo duyệt bài    │ • Hoàn thiện bản quyền │
└──────────────────────────────────────┴────────────────────────┴────────────────────────┴────────────────────────┴────────────────────────┴────────────────────────┘
```

---

## 🏛️ III. CHI TIẾT 5 GIAI ĐOẠN QUY TRÌNH (TRỤC TUNG Y-AXIS)

```
                                    LUỒNG VẬN HÀNH TUẦN TỰ 5 BƯỚC
                                    
  [GIAI ĐOẠN 1: TƯ DUY & BỐI CẢNH] ──► Phân tích Mục tiêu, Chọn Profile Nội dung, Nạp Tri thức Brain
                  │
                  ▼
  [GIAI ĐOẠN 2: ĐỒNG SÁNG TÁC]     ──► Sinh bản thảo thô theo cấu trúc chuyên biệt (Anti-AI-bias)
                  │
                  ▼
  [GIAI ĐOẠN 3: PHẢN BIỆN BAREM]   ──► Chấm điểm Barem, soi lỗi ngụy biện logic & lỗ hổng lập luận
                  │
                  ▼
  [GIAI ĐOẠN 4: CHỮA BÀI TỰ NHIÊN] ──► Tối ưu văn phong, bơm nhịp điệu (Burstiness), xóa lối nói máy
                  │
                  ▼
  [GIAI ĐOẠN 5: GIÁM ĐỊNH PHÁP Y]  ──► Quét % AI lần cuối, nghiệm thu liêm chính ➔ [XUẤT BẢN]
```

---

### 🧠 GIAI ĐOẠN 1: INTENT, PERSONA & CONTEXT ARCHITECT (ĐỊNH VỊ TƯ DUY & PROFILE BỐI CẢNH)
* **Bản chất:** Đây là trục **"Tư duy & Đối thoại chiến lược"** giữa Bot và Người viết. Thay vì viết ngay, Bot sẽ phân tích sâu:
  1. **Mục tiêu tối thượng (Writing Intent/Goal):** Viết để thuyết phục, truyền cảm hứng, bảo vệ luận án, giải thích kỹ thuật hay giải trí?
  2. **Profile Người viết & Chân dung Độc giả (Personas):**
     * Nạp profile phong cách của người viết (Văn phong chuyên gia, hóm hỉnh, hàn lâm, hay sâu lắng).
     * Định vị chân dung người đọc (trình độ chuyên môn, nỗi đau, kỳ vọng).
  3. **Kết nối Tri thức Brain (Knowledge Layer Integration):**
     * Tự động trích xuất các ghi chú, kinh nghiệm, tài liệu tham khảo từ `Brain/` hoặc thư mục dự án để làm bối cảnh độc quyền.

---

### 🖋️ GIAI ĐOẠN 2: CO-WRITER & GENERATIVE DRAFTING (ĐỒNG SÁNG TÁC BẢN THẢO)
* **Bản chất:** Hiện thực hóa khung tư duy ở Giai đoạn 1 thành văn bản có cấu trúc chuẩn mực.
* **Đặc tính cốt lõi:**
  * Áp dụng cơ chế **Anti-AI-Bias by Design**: Không dùng các công thức chuyển đoạn mặc định của LLM.
  * Tự động điều chỉnh cấu trúc theo từng loại hình: Dạng Tháp ngược (Báo chí), Dạng Luận điểm - Phản đề (Học thuật), Dạng Kể chuyện lồng ghép Hook (Blog), Dạng 3 Hồi (Tiểu thuyết).

---

### 📊 GIAI ĐOẠN 3: CRITIQUE, GRADING & LOGIC AUDIT (PHẢN BIỆN, CHẤM ĐIỂM & SOI LỖ HỔNG)
* **Bản chất:** Chuyển vai thành Hội đồng thẩm định độc lập hoặc Giám khảo chấm thi khó tính.
* **Các bộ tiêu chuẩn:**
  * **Học thuật:** Chấm theo barem IELTS/VSTEP, Tiêu chuẩn Luận văn (Độ sâu nghiên cứu, tính mới, phương pháp luận).
  * **Báo chí/Blog:** Chấm theo thang đo Value-Density (Mật độ giá trị), tính thực tế, độ mạch lạc.
  * **Tiểu thuyết:** Soi mâu thuẫn tính cách nhân vật (Out-of-character), lỗ hổng cốt truyện (Plot Holes).

---

### ✨ GIAI ĐOẠN 4: HUMANIZE, REWRITE & STYLOMETRIC POLISH (TỐI ƯU & CHỮA BÀI TỰ NHIÊN)
* **Bản chất:** Biên tập chuyên sâu dựa trên kết quả phản biện của Giai đoạn 3.
* **Kỹ thuật thực hiện:**
  * **De-nominalization:** Xóa bỏ triệt để các tiền tố danh từ hóa sáo rỗng (*"sự phát triển của...", "việc thực hiện quá trình..."*).
  * **Burstiness Injection:** Điều chỉnh độ dài câu trập trùng, nhịp điệu thở tự nhiên của con người.
  * **Thuần Việt hóa:** Chêm xen ngôn ngữ giàu hình ảnh, thành ngữ thuần Việt phù hợp với ngữ cảnh.

---

### 🛡️ GIAI ĐOẠN 5: AI FORENSICS, AUTHENTICITY & INTEGRITY GATE (GIÁM ĐỊNH PHÁP Y & NGHIỆM THU)
* **Bản chất:** Cổng kiểm soát liêm chính và đo lường định lượng cứng trước khi xuất bản.
* **Bộ chỉ số nghiệm thu:**
  * **Chỉ số Burstiness ($\sigma > 12$):** Đảm bảo bài viết không phẳng lì theo lối máy sinh.
  * **Chỉ số Type-Token Ratio (TTR):** Đảm bảo độ phong phú ngôn từ.
  * **Quét Cliché sạch 100%:** Cam kết loại bỏ toàn bộ các mẫu câu nhận diện của AI.
  * **Xuất Chứng nhận Liêm chính (Integrity Badge):** Báo cáo minh chứng phục vụ nộp bài hoặc lưu trữ.

---

## 🎯 IV. CHI TIẾT 5 LOẠI HÌNH NỘI DUNG (TRỤC HOÀNH X-AXIS)

| Loại hình (Archetype) | Đặc trưng Trục 1 (Intent & Persona) | Khung cấu trúc Trục 2 (Drafting) | Tiêu chí Trục 3 (Critique) | Yêu cầu Trục 4 (Humanize) |
| :--- | :--- | :--- | :--- | :--- |
| **A. Blog & Thought Leadership** | Focus vào Search Intent, Pain point độc giả, Góc nhìn độc bản (Unique Angle/Hook). | Mở đầu bằng Hook hấp dẫn ➔ Thân bài giải quyết vấn đề ➔ CTA hành động rõ ràng. | Chấm điểm độ giữ chân, tính ứng dụng thực tế, mật độ thông tin. | Giọng đàm thoại gần gũi, văn phong sắc bén, giàu năng lượng. |
| **B. Bài luận & Thi cử (Essay/Exam)** | Bám sát yêu cầu đề bài, định hình Luận đề trung tâm (Thesis Statement), barem điểm. | Cấu trúc 4–5 đoạn chuẩn mực: Mở bài ➔ 2-3 Đoạn thân bài (PEEL/TEEL) ➔ Kết luận. | Soi lỗi ngụy biện, mâu thuẫn tiền đề, chấm điểm theo Barem Task Response. | Xóa bỏ liên từ sáo rỗng, chuyển ý học thuật tự nhiên, tinh tế. |
| **C. Nghiên cứu & Báo cáo chuyên sâu** | Tổng quan tài liệu, xác định Research Gap, Khung lý thuyết, kết nối tri thức `Brain/`. | Cấu trúc IMRAD (Introduction - Methodology - Results - Analysis - Discussion). | Kiểm tra độ chặt chẽ của phương pháp luận, độ tin cậy số liệu và trích dẫn. | Thuật ngữ chuẩn xác, diễn đạt khách quan, triệt tiêu cảm xúc chủ quan. |
| **D. Báo chí & Phân tích chuyên luận** | Bối cảnh thời sự, góc nhìn đa chiều của các bên liên quan, tính thời điểm (Timeliness). | Cấu trúc Tháp ngược (Inverted Pyramid), trích dẫn phỏng vấn, dữ liệu thực chứng. | Kiểm tra tính khách quan, nguồn tin độc lập, cân bằng quan điểm. | Câu văn đanh thép, ngắn gọn, gãy gọn, loại bỏ tính từ cảm tính. |
| **E. Tiểu thuyết & Sáng tác văn học** | Character Forge 3D, Ma trận thế giới (World-Building), Xung đột cốt lõi (Core Conflict). | Cấu trúc 3 Hồi (Three-Act Arc), nhịp thắt/mở nút, tương phản đối thoại và độc thoại nội tâm. | Soi Plot Holes, tính nhất quán của nhân vật, nhịp độ dồn dập/chùng lại. | Giàu nhạc tính, câu từ gợi cảm xúc, đậm chất điện ảnh (Show, Don't Tell). |

---

## 💻 V. MÃ NGUỒN LÕI MA TRẬN: `studio_engine.py`

Script Python siêu nhẹ (< 50KB, 0% GPU) tích hợp xử lý đa Profile:

```python
# studio_engine.py
import re
import math
import json
import argparse

class AgentWritingStudioMatrix:
    def __init__(self):
        # 1. Bộ từ điển Cliché AI tiếng Việt
        self.ai_cliches = [
            r"trong bối cảnh (hiện nay|kỷ nguyên số|toàn cầu hóa|phát triển mạnh mẽ)",
            r"sự phát triển (vượt bậc|không ngừng|mạnh mẽ) của",
            r"không thể phủ nhận rằng",
            r"đóng vai trò (quan trọng|then chốt|cốt lõi|cực kỳ quan trọng)",
            r"là (kim chỉ nam|tiền đề vững chắc|bước đệm quan trọng)",
            r"không chỉ (.*?)\s+mà còn",
            r"một mặt (.*?)\s+mặt khác",
            r"đặt ra không ít (thách thức|khó khăn)",
            r"tóm lại, việc",
            r"đòi hỏi sự (chung tay|phối hợp chặt chẽ)"
        ]

        # 2. Cấu hình tiêu chí theo từng Archetype (Loại hình)
        self.archetypes = {
            "blog": {"target_burstiness": 14, "tone": "conversational", "rubric": "Engagement & Actionability"},
            "essay": {"target_burstiness": 12, "tone": "academic", "rubric": "Logical Cohesion & Thesis Depth"},
            "research": {"target_burstiness": 10, "tone": "formal", "rubric": "Methodology & Citation Rigor"},
            "journalism": {"target_burstiness": 15, "tone": "objective", "rubric": "Factuality & Inverted Pyramid"},
            "novel": {"target_burstiness": 18, "tone": "literary", "rubric": "Pacing, Voice & Plot Consistency"}
        }

    def split_sentences(self, text):
        raw = re.split(r'(?<=[.!?\n])\s+', text.strip())
        return [s.strip() for s in raw if len(s.strip()) > 5]

    # --- TRỤC 1: PHÂN TÍCH PROFILE & BỐI CẢNH (INTENT ANALYZER) ---
    def analyze_intent(self, prompt, archetype="blog"):
        config = self.archetypes.get(archetype, self.archetypes["blog"])
        return {
            "mode": "INTENT_ARCHITECT",
            "archetype": archetype.upper(),
            "target_tone": config["tone"],
            "core_rubric": config["rubric"],
            "recommended_flow": [
                "1. Định vị Góc nhìn độc bản (Hook/Thesis)",
                "2. Lập cấu trúc bản thảo chuyên biệt",
                "3. Phản biện lỗ hổng lập luận",
                "4. Chữa bài tăng nhịp điệu",
                "5. Giám định pháp y liêm chính"
            ]
        }

    # --- TRỤC 3: PHẢN BIỆN BAREM THEO LOẠI HÌNH (CRITIQUE) ---
    def critique(self, text, archetype="essay"):
        sentences = self.split_sentences(text)
        words = re.findall(r'\b\w+\b', text.lower())
        ttr = len(set(words)) / len(words) if words else 0
        avg_len = len(words) / len(sentences) if sentences else 0
        
        config = self.archetypes.get(archetype, self.archetypes["essay"])
        vocab_score = min(10, round(ttr * 16, 1))
        structure_score = 8.5 if 12 <= avg_len <= 26 else 6.5
        
        return {
            "mode": "CRITIQUE_AUDIT",
            "archetype": archetype.upper(),
            "rubric_applied": config["rubric"],
            "overall_score": round((vocab_score + structure_score + 8.2) / 3, 1),
            "breakdown": {
                "Độ đa dạng từ vựng (TTR)": f"{vocab_score}/10",
                "Cấu trúc nhịp câu": f"{structure_score}/10",
                "Tính phù hợp thể loại": f"Văn phong {config['tone']} đạt chuẩn"
            }
        }

    # --- TRỤC 5: GIÁM ĐỊNH PHÁP Y AI TOÀN DIỆN (FORENSICS) ---
    def inspect(self, text, archetype="blog"):
        sentences = self.split_sentences(text)
        if not sentences: return {"error": "Văn bản rỗng."}

        words = re.findall(r'\b\w+\b', text.lower())
        total_words = len(words)
        unique_words = len(set(words))
        ttr = (unique_words / total_words) if total_words > 0 else 0

        sentence_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
        avg_len = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((l - avg_len) ** 2 for l in sentence_lengths) / len(sentence_lengths)
        std_dev = math.sqrt(variance)

        flagged = []
        cliche_count = 0
        for idx, s in enumerate(sentences):
            s_cliches = [p for p in self.ai_cliches if re.search(p, s, re.IGNORECASE)]
            cliche_count += len(s_cliches)
            w_count = len(re.findall(r'\b\w+\b', s))
            
            score = 15
            reasons = []
            if s_cliches:
                score += 45 * len(s_cliches)
                reasons.append(f"Mẫu câu đệm AI: {len(s_cliches)} cụm")
            if 20 <= w_count <= 35 and std_dev < 7:
                score += 25
                reasons.append("Độ dài câu phẳng lì theo phân phối mặc định của LLM")
            if re.search(r"\b(sự|việc|quá trình)\b", s.lower()):
                score += 15
                reasons.append("Lạm dụng danh từ hóa (Nominalization)")

            score = min(98, max(10, score))
            flagged.append({
                "id": idx + 1,
                "text": s,
                "word_count": w_count,
                "ai_score": score,
                "reasons": reasons
            })

        ai_count = sum(1 for f in flagged if f["ai_score"] >= 65)
        overall_ai = round((ai_count / len(sentences)) * 100, 1)

        return {
            "mode": "FORENSICS_GATE",
            "archetype_scanned": archetype.upper(),
            "overall_ai_percent": f"{overall_ai}%",
            "burstiness_std_dev": round(std_dev, 2),
            "burstiness_status": "Rất phẳng (Cần Humanize)" if std_dev < 7 else "Tự nhiên (Đạt chuẩn Người viết)",
            "vocabulary_ttr": round(ttr, 3),
            "total_sentences": len(sentences),
            "flagged_sentences": flagged
        }

if __name__ == "__main__":
    engine = AgentWritingStudioMatrix()
    sample = "Trong bối cảnh kỷ nguyên số phát triển mạnh mẽ hiện nay, trí tuệ nhân tạo đóng vai trò quan trọng trong việc thúc đẩy giáo dục."
    print("--- 1. PHÂN TÍCH TƯ DUY (TRỤC 1) ---")
    print(json.dumps(engine.analyze_intent("Viết bài phân tích AI", archetype="blog"), ensure_ascii=False, indent=2))
    print("\n--- 2. GIÁM ĐỊNH PHÁP Y (TRỤC 5) ---")
    print(json.dumps(engine.inspect(sample, archetype="blog"), ensure_ascii=False, indent=2))
```

---

## 🤖 VI. BỘ ĐẶC TẢ LỆNH ĐIỀU HÀNH MA TRẬN (SKILL COMMANDS)

Các lệnh điều hành hỗ trợ gắn kèm cờ `--type [blog|essay|research|journalism|novel]`:

1. **`/context [chủ đề] [--type blog|essay|research|novel]`**:  
   ➔ **Giai đoạn 1:** Phân tích Search Intent, xây dựng Chân dung độc giả/Persona, thiết lập khung lý thuyết hoặc Ma trận thế giới/Nhân vật 3 chiều.
2. **`/draft [yêu cầu] [--type ...]`**:  
   ➔ **Giai đoạn 2:** Đồng sáng tác bản thảo chuẩn Anti-AI-bias theo đúng cấu trúc đặc thù của thể loại.
3. **`/critique [bản thảo] [--type ...]`**:  
   ➔ **Giai đoạn 3:** Chấm điểm Barem chuyên biệt, soi lỗi ngụy biện logic, kiểm tra liên kết và phát hiện lỗ hổng cốt truyện.
4. **`/humanize [bản thảo] [--type ...]`**:  
   ➔ **Giai đoạn 4:** Xóa bỏ lối danh từ hóa sáo rỗng, bơm nhịp điệu Burstiness và thuần Việt hóa văn phong.
5. **`/audit [bản thảo] [--type ...]`**:  
   ➔ **Giai đoạn 5:** Giám định pháp y AI lần cuối, cam kết độ nguyên bản và xuất báo cáo nghiệm thu xuất bản.
