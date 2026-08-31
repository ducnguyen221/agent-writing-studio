"""Hàng rào de-name — phần public của repo không được mang tên riêng repo nguồn.

Luật một câu: repo này chưng cất PHƯƠNG PHÁP rồi tự viết lại bằng tiếng Việt; sổ nguồn
(lấy gì, không lấy gì, SHA đã pin) sống ở xưởng, KHÔNG nằm trong repo. Test này là hàng
rào chống tên bò ngược vào qua một lần "cải tiến" sau này — thay cho bộ test provenance
cũ vốn đọc `upstream.json` và `vendor-notes/` đã dời đi.

Ngoại lệ DUY NHẤT: `skills/04-humanizer/assets/thanh-ngu.json` là nguồn duy nhất ta MANG
DỮ LIỆU. License MIT bắt buộc giữ copyright notice + permission notice khi phân phối, nên
tên nguồn ở file đó là NGHĨA VỤ PHÁP LÝ, không phải lựa chọn — và test dưới đây bắt nó
phải còn.
"""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

# Cây public: thứ được clone/cài. `docs/plans` và `docs/results` là nhật ký làm việc,
# nằm ngoài hàng rào (chúng ghi lại chính quá trình de-name này).
PUBLIC_DIRS = ("skills", "shared", "docs")
PUBLIC_FILES = ("README.md",)
EXCLUDED_PREFIXES = ("docs/plans/", "docs/results/")
SCANNED_SUFFIXES = {".md", ".json", ".py", ".txt", ".yaml", ".yml"}

# Ngoại lệ pháp lý: file mang DỮ LIỆU cấp phép MIT, notice bắt buộc phải ở lại.
MIT_DATA_FILE = "skills/04-humanizer/assets/thanh-ngu.json"

# Slug repo nguồn đầy đủ — dạng `owner/repo`.
BANNED_SLUGS = (
    "blader/humanizer",
    "SalZaki/antislop",
    "danielmiessler/fabric",
    "stanford-oval/storm",
    "LAY-lgtm/novel-writing-framework",
    "simondgoldstein/deep-drafter",
    "devswha/patina",
    "seyedehsanhadi/sloptrim",
    "NousResearch/autonovel",
    "anthropics/skills",
    "causalNLP/logical-fallacy",
    "1ec5/hunspell-vi",
)

# Tên trần đủ đặc thù để nhận ra repo nguồn dù không có phần `owner/`.
# CHÚ Ý — KHÔNG cấm chuỗi "humanizer" trần: `skills/04-humanizer/` là TÊN TRỤC hợp lệ,
# và "công cụ humanizer trên thị trường" là danh từ chung. Chỉ slug đầy đủ mới bị cấm.
# Cũng không cấm "storm"/"fabric" trần: `verified_fabrication` là thuật ngữ của repo.
BANNED_BARE = (
    "antislop",
    "sloptrim",
    "patina",
    "deep-drafter",
    "autonovel",
    "causalNLP",
    "blader",
    "VIVID",
    "ReML",
    "novel-writing-framework",
    "logical-fallacy",
    "hunspell-vi",
    "doc-coauthoring",
)

# Con trỏ sang sổ nguồn đã dời khỏi repo.
BANNED_POINTERS = ("vendor-notes/", "upstream.json", "06-distill-repo")

BANNED = tuple(BANNED_SLUGS) + tuple(BANNED_BARE) + tuple(BANNED_POINTERS)

# Sổ nguồn phải KHÔNG còn trong repo (đã dời về xưởng OpcOS 31/08/2026).
MOVED_OUT = (
    "upstream.json",
    "vendor-notes",
    "skills/05-forensics/references/06-distill-repo.md",
    "skills/04-humanizer/scripts/build_thanh_ngu.py",
)

CATALOG_CODE = re.compile(r"^studio:catalog#\d+$")


def public_files():
    seen = []
    for name in PUBLIC_FILES:
        path = ROOT / name
        if path.is_file():
            seen.append(path)
    for folder in PUBLIC_DIRS:
        for path in sorted((ROOT / folder).rglob("*")):
            if not path.is_file() or path.suffix.lower() not in SCANNED_SUFFIXES:
                continue
            relative = path.relative_to(ROOT).as_posix()
            if relative.startswith(EXCLUDED_PREFIXES):
                continue
            seen.append(path)
    return seen


