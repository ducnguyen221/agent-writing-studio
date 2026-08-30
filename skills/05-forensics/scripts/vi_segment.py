#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vi_segment.py — tách câu tiếng Việt an toàn với viết tắt học thuật.

Dùng chung cho extract.py và counters.py. Không tách nhầm ở:
  PGS. TS. ThS. GS. TSKH.        học hàm học vị
  et al.  và cs.                  trích dẫn nhiều tác giả
  TP. Q. P. H.                    địa danh
  tr. NXB. Nxb. v.v. vd. tt.      trích dẫn / viết tắt
  1.1.  2.3.4.                    số thứ tự mục
  3.14  1.500.000                 số thập phân / phân cách nghìn

Cách làm: che các mẫu trên bằng ký tự thay thế riêng (U+E000, vùng Private Use),
tách câu, rồi khôi phục. Offset được giữ nguyên vì thay thế là 1-1 theo ký tự.

KHÔNG BỎ CÂU NÀO. Bản trước có ngưỡng `min_chars=15`: câu ngắn hơn 15 ký tự bị loại im lặng. Ca
`.work/cot-b-ai-baitap` (cổng Phase 5) cho thấy đó là lỗi tính đúng chứ không phải phép lọc nhiễu —
hai câu hỏi tu từ mở đoạn ("Cấm thì sao?", 12 ký tự) biến mất khỏi `sentences.json`, nên bản tự khai
`machine_written_spans[]` chỉ phủ 45/47 câu mà vẫn "hợp lệ" theo schema; và chính hai câu đó lại là
một tật máy (docs/results/self-audit-cot-B.md §5 mục 2). Nay mọi câu đều được giữ; câu ngắn chỉ được
GẮN CỜ `short: True` để người đọc tự quyết, không bị loại khỏi phép đo.
"""
import re

DOT = ""  # placeholder 1 ký tự cho dấu chấm KHÔNG kết câu

ABBREV = [
    "PGS", "GS", "TS", "TSKH", "ThS", "Th.S", "BS", "KS", "CN", "NCS",
    "TP", "Tp", "Q", "P", "H", "X", "TX", "TT",
    "tr", "Tr", "NXB", "Nxb", "vd", "VD", "v.v", "vv", "St", "Mr", "Mrs",
    "ĐH", "CĐ", "THPT", "THCS", "No", "no",
    # Trích dẫn học thuật: "Bastani et al. (2025) cho thấy…" là MỘT câu.
    # Ca .work/3c: thiếu mục này làm vỡ câu thành mảnh ", 2015; OECD, 2023; ...)."
    "et al", "và cs",
]

_ABBREV_RX = re.compile(r"\b(" + "|".join(re.escape(a) for a in ABBREV) + r")\.", re.UNICODE)
_DECIMAL_RX = re.compile(r"(?<=\d)\.(?=\d)")
_INITIAL_RX = re.compile(r"\b([A-ZĐÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĂĨŨƠƯ])\.(?=\s*[A-ZĐ])")
# Che TOÀN BỘ dấu chấm bên trong các token này (kể cả dấu chấm cuối):
#   v.v.          — "vân vân"
#   1.1.  2.3.4.  — số thứ tự mục
_ALLDOTS_RX = re.compile(r"\bv\.v\.?|\b\d+(?:\.\d+)+\.?", re.IGNORECASE)
_ORTHOGRAPHIC_SYLLABLE_RX = re.compile(r"[0-9A-Za-zÀ-ỹĐđ]+", re.UNICODE)


def count_orthographic_syllables(text: str) -> int:
    """Đếm đơn vị chữ/số, không tính token chỉ chứa dấu câu hoặc ký tự ẩn."""
    return len(_ORTHOGRAPHIC_SYLLABLE_RX.findall(text))


def _mask_all_dots(m):
    return m.group(0).replace(".", DOT)


def _mask(text: str) -> str:
    text = _ALLDOTS_RX.sub(_mask_all_dots, text)
    text = _DECIMAL_RX.sub(DOT, text)
    text = _ABBREV_RX.sub(lambda m: m.group(1) + DOT, text)
    text = _INITIAL_RX.sub(lambda m: m.group(1) + DOT, text)
    return text


SHORT_SENTENCE_CHARS = 15


def split_sentences(text: str, short_chars: int = SHORT_SENTENCE_CHARS):
    """Trả list dict {start, end, text, short} với offset TÍNH TRÊN VĂN BẢN GỐC.

    Phủ 100% văn bản: nối `text` của mọi câu lại thì được đúng văn bản gốc sau khi bỏ khoảng trắng.
    `short` là CỜ, không phải bộ lọc — câu ngắn hơn `short_chars` ký tự vẫn có mặt và vẫn có id.
    """
    masked = _mask(text)
    assert len(masked) == len(text), "mask phải giữ nguyên độ dài để offset còn đúng"
    out = []
    for m in re.finditer(r"[^.!?\n]+[.!?]*", masked):
        a, b = m.start(), m.end()
        raw = text[a:b].strip()
        if not raw:
            continue
        lead = len(text[a:b]) - len(text[a:b].lstrip())
        out.append({"start": a + lead, "end": a + lead + len(raw), "text": raw,
                    "short": len(raw) < short_chars})
    return out


if __name__ == "__main__":
    demo = ("PGS. TS. Nguyễn Văn A công tác tại TP. Hồ Chí Minh. "
            "Bastani et al. (2025) cho thấy điều ngược lại. "
            "Xem tr. 45, NXB. Chính trị Quốc gia, v.v. "
            "Mục 1.1. trình bày kết quả; tỷ lệ đạt 3.14% trong năm 2025. "
            "Vì sao? Đây là câu cuối cùng!")
    for s in split_sentences(demo):
        mark = " [short]" if s["short"] else ""
        print(f"[{s['start']:3d}-{s['end']:3d}]{mark} {s['text']}")
