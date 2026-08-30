"""Hợp đồng của trục 4 (`04-humanizer`).

Trục 4 là con dao hai lưỡi của repo: nó SỬA văn bản thật. Vì vậy test ở đây canh ba thứ mà
không có gì khác trong repo phát hiện được nếu chúng vỡ:

1. **Ranh giới đạo đức** còn nguyên trong SKILL.md — làm văn hay hơn, không phải né máy chấm.
2. **Chống sửa oan** còn giữ đủ các chốt đã tốn một ca giám định thật mới rút ra được:
   văn hành chính chuẩn, lặp có chủ ý, câu Link của PEEL, carve-out của `value_density`,
   và danh sách mẫu tiếng Anh KHÔNG được mang sang.
3. **Cổng 0-token** fail-closed khi có fact bị thêm, và đọc `genre_baseline` TRƯỚC khi báo
   counter.
"""

import contextlib
import importlib.util
import io
import json
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills/04-humanizer/SKILL.md"
REFERENCES = ROOT / "skills/04-humanizer/references"
SCRIPT = ROOT / "skills/04-humanizer/scripts/polish_check.py"
THANH_NGU = ROOT / "skills/04-humanizer/assets/thanh-ngu.json"
TELLS = ROOT / "shared/rules/vi-ai-tells.json"
SCENARIO = ROOT / "tests/skills/scenarios/04-van-nguoi-trang-trong.md"

REQUIRED_REFERENCES = (
    "01-quy-trinh-hai-luot.md",
    "02-vung-bao-ve.md",
    "03-chong-sua-oan.md",
    "04-ban-do-loi-cach-sua.md",
    "05-chinh-ta.md",
)

# Những từ chỉ xuất hiện nếu ai đó dịch một blacklist tiếng Anh rồi dán vào. Danh mục tell của
# repo này là HỌ TÍN HIỆU kèm phản chứng tiếng Việt, không phải danh sách từ.
ENGLISH_SLOP = (
    "delve", "leverage", "furthermore", "moreover", "tapestry", "landscape",
    "utilize", "seamless", "realm", "underscore", "pivotal", "testament",
    "crucial", "robust", "notably", "intricate", "multifaceted", "elevate",
)


def skill_text():
    return SKILL.read_text(encoding="utf-8")


def reference_text(name):
    return (REFERENCES / name).read_text(encoding="utf-8")