class DeNameFenceTests(unittest.TestCase):
    def test_the_fence_actually_scans_something(self):
        """Hàng rào quét rỗng thì luôn xanh — và xanh vì lý do sai."""
        files = public_files()
        self.assertGreater(len(files), 50, "Cây public quét được quá ít file, hàng rào vô nghĩa")
        names = {p.relative_to(ROOT).as_posix() for p in files}
        self.assertIn("README.md", names)
        self.assertIn(MIT_DATA_FILE, names)
        self.assertIn("shared/rules/vi-ai-tells.json", names)

    def test_no_source_repo_name_in_the_public_tree(self):
        hits = []
        for path in public_files():
            relative = path.relative_to(ROOT).as_posix()
            content = path.read_text(encoding="utf-8")
            lowered = content.lower()
            for needle in BANNED:
                if needle.lower() not in lowered:
                    continue
                # Ngoại lệ MIT: notice bắt buộc của kho thành ngữ.
                if relative == MIT_DATA_FILE and needle in ("VIVID", "ReML"):
                    continue
                line = next(
                    (
                        f"{n}: {text.strip()[:90]}"
                        for n, text in enumerate(content.splitlines(), 1)
                        if needle.lower() in text.lower()
                    ),
                    "?",
                )
                hits.append(f"{relative} :: {needle!r} @ {line}")
        self.assertEqual(hits, [], "Tên repo nguồn còn trong cây public:\n" + "\n".join(hits))

    def test_source_ledger_left_the_repo(self):
        for relative in MOVED_OUT:
            with self.subTest(path=relative):
                self.assertFalse(
                    (ROOT / relative).exists(),
                    f"{relative} phải dời về sổ xưởng, không ở trong repo public",
                )

    def test_mit_data_file_keeps_its_notice(self):
        """Không giữ notice là VI PHẠM LICENSE, không phải một lựa chọn sạch hơn."""
        data = json.loads((ROOT / MIT_DATA_FILE).read_text(encoding="utf-8"))
        self.assertIn("attribution", data, "thanh-ngu.json thiếu khối attribution")
        attribution = data["attribution"]
        for key in ("source_repo", "license", "copyright_notice", "license_notice"):
            self.assertIn(key, attribution, f"attribution thiếu {key} — MIT bắt buộc giữ")
            self.assertTrue(str(attribution[key]).strip(), f"attribution: {key} rỗng")
        self.assertEqual(attribution["license"], "MIT")
        self.assertIn("Copyright", attribution["copyright_notice"])
        self.assertIn("Permission is hereby granted", attribution["license_notice"])

    def test_tells_registry_uses_internal_catalog_codes(self):
        data = json.loads((ROOT / "shared/rules/vi-ai-tells.json").read_text(encoding="utf-8"))
        seen_catalog = 0
        allowed_prefixes = ("studio:catalog#", "counters.py:", "docs/results/")
        for entry in data["entries"]:
            for source in entry.get("source", []):
                with self.subTest(tell=entry["id"], source=source):
                    self.assertTrue(
                        source.startswith(allowed_prefixes),
                        f"source {source!r} không thuộc dạng nội bộ nào được phép",
                    )
                    if CATALOG_CODE.match(source):
                        seen_catalog += 1
        for excluded in data["excluded_patterns"]:
            source = excluded["source"]
            with self.subTest(excluded=excluded["name"]):
                self.assertTrue(
                    CATALOG_CODE.match(source),
                    f"excluded_patterns source phải là mã nội bộ, thấy {source!r}",
                )
                seen_catalog += 1
        self.assertGreaterEqual(seen_catalog, 35, "Mã nội bộ studio:catalog# bị mất khi de-name")

    def test_tells_provenance_names_no_repo(self):
        data = json.loads((ROOT / "shared/rules/vi-ai-tells.json").read_text(encoding="utf-8"))
        provenance = data["provenance"]
        self.assertTrue(provenance.strip())
        lowered = provenance.lower()
        for needle in BANNED:
            self.assertNotIn(needle.lower(), lowered, f"provenance còn nhắc {needle!r}")
        self.assertIn("sổ xưởng", lowered)


if __name__ == "__main__":
    unittest.main()
