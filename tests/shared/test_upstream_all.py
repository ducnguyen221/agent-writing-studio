"""Provenance cho MỌI nguồn distill — `upstream.json` và `vendor-notes/`.

Luật một câu: repo nào không cho chép — không có license, hoặc có license copyleft —
thì chỉ được lấy ý tưởng, và điều đó phải ghi thành dữ liệu (`storage: idea-only`)
chứ không phải ghi trong đầu ai đó.
"""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / "upstream.json"
VENDOR = ROOT / "vendor-notes"

SHA40 = re.compile(r"^[0-9a-f]{40}$")

# 13 nguồn: antislop đã pin từ đợt trước + 12 nguồn của đợt này.
EXPECTED = {
    "SalZaki/antislop": "antislop",
    "danielmiessler/fabric": "fabric",
    "stanford-oval/storm": "storm",
    "LAY-lgtm/novel-writing-framework": "novel-writing-framework",
    "simondgoldstein/deep-drafter": "deep-drafter",
    "devswha/patina": "patina",
    "seyedehsanhadi/sloptrim": "sloptrim",
    "NousResearch/autonovel": "autonovel",
    "anthropics/skills": "anthropics-skills",
    "causalNLP/logical-fallacy": "logical-fallacy",
    "ReML-AI/VIVID": "vivid",
    "1ec5/hunspell-vi": "hunspell-vi",
    "blader/humanizer": "humanizer",
}

# Repo không license: cấm chép nội dung, chỉ lấy sơ đồ hoặc tên.
LICENSE_NONE = {
    "NousResearch/autonovel",
    "anthropics/skills",
    "causalNLP/logical-fallacy",
}

# Repo có license COPYLEFT: license hợp lệ, nhưng mang nội dung vào đây sẽ kéo nghĩa vụ
# cấp phép sang cả repo. Hệ quả vận hành giống hệt repo không license: chỉ lấy ý tưởng.
LICENSE_COPYLEFT = {
    "1ec5/hunspell-vi",
}

# Repo bị cấm chép nội dung vì một trong hai lý do trên.
NO_COPY = LICENSE_NONE | LICENSE_COPYLEFT

COPYLEFT_PATTERN = re.compile(r"(?i)\b(a?gpl|lgpl|cc-?by-?sa|mpl|epl)")


def upstream():
    return json.loads(UPSTREAM.read_text(encoding="utf-8"))


def sources():
    return upstream()["sources"]


