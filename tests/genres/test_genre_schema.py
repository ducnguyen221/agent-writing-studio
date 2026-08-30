"""Kiểm hợp đồng `shared/genres/*.md` theo `shared/genres/_schema.md`.

Test này là cổng chặn của Phase 0: hồ sơ thể loại là DỮ LIỆU, nên nó phải parse được
bằng máy. Nếu một hồ sơ không qua đây thì bốn skill viết không có gì để đọc.
"""

import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
GENRES_DIR = ROOT / "shared/genres"
SCHEMA_DOC = GENRES_DIR / "_schema.md"

SECTION_TITLES = {
    1: "Intent và bối cảnh",
    2: "Khung viết",
    3: "Rubric chất lượng",
    4: "Quy tắc biên tập",
    5: "Must-have cho forensics",
}

REQUIRED_KEYS = {
    1: {"required_inputs", "intent_questions", "audience_fields", "stop_if_missing"},
    2: {"structures", "default_structure", "anti_llm_defaults", "outline_depth", "outline_layers"},
    3: {"criteria", "lenses", "blind_referee"},
    4: {
        "preserve",
        "moves_allowed",
        "moves_forbidden",
        "tell_families",
        "voice_priority",
    },
    5: {"must_have", "genre_baseline"},
}

# Danh mục lăng kính. Nguồn thật sẽ là `skills/03-critique/references/01-lang-kinh.md`
# (Phase 2); khi file đó tồn tại, test đọc từ đó và danh sách dưới chỉ còn là dự phòng.
LENS_CATALOGUE_FALLBACK = {
    "fallacy_scan",
    "claim_check",
    "task_response",
    "source_reliability",
    "source_independence",
    "balance_check",
    "method_rigor",
    "plot_consistency",
    "character_consistency",
    "pacing_curve",
    "three_chapter_selfcheck",
    "value_density",
    "retention",
}

# Hồ sơ đầy đủ (đủ §1–§5) và hồ sơ một phần (chỉ §5). Danh sách này là hợp đồng của Phase 1b:
# thêm thể loại mới thì thêm vào đây, nhưng không được HẠ một hồ sơ full xuống partial mà không ai biết.
FULL_GENRES = {"essay", "research", "novel", "journalism", "blog"}
PARTIAL_GENRES = {
    "chinh-luan",
    "de-cuong-nghien-cuu",
    "bao-cao-thuc-tap",
    "sang-kien-kinh-nghiem",
}

HEADING = re.compile(r"(?m)^##\s+(\d)\.\s+(.+?)\s*$")
YAML_BLOCK = re.compile(r"(?ms)^```yaml\r?\n(.*?)^```\s*$")


def lens_catalogue():
    """Danh mục lăng kính: đọc từ reference của trục 3 nếu đã có, nếu chưa thì dùng bản dự phòng."""
    reference = ROOT / "skills/03-critique/references/01-lang-kinh.md"
    if not reference.is_file():
        return LENS_CATALOGUE_FALLBACK
    text = reference.read_text(encoding="utf-8")
    found = set(re.findall(r"`([a-z][a-z0-9_]+)`", text))
    return found & LENS_CATALOGUE_FALLBACK or LENS_CATALOGUE_FALLBACK


def genre_files():
    return sorted(p for p in GENRES_DIR.glob("*.md") if p.name != "_schema.md")


def split_sections(text):
    """Trả {số mục: (tiêu đề, thân mục)} theo các heading `## N. …`."""
    matches = list(HEADING.finditer(text))
    sections = {}
    for index, match in enumerate(matches):
        number = int(match.group(1))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[number] = (match.group(2), text[match.end(): end])
    return sections