def load_polish_check():
    spec = importlib.util.spec_from_file_location("humanizer_polish_check", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SkillStructureTests(unittest.TestCase):
    def test_skill_file_exists_with_frontmatter_contract(self):
        self.assertTrue(SKILL.is_file(), "Thiếu skills/04-humanizer/SKILL.md")
        text = skill_text()
        self.assertRegex(text, r"(?m)^name: 04-humanizer$")
        self.assertRegex(text, r"(?m)^description: Use when ")

    def test_skill_stays_under_the_word_budget(self):
        words = len(skill_text().split())
        self.assertLessEqual(words, 550, f"SKILL.md dài {words} từ, trần là 550")

    def test_skill_reads_section_four_and_writes_the_schema(self):
        text = skill_text()
        self.assertIn("§4", text, "SKILL.md phải nói rõ nó đọc mục §4 của hồ sơ thể loại")
        self.assertIn("vi-ai-tells.json", text)
        self.assertIn("`fix`", text, "SKILL.md phải nói rõ nó đọc cột fix của danh mục tell")
        self.assertIn("polish.schema.json", text)

    def test_skill_has_no_genre_branching(self):
        text = skill_text()
        for forbidden in ("if genre", 'genre == "'):
            self.assertNotIn(forbidden, text, f"SKILL.md chứa nhánh theo thể loại: {forbidden!r}")

    def test_all_references_exist_and_are_linked(self):
        text = skill_text()
        for name in REQUIRED_REFERENCES:
            with self.subTest(reference=name):
                path = REFERENCES / name
                self.assertTrue(path.is_file(), f"Thiếu references/{name}")
                self.assertTrue(path.read_text(encoding="utf-8").strip())
                self.assertIn(f"references/{name}", text, f"SKILL.md không trỏ tới {name}")


class EthicalBoundaryTests(unittest.TestCase):
    def test_skill_states_the_ethical_boundary(self):
        """Làm văn hay hơn cho người đọc, KHÔNG phải né máy chấm."""
        text = skill_text()
        self.assertIn("Ranh giới đạo đức", text)
        self.assertIn("né máy chấm", text)
        self.assertIn("cho người đọc", text)

    def test_skill_requires_a_declared_origin(self):
        """Trục 4 chỉ chạy khi biết bài từ đâu ra."""
        text = skill_text()
        self.assertIn("draft.meta.json", text)
        self.assertIn("tự khai", text)

    def test_skill_forbids_reading_the_forensics_score(self):
        text = skill_text()
        self.assertIn("Không xem điểm trục 5", text)
        self.assertIn("forensics_score_seen", text)

    def test_skill_requires_the_stylometric_polish_flag(self):
        self.assertIn("stylometric_polish", skill_text())

    def test_skill_rejects_because_it_sounds_like_ai_as_a_reason(self):
        self.assertIn("bớt giống AI", skill_text())


class AntiOverEditTests(unittest.TestCase):
    """`03-chong-sua-oan.md` — file mà mọi chốt trong đó đều đổi bằng một ca thật."""

    def test_reference_keeps_the_measured_cliche_counterevidence(self):
        text = reference_text("03-chong-sua-oan.md")
        self.assertIn("1,04", text)
        self.assertIn("0,50", text)
        self.assertIn("03-chong-bao-oan", text)

    def test_reference_protects_intentional_repetition_and_author_asides(self):
        text = reference_text("03-chong-sua-oan.md")
        self.assertIn("Lặp có chủ ý", text)
        self.assertIn("tự sửa mình", text)

    def test_reference_protects_the_peel_link_sentence(self):
        """T31: câu Link của PEEL là cấu trúc bắt buộc, không phải tell."""
        text = reference_text("03-chong-sua-oan.md")
        self.assertIn("T31", text)
        self.assertIn("PEEL", text)

    def test_reference_keeps_the_value_density_carve_out(self):
        text = " ".join(reference_text("03-chong-sua-oan.md").split())
        self.assertIn("value_density", text)
        for zone in ("(1)", "(2)", "(3)", "(4)"):
            self.assertIn(zone, text, "carve-out phải giữ đủ 4 vùng không được chạm")
        self.assertIn("đoạn thân", text)

    def test_reference_protects_the_administrative_report_skeleton(self):
        text = reference_text("03-chong-sua-oan.md")
        self.assertIn("T06", text)
        self.assertIn("phương hướng", text)

    def test_reference_lists_what_was_not_carried_over(self):
        """Em dash và ngoặc kép cong đã bị bác bằng thực đo — phải nói rõ là KHÔNG mang sang."""
        text = reference_text("03-chong-sua-oan.md")
        for excluded in ("Em dash", "Ngoặc kép cong", "Title Case"):
            self.assertIn(excluded, text, f"Thiếu mẫu bị loại: {excluded}")
        self.assertIn("needs_corpus", text, "Pattern 7 phải được nói rõ là vẫn để rỗng")

    def test_reference_says_genre_baseline_wins_over_counters(self):
        text = reference_text("03-chong-sua-oan.md")
        self.assertIn("genre_baseline", text)
        self.assertIn("baseline thể loại", text)


class ProtectedZoneTests(unittest.TestCase):
    def test_reference_lists_the_default_protected_zones(self):
        text = reference_text("02-vung-bao-ve.md")
        for zone in ("Số liệu", "Trích dẫn nguyên văn", "Tên riêng", "frontmatter"):
            self.assertIn(zone, text, f"Thiếu vùng bảo vệ mặc định: {zone}")

    def test_reference_scopes_the_fiction_exception_to_the_genre_profile(self):
        text = reference_text("02-vung-bao-ve.md")
        self.assertIn("hư cấu", text)
        self.assertIn("không tự suy ra ngoại lệ", text)


class ErrorMapTests(unittest.TestCase):
    def test_error_map_points_at_the_existing_table_instead_of_copying_it(self):
        text = reference_text("04-ban-do-loi-cach-sua.md")
        self.assertIn("10-mau-bao-cao-va-cach-sua.md", text)
        self.assertIn("không được chép lại", text)

    def test_error_map_adds_the_tell_id_column(self):
        text = reference_text("04-ban-do-loi-cach-sua.md")
        self.assertIn("tell_id", text)
        self.assertGreaterEqual(
            len(set(re.findall(r"`(T\d{2})`", text))), 8, "Bản đồ phải nối được ít nhất 8 họ tell"
        )

    def test_error_map_allows_a_null_tell_id(self):
        text = reference_text("04-ban-do-loi-cach-sua.md")
        self.assertIn("`null`", text)


class SpellingReferenceTests(unittest.TestCase):
    def test_spelling_reference_records_the_copyleft_finding_and_refuses_to_vendor(self):
        text = reference_text("05-chinh-ta.md")
        self.assertIn("GPLv2", text)
        self.assertIn("không vendor", text.lower())
        self.assertIn("tự cài", text)

    def test_spelling_reference_refuses_typos_as_an_authorship_signal(self):
        text = reference_text("05-chinh-ta.md")
        self.assertIn("nói về **người gõ**", text)


class IdiomAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(THANH_NGU.read_text(encoding="utf-8"))

    def test_attribution_names_repo_license_and_pinned_sha(self):
        attribution = self.data["attribution"]
        self.assertIn("ReML-AI/VIVID", attribution["source_repo"])
        self.assertEqual(attribution["license"], "MIT")
        self.assertRegex(attribution["repo_commit"], r"^[0-9a-f]{40}$")
        self.assertRegex(attribution["source_file_blob_sha"], r"^[0-9a-f]{40}$")

    def test_attribution_carries_the_mit_notice_it_is_required_to_carry(self):
        """MIT đặt đúng MỘT điều kiện: giữ notice khi phân phối lại. Không giữ là vi phạm."""
        attribution = self.data["attribution"]
        self.assertRegex(attribution["copyright_notice"], r"(?i)^copyright \(c\) \d{4} ")
        notice = attribution["license_notice"]
        self.assertIn("Permission is hereby granted", notice)
        self.assertIn(
            "The above copyright notice and this permission notice shall be included",
            notice,
            "Thiếu đúng câu ràng buộc của MIT thì notice chỉ là trang trí",
        )
        self.assertIn("WITHOUT WARRANTY OF ANY KIND", notice)

    def test_subset_is_selective_not_the_whole_corpus(self):
        selection = self.data["selection"]
        self.assertEqual(selection["selected"], len(self.data["entries"]))
        self.assertLess(
            selection["selected"],
            selection["source_total"] // 10,
            "Tập con phải là tập con thật, không phải bê cả kho vào",
        )
        self.assertTrue(selection["criteria_keep"])
        self.assertTrue(selection["criteria_drop"])

    def test_every_entry_has_the_four_required_fields(self):
        seen = set()
        for entry in self.data["entries"]:
            with self.subTest(entry=entry.get("id")):
                for field in ("id", "thanh_ngu", "nghia", "ngu_canh", "the_loai"):
                    self.assertTrue(entry.get(field), f"Thiếu trường {field}")
                self.assertNotIn(entry["id"], seen, "id trùng")
                seen.add(entry["id"])

    def test_every_declared_genre_is_allowed_and_research_is_excluded(self):
        allowed = set(self.data["the_loai_hop_le"])
        self.assertNotIn("research", allowed, "§4 của research.md cấm thêm sắc thái đánh giá")
        for entry in self.data["entries"]:
            with self.subTest(entry=entry["id"]):
                self.assertFalse(set(entry["the_loai"]) - allowed)

    def test_usage_rules_forbid_sprinkling_idioms(self):
        rules = " ".join(self.data["usage_rules"])
        self.assertIn("THAY THẾ", rules)
        self.assertIn("research", rules)
        self.assertIn("Writer profile thắng", rules)


class TellRegistryTests(unittest.TestCase):
    """Danh mục tell mà trục 4 đọc: phải là tiếng Việt, không phải blacklist dịch."""

    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(TELLS.read_text(encoding="utf-8"))

    def test_no_english_style_blacklist_leaked_into_the_examples(self):
        for entry in self.data["entries"]:
            blob = " ".join(
                str(entry.get(field) or "")
                for field in ("vi_example", "vi_counterexample", "fix", "name")
            ).lower()
            for word in ENGLISH_SLOP:
                with self.subTest(entry=entry["id"], word=word):
                    self.assertNotIn(
                        word, blob, f"{entry['id']} chứa từ tiếng Anh dịch từ blacklist: {word}"
                    )

    def test_pattern_seven_is_still_empty_and_needs_corpus(self):
        entry = next(item for item in self.data["entries"] if item["id"] == "T07")
        self.assertEqual(entry["status"], "needs_corpus")
        for field in ("vi_example", "vi_counterexample", "fix"):
            self.assertEqual(entry[field], "", f"{field} phải để rỗng cho tới khi có corpus")

    def test_rejected_english_patterns_are_still_rejected(self):
        names = " ".join(item["name"] for item in self.data["excluded_patterns"]).lower()
        self.assertIn("em dash", names)
        self.assertIn("ngoặc kép cong", names)


class PolishCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_polish_check()

    def test_facts_added_is_fail_closed(self):
        problems = self.module.check_facts({"facts_added": ["48% học sinh"], "facts_removed": []})
        self.assertTrue(problems)
        self.assertIn("facts_added", problems[0])

    def test_facts_removed_is_fail_closed(self):
        problems = self.module.check_facts({"facts_added": [], "facts_removed": ["(OECD, 2023)"]})
        self.assertTrue(problems)

    def test_missing_facts_fields_are_fail_closed_too(self):
        self.assertTrue(self.module.check_facts({}))

    def test_empty_facts_pass(self):
        self.assertEqual(self.module.check_facts({"facts_added": [], "facts_removed": []}), [])

    def test_cli_returns_the_fail_closed_exit_code(self):
        text = "Đây là một câu đủ dài để bộ tách câu giữ lại. " * 12
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            (tmpdir / "before.md").write_text(text, encoding="utf-8")
            (tmpdir / "after.md").write_text(text, encoding="utf-8")
            diff = {
                "schema_version": "1.0",
                "genre": "essay",
                "source_declared": {"how": "user_declared", "user_statement": "Bài của tôi."},
                "edits": [],
                "facts_added": ["một con số mới"],
                "facts_removed": [],
                "counters_before": {},
                "counters_after": {},
                "metadata": {"stylometric_polish": True, "forensics_score_seen": False},
            }
            (tmpdir / "polish.diff.json").write_text(
                json.dumps(diff, ensure_ascii=False), encoding="utf-8"
            )
            with contextlib.redirect_stdout(io.StringIO()):
                code = self.module.main(
                    [
                        "--before", str(tmpdir / "before.md"),
                        "--after", str(tmpdir / "after.md"),
                        "--genre", "essay",
                        "--diff", str(tmpdir / "polish.diff.json"),
                    ]
                )
            self.assertEqual(code, self.module.EXIT_FAIL)
            written = json.loads((tmpdir / "polish.diff.json").read_text(encoding="utf-8"))
            self.assertTrue(written["counters_before"], "counters_before phải được ghi vào diff")
            self.assertTrue(written["counters_after"], "counters_after phải được ghi vào diff")

    def test_baseline_is_read_from_the_tell_registry_before_reporting_counters(self):
        """Thể loại VN có genre_baseline: NOMINAL và TEMPLATES không phải chỗ phải sửa."""
        baseline = self.module.baseline_counters("bao-cao-thuc-tap")
        self.assertIn("NOMINAL", baseline)
        self.assertIn("T13", baseline["NOMINAL"])
        self.assertIn("TEMPLATES", baseline)

    def test_genre_without_baseline_gets_no_label_from_the_registry(self):
        self.assertEqual(self.module.baseline_counters("essay"), {})
        self.assertEqual(self.module.baseline_counters(""), {})

    def test_section_five_is_the_second_baseline_source(self):
        """Hai nguồn baseline, hợp nhất bằng phép HỢP — §5 vẫn phải sống sau khi thống nhất slug.

        Phase 1b đã thêm `research` vào `genre_baseline` của T13, nên nguồn thứ nhất
        (danh mục tell) từ nay cũng biết cột NOMINAL là baseline của bài nghiên cứu.
        Nguồn thứ hai không vì thế mà thừa: §5 của `research.md` khai những tín hiệu
        KHÔNG ứng với mục tell nào có cột counter — cấu trúc IMRAD lặp lại và cụm quy
        ước mở đầu — nên chỉ đọc danh mục tell là bỏ mất cột TEMPLATES.
        """
        signals = self.module.genre_normal_signals("research")
        self.assertTrue(signals)
        from_signals = self.module.baseline_from_signals(signals)
        self.assertIn("NOMINAL", from_signals)
        self.assertIn("TEMPLATES", from_signals)
        from_registry = self.module.baseline_counters("research")
        self.assertIn("NOMINAL", from_registry, "Phase 1b: T13 phải khai research")
        self.assertNotIn(
            "TEMPLATES",
            from_registry,
            "Nếu danh mục tell đã phủ cả TEMPLATES thì test này phải được viết lại, "
            "không phải xoá: điểm cần khoá là §5 vẫn được đọc",
        )

    def test_missing_genre_profile_is_reported_as_unknown_not_as_no_baseline(self):
        self.assertIsNone(self.module.genre_normal_signals("khong-co-the-loai-nay"))

    def test_counter_rows_label_baseline_columns(self):
        before = {
            "G1_khuon_hinh_thuc": {"template_repeats": {}, "sentence_len": {"cv": 0.5}},
            "G2_tu_vung": {"nominalisation": {"per_1000_syllables": 7.0}, "english_gloss": {}},
        }
        rows = self.module.counter_rows(
            before, before, {"NOMINAL": ["T13"]}, {"TEMPLATES": ["một tín hiệu §5"]}
        )
        by_column = {row["column"]: row for row in rows}
        self.assertTrue(by_column["NOMINAL"]["baseline_the_loai"])
        self.assertTrue(by_column["TEMPLATES"]["baseline_the_loai"])
        self.assertFalse(by_column["SENTENCE_CV"]["baseline_the_loai"])
        rendered = self.module.render(rows, [], [], [])
        self.assertIn("baseline thể loại", rendered)
        self.assertIn("KHÔNG phải chỗ phải sửa", rendered)

    def test_essay_gets_no_templates_baseline_label(self):
        """§5 của essay khai CỤM CHUYỂN ĐOẠN là bình thường; cột TEMPLATES đếm KHUÔN CÂU GHÉP ĐÔI.

        Hai thứ khác nhau. Dán nhãn "baseline thể loại" lên TEMPLATES của bài luận là bảo người sửa
        bỏ qua đúng cột đang đo thứ mà `essay.md` §2 CẤM sinh ra. Nguồn: cổng Phase 5.
        """
        from_signals = self.module.baseline_from_signals(self.module.genre_normal_signals("essay"))
        self.assertNotIn("TEMPLATES", from_signals)
        self.assertEqual({}, self.module.baseline_counters("essay"))
        rows = self.module.counter_rows({}, {}, self.module.baseline_counters("essay"), from_signals)
        by_column = {row["column"]: row for row in rows}
        self.assertFalse(by_column["TEMPLATES"]["baseline_the_loai"])

    def test_a_section_five_signal_that_names_a_tell_maps_explicitly(self):
        """Đường tường minh: §5 nêu mã tell thì không phải dò từ khoá nữa."""
        mapped = self.module.baseline_from_signals(
            ["Bộ ba danh từ song hành trong câu tổng kết (T10): phép tu từ được dạy"]
        )
        self.assertIn("TEMPLATES", mapped)
        self.assertEqual(
            {}, self.module.baseline_from_signals(["Một tín hiệu không nói về cột nào cả"])
        )

    def test_missing_provenance_sidecar_is_a_warning_not_a_silent_pass(self):
        """Ranh giới đạo đức của trục 4 phải quan sát được TỪ BẢN GIAO, không chỉ từ thư mục ca."""
        with tempfile.TemporaryDirectory() as tmp:
            after = Path(tmp) / "polished.md"
            after.write_text("Một câu đủ dài để không ai nhầm nó với mảnh cụt.", encoding="utf-8")
            warnings = self.module.check_provenance(after, after.read_text(encoding="utf-8"))
            self.assertTrue(warnings)
            self.assertIn("polished.provenance.json", warnings[0])

    def test_provenance_sidecar_next_to_the_delivered_file_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            after = Path(tmp) / "polished.md"
            after.write_text("Một câu đủ dài để không ai nhầm nó với mảnh cụt.", encoding="utf-8")
            sidecar = {
                "schema_version": "1.0",
                "genre": "essay",
                "origin": {
                    "sentences_total": 1,
                    "machine_pct": 100.0,
                    "machine_edited_pct": 0.0,
                    "human_pct": 0.0,
                },
                "model": {"name": "test"},
                "stylometric_polish": True,
                "draft_meta_sha256": "0" * 64,
            }
            self.module.provenance_path_for(after).write_text(
                json.dumps(sidecar, ensure_ascii=False), encoding="utf-8"
            )
            self.assertEqual(
                [], self.module.check_provenance(after, after.read_text(encoding="utf-8"))
            )

    def test_an_html_comment_footer_counts_as_provenance_too(self):
        """Người dùng được chọn footer thay sidecar; điều bắt buộc là bản giao MANG bản tự khai."""
        with tempfile.TemporaryDirectory() as tmp:
            after = Path(tmp) / "polished.md"
            payload = {
                "schema_version": "1.0",
                "genre": "essay",
                "origin": {
                    "sentences_total": 1,
                    "machine_pct": 100.0,
                    "machine_edited_pct": 0.0,
                    "human_pct": 0.0,
                },
                "model": {"name": "test"},
                "stylometric_polish": True,
                "draft_meta_sha256": "0" * 64,
            }
            body = "Một câu đủ dài để không ai nhầm nó với mảnh cụt."
            footer = "<!-- provenance: " + json.dumps(payload, ensure_ascii=False) + " -->"
            after.write_text(body + chr(10) + chr(10) + footer, encoding="utf-8")
            text = after.read_text(encoding="utf-8")
            data, source = self.module.load_provenance(after, text)
            self.assertEqual(source, "footer")
            self.assertEqual([], self.module.check_provenance(after, text))

    def test_provenance_that_lies_about_polishing_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            after = Path(tmp) / "polished.md"
            after.write_text("Một câu đủ dài để không ai nhầm nó với mảnh cụt.", encoding="utf-8")
            self.module.provenance_path_for(after).write_text(
                json.dumps({"schema_version": "1.0", "stylometric_polish": False}),
                encoding="utf-8",
            )
            warnings = self.module.check_provenance(after, after.read_text(encoding="utf-8"))
            self.assertTrue(any("stylometric_polish" in item for item in warnings))

    def test_route_to_warnings_survive_the_merge(self):
        """Cảnh báo dạng object là việc trục 4 CỐ Ý KHÔNG LÀM — gộp kiểu cũ sẽ làm rơi nó."""
        routed = {
            "message": "must_fix F2 đòi hạ mức khẳng định — việc của vòng viết lại.",
            "route_to": "02-cowriter:round2",
        }
        merged = self.module.merge_warnings([routed, "b"], ["a", "b"])
        self.assertIn(routed, merged)
        self.assertEqual(["a", "b"], [item for item in merged if isinstance(item, str)])

    def test_burstiness_warning_fires_on_a_sharp_cv_jump(self):
        before = {"G1_khuon_hinh_thuc": {"sentence_len": {"cv": 0.40}}}
        after = {"G1_khuon_hinh_thuc": {"sentence_len": {"cv": 0.62}}}
        warnings = self.module.check_burstiness(before, after)
        self.assertTrue(warnings)
        self.assertIn("burstiness", warnings[0])

    def test_burstiness_warning_stays_quiet_on_a_normal_edit(self):
        before = {"G1_khuon_hinh_thuc": {"sentence_len": {"cv": 0.763}}}
        after = {"G1_khuon_hinh_thuc": {"sentence_len": {"cv": 0.761}}}
        self.assertEqual(self.module.check_burstiness(before, after), [])

    def test_short_sentence_ratio_jump_is_its_own_warning(self):
        same = {"G1_khuon_hinh_thuc": {"sentence_len": {"cv": 0.5}}}
        warnings = self.module.check_burstiness(same, same, 0.20, 0.38)
        self.assertTrue(warnings)
        self.assertIn("âm tiết", warnings[0])

    def test_metadata_warnings_cover_the_three_ethical_flags(self):
        warnings = " ".join(
            self.module.check_metadata({"metadata": {"stylometric_polish": False,
                                                     "forensics_score_seen": True}})
        )
        self.assertIn("stylometric_polish", warnings)
        self.assertIn("forensics_score_seen", warnings)
        self.assertIn("source_declared", warnings)

    def test_script_calls_no_model(self):
        source = SCRIPT.read_text(encoding="utf-8")
        for forbidden in ("anthropic", "openai", "requests.post", "urllib.request"):
            self.assertNotIn(forbidden, source, f"Cổng 0-token không được gọi mạng: {forbidden}")


class NewTokenTests(unittest.TestCase):
    """So tập token số và tên viết hoa — cổng Phase 3, Fable 30/08, rủi ro số 4.

    `facts_added` rỗng KHÔNG chứng minh được là không có fact mới, vì trường ấy do chính người
    vừa sửa khai. Phép so dưới đây không tin lời khai; nó đọc thẳng hai bản văn.
    """

    @classmethod
    def setUpClass(cls):
        cls.module = load_polish_check()

    def test_a_fabricated_number_shows_up_as_a_new_token(self):
        before = "Nhà trường đã tập huấn cho giáo viên trong năm 2023."
        after = (
            "Nhà trường đã tập huấn cho giáo viên trong năm 2023. "
            "Khảo sát nội bộ cho thấy 63,5% giáo viên đã dự đủ ba buổi."
        )
        found = self.module.new_tokens(before, after)
        self.assertIn("63,5%", found["numbers"])

    def test_a_fabricated_organisation_shows_up_as_a_new_name(self):
        before = "Nhà trường đã tập huấn cho giáo viên trong năm 2023."
        after = (
            "Nhà trường đã tập huấn cho giáo viên trong năm 2023, "
            "theo báo cáo của Viện Khoa học Giáo dục."
        )
        found = self.module.new_tokens(before, after)
        self.assertIn("Viện", found["names"])

    def test_an_untouched_text_reports_nothing(self):
        text = "Tổ chuyên môn họp ngày 12/9. Cô Hoa báo cáo 24 tiết dự giờ trong học kỳ."
        self.assertEqual(
            self.module.new_tokens(text, text), {"numbers": [], "names": []}
        )

    def test_reformatting_a_number_is_not_a_new_fact(self):
        """`1.000` -> `1000` là sửa cách trình bày, không phải thêm số liệu."""
        before = "Trường có 1.000 học sinh và 0,5 suất ăn dự phòng mỗi lớp."
        after = "Trường có 1000 học sinh. Mỗi lớp có 0.5 suất ăn dự phòng."
        self.assertEqual(self.module.new_tokens(before, after)["numbers"], [])

    def test_splitting_a_sentence_does_not_invent_a_name(self):
        """Tách câu đẩy một từ lên đầu câu; tiếng Việt viết hoa đầu câu nên đó không phải tên mới."""
        before = "Cô Hoa dạy lớp 6A và thầy Nam dạy lớp 6B trong học kỳ này."
        after = "Cô Hoa dạy lớp 6A. Thầy Nam dạy lớp 6B trong học kỳ này."
        self.assertEqual(self.module.new_tokens(before, after)["names"], [])

    def test_a_new_sentence_initial_capital_is_not_reported(self):
        """Ngưỡng thấp có chủ ý: đầu câu là vùng mù, đổi lại là không báo oan mỗi lần tách câu."""
        before = "Kết quả cho thấy tỷ lệ đạt tăng."
        after = "Kết quả cho thấy tỷ lệ đạt tăng. Nhiều lớp giữ được nhịp học."
        self.assertEqual(self.module.new_tokens(before, after)["names"], [])

    def test_an_acronym_counts_even_at_the_start_of_a_sentence(self):
        before = "Báo cáo nêu kết quả kiểm tra giữa kỳ."
        after = "Báo cáo nêu kết quả kiểm tra giữa kỳ. OECD xếp Việt Nam ở nhóm giữa."
        self.assertIn("OECD", self.module.new_tokens(before, after)["names"])

    def test_a_name_already_present_anywhere_before_is_not_new(self):
        """Tên đứng đầu câu ở bản trước vẫn tính là đã có — nếu không thì mỗi lần gộp câu là một báo oan."""
        before = "Hoa phụ trách lớp 6A. Tổ đã họp xong."
        after = "Tổ đã họp xong, cô Hoa phụ trách lớp 6A."
        self.assertEqual(self.module.new_tokens(before, after)["names"], [])

    def test_the_warning_lists_the_offending_tokens(self):
        before = "Tổ chuyên môn họp ngày 12/9."
        after = "Tổ chuyên môn họp ngày 12/9. Sở Giáo dục yêu cầu nộp trước 30/9."
        warnings = self.module.check_new_tokens(before, after)
        joined = " ".join(warnings)
        self.assertIn("30/9", joined)
        self.assertIn("Giáo", joined)
        self.assertIn("facts_added", joined)

    def test_no_warning_when_nothing_new_appeared(self):
        text = "Tổ chuyên môn họp ngày 12/9. Cô Hoa báo cáo 24 tiết dự giờ."
        self.assertEqual(self.module.check_new_tokens(text, text), [])

    def test_cli_warns_with_exit_code_one_on_a_fabricated_fact(self):
        base = "Nhà trường tổ chức tập huấn cho giáo viên trong năm học vừa qua. " * 8
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            (tmpdir / "before.md").write_text(base, encoding="utf-8")
            (tmpdir / "after.md").write_text(
                base + "Khảo sát của Viện Khoa học Giáo dục cho thấy 63,5% giáo viên đã dự đủ.",
                encoding="utf-8",
            )
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = self.module.main(
                    [
                        "--before", str(tmpdir / "before.md"),
                        "--after", str(tmpdir / "after.md"),
                        "--genre", "essay",
                    ]
                )
            self.assertEqual(code, self.module.EXIT_WARN)
            output = buffer.getvalue()
            self.assertIn("63,5%", output)
            self.assertIn("Viện", output)


class ScenarioTests(unittest.TestCase):
    def test_formal_human_scenario_protects_the_report_skeleton(self):
        self.assertTrue(SCENARIO.is_file(), "Thiếu kịch bản 04-van-nguoi-trang-trong.md")
        text = SCENARIO.read_text(encoding="utf-8")
        for part in ("Kết quả đạt được", "Tồn tại", "Phương hướng"):
            self.assertIn(part, text, f"Kịch bản phải nêu mục '{part}' là vùng không được xoá")
        for tell in ("T06", "T10", "T13"):
            self.assertIn(tell, text)

    def test_scenario_caps_the_number_of_edits(self):
        text = SCENARIO.read_text(encoding="utf-8")
        self.assertIn("không vượt quá một", text, "Kịch bản phải đặt ngưỡng số nhát sửa")

    def test_scenario_refuses_to_infer_authorship(self):
        text = SCENARIO.read_text(encoding="utf-8")
        self.assertIn("không phải bằng chứng bài do máy viết", text)

    def test_scenario_expects_a_valid_diff_shape(self):
        text = SCENARIO.read_text(encoding="utf-8")
        self.assertIn("facts_added", text)
        self.assertIn("stylometric_polish", text)


if __name__ == "__main__":
    unittest.main()
