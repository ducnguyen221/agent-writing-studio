import json
import math
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from shared.scripts.scoring import score_evidence

        cls.score_evidence = staticmethod(score_evidence)
        cls.rules = json.loads(
            (ROOT / "shared/rules/forensics-scoring-v3.json").read_text(encoding="utf-8")
        )

    def reading(self, labels, group_scores=None):
        return {
            "sealed_before_counters": True,
            "sentences": [
                {"id": f"s{i:04d}", "label": label}
                for i, label in enumerate(labels, start=1)
            ],
            "group_scores": group_scores or {"G1": 0, "G2": 0, "G3": 0, "G4": 0},
            "limitations": ["Chưa có corpus mốc cùng thể loại."],
        }

    def test_same_input_produces_same_output(self):
        reading = self.reading(
            ["FLAG", "NOTE", "PLAIN", "SKIP"],
            {"G1": 18, "G2": 17, "G3": 11, "G4": 18},
        )
        first = self.score_evidence(reading, genre="essay", rules=self.rules)
        second = self.score_evidence(reading, genre="essay", rules=self.rules)
        self.assertEqual(first, second)
        first_bytes = json.dumps(first, ensure_ascii=False, sort_keys=True).encode("utf-8")
        second_bytes = json.dumps(second, ensure_ascii=False, sort_keys=True).encode("utf-8")
        self.assertEqual(first_bytes, second_bytes)
        self.assertNotIn("ai_probability", first)

    def test_vocab_and_form_only_cannot_reach_priority_check(self):
        result = self.score_evidence(
            self.reading(["FLAG"] * 5, {"G1": 30, "G2": 20, "G3": 0, "G4": 0}),
            genre="essay",
            rules=self.rules,
        )
        self.assertEqual(result["review_priority"], 30)
        self.assertEqual(result["label"], "worth_reviewing")

    def test_coverage_excludes_skip_and_weights_note(self):
        result = self.score_evidence(
            self.reading(["FLAG", "NOTE", "PLAIN", "SKIP"]),
            genre="essay",
            rules=self.rules,
        )
        self.assertEqual(result["ai_signal_coverage"]["eligible_sentence_count"], 3)
        self.assertEqual(result["ai_signal_coverage"]["flag_count"], 1)
        self.assertEqual(result["ai_signal_coverage"]["note_count"], 1)
        self.assertEqual(result["ai_signal_coverage"]["percent"], 46.7)

    def test_unsealed_reading_is_rejected(self):
        reading = self.reading(["PLAIN"])
        reading["sealed_before_counters"] = False
        with self.assertRaisesRegex(ValueError, "đọc mù"):
            self.score_evidence(reading, genre="essay", rules=self.rules)

    def test_string_false_cannot_bypass_blind_reading_seal(self):
        reading = self.reading(["PLAIN"])
        reading["sealed_before_counters"] = "false"
        with self.assertRaisesRegex(ValueError, "đọc mù"):
            self.score_evidence(reading, genre="essay", rules=self.rules)

    def test_calibration_flag_must_be_boolean(self):
        with self.assertRaisesRegex(ValueError, "calibrated"):
            self.score_evidence(
                self.reading(["PLAIN"]),
                genre="essay",
                rules=self.rules,
                calibration={"calibrated": "false"},
            )

    def test_non_finite_group_score_is_rejected(self):
        for invalid in (math.nan, math.inf, -math.inf):
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(ValueError, "hữu hạn"):
                    self.score_evidence(
                        self.reading(
                            ["PLAIN"],
                            {"G1": invalid, "G2": 0, "G3": 0, "G4": 0},
                        ),
                        genre="essay",
                        rules=self.rules,
                    )

    def test_non_finite_calibration_margin_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "hữu hạn"):
            self.score_evidence(
                self.reading(["PLAIN"]),
                genre="essay",
                rules=self.rules,
                calibration={
                    "calibrated": True,
                    "review_priority_margin": math.nan,
                    "coverage_margin": 10,
                },
            )

    def test_uncalibrated_result_has_wide_ranges(self):
        result = self.score_evidence(
            self.reading(["FLAG", "PLAIN"], {"G1": 10, "G2": 5, "G3": 20, "G4": 10}),
            genre="essay",
            rules=self.rules,
        )
        self.assertEqual(result["review_priority_range"], {"low": 20, "high": 70, "calibrated": False})
        self.assertEqual(result["ai_signal_coverage"]["low"], 40.0)
        self.assertEqual(result["ai_signal_coverage"]["high"], 60.0)

    def test_conflict_checks_are_explicit(self):
        result = self.score_evidence(
            self.reading(
                ["FLAG"] + ["PLAIN"] * 19,
                {"G1": 20, "G2": 10, "G3": 20, "G4": 20},
            ),
            genre="essay",
            rules=self.rules,
        )
        self.assertIn("document_level_signal", result["conflict_checks"])

    def test_no_eligible_sentence_returns_insufficient_evidence(self):
        result = self.score_evidence(
            self.reading(["SKIP", "SKIP"]), genre="essay", rules=self.rules
        )
        self.assertEqual(result["label"], "insufficient_evidence")
        self.assertNotIn("ai_probability", result)