class GenreSchemaTests(unittest.TestCase):
    def test_schema_doc_exists_and_lists_five_sections(self):
        self.assertTrue(SCHEMA_DOC.is_file(), "Thiếu shared/genres/_schema.md")
        doc = SCHEMA_DOC.read_text(encoding="utf-8")
        for number, title in SECTION_TITLES.items():
            self.assertIn(f"§{number} ·", doc, f"_schema.md chưa mô tả mục §{number}")
            self.assertIn(title, doc, f"_schema.md chưa nêu tên mục §{number}")
        for keys in REQUIRED_KEYS.values():
            for key in keys:
                self.assertIn(f"`{key}`", doc, f"_schema.md chưa giải thích khoá {key}")

    def test_at_least_one_genre_profile_exists(self):
        self.assertTrue(genre_files(), "Chưa có hồ sơ thể loại nào trong shared/genres/")

    def test_every_genre_profile_matches_schema(self):
        catalogue = lens_catalogue()
        for path in genre_files():
            with self.subTest(genre=path.name):
                text = path.read_text(encoding="utf-8")
                sections = split_sections(text)
                present = sorted(sections)

                # full = đủ 1..5; partial = CHỈ có §5. Không có tổ hợp thứ ba.
                if present == [5]:
                    expected = [5]
                else:
                    expected = [1, 2, 3, 4, 5]
                self.assertEqual(
                    present,
                    expected,
                    f"{path.name}: hồ sơ phải có đủ ## 1.–## 5., hoặc chỉ ## 5. (partial)",
                )

                for number in expected:
                    title, body = sections[number]
                    self.assertEqual(
                        title,
                        SECTION_TITLES[number],
                        f"{path.name} §{number}: tên mục phải là '{SECTION_TITLES[number]}'",
                    )
                    blocks = YAML_BLOCK.findall(body)
                    self.assertEqual(
                        len(blocks),
                        1,
                        f"{path.name} §{number}: phải có đúng một khối yaml, đang có {len(blocks)}",
                    )
                    data = yaml.safe_load(blocks[0])
                    self.assertIsInstance(
                        data, dict, f"{path.name} §{number}: khối yaml phải là mapping"
                    )
                    missing = REQUIRED_KEYS[number] - set(data)
                    self.assertFalse(
                        missing,
                        f"{path.name} §{number}: thiếu khoá {sorted(missing)}",
                    )
                    self.check_section(path.name, number, data, catalogue)

    def check_section(self, name, number, data, catalogue):
        if number == 1:
            for key in REQUIRED_KEYS[1]:
                self.assertIsInstance(data[key], list, f"{name} §1: {key} phải là list")
            self.assertTrue(data["intent_questions"], f"{name} §1: intent_questions rỗng")
            self.assertTrue(data["stop_if_missing"], f"{name} §1: stop_if_missing rỗng")

        if number == 2:
            self.assertIsInstance(data["structures"], list)
            ids = []
            for item in data["structures"]:
                self.assertIsInstance(item, dict, f"{name} §2: mỗi structure phải là mapping")
                self.assertIn("id", item)
                self.assertIn("parts", item)
                self.assertIsInstance(item["parts"], list)
                self.assertTrue(item["parts"], f"{name} §2: structure {item['id']} rỗng parts")
                ids.append(item["id"])
            self.assertIn(
                data["default_structure"],
                ids,
                f"{name} §2: default_structure phải là một id trong structures",
            )
            self.assertIsInstance(data["anti_llm_defaults"], list)
            self.assertIsInstance(data["outline_depth"], int)
            self.assertGreaterEqual(data["outline_depth"], 1)
            # Skill ép SỐ tầng, hồ sơ thể loại khai NGHĨA từng tầng. Lệch số mục là hợp đồng
            # gãy: trục 2 duyệt ba tầng trong khi hồ sơ chỉ nói được nghĩa của hai.
            self.assertIsInstance(data["outline_layers"], list, f"{name} §2: outline_layers phải là list")
            self.assertEqual(
                len(data["outline_layers"]),
                data["outline_depth"],
                f"{name} §2: outline_layers phải có đúng outline_depth mục",
            )
            for layer in data["outline_layers"]:
                self.assertTrue(
                    str(layer).strip(),
                    f"{name} §2: outline_layers có mục rỗng — tầng không nói được nghĩa thì không duyệt được",
                )

        if number == 3:
            self.assertIsInstance(data["criteria"], list)
            self.assertTrue(data["criteria"], f"{name} §3: criteria rỗng")
            seen = set()
            for item in data["criteria"]:
                self.assertIsInstance(item, dict)
                missing = {"id", "name", "evidence", "question"} - set(item)
                self.assertFalse(missing, f"{name} §3: criterion thiếu {sorted(missing)}")
                self.assertNotIn(item["id"], seen, f"{name} §3: trùng id {item['id']}")
                seen.add(item["id"])
                self.assertTrue(
                    str(item["question"]).strip().endswith("?"),
                    f"{name} §3: criterion {item['id']} phải hỏi một câu hỏi thật",
                )
            self.assertIsInstance(data["lenses"], list)
            unknown = set(data["lenses"]) - catalogue
            self.assertFalse(
                unknown,
                f"{name} §3: lăng kính ngoài danh mục {sorted(unknown)}",
            )
            self.assertIsInstance(data["blind_referee"], bool)

        if number == 4:
            for key in ("preserve", "moves_allowed", "moves_forbidden", "tell_families"):
                self.assertIsInstance(data[key], list, f"{name} §4: {key} phải là list")
            self.assertTrue(data["preserve"], f"{name} §4: preserve rỗng")
            for tell_id in data["tell_families"]:
                self.assertRegex(
                    str(tell_id),
                    r"^T\d{2}$",
                    f"{name} §4: tell_families phải là id dạng T07, gặp {tell_id!r}",
                )
            self.assertEqual(
                data["voice_priority"][:2],
                ["writer_profile", "genre_default"],
                f"{name} §4: writer_profile phải đứng trước genre_default",
            )

        if number == 5:
            self.assertIsInstance(data["must_have"], list)
            self.assertTrue(data["must_have"], f"{name} §5: must_have rỗng")
            levels = set()
            for item in data["must_have"]:
                self.assertIsInstance(item, dict)
                missing = {"level", "statement", "verify"} - set(item)
                self.assertFalse(missing, f"{name} §5: must_have thiếu {sorted(missing)}")
                self.assertIn(
                    item["level"],
                    {"core", "minor"},
                    f"{name} §5: level phải là core hoặc minor, gặp {item['level']!r}",
                )
                levels.add(item["level"])
            self.assertIn("core", levels, f"{name} §5: phải có ít nhất một must_have core")
            baseline = data["genre_baseline"]
            self.assertIsInstance(baseline, dict, f"{name} §5: genre_baseline phải là mapping")
            self.assertIn("normal_signals", baseline)
            self.assertIsInstance(baseline["normal_signals"], list)

    def test_the_nine_expected_profiles_exist_with_the_expected_shape(self):
        """5 hồ sơ đầy đủ + 4 hồ sơ một phần. Đây là sản phẩm của Phase 1b."""
        present = {path.stem for path in genre_files()}
        missing = (FULL_GENRES | PARTIAL_GENRES) - present
        self.assertFalse(missing, f"Thiếu hồ sơ thể loại: {sorted(missing)}")
        for slug in sorted(FULL_GENRES | PARTIAL_GENRES):
            with self.subTest(genre=slug):
                sections = split_sections(
                    (GENRES_DIR / f"{slug}.md").read_text(encoding="utf-8")
                )
                expected = [5] if slug in PARTIAL_GENRES else [1, 2, 3, 4, 5]
                self.assertEqual(
                    sorted(sections),
                    expected,
                    f"{slug}.md: hồ sơ {'partial' if slug in PARTIAL_GENRES else 'full'} sai hình dạng",
                )

    def test_every_section_opens_with_the_sentence_saying_who_reads_it(self):
        """Tiêu chí nghiệm thu spec §4: mỗi mục mở đầu bằng 'Trục N đọc mục này để …'."""
        for path in genre_files():
            sections = split_sections(path.read_text(encoding="utf-8"))
            for number, (_, body) in sections.items():
                with self.subTest(genre=path.name, section=number):
                    self.assertIn(
                        f"Trục {number} đọc mục này để",
                        body,
                        f"{path.name} §{number}: thiếu câu 'Trục {number} đọc mục này để …'",
                    )

    def test_every_genre_baseline_slug_in_the_tells_registry_has_a_profile(self):
        """Baseline trỏ tới thể loại không có hồ sơ = trục 5 không tìm được §5 để hạ tín hiệu.

        Lỗi này im lặng: `polish_check.py` chỉ ghi 'KHÔNG đọc được' rồi chạy tiếp, nên
        không có test thì không ai biết. Nguồn: cổng Phase 0 (Fable, 30/08).
        """
        registry_path = ROOT / "shared/rules/vi-ai-tells.json"
        if not registry_path.is_file():
            self.skipTest("Chưa có shared/rules/vi-ai-tells.json")
        import json

        slugs = set()
        for entry in json.loads(registry_path.read_text(encoding="utf-8"))["entries"]:
            slugs.update(entry.get("genre_baseline", []))
        self.assertTrue(slugs, "Không mục tell nào khai genre_baseline")
        present = {path.stem for path in genre_files()}
        orphan = slugs - present
        self.assertFalse(
            orphan,
            f"genre_baseline trỏ tới thể loại không có hồ sơ shared/genres/<slug>.md: {sorted(orphan)}",
        )

    def test_tell_families_reference_real_entries(self):
        registry_path = ROOT / "shared/rules/vi-ai-tells.json"
        if not registry_path.is_file():
            self.skipTest("Chưa có shared/rules/vi-ai-tells.json")
        import json

        known = {
            entry["id"]
            for entry in json.loads(registry_path.read_text(encoding="utf-8"))["entries"]
        }
        for path in genre_files():
            sections = split_sections(path.read_text(encoding="utf-8"))
            if 4 not in sections:
                continue
            blocks = YAML_BLOCK.findall(sections[4][1])
            data = yaml.safe_load(blocks[0])
            unknown = set(data["tell_families"]) - known
            self.assertFalse(
                unknown,
                f"{path.name} §4: tell_families trỏ tới id không có trong vi-ai-tells.json: {sorted(unknown)}",
            )


if __name__ == "__main__":
    unittest.main()
