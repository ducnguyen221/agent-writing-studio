#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
profile_build.py — dựng writer profile từ bài chính chủ. KHÔNG gọi mô hình.

    python profile_build.py --writer writer-a
    python profile_build.py --writer writer-a --samples-dir /duong/dan/khac --dry-run
    python profile_build.py --writer writer-a --samples-dir <kho>/bai-mau --out <kho>/profile.yaml --keep-manual

Đọc mọi file `.txt` / `.md` / `.docx` trong `<writers>/<slug>/samples/`, đo từng bài
bằng `vi_segment.py` + `counters.py` của trục 5, rồi lấy **trung vị** làm vân tay. Xuất
`<writers>/<slug>/profile.yaml` theo `shared/writers/writer.schema.json`.

`<writers>` = `$WRITING_STUDIO_DATA/writers/` nếu biến môi trường đó có, ngược lại
`shared/writers/` trong repo. `--samples-dir` / `--out` tường minh luôn thắng cả hai — và đó là
cách dùng khi hồ sơ giọng, bài mẫu nằm trong kho tri thức cá nhân (`OPCOS_BRAIN_PATH`).

Bài mẫu trong kho tri thức thường có frontmatter YAML: khối `---` ĐẦU file `.md`/`.txt` bị bỏ
trước khi đo (kèm các dòng trống ngay sau nó). Vạch `---` giữa thân bài là câu chữ của tác giả,
không bị đụng.

`--keep-manual [PATH]` dựng lại mà không mất phần người đã điền tay: nạp hồ sơ cũ (mặc định =
`--out`) rồi giữ `voice_notes`, `provenance.ownership_confirmed_by`, `known_typos`, các
`pet_templates` có id ngoài `counters.TEMPLATES`, hợp `necessary_english_terms` và các dòng
`limitations` viết tay. Chỉ in số lượng đã giữ, không in nội dung.

Ba luật của script này, đọc trước khi sửa:

1. **Trung vị của từng bài, không phải số đo trên văn bản đã nối.** Nối bài lại rồi đo sẽ
   trộn mất khác biệt giữa các bài, và một bài dài sẽ nuốt mất giọng của các bài ngắn.
2. **Dưới 3 bài thì `status: draft`.** Hai bài không tách được thói quen của NGƯỜI ra khỏi
   đặc thù của BÀI. Hồ sơ draft không được dùng để hạ finding ở trục 5.
3. **Không in nội dung bài ra stdout, không ghi nội dung bài vào profile.** Bài mẫu là văn
   của người thật. Script chỉ in tên file, số đo và cảnh báo; `provenance.samples[]` chỉ
   giữ mã băm rút gọn. Trích dẫn ví dụ cho `pet_templates` phải bật tay bằng
   `--with-examples` và chỉ khi chủ hồ sơ đồng ý.

