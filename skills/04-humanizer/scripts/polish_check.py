#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
polish_check.py — CỔNG 0-TOKEN cho trục 4. Không gọi mô hình, không sửa văn bản.

Ý tưởng cổng-khi-lưu lấy từ `sloptrim` (Apache-2.0, reference-only, xem
`vendor-notes/sloptrim/`). Không chép một dòng mã nào; ở đây chỉ có phép so trước/sau.

Script này ĐO và CHẶN. Nó không bao giờ nói bản nào hay hơn:

  1. Chạy `analyse()` của skills/05-forensics/scripts/counters.py trên bản TRƯỚC và bản SAU,
     ghi vào `counters_before` / `counters_after` của polish.diff.json.
  2. FAIL-CLOSED nếu `facts_added` hoặc `facts_removed` khác rỗng. Biên tập không được thêm
     hay bớt sự kiện, tên, số, ngày, trích dẫn.
  3. Cảnh báo khi CV độ dài câu tăng bất thường — dấu hiệu bơm burstiness giả (chèn câu ngắn
     ngẫu nhiên cho "tự nhiên hơn").
  4. So tập token SỐ và tập TÊN VIẾT HOA của bản sau với bản trước. Token chỉ có ở bản sau =
     fact nghe hợp lý nhưng không có nguồn — thứ mà `facts_added` rỗng KHÔNG bắt được, vì người
     điền `facts_added` chính là người vừa thêm nó. Cảnh báo kèm liệt kê, mã thoát 1.
  5. TRƯỚC KHI in cột `NOMINAL` / `TEMPLATES`, đọc `genre_baseline` trong
     shared/rules/vi-ai-tells.json và mục §5 của hồ sơ thể loại. Ở thể loại có baseline, con số
     vẫn được in nhưng kèm nhãn "baseline thể loại" và KHÔNG được coi là chỗ phải sửa.
  6. Đòi PROVENANCE ĐI THEO BẢN GIAO: cạnh `--after` phải có sidecar `<tên bản giao>.provenance.json`
     (hoặc footer HTML-comment ngay trong bản giao, nếu người dùng chọn cách đó). Thiếu là cảnh báo,
     mã thoát 1. Lý do ở docs/results/self-audit-cot-B.md mục 4: sau trục 4, văn bản không mang một
     dấu nào cho biết nó đã qua biên tập máy — ranh giới đạo đức chỉ quan sát được từ sidecar, mà
     sidecar thì ở lại trong thư mục ca còn bản giao thì đi.

Cách chạy:

    python polish_check.py --before draft.md --after polished.md --genre research \
        --diff .work/case/polish.diff.json

