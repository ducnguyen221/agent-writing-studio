"""Danh mục tell tiếng Việt — `shared/rules/vi-ai-tells.json`.

Đây là file dễ gây hại nhất trong repo: một danh sách tín hiệu áp lên văn hành chính
và học thuật tiếng Việt vốn công thức. Test dưới đây là hàng rào, không phải thủ tục.

Ba điều được canh:
1. Mỗi mục phải có ví dụ Việt VÀ phản chứng Việt. Không phản chứng thì không được tồn tại.
2. Đợt này không mục nào được `calibrated` — nghĩa là trục 5 chưa được dùng file này để
   buộc tội ai.
3. Máy chấm (`scoring.py`, `forensics-scoring-v3.json`, registry rule) KHÔNG được tham
   chiếu mục `candidate`.
"""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "shared/rules/vi-ai-tells.json"

FAMILIES = {"G1", "G2", "G3", "G4"}
STATUSES = {"candidate", "calibrated", "needs_corpus"}
EXCLUDED_UPSTREAM = {14, 15, 17, 19, 26}
BASELINE_REQUIRED = {"T06", "T10"}
VN_ADMIN_GENRES = {"bao-cao-thuc-tap", "sang-kien-kinh-nghiem", "chinh-luan"}

REQUIRED_KEYS = {
    "id",
    "family",
    "name",
    "label",
    "what",
    "vi_example",
    "vi_counterexample",
    "genre_baseline",
    "fix",
    "status",
    "source",
}


def registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def entries():
    return registry()["entries"]