class ClusterRequirementTests(unittest.TestCase):
    """Luật cụm: tín hiệu đứng CỤM mới được cộng điểm G1/G2.

    Một khuôn tu từ lẻ, một câu danh từ hoá lẻ là văn người bình thường. Cái phân biệt được
    dáng máy là NHIỀU HỌ dồn về một chỗ, hoặc MỘT HỌ lặp như phản xạ. Chấm điểm tín hiệu lẻ
    là chấm xác suất nền của tiếng Việt — đúng cơ chế sinh ra báo oan.

    Ba file phải nói cùng một luật, nếu không thì rule máy đọc và luật người đọc trôi khỏi nhau.
    """

    @classmethod
    def setUpClass(cls):
        cls.rules = json.loads(
            (ROOT / "shared/rules/forensics-scoring-v3.json").read_text(encoding="utf-8")
        )
        cls.reference = (
            ROOT / "skills/05-forensics/references/09-cham-diem-agent-first.md"
        ).read_text(encoding="utf-8")
        cls.skill = (ROOT / "skills/05-forensics/05b-scoring/SKILL.md").read_text(encoding="utf-8")

    def test_rules_declare_the_cluster_requirement(self):
        cluster = self.rules["cluster_requirement"]
        self.assertEqual(cluster["applies_to_groups"], ["G1", "G2"])
        self.assertEqual(cluster["distinct_families_in_one_paragraph"], 2)
        self.assertEqual(cluster["same_family_repeats_in_document"], 3)
        self.assertEqual(cluster["solo_signal_max_label"], "NOTE")
        self.assertIs(cluster["solo_signal_scores"], False)

    def test_cluster_requirement_does_not_change_the_existing_caps(self):
        """Luật cụm thêm ĐIỀU KIỆN, không đổi THANG. Trần G1/G2 phải nguyên như cũ."""
        self.assertEqual(self.rules["group_caps"]["G1"], 30)
        self.assertEqual(self.rules["group_caps"]["G2"], 20)
        self.assertEqual(self.rules["group_caps"]["G3"], 25)
        self.assertEqual(self.rules["group_caps"]["G4"], 25)
        self.assertEqual(self.rules["sentence_weights"], {"PLAIN": 0.0, "NOTE": 0.4, "FLAG": 1.0})

    def test_reference_states_the_cluster_rule_as_a_general_law(self):
        text = self.reference
        self.assertIn("cluster_requirement", text, "reference phải trỏ tới rule máy đọc")
        self.assertIn("≥2 họ tín hiệu khác nhau", text)
        self.assertIn("≥3 lượt", text)
        self.assertIn("không bao giờ `FLAG`", text)
        self.assertIn(
            "không đổi thang",
            text.lower(),
            "phải nói rõ luật cụm không đụng tới trần G1≤30 / G2≤20",
        )

    def test_reference_explains_why_a_solo_signal_is_not_evidence(self):
        flat = " ".join(self.reference.split())
        self.assertIn("văn người bình thường", flat, "phải nói rõ vì sao tell lẻ không phải bằng chứng")
        self.assertIn("báo oan", flat)

    def test_scoring_skill_carries_the_same_rule(self):
        text = self.skill
        self.assertIn("cluster_requirement", text)
        self.assertIn("≥2 họ tín hiệu khác nhau", text)
        self.assertIn("≥3 lượt", text)
        self.assertIn("không cộng điểm", text)

    def test_humanizer_orders_edits_by_cluster_density(self):
        """Trục 4 dùng cùng ranh giới ấy để xếp thứ tự sửa, không để buộc tội."""
        text = (
            ROOT / "skills/04-humanizer/references/04-ban-do-loi-cach-sua.md"
        ).read_text(encoding="utf-8")
        self.assertIn("cụm trước, lẻ sau", text)
        self.assertIn("09-cham-diem-agent-first.md", text)
        self.assertIn("lượt hai", text)


if __name__ == "__main__":
    unittest.main()