class UpstreamAllTests(unittest.TestCase):
    def test_every_expected_source_is_pinned(self):
        names = {s["name"] for s in sources()}
        missing = set(EXPECTED) - names
        self.assertFalse(missing, f"upstream.json thiếu nguồn: {sorted(missing)}")
        self.assertGreaterEqual(len(names), 12, "Kế hoạch yêu cầu tối thiểu 12 nguồn có provenance")

    def test_every_source_has_full_sha_license_and_took(self):
        for source in sources():
            with self.subTest(source=source.get("name")):
                for key in ("type", "storage", "url", "branch", "baseline", "baseline_date",
                            "reviewed_date", "license", "took", "update"):
                    self.assertIn(key, source, f"{source.get('name')}: thiếu khoá {key}")
                self.assertRegex(
                    source["baseline"],
                    SHA40,
                    f"{source['name']}: baseline phải là SHA đầy đủ 40 ký tự hex",
                )
                self.assertTrue(str(source["license"]).strip(), f"{source['name']}: license rỗng")
                self.assertTrue(source["took"], f"{source['name']}: took rỗng")
                for item in source["took"]:
                    self.assertTrue(str(item).strip(), f"{source['name']}: took có mục rỗng")
                self.assertTrue(str(source["update"]).strip())

    def test_unlicensed_sources_are_idea_only(self):
        by_name = {s["name"]: s for s in sources()}
        for name in LICENSE_NONE:
            with self.subTest(source=name):
                self.assertIn(name, by_name)
                source = by_name[name]
                self.assertTrue(
                    str(source["license"]).lower().startswith("none"),
                    f"{name}: license phải ghi rõ là none",
                )
                self.assertEqual(
                    source["storage"],
                    "idea-only",
                    f"{name}: repo không license BẮT BUỘC storage=idea-only",
                )

    def test_copyleft_sources_declare_the_licence_and_stay_idea_only(self):
        """Copyleft KHÔNG phải là không có license — nhưng hệ quả vận hành như nhau.

        Ghi `license: none` cho một repo copyleft là ghi sai sự thật: bản quyền có,
        điều khoản có, và chính điều khoản đó mới là lý do không được chép.
        """
        by_name = {s["name"]: s for s in sources()}
        for name in LICENSE_COPYLEFT:
            with self.subTest(source=name):
                self.assertIn(name, by_name)
                source = by_name[name]
                licence = str(source["license"])
                self.assertFalse(
                    licence.lower().startswith("none"),
                    f"{name}: repo CÓ license copyleft, không được ghi là none",
                )
                self.assertRegex(
                    licence,
                    COPYLEFT_PATTERN,
                    f"{name}: license phải nêu tên giấy phép copyleft cụ thể",
                )
                self.assertEqual(
                    source["storage"],
                    "idea-only",
                    f"{name}: license copyleft BẮT BUỘC storage=idea-only",
                )

    def test_license_none_or_copyleft_implies_idea_only_for_any_source(self):
        """Luật tổng quát, không chỉ cho các repo đã biết tên."""
        for source in sources():
            licence = str(source["license"])
            blocked = licence.lower().startswith("none") or COPYLEFT_PATTERN.search(licence)
            if blocked:
                with self.subTest(source=source["name"]):
                    self.assertEqual(
                        source["storage"],
                        "idea-only",
                        f"{source['name']}: license {licence!r} cấm chép nội dung ⇒ phải idea-only",
                    )

    def test_manually_checked_licenses_record_the_check(self):
        """Hai repo mà API GitHub trả license rỗng: phải có ghi chép kiểm tay."""
        by_name = {s["name"]: s for s in sources()}
        for name in ("anthropics/skills", "1ec5/hunspell-vi"):
            with self.subTest(source=name):
                note = by_name[name].get("license_check", "")
                self.assertTrue(note.strip(), f"{name}: thiếu license_check ghi kết quả kiểm tay")
                self.assertIn("2026", note, f"{name}: license_check phải ghi ngày kiểm")

    def test_every_source_has_vendor_notes(self):
        for source in sources():
            slug = EXPECTED.get(source["name"])
            if slug is None:
                continue
            with self.subTest(source=source["name"]):
                folder = VENDOR / slug
                self.assertTrue(folder.is_dir(), f"Thiếu vendor-notes/{slug}/")
                for filename in ("SOURCES.md", "DISTILL-NOTES.md"):
                    path = folder / filename
                    self.assertTrue(path.is_file(), f"Thiếu vendor-notes/{slug}/{filename}")
                    self.assertTrue(path.read_text(encoding="utf-8").strip())

    def test_vendor_notes_follow_the_template(self):
        for slug in EXPECTED.values():
            with self.subTest(repo=slug):
                notes = (VENDOR / slug / "DISTILL-NOTES.md").read_text(encoding="utf-8")
                for heading in ("## Đã chưng cất", "## Không mang sang", "## Ranh giới"):
                    self.assertIn(heading, notes, f"{slug}: thiếu mục {heading}")

    def test_vendor_notes_record_the_pinned_sha(self):
        for source in sources():
            slug = EXPECTED.get(source["name"])
            if slug is None:
                continue
            with self.subTest(repo=slug):
                text = (VENDOR / slug / "SOURCES.md").read_text(encoding="utf-8")
                self.assertIn(
                    source["baseline"],
                    text,
                    f"{slug}/SOURCES.md phải ghi đúng SHA đã pin trong upstream.json",
                )

    def test_unlicensed_vendor_notes_say_idea_only_out_loud(self):
        for name in NO_COPY:
            slug = EXPECTED[name]
            with self.subTest(repo=slug):
                sources_md = (VENDOR / slug / "SOURCES.md").read_text(encoding="utf-8")
                notes_md = (VENDOR / slug / "DISTILL-NOTES.md").read_text(encoding="utf-8")
                self.assertIn("idea-only", sources_md, f"{slug}: SOURCES.md phải ghi idea-only")
                self.assertIn(
                    "KHÔNG CÓ LICENSE",
                    sources_md + notes_md,
                    f"{slug}: phải nói thẳng repo không có license",
                )

    def test_storage_values_are_known(self):
        allowed = set(upstream()["storage_meaning"])
        for source in sources():
            with self.subTest(source=source["name"]):
                self.assertIn(source["storage"], allowed)


if __name__ == "__main__":
    unittest.main()