Mã thoát: 0 = dựng xong · 1 = dựng xong nhưng có cảnh báo (thiếu bài, thiếu tokenizer) ·
2 = không dựng được (không có bài nào đọc được).
"""
import argparse
import hashlib
import importlib.util
import os
import re
import statistics
import sys
from datetime import date
from pathlib import Path

TOOL_VERSION = "profile_build.py 1.1"

ROOT = Path(__file__).resolve().parents[2]
FORENSICS_SCRIPTS = ROOT / "skills/05-forensics/scripts"

# Đường mặc định trong repo. Chỉ dùng khi KHÔNG có station: người ngoài clone repo về vẫn chạy được.
REPO_WRITERS_DIR = ROOT / "shared/writers"
STATION_ENV = "WRITING_STUDIO_DATA"


def writers_dir() -> Path:
    """Thư mục hồ sơ người viết.

    Thứ tự: tham số CLI tường minh (xử lý ở `main`) > station `$WRITING_STUDIO_DATA/writers` >
    `shared/writers/` trong repo. Đọc env tại LÚC GỌI chứ không phải lúc nạp module, để test
    monkeypatch được và để một tiến trình đổi env giữa chừng vẫn đúng.
    """
    station = (os.environ.get(STATION_ENV) or "").strip()
    if station:
        return Path(station) / "writers"
    return REPO_WRITERS_DIR

EXIT_OK, EXIT_WARN, EXIT_FAIL = 0, 1, 2

MIN_SAMPLES_FOR_READY = 3
# Khuôn tu từ chỉ vào pet_templates khi có mặt ở ÍT NHẤT 2 bài khác nhau. Một bài thì đó là
# thói quen của bài đó, không phải của người viết — và pet_templates được trục 5 dùng để HẠ
# finding, nên ngưỡng lỏng ở đây là báo-oan-ngược.
MIN_SAMPLES_FOR_PET_TEMPLATE = 2
MIN_SAMPLES_FOR_ENGLISH_TERM = 2

SUPPORTED_SUFFIXES = {".txt": "txt", ".md": "md", ".docx": "docx"}

# KIỂU BỎ DẤU. Chỉ đếm ba vần không nhập nhằng: oa, oe, uy.
#   kiểu CŨ  đặt dấu lên nguyên âm ĐẦU:  hòa · khỏe · thủy   -> chuỗi "òa" "ỏe" "ủy"
#   kiểu MỚI đặt dấu lên nguyên âm CHÍNH: hoà · khoẻ · thuỷ  -> chuỗi "oà" "oẻ" "uỷ"
# Hai điều kiện lọc, thiếu một là đếm sai gần hết văn bản tiếng Việt:
#   (a) chỉ tính ÂM TIẾT MỞ — vần phải kết thúc ngay tại đó. Âm tiết có phụ âm cuối
#       (toán, khoảng, hoạt, hoài, huyện) viết GIỐNG NHAU ở cả hai kiểu, không phải bằng chứng.
#   (b) loại trừ `qu`: trong "quý / quỳ / quỷ" chữ u thuộc phụ âm đầu `qu`, dấu luôn nằm
#       trên y ở cả hai kiểu.
_END = r"(?![0-9A-Za-zÀ-ỹĐđ])"
_TONE_OLD_RX = re.compile(
    rf"(?:[òóỏõọ]a|[òóỏõọ]e|(?<![qQ])[ùúủũụ]y){_END}",
    re.UNICODE,
)
_TONE_NEW_RX = re.compile(
    rf"(?:o[àáảãạ]|o[èéẻẽẹ]|(?<![qQ])u[ỳýỷỹỵ]){_END}",
    re.UNICODE,
)


def _load(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Không nạp được module bắt buộc: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


COUNTERS = _load("forensics_counters", FORENSICS_SCRIPTS / "counters.py")
EXTRACT = _load("forensics_extract", FORENSICS_SCRIPTS / "extract.py")


# ---------- đọc bài ----------
# Frontmatter YAML chỉ được nhận ở ĐẦU file. Bài Facebook dùng `---` làm vạch ngăn giữa các phần
# của thân bài; neo `\A` là thứ giữ cho vạch ấy không bị cắt nhầm.
_FRONT_MATTER_RX = re.compile(r"\A﻿?---[ \t]*\n.*?\n---[ \t]*\n", re.DOTALL)


def strip_front_matter(text):
    """Bỏ khối frontmatter đầu file và các dòng trống ngay sau nó. Không có thì trả nguyên."""
    match = _FRONT_MATTER_RX.match(text)
    if not match:
        return text
    return text[match.end():].lstrip("\n")


def read_sample(path):
    """Trả nguyên văn bài. .docx đi qua extract.from_docx của trục 5."""
    suffix = path.suffix.lower()
    if suffix == ".docx":
        text, _meta = EXTRACT.from_docx(path)
        return text
    return strip_front_matter(path.read_text(encoding="utf-8"))


def collect_samples(samples_dir):
    if not samples_dir.is_dir():
        return []
    return sorted(
        p for p in samples_dir.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_SUFFIXES
    )


# ---------- đo một bài ----------
def detect_tone_style(text):
    """Đếm kiểu bỏ dấu. Trả (nhãn, {'old': n, 'new': n})."""
    old_hits = len(_TONE_OLD_RX.findall(text))
    new_hits = len(_TONE_NEW_RX.findall(text))
    evidence = {"old": old_hits, "new": new_hits}
    total = old_hits + new_hits
    if total < 5:
        return "unknown", evidence
    if old_hits >= total * 0.8:
        return "old", evidence
    if new_hits >= total * 0.8:
        return "new", evidence
    return "mixed", evidence


def measure(text):
    """Số đo của MỘT bài. Không giữ lại nguyên văn ở giá trị trả về."""
    sents = COUNTERS.sentences(text)
    analysis = COUNTERS.analyse(text, sents=sents)
    sentence_len = analysis["G1_khuon_hinh_thuc"]["sentence_len"]
    tone_label, tone_evidence = detect_tone_style(text)
    english_terms = sorted({term.strip() for term in COUNTERS.find_gloss(text) if term.strip()})
    return {
        "chars": len(text),
        "sentences": analysis["size"]["sentences"],
        "syllables": analysis["size"]["syllables"],
        "tokenizer": analysis["size"]["tokenizer"],
        "sentence_len_mean": sentence_len["mean"],
        "sentence_len_cv": sentence_len["cv"],
        "gloss_per_1000": analysis["G2_tu_vung"]["english_gloss"]["per_1000_syllables"],
        "nominal_per_1000": analysis["G2_tu_vung"]["nominalisation"]["per_1000_syllables"],
        "templates": analysis["G1_khuon_hinh_thuc"]["template_repeats"],
        "english_terms": english_terms,
        "tone_label": tone_label,
        "tone_evidence": tone_evidence,
        "flags": list(analysis["flags"]),
    }


# ---------- gộp ----------
def median_of(values):
    kept = [v for v in values if isinstance(v, (int, float))]
    if not kept:
        return None
    return round(statistics.median(kept), 3)


def build_pet_templates(measurements, with_examples=False):
    """Khuôn có mặt ở >= 2 bài khác nhau."""
    seen, hits, example = {}, {}, {}
    for item in measurements:
        for name, data in item["templates"].items():
            seen[name] = seen.get(name, 0) + 1
            hits[name] = hits.get(name, 0) + data["count"]
            example.setdefault(name, (data.get("examples") or [""])[0])
    out = []
    for name in sorted(seen):
        if seen[name] < MIN_SAMPLES_FOR_PET_TEMPLATE or hits[name] < 2:
            continue
        entry = {"id": name, "seen_in_samples": seen[name], "total_hits": hits[name]}
        if with_examples and example[name]:
            entry["example"] = example[name][:120]
        out.append(entry)
    return out


def build_english_terms(measurements):
    counter = {}
    for item in measurements:
        for term in set(item["english_terms"]):
            counter[term] = counter.get(term, 0) + 1
    return sorted(term for term, n in counter.items() if n >= MIN_SAMPLES_FOR_ENGLISH_TERM)


def merge_tone(measurements):
    old = sum(item["tone_evidence"]["old"] for item in measurements)
    new = sum(item["tone_evidence"]["new"] for item in measurements)
    total = old + new
    if total < 5:
        label = "unknown"
    elif old >= total * 0.8:
        label = "old"
    elif new >= total * 0.8:
        label = "new"
    else:
        label = "mixed"
    return label, {"old": old, "new": new}


def build_profile(slug, paths, language="vi", genre=None, with_examples=False):
    """Trả (profile_dict, warnings)."""
    warnings = []
    measurements, samples = [], []
    for index, path in enumerate(paths, start=1):
        text = read_sample(path)
        if not text.strip():
            warnings.append(f"Bỏ qua bài rỗng: {path.name}")
            continue
        item = measure(text)
        measurements.append(item)
        samples.append({
            "id": f"s{index:02d}",
            "sha256_12": hashlib.sha256(text.encode("utf-8")).hexdigest()[:12],
            "chars": item["chars"],
            "sentences": item["sentences"],
            "syllables": item["syllables"],
            "format": SUPPORTED_SUFFIXES[path.suffix.lower()],
        })

    if not measurements:
        return None, warnings + ["Không có bài nào đọc được."]

    built_from = len(measurements)
    status = "ready" if built_from >= MIN_SAMPLES_FOR_READY else "draft"
    if status == "draft":
        warnings.append(
            f"Chỉ có {built_from} bài (cần >= {MIN_SAMPLES_FOR_READY}). "
            "Hồ sơ ở trạng thái draft: dùng để tham khảo, KHÔNG được dùng để hạ finding ở trục 5."
        )
    if any("tokenizer=syllable" in flag for item in measurements for flag in item["flags"]):
        warnings.append(
            "Chưa cài underthesea — mọi chỉ số từ vựng đo ở mức âm tiết, độ tin cậy thấp hơn."
        )

    tone_label, tone_evidence = merge_tone(measurements)
    means = [item["sentence_len_mean"] for item in measurements]

    limitations = [
        f"Dựng từ {built_from} bài; vân tay chỉ nói về thể loại và giai đoạn của chính các bài đó.",
        "known_typos để rỗng: script không có từ điển, đoán lỗi chính tả của người khác là báo oan.",
    ]
    if genre is None:
        limitations.append(
            "Không khai thể loại: nếu bộ bài mẫu trộn nhiều thể loại thì fingerprint chỉ đọc "
            "được ở mức tham khảo."
        )
    if status == "draft":
        limitations.append("Dưới 3 bài: chưa tách được thói quen của người khỏi đặc thù của bài.")

    profile = {
        "profile_version": "1.0",
        "name": slug,
        "language": language,
        "genre": genre,
        "built_from": built_from,
        "status": status,
        "fingerprint": {
            "sentence_len": {
                "mean": median_of(means),
                "cv": median_of([item["sentence_len_cv"] for item in measurements]),
                "median_per_sample": [
                    round(value, 2) if isinstance(value, (int, float)) else None
                    for value in means
                ],
            },
            "gloss_per_1000": median_of([item["gloss_per_1000"] for item in measurements]),
            "nominal_per_1000": median_of([item["nominal_per_1000"] for item in measurements]),
            "tone_style": tone_label,
            "tone_style_evidence": tone_evidence,
        },
        "pet_templates": build_pet_templates(measurements, with_examples=with_examples),
        "necessary_english_terms": build_english_terms(measurements),
        "known_typos": [],
        "voice_notes": (
            "CHƯA ĐIỀN. Script không đo được giọng — mục này do người dựng hồ sơ viết sau khi "
            "đọc bài mẫu, hoặc do chính tác giả tự mô tả."
        ),
        "provenance": {
            "built_at": date.today().isoformat(),
            "built_by": TOOL_VERSION,
            "ownership_confirmed_by": None,
            "samples": samples,
        },
        "limitations": limitations,
    }
    return profile, warnings


# ---------- giữ phần điền tay ----------
_MACHINE_LIMITATION_PREFIXES = (
    "Dựng từ ",
    "known_typos để rỗng:",
    "Không khai thể loại:",
    "Dưới 3 bài:",
    "Giữ lại từ hồ sơ dựng ",
)
_UNFILLED_NOTES_PREFIX = "CHƯA ĐIỀN"


def load_old_profile(path):
    """Trả (dict | None, cảnh báo | None). Không ném lỗi: thiếu hồ sơ cũ chỉ là cảnh báo."""
    if not path.is_file():
        return None, f"--keep-manual: không có hồ sơ cũ ở {path}; không giữ được gì."
    try:
        import yaml
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # YAML hỏng hay thiếu PyYAML đều không được làm mất hồ sơ mới
        return None, f"--keep-manual: không đọc được hồ sơ cũ ({type(exc).__name__}); không giữ được gì."
    if not isinstance(data, dict):
        return None, "--keep-manual: hồ sơ cũ không phải một bảng YAML; không giữ được gì."
    return data, None


def merge_manual(profile, old):
    """Chép phần điền tay của hồ sơ cũ sang hồ sơ vừa đo. Trả danh sách mô tả SỐ LƯỢNG đã giữ."""
    kept = []
    old_provenance = old.get("provenance") or {}

    notes = old.get("voice_notes")
    if isinstance(notes, str) and notes.strip() and not notes.lstrip().startswith(_UNFILLED_NOTES_PREFIX):
        profile["voice_notes"] = notes
        kept.append("voice_notes")

    owner = old_provenance.get("ownership_confirmed_by")
    if isinstance(owner, str) and owner.strip():
        profile["provenance"]["ownership_confirmed_by"] = owner
        kept.append("ownership_confirmed_by")

    typos = [item for item in (old.get("known_typos") or []) if isinstance(item, dict)]
    if typos:
        profile["known_typos"] = typos
        kept.append(f"{len(typos)} known_typos")

    # Khuôn do script đo được thì lần đo mới là sự thật; chỉ khuôn người thêm tay mới được giữ.
    measured_ids = {item["id"] for item in profile["pet_templates"]}
    manual_templates = [
        item for item in (old.get("pet_templates") or [])
        if isinstance(item, dict) and item.get("id")
        and item["id"] not in COUNTERS.TEMPLATES and item["id"] not in measured_ids
    ]
    profile["pet_templates"].extend(manual_templates)
    kept.append(f"{len(manual_templates)} pet_templates")

    # Giữ thứ tự người đã xếp; thuật ngữ mới đo được nối sau.
    old_terms = [t for t in (old.get("necessary_english_terms") or []) if isinstance(t, str) and t.strip()]
    machine_terms = profile["necessary_english_terms"]
    merged_terms = list(dict.fromkeys(old_terms + [t for t in machine_terms if t not in old_terms]))
    profile["necessary_english_terms"] = merged_terms
    kept.append(f"{len([t for t in merged_terms if t not in machine_terms])} thuật ngữ")

    limitations = [
        line for line in profile["limitations"]
        if not (typos and line.startswith("known_typos để rỗng:"))
    ]
    manual_lines = [
        line for line in (old.get("limitations") or [])
        if isinstance(line, str) and line.strip()
        and not line.startswith(_MACHINE_LIMITATION_PREFIXES) and line not in limitations
    ]
    kept.append(f"{len(manual_lines)} dòng limitations")
    old_built_at = old_provenance.get("built_at") or "không rõ ngày"
    profile["limitations"] = limitations + manual_lines + [
        f"Giữ lại từ hồ sơ dựng {old_built_at}: {', '.join(kept)}."
    ]
    return kept


# ---------- xuất ----------
def to_yaml(profile):
    try:
        import yaml
    except ImportError:
        raise SystemExit("Cần PyYAML để xuất profile.yaml: pip install pyyaml")

    class _Dumper(yaml.SafeDumper):
        pass

    def _str(dumper, value):
        # Chuỗi nhiều dòng (voice_notes) xuất dạng khối `|` để người còn sửa tay được.
        style = "|" if "\n" in value else None
        return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)

    _Dumper.add_representer(str, _str)
    return yaml.dump(profile, Dumper=_Dumper, allow_unicode=True, sort_keys=False, width=100)


def main():
    # FIX 30/08 (cổng Phase 4, Fable): console Windows mặc định cp1252 → in tiếng Việt ra stdout/stderr
    # ném UnicodeEncodeError SAU KHI đã ghi profile → exit 1 dù việc đã xong. Ép UTF-8 tại đây,
    # không phụ thuộc PYTHONUTF8/PYTHONIOENCODING của shell gọi.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(
        description="Dựng writer profile từ bài chính chủ. Không in nội dung bài."
    )
    parser.add_argument("--writer", required=True,
                        help="Slug thư mục trong $WRITING_STUDIO_DATA/writers/ (fallback shared/writers/)")
    parser.add_argument(
        "--samples-dir",
        help="Ghi đè đường dẫn samples/ (mặc định theo slug). Trỏ được vào thư mục bài mẫu trong "
             "kho tri thức; frontmatter YAML đầu file .md bị bỏ.",
    )
    parser.add_argument("--out", help="Ghi đè đường dẫn profile.yaml")
    parser.add_argument(
        "--keep-manual",
        nargs="?",
        const="",
        default=None,
        metavar="PATH",
        help="Giữ phần điền tay (voice_notes, ownership_confirmed_by, known_typos, pet_templates "
             "thêm tay, thuật ngữ, limitations) từ hồ sơ cũ. Không ghi PATH = dùng --out.",
    )
    parser.add_argument("--language", default="vi")
    parser.add_argument("--genre", default=None, help="Slug thể loại trong shared/genres/")
    parser.add_argument(
        "--with-examples",
        action="store_true",
        help="Ghi kèm một trích dẫn <=120 ký tự cho mỗi pet_template. CHỈ bật khi chủ hồ sơ đồng ý.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Không ghi file, chỉ báo tóm tắt")
    args = parser.parse_args()

    slug = args.writer
    base_dir = writers_dir()
    samples_dir = Path(args.samples_dir) if args.samples_dir else base_dir / slug / "samples"
    paths = collect_samples(samples_dir)
    if not paths:
        print(f"Không tìm thấy bài mẫu nào trong {samples_dir}", file=sys.stderr)
        print("Chấp nhận .txt, .md, .docx.", file=sys.stderr)
        return EXIT_FAIL

    profile, warnings = build_profile(
        slug, paths,
        language=args.language, genre=args.genre, with_examples=args.with_examples,
    )
    if profile is None:
        for line in warnings:
            print(f"  ! {line}", file=sys.stderr)
        return EXIT_FAIL

    out_path = Path(args.out) if args.out else base_dir / slug / "profile.yaml"
    kept = None
    if args.keep_manual is not None:
        # Đọc hồ sơ cũ TRƯỚC khi ghi: mặc định nó chính là file sắp bị ghi đè.
        old_path = Path(args.keep_manual) if args.keep_manual else out_path
        old, problem = load_old_profile(old_path)
        if problem:
            warnings.append(problem)
        else:
            kept = merge_manual(profile, old)
    text = to_yaml(profile)
    if not args.dry_run:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")

    fingerprint = profile["fingerprint"]
    # Chỉ số đo và tên file. Không một câu nào của bài mẫu đi qua stdout.
    print(f"writer      : {slug}")
    print(f"bài mẫu     : {profile['built_from']} ({', '.join(p.name for p in paths)})")
    print(f"status      : {profile['status']}")
    print(f"câu (trung vị): mean={fingerprint['sentence_len']['mean']} "
          f"cv={fingerprint['sentence_len']['cv']}")
    print(f"gloss/1000  : {fingerprint['gloss_per_1000']}")
    print(f"nominal/1000: {fingerprint['nominal_per_1000']}")
    print(f"tone_style  : {fingerprint['tone_style']} {fingerprint['tone_style_evidence']}")
    print(f"pet_templates: {[t['id'] for t in profile['pet_templates']] or '(chưa có)'}")
    print(f"thuật ngữ Anh: {profile['necessary_english_terms'] or '(chưa có)'}")
    if kept is not None:
        print(f"giữ tay     : {', '.join(kept)}")
    print(f"ghi ra      : {'(dry-run, không ghi)' if args.dry_run else out_path}")
    for line in warnings:
        print(f"  ! {line}")
    return EXIT_WARN if warnings else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