Mã thoát: 0 = qua · 1 = có cảnh báo, cần người xem · 2 = FAIL-CLOSED, không được nhận bản sửa.
"""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COUNTERS_PATH = ROOT / "skills/05-forensics/scripts/counters.py"
TELLS_PATH = ROOT / "shared/rules/vi-ai-tells.json"
GENRES_DIR = ROOT / "shared/genres"

EXIT_OK, EXIT_WARN, EXIT_FAIL = 0, 1, 2

# Ánh xạ họ tell -> cột counter mà nó nói về. Nguồn: trường `note` của T09 và T13 trong
# vi-ai-tells.json ("Gộp với TEMPLATES / NOMINAL sẵn có trong counters.py") và bảng plan §1.1
# (pattern 6 và 10 khai genre_baseline). counters.py KHÔNG biết genre_baseline; đây là chỗ nối.
COUNTER_BY_TELL = {
    "T09": ("TEMPLATES",),
    "T10": ("TEMPLATES",),
    "T13": ("NOMINAL",),
    # Hai họ thêm sau cổng Phase 5; cả hai có khuôn đếm được trong counters.TEMPLATES.
    "T37": ("TEMPLATES",),
    "T38": ("TEMPLATES",),
}

# Hai nguồn khai baseline KHÔNG trùng nhau và cả hai đều phải được đọc:
#   · vi-ai-tells.json khai theo slug thể loại VN (`bao-cao-thuc-tap`, `chinh-luan`…);
#   · §5 của hồ sơ thể loại khai bằng văn xuôi (`research.md` nói danh từ hoá là bình thường,
#     nhưng không có mục tell nào liệt kê slug `research`).
# Bỏ nguồn thứ hai thì bài nghiên cứu bị báo NOMINAL như một chỗ phải sửa — đúng kiểu sửa oan
# mà references/03-chong-sua-oan.md mục 5 cấm.
#
# Một cột chỉ được dán nhãn baseline khi §5 khai ĐÚNG THỨ CỘT ĐÓ ĐO. Hai đường:
#   · tường minh — tín hiệu nêu đích danh mã tell (`(T10)`) hoặc tên cột (`TEMPLATES`);
#   · theo hiện tượng — tín hiệu gọi tên đúng hiện tượng cột đó đếm, theo danh sách hẹp dưới đây.
#
# BỎ "cụm quy ước" và "cụm chuyển đoạn" khỏi TEMPLATES (cổng Phase 5, ca `.work/cot-b-ai-baitap`):
# cột TEMPLATES đếm KHUÔN CÂU GHÉP ĐÔI ("không chỉ X mà còn", "một mặt… mặt khác"), nó không đếm cụm
# chuyển đoạn. `essay.md` §5 khai "cụm chuyển đoạn quy ước ở mật độ vừa phải" là bình thường — đúng,
# nhưng đó là lời khai về một hiện tượng KHÁC, nên dán nhãn "baseline thể loại" lên cột TEMPLATES của
# bài luận là nói sai: nó bảo người sửa bỏ qua đúng cột đang đo thứ essay.md §2 CẤM sinh ra.
SIGNAL_KEYWORDS = {
    "NOMINAL": ("danh từ hoá", "danh từ hóa", "bị động"),
    "TEMPLATES": ("khuôn", "lặp lại"),
    "GLOSS": ("thuật ngữ", "tiếng anh"),
}
# Đường tường minh: tên cột viết thẳng trong tín hiệu §5.
COLUMN_NAMES = tuple(SIGNAL_KEYWORDS)
_TELL_IN_SIGNAL_RX = re.compile(r"\bT\d{2}\b")

# Ngưỡng nghi "bơm burstiness giả" — chèn câu ngắn rỗng cho biểu đồ độ dài câu trông người hơn.
# Hai tín hiệu độc lập, chỉ cần một cái vượt ngưỡng là cảnh báo (KHÔNG phải điều kiện AND: trên ca
# .work/3c, chèn một câu rỗng sau mỗi ba câu đẩy CV 0,763 -> 0,864, tức +0,101 tuyệt đối nhưng chỉ
# +13% tương đối — điều kiện AND sẽ bỏ lọt đúng ca mà nó sinh ra để bắt).
CV_ABS_JUMP = 0.10
CV_REL_JUMP = 0.25
SHORT_SENTENCE_SYLLABLES = 8      # dưới ngưỡng này coi là câu ngắn
SHORT_RATIO_JUMP = 0.05           # tỷ lệ câu ngắn tăng thêm bao nhiêu thì đáng nói


def load_counters():
    spec = importlib.util.spec_from_file_location("forensics_counters", COUNTERS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Không nạp được counters.py bắt buộc: {COUNTERS_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------- baseline thể loại ----------

def baseline_counters(genre, tells_path=TELLS_PATH):
    """{tên cột counter: [id tell khai baseline]} cho thể loại này.

    Đọc genre_baseline của vi-ai-tells.json. Thể loại rỗng hoặc không khớp mục nào -> {}.
    """
    if not genre:
        return {}
    data = json.loads(Path(tells_path).read_text(encoding="utf-8"))
    result = {}
    for entry in data.get("entries", []):
        columns = COUNTER_BY_TELL.get(entry.get("id"))
        if not columns:
            continue
        if genre in (entry.get("genre_baseline") or []):
            for column in columns:
                result.setdefault(column, []).append(entry["id"])
    return result


def baseline_from_signals(normal_signals):
    """{cột counter: [tín hiệu §5 khai nó là bình thường]}. `None` (không có hồ sơ) -> {}.

    Tín hiệu vào được một cột theo hai đường, đường nào cũng đòi §5 nói về ĐÚNG cột đó:

    1. **Tường minh** — tín hiệu nêu mã tell có cột tương ứng (`(T13)` -> NOMINAL) hoặc viết thẳng
       tên cột. Đây là đường nên dùng; nó không phụ thuộc câu chữ.
    2. **Theo hiện tượng** — tín hiệu gọi tên đúng hiện tượng cột đó đếm (`SIGNAL_KEYWORDS`). Đây là
       đường tạm: nó dò từ khoá trong văn xuôi, nên vừa bỏ sót vừa dán nhầm. Chỗ nó đã dán nhầm là
       `essay` (xem chú thích ở `SIGNAL_KEYWORDS`). Bỏ hẳn đường này thì §5 thành nguồn chết cho các
       hồ sơ không ghi mã tell, nên nó ở lại cho tới khi §5 khai cột tường minh — việc thuộc
       `shared/genres/`, không thuộc script này.
    """
    result = {}
    for signal in normal_signals or []:
        lowered = signal.lower()
        columns = set()
        for tell_id in _TELL_IN_SIGNAL_RX.findall(signal):
            columns.update(COUNTER_BY_TELL.get(tell_id, ()))
        for column in COLUMN_NAMES:
            if column in signal:
                columns.add(column)
        for column, keywords in SIGNAL_KEYWORDS.items():
            if any(keyword in lowered for keyword in keywords):
                columns.add(column)
        for column in columns:
            result.setdefault(column, []).append(signal)
    return result


def genre_normal_signals(genre, genres_dir=GENRES_DIR):
    """normal_signals khai ở §5 của hồ sơ thể loại. Không có hồ sơ -> None (khác với [])."""
    if not genre:
        return None
    path = Path(genres_dir) / f"{genre}.md"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    heads = list(re.finditer(r"(?m)^##\s+(\d)\.\s", text))
    for index, head in enumerate(heads):
        if head.group(1) != "5":
            continue
        end = heads[index + 1].start() if index + 1 < len(heads) else len(text)
        block = re.search(r"(?ms)^```yaml\r?\n(.*?)^```", text[head.end(): end])
        if not block:
            return None
        signals = re.search(
            r"(?ms)^genre_baseline:\s*\n\s+normal_signals:\s*\n((?:\s+-\s.*\n?)+)", block.group(1)
        )
        if not signals:
            return []
        return [
            re.sub(r'^\s*-\s*["\']?|["\']?\s*$', "", line)
            for line in signals.group(1).splitlines()
            if line.strip()
        ]
    return None


# ---------- đọc số từ kết quả counters ----------

def _nominal_per_1000(counters):
    return (counters.get("G2_tu_vung", {}).get("nominalisation", {}) or {}).get(
        "per_1000_syllables"
    )


def _template_total(counters):
    repeats = counters.get("G1_khuon_hinh_thuc", {}).get("template_repeats", {}) or {}
    return sum(item.get("count", 0) for item in repeats.values())


def _sentence_cv(counters):
    return (counters.get("G1_khuon_hinh_thuc", {}).get("sentence_len", {}) or {}).get("cv")


def counter_rows(before, after, baseline, signal_baseline=None):
    """Bảng đối chiếu. Mỗi dòng: cột, trước, sau, có phải baseline thể loại không.

    `baseline` từ vi-ai-tells.json, `signal_baseline` từ §5 hồ sơ thể loại. Một cột chỉ cần
    MỘT trong hai nguồn khai là đủ để mang nhãn baseline.
    """
    rows = [
        {
            "column": "NOMINAL",
            "label": "danh từ hoá / 1000 âm tiết",
            "before": _nominal_per_1000(before),
            "after": _nominal_per_1000(after),
        },
        {
            "column": "TEMPLATES",
            "label": "tổng lượt khuôn câu",
            "before": _template_total(before),
            "after": _template_total(after),
        },
        {
            "column": "SENTENCE_CV",
            "label": "CV độ dài câu",
            "before": _sentence_cv(before),
            "after": _sentence_cv(after),
        },
        {
            "column": "GLOSS",
            "label": "gloss tiếng Anh / 1000 âm tiết",
            "before": (before.get("G2_tu_vung", {}).get("english_gloss", {}) or {}).get(
                "per_1000_syllables"
            ),
            "after": (after.get("G2_tu_vung", {}).get("english_gloss", {}) or {}).get(
                "per_1000_syllables"
            ),
        },
    ]
    signal_baseline = signal_baseline or {}
    for row in rows:
        tells = baseline.get(row["column"]) or []
        signals = signal_baseline.get(row["column"]) or []
        row["baseline_tells"] = tells
        row["baseline_signals"] = signals
        row["baseline_the_loai"] = bool(tells or signals)
        sources = []
        if tells:
            sources.append("vi-ai-tells: " + ", ".join(tells))
        if signals:
            sources.append("§5 hồ sơ thể loại")
        row["baseline_source"] = sources
    return rows


# ---------- token số và tên riêng ----------
# Nguồn: cổng Phase 3, Fable 30/08 — rủi ro số 4. `facts_added` rỗng KHÔNG chứng minh được là
# không có fact mới: trường ấy do chính người vừa sửa khai. Một con số hay một cái tên "nghe hợp
# lý" lọt vào bản sau thì không ai đếm. Phép so tập token dưới đây là 0-token, không gọi mô hình,
# và cố ý CHỈ CẢNH BÁO: nó không biết "TP. Hồ Chí Minh" là một tên hay ba token.

NUMBER_RX = re.compile(r"\d+(?:[.,/]\d+)*%?")
# Từ theo nghĩa Unicode: giữ nguyên dấu tiếng Việt, không nuốt chữ số.
WORD_RX = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*", re.UNICODE)
# Ký tự dẫn đầu dòng của markdown và dấu mở ngoặc: đứng ngay sau chúng vẫn là đầu câu.
_LEAD_CHARS = " \t#*->_\"'“”‘’()[]|•·"
_SENTENCE_END = ".!?:;…"


def _normalise_number(token):
    """`1.000`, `1,000`, `1000` về cùng một dạng; giữ `/` của ngày tháng và giữ `%`.

    Đổi cách viết dấu phân cách là việc biên tập hợp lệ, không phải thêm số liệu.
    """
    token = token.rstrip(".,")
    percent = token.endswith("%")
    core = token.rstrip("%").replace(".", "").replace(",", "")
    return core + ("%" if percent else "")


def number_tokens(text):
    """{dạng chuẩn hoá: dạng nguyên văn gặp đầu tiên}."""
    found = {}
    for raw in NUMBER_RX.findall(text):
        key = _normalise_number(raw)
        if key:
            found.setdefault(key, raw)
    return found


def _is_sentence_initial(text, start):
    prefix = text[:start].rstrip(_LEAD_CHARS)
    if not prefix:
        return True
    return prefix[-1] == "\n" or prefix[-1] in _SENTENCE_END


def name_tokens(text, skip_sentence_initial=True):
    """Tập từ viết hoa được coi là TÊN RIÊNG.

    Tiếng Việt viết hoa đầu câu, nên từ đứng đầu câu KHÔNG được tính là tên: tính vào thì mỗi câu
    mới tách ra lại thành một "tên mới". Viết tắt toàn chữ hoa (OECD, THPT) tính ở mọi vị trí.

    Bản TRƯỚC gọi với `skip_sentence_initial=False`: một cái tên đã có ở đâu đó trong bản trước
    thì không phải tên mới, kể cả khi ở đó nó đứng đầu câu.
    """
    found = set()
    for match in WORD_RX.finditer(text):
        token = match.group(0)
        if not token[:1].isupper():
            continue
        if len(token) >= 2 and token.isupper():
            found.add(token)
            continue
        if skip_sentence_initial and _is_sentence_initial(text, match.start()):
            continue
        found.add(token)
    return found


def new_tokens(text_before, text_after):
    """{'numbers': [...], 'names': [...]} — thứ chỉ có ở bản sau."""
    before_numbers = number_tokens(text_before)
    after_numbers = number_tokens(text_after)
    numbers = sorted(after_numbers[key] for key in set(after_numbers) - set(before_numbers))
    names = sorted(name_tokens(text_after, True) - name_tokens(text_before, False))
    return {"numbers": numbers, "names": names}


def check_new_tokens(text_before, text_after):
    """Cảnh báo (không fail-closed) khi bản sau mọc ra số hoặc tên không có ở bản trước."""
    found = new_tokens(text_before, text_after)
    warnings = []
    if found["numbers"]:
        warnings.append(
            "Bản sau có {} token SỐ không có ở bản trước: {}. Biên tập không sinh ra số liệu; "
            "mỗi token phải chỉ được chỗ tương ứng trong bản trước, chỉ không được thì đó là "
            "fact thêm — đưa vào `facts_added` và dừng.".format(
                len(found["numbers"]), ", ".join(found["numbers"])
            )
        )
    if found["names"]:
        warnings.append(
            "Bản sau có {} TÊN VIẾT HOA không có ở bản trước: {}. Kiểm từng cái: tên người, tên "
            "tổ chức, tên văn bản mới xuất hiện là fact thêm. Chỉ đổi cách trình bày thì ghi lý "
            "do vào `reason` của nhát sửa tương ứng.".format(
                len(found["names"]), ", ".join(found["names"])
            )
        )
    return warnings


# ---------- provenance đi theo bản giao ----------
# Nguồn: docs/results/self-audit-cot-B.md mục 4. Người chấm mù đọc `polished.md` không thấy gì cho
# biết bài đã qua trục 4; `metadata.stylometric_polish: true` nằm trong polish.diff.json, mà file đó
# không đi cùng bản giao. Sidecar dưới đây là bản tự khai TỐI THIỂU đi theo file văn bản.

PROVENANCE_SUFFIX = ".provenance.json"
PROVENANCE_REQUIRED = ("schema_version", "genre", "origin", "model", "stylometric_polish",
                       "draft_meta_sha256")
_FOOTER_RX = re.compile(r"<!--\s*provenance\s*:?\s*(\{.*?\})\s*-->", re.S)


def provenance_path_for(after_path):
    """polished.md -> polished.provenance.json (cạnh chính nó, cùng tên gốc)."""
    after_path = Path(after_path)
    return after_path.with_suffix("").with_name(after_path.stem + PROVENANCE_SUFFIX)


def load_provenance(after_path, text_after, explicit=None):
    """Trả (dữ liệu, nguồn). Nguồn: 'sidecar' · 'footer' · None khi không có."""
    path = Path(explicit) if explicit else provenance_path_for(after_path)
    if path.is_file():
        try:
            return json.loads(path.read_text(encoding="utf-8")), "sidecar"
        except json.JSONDecodeError as error:
            raise ValueError(f"Sidecar provenance không phải JSON hợp lệ: {path}") from error
    match = _FOOTER_RX.search(text_after)
    if match:
        try:
            return json.loads(match.group(1)), "footer"
        except json.JSONDecodeError:
            return {}, "footer"
    return None, None


def check_provenance(after_path, text_after, explicit=None):
    """Cảnh báo (mã thoát 1) khi bản giao đi ra mà không mang bản tự khai theo."""
    data, source = load_provenance(after_path, text_after, explicit)
    if data is None:
        return [
            "Không có bản tự khai đi kèm bản giao. Trục 4 phải xuất `{}` cạnh bản đã sửa (hoặc "
            "footer HTML-comment trong chính file, nếu người dùng chọn). Không có nó thì người "
            "nhận cầm một văn bản đã qua biên tập máy mà không có cách nào biết — ranh giới đạo "
            "đức của trục 4 chỉ còn là lời hứa.".format(provenance_path_for(after_path).name)
        ]
    warnings = []
    if not data:
        return ["Footer provenance có mặt nhưng không đọc được JSON bên trong."]
    missing = [key for key in PROVENANCE_REQUIRED if key not in data]
    if missing:
        warnings.append(
            f"Bản tự khai ({source}) thiếu trường bắt buộc: {', '.join(missing)}. "
            "Xem shared/schemas/provenance.schema.json."
        )
    if data.get("stylometric_polish") is not True:
        warnings.append(
            f"Bản tự khai ({source}) không khai `stylometric_polish: true` — bản đã qua trục 4 "
            "phải tự khai điều đó."
        )
    origin = data.get("origin") or {}
    if origin.get("undeclared_sentences"):
        warnings.append(
            "Bản tự khai ghi {} câu CHƯA KHAI: tỷ lệ phần trăm ở trên lạc quan hơn văn bản. "
            "Chạy shared/scripts/check_spans.py rồi khai lại trước khi giao."
            .format(origin["undeclared_sentences"])
        )
    return warnings


# ---------- kiểm tra ----------

def check_facts(diff):
    """Fail-closed. Trả list lỗi; rỗng nghĩa là qua."""
    problems = []
    for field in ("facts_added", "facts_removed"):
        values = diff.get(field)
        if values is None:
            problems.append(f"polish.diff.json thiếu trường bắt buộc `{field}`")
        elif values:
            problems.append(
                f"`{field}` khác rỗng ({len(values)} mục): {values[:3]} — "
                "dừng, trả bản gốc, báo người dùng"
            )
    return problems


def short_sentence_ratio(module, text):
    """Tỷ lệ câu dưới SHORT_SENTENCE_SYLLABLES âm tiết. None khi văn bản không có câu nào."""
    sentences = module.sentences(text)
    if not sentences:
        return None
    short = sum(
        1
        for sentence in sentences
        if module.count_syllables(sentence["text"]) < SHORT_SENTENCE_SYLLABLES
    )
    return round(short / len(sentences), 4)


def check_burstiness(before, after, short_before=None, short_after=None):
    """Cảnh báo khi phân bố độ dài câu bị nống lên một cách nhân tạo.

    Đây là cảnh báo, không phải fail: tách một câu dài bị chôn chủ thể là phép sửa hợp lệ và
    cũng làm CV nhích lên. Người đọc diff quyết định, script chỉ chỉ chỗ.
    """
    warnings = []
    cv_before, cv_after = _sentence_cv(before), _sentence_cv(after)
    if cv_before not in (None, 0) and cv_after is not None:
        jump = cv_after - cv_before
        if jump >= CV_ABS_JUMP or jump / cv_before >= CV_REL_JUMP:
            warnings.append(
                f"CV độ dài câu tăng {cv_before} -> {cv_after} (+{round(jump, 3)}). "
                "Dấu hiệu bơm burstiness giả: chèn câu ngắn cho biểu đồ độ dài câu trông tự nhiên "
                "hơn. Kiểm từng câu mới thêm; câu không mang thông tin thì hoàn tác."
            )
    if short_before is not None and short_after is not None:
        jump = short_after - short_before
        if jump >= SHORT_RATIO_JUMP:
            warnings.append(
                f"Tỷ lệ câu dưới {SHORT_SENTENCE_SYLLABLES} âm tiết tăng {short_before} -> "
                f"{short_after}. Câu ngắn thêm phải mang thông tin hoặc làm nhịp có chủ ý; "
                "câu ngắn rỗng là burstiness giả."
            )
    return warnings


def merge_warnings(existing, produced):
    """Gộp cảnh báo cũ với cảnh báo vừa đo, KHÔNG làm rơi phần tử dạng object.

    `warnings[]` của polish.schema.json nhận cả chuỗi lẫn object `{message, route_to, …}`. Object là
    việc trục 4 CỐ Ý KHÔNG LÀM và chuyển cho trục 2 vòng 2 — ví dụ must_fix đòi hạ mức khẳng định.
    Bản trước gộp bằng `sorted(set(...))`, mà object thì không hash được và cũng không so được thứ
    tự: gộp kiểu đó vừa vỡ vừa xoá mất đúng thứ phải giữ lại.
    """
    objects, strings = [], []
    for item in list(existing or []) + list(produced or []):
        if isinstance(item, str):
            if item not in strings:
                strings.append(item)
        else:
            if item not in objects:
                objects.append(item)
    return objects + sorted(strings)


def check_flags(after):
    """Cờ của counters.py trên bản sau, ví dụ injection_attempt hoặc thiếu bằng chứng."""
    return [f"counters.py gắn cờ trên bản sau: {flag}" for flag in after.get("flags", [])]


def check_metadata(diff):
    warnings = []
    metadata = diff.get("metadata") or {}
    if metadata.get("stylometric_polish") is not True:
        warnings.append(
            "metadata.stylometric_polish phải là true — bản đã qua trục 4 phải tự khai điều đó"
        )
    if metadata.get("forensics_score_seen") not in (False, None):
        warnings.append(
            "metadata.forensics_score_seen khác false — trục 4 không được xem điểm trục 5 "
            "của chính bài đang sửa"
        )
    if not (diff.get("source_declared") or {}).get("how"):
        warnings.append(
            "source_declared.how trống — trục 4 chỉ chạy khi có draft.meta.json hoặc người dùng khai"
        )
    return warnings


# ---------- trình bày ----------

def render(rows, normal_signals, warnings, problems):
    lines = ["== polish_check · cổng 0-token, chỉ đo ==", ""]
    lines.append(f"{'cột':<14}{'trước':>12}{'sau':>12}   ghi chú")
    for row in rows:
        note = ""
        if row["baseline_the_loai"]:
            note = (
                f"baseline thể loại [{' · '.join(row['baseline_source'])}] "
                "— KHÔNG phải chỗ phải sửa"
            )
        lines.append(
            f"{row['column']:<14}{str(row['before']):>12}{str(row['after']):>12}   {note}"
        )
    lines.append("")
    if normal_signals is None:
        lines.append("§5 hồ sơ thể loại: KHÔNG đọc được — không có file, mọi cột đọc không có baseline")
    else:
        lines.append(f"§5 hồ sơ thể loại khai {len(normal_signals)} tín hiệu bình thường:")
        for signal in normal_signals:
            lines.append(f"  · {signal}")
    lines.append("")
    for warning in warnings:
        lines.append(f"[CẢNH BÁO] {warning}")
    for problem in problems:
        lines.append(f"[FAIL-CLOSED] {problem}")
    if not warnings and not problems:
        lines.append("Không có cảnh báo. Số ở trên là mô tả, không phải danh sách việc phải làm.")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Cổng 0-token trước/sau cho trục 4")
    parser.add_argument("--before", required=True, help="bản gốc (.md hoặc .txt)")
    parser.add_argument("--after", required=True, help="bản đã sửa")
    parser.add_argument("--genre", default="", help="slug hồ sơ thể loại, ví dụ research")
    parser.add_argument("--diff", help="polish.diff.json; có thì kiểm facts và ghi counters vào")
    parser.add_argument(
        "--provenance",
        help="bản tự khai đi kèm bản giao; mặc định tìm <tên bản giao>.provenance.json cạnh --after",
    )
    parser.add_argument("--out", help="ghi bản diff đã bổ sung counters ra đây (mặc định: đè --diff)")
    args = parser.parse_args(argv)

    counters = load_counters()
    text_before = Path(args.before).read_text(encoding="utf-8")
    text_after = Path(args.after).read_text(encoding="utf-8")
    before = counters.analyse(text_before)
    after = counters.analyse(text_after)

    # Đọc CẢ HAI nguồn baseline TRƯỚC khi in bất kỳ cột counter nào.
    baseline = baseline_counters(args.genre)
    normal_signals = genre_normal_signals(args.genre)
    rows = counter_rows(before, after, baseline, baseline_from_signals(normal_signals))

    warnings = (
        check_burstiness(
            before,
            after,
            short_sentence_ratio(counters, text_before),
            short_sentence_ratio(counters, text_after),
        )
        + check_new_tokens(text_before, text_after)
        + check_flags(after)
        + check_provenance(args.after, text_after, args.provenance)
    )
    problems = []

    diff = None
    if args.diff:
        diff_path = Path(args.diff)
        if not diff_path.is_file():
            raise FileNotFoundError(f"Không tìm thấy polish.diff.json: {diff_path}")
        diff = json.loads(diff_path.read_text(encoding="utf-8"))
        problems += check_facts(diff)
        warnings += check_metadata(diff)
        diff["counters_before"] = before
        diff["counters_after"] = after
        diff["warnings"] = merge_warnings(diff.get("warnings"), warnings)
        out_path = Path(args.out) if args.out else diff_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(diff, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
        )

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(render(rows, normal_signals, warnings, problems))
    if args.diff:
        print(f"\n-> counters_before/after đã ghi vào {args.out or args.diff}")

    if problems:
        return EXIT_FAIL
    return EXIT_WARN if warnings else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