class TellsRegistryTests(unittest.TestCase):
    def test_registry_shape(self):
        data = registry()
        self.assertEqual(data["schema_version"], "1.0")
        for key in ("purpose", "provenance", "families", "status_meaning", "usage_rules", "entries"):
            self.assertIn(key, data, f"Thiếu khoá gốc {key}")
        self.assertEqual(set(data["families"]), FAMILIES)
        self.assertGreaterEqual(len(data["entries"]), 25, "Phải có ít nhất 25 họ tell")

    def test_every_entry_has_required_keys_and_unique_id(self):
        seen_ids, seen_names = set(), set()
        for entry in entries():
            with self.subTest(tell=entry.get("id")):
                missing = REQUIRED_KEYS - set(entry)
                self.assertFalse(missing, f"{entry.get('id')}: thiếu khoá {sorted(missing)}")
                self.assertRegex(entry["id"], r"^T\d{2}$")
                self.assertNotIn(entry["id"], seen_ids, f"Trùng id {entry['id']}")
                seen_ids.add(entry["id"])
                self.assertRegex(entry["name"], r"^[a-z][a-z0-9_]*$", "name phải là snake_case")
                self.assertNotIn(entry["name"], seen_names, f"Trùng name {entry['name']}")
                seen_names.add(entry["name"])
                self.assertIn(entry["family"], FAMILIES)
                self.assertIn(entry["status"], STATUSES)
                self.assertIsInstance(entry["genre_baseline"], list)
                self.assertIsInstance(entry["source"], list)
                self.assertTrue(entry["source"], f"{entry['id']}: source rỗng")
                self.assertTrue(entry["what"].strip(), f"{entry['id']}: what rỗng")

    def test_candidate_entries_have_vietnamese_example_and_counterexample(self):
        for entry in entries():
            if entry["status"] == "needs_corpus":
                continue
            with self.subTest(tell=entry["id"]):
                for key in ("vi_example", "vi_counterexample", "fix"):
                    self.assertTrue(
                        entry[key].strip(),
                        f"{entry['id']}: {key} rỗng — mục không có phản chứng thì không được tồn tại",
                    )
                # Ví dụ và phản chứng phải khác nhau thật sự, không phải chép lại nhau.
                self.assertNotEqual(
                    entry["vi_example"].strip(),
                    entry["vi_counterexample"].strip(),
                    f"{entry['id']}: phản chứng trùng ví dụ",
                )
                self.assertGreater(
                    len(entry["vi_counterexample"]),
                    30,
                    f"{entry['id']}: phản chứng quá ngắn để đứng vững",
                )

    def test_needs_corpus_entries_are_deliberately_empty(self):
        blocked = [e for e in entries() if e["status"] == "needs_corpus"]
        self.assertTrue(blocked, "Phải còn ít nhất một mục needs_corpus (pattern 7)")
        for entry in blocked:
            with self.subTest(tell=entry["id"]):
                for key in ("vi_example", "vi_counterexample", "fix"):
                    self.assertEqual(
                        entry[key],
                        "",
                        f"{entry['id']}: mục needs_corpus PHẢI để rỗng, không được điền tạm",
                    )
                self.assertTrue(entry.get("blocked_reason", "").strip())
                self.assertTrue(entry.get("corpus_requirement", "").strip())

    def test_no_entry_is_calibrated_in_this_round(self):
        calibrated = [e["id"] for e in entries() if e["status"] == "calibrated"]
        self.assertEqual(
            [],
            calibrated,
            "Đợt này chưa có corpus. Mục calibrated cho phép trục 5 tạo finding — chưa được.",
        )

    def test_excluded_english_only_patterns_stay_out(self):
        data = registry()
        recorded = set()
        for item in data["excluded_patterns"]:
            number = int(item["source"].rsplit("#", 1)[1])
            recorded.add(number)
            self.assertTrue(item["why"].strip(), f"Pattern {number}: phải ghi lý do loại")
        self.assertEqual(
            EXCLUDED_UPSTREAM,
            recorded,
            "Phải ghi rõ đã loại pattern 14/15/17/19/26 và vì sao",
        )
        cited = {
            int(match)
            for entry in entries()
            for source in entry["source"]
            for match in re.findall(r"studio:catalog#(\d+)", source)
        }
        # 15 được gộp vào T16 ở dạng có nghĩa; các pattern còn lại không được xuất hiện.
        leaked = (cited & EXCLUDED_UPSTREAM) - {15}
        self.assertFalse(leaked, f"Pattern chỉ đúng cho tiếng Anh lọt vào danh mục: {sorted(leaked)}")

    def test_vietnamese_administrative_patterns_declare_genre_baseline(self):
        by_id = {e["id"]: e for e in entries()}
        for tell_id in BASELINE_REQUIRED:
            with self.subTest(tell=tell_id):
                self.assertIn(tell_id, by_id, f"Thiếu {tell_id}")
                baseline = set(by_id[tell_id]["genre_baseline"])
                self.assertTrue(
                    VN_ADMIN_GENRES <= baseline,
                    f"{tell_id}: phải khai {sorted(VN_ADMIN_GENRES)} là văn phong chuẩn, "
                    f"đang khai {sorted(baseline)}",
                )
                self.assertTrue(
                    by_id[tell_id].get("warning", "").strip(),
                    f"{tell_id}: phải có cảnh báo báo oan",
                )

    def test_merged_patterns_cite_both_sources(self):
        by_id = {e["id"]: e for e in entries()}
        merged = {
            "T09": "counters.py:TEMPLATES",
            "T13": "counters.py:NOMINAL",
        }
        for tell_id, needle in merged.items():
            with self.subTest(tell=tell_id):
                sources = " ".join(by_id[tell_id]["source"])
                self.assertIn("studio:catalog#", sources)
                self.assertIn(needle, sources, f"{tell_id}: phải ghi cả nguồn counters.py đã có")

    def test_merged_patterns_point_at_real_counters(self):
        counters = (ROOT / "skills/05-forensics/scripts/counters.py").read_text(encoding="utf-8")
        for entry in entries():
            for source in entry["source"]:
                if not source.startswith("counters.py:"):
                    continue
                symbol = source.split(":", 1)[1].split(".")[0]
                with self.subTest(symbol=symbol):
                    self.assertRegex(
                        counters,
                        rf"(?m)^{re.escape(symbol)}\s*=",
                        f"{entry['id']}: counters.py không có ký hiệu {symbol}",
                    )

    def test_the_three_tells_found_by_the_column_b_audit_are_registered(self):
        """Ba tật máy mà cả người chấm mù lẫn lớp 0-token đều bỏ lọt trong ca cột B.

        Chúng vào danh mục ở trạng thái `candidate`: trục 4 được dùng để nhận ra và sửa, trục 5
        KHÔNG được dùng để tạo finding cho tới khi có corpus. Nguồn: docs/results/self-audit-cot-B.md
        §5. Test khoá cả ba, vì thứ đắt nhất ở đây là ví dụ và phản chứng tiếng Việt tự soạn.
        """
        by_id = {e["id"]: e for e in entries()}
        expected = {
            "T36": ("G3", "vi_du_gia_dinh_thay_trai_nghiem"),
            "T37": ("G1", "cau_hoi_tu_tu_mo_doan"),
            "T38": ("G1", "phan_doi_doi_xung"),
        }
        for tell_id, (family, name) in expected.items():
            with self.subTest(tell=tell_id):
                self.assertIn(tell_id, by_id, f"Thiếu {tell_id}")
                entry = by_id[tell_id]
                self.assertEqual(entry["family"], family)
                self.assertEqual(entry["name"], name)
                self.assertEqual(entry["status"], "candidate")
                self.assertTrue(entry["vi_example"].strip())
                self.assertTrue(entry["vi_counterexample"].strip())
                self.assertTrue(
                    entry.get("warning", "").strip(),
                    f"{tell_id}: cả ba đều có thể báo oan một thể loại, phải có cảnh báo",
                )
                self.assertTrue(
                    any("self-audit-cot-B" in source for source in entry["source"]),
                    f"{tell_id}: phải ghi nguồn là ca đã tìm ra nó",
                )

    def test_counter_backed_tells_name_a_template_that_exists(self):
        """`counters.py:TEMPLATES.<khuôn>` phải trỏ tới một khoá CÓ THẬT trong TEMPLATES.

        Chỉ kiểm tên biến TEMPLATES thì đổi tên khuôn không ai biết, và mục tell sẽ chỉ vào một
        phép đếm không tồn tại.
        """
        counters = (ROOT / "skills/05-forensics/scripts/counters.py").read_text(encoding="utf-8")
        checked = 0
        for entry in entries():
            for source in entry["source"]:
                match = re.fullmatch(r"counters\.py:TEMPLATES\.(\w+)", source)
                if not match:
                    continue
                checked += 1
                with self.subTest(tell=entry["id"], template=match.group(1)):
                    self.assertIn(
                        f'"{match.group(1)}"',
                        counters,
                        f"{entry['id']}: TEMPLATES không có khuôn {match.group(1)}",
                    )
        self.assertGreaterEqual(checked, 4, "Phải còn ít nhất 4 mục tell nối thẳng vào TEMPLATES")

    def test_scoring_machinery_does_not_reference_candidate_tells(self):
        """Máy chấm không được biết tới mục chưa hiệu chỉnh.

        Nếu scoring.py hay bảng điểm forensics tham chiếu một tell `candidate`, thì trục 5
        đang buộc tội bằng một danh sách chưa qua corpus — đúng cái luật này cấm.
        """
        candidate_ids = {e["id"] for e in entries() if e["status"] != "calibrated"}
        candidate_names = {e["name"] for e in entries() if e["status"] != "calibrated"}
        watched = [
            ROOT / "shared/scripts/scoring.py",
            ROOT / "shared/rules/forensics-scoring-v3.json",
            ROOT / "shared/rules/forensic-rule-registry.json",
        ]
        for path in watched:
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            with self.subTest(file=path.name):
                self.assertNotIn(
                    "vi-ai-tells",
                    text,
                    f"{path.name} không được nạp danh mục tell khi chưa hiệu chỉnh",
                )
                hits = {tid for tid in candidate_ids if re.search(rf"\b{tid}\b", text)}
                self.assertFalse(hits, f"{path.name} tham chiếu tell candidate: {sorted(hits)}")
                name_hits = {name for name in candidate_names if name in text}
                self.assertFalse(
                    name_hits, f"{path.name} tham chiếu tell candidate: {sorted(name_hits)}"
                )

    def test_reading_skill_states_candidate_cannot_create_findings(self):
        skill = (ROOT / "skills/05a-reading/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("vi-ai-tells.json", skill, "05a-reading phải nói rõ nạp danh mục để làm gì")
        self.assertIn("vi_counterexample", skill)
        self.assertIn("genre_baseline", skill)
        self.assertIn("candidate", skill)
        self.assertLessEqual(len(skill.split()), 550, "05a-reading vượt 550 từ")


if __name__ == "__main__":
    unittest.main()
