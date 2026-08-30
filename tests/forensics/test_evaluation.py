import json
import unittest


class EvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from shared.scripts.evaluate import evaluate

        cls.evaluate = staticmethod(evaluate)

    def records(self):
        return [
            {
                "fixture_id": "h01",
                "language": "vi",
                "genre": "essay",
                "truth": "human",
                "label": "low_signal",
                "predicted_rule_ids": [],
                "supported_rule_ids": [],
            },
            {
                "fixture_id": "h02",
                "language": "vi",
                "genre": "essay",
                "truth": "human",
                "label": "priority_check",
                "predicted_rule_ids": ["G2-EMPTY-CLAIM"],
                "supported_rule_ids": [],
            },
            {
                "fixture_id": "a01",
                "language": "vi",
                "genre": "essay",
                "truth": "ai",
                "label": "priority_check",
                "predicted_rule_ids": ["G1-REPEATED-FRAME"],
                "supported_rule_ids": ["G1-REPEATED-FRAME"],
            },
            {
                "fixture_id": "m01",
                "language": "vi",
                "genre": "essay",
                "truth": "mixed",
                "label": "worth_reviewing",
                "predicted_rule_ids": ["G1-REPEATED-FRAME"],
                "supported_rule_ids": ["G1-REPEATED-FRAME"],
                "expected_spans": [[10, 30]],
                "predicted_spans": [[20, 40]],
            },
        ]

    def test_human_false_positive_rate_is_first_release_metric_with_interval(self):
        result = self.evaluate(self.records())
        self.assertEqual(result["human_priority_check_fpr"]["errors"], 1)
        self.assertEqual(result["human_priority_check_fpr"]["total"], 2)
        self.assertEqual(result["human_priority_check_fpr"]["rate"], 0.5)
        self.assertIn("wilson_95", result["human_priority_check_fpr"])

    def test_reports_ai_recall_rule_precision_and_mixed_span_overlap(self):
        result = self.evaluate(self.records())
        self.assertEqual(result["ai_priority_check_recall"]["rate"], 1.0)
        self.assertEqual(result["rule_precision"]["G1-REPEATED-FRAME"]["rate"], 1.0)
        self.assertEqual(result["mixed_span_iou"]["mean"], 0.3333)

    def test_output_is_aggregate_only_and_deterministic(self):
        first = self.evaluate(self.records())
        second = self.evaluate(list(reversed(self.records())))
        self.assertEqual(first, second)
        serialized = json.dumps(first, ensure_ascii=False).lower()
        self.assertNotIn("fixture_id", serialized)
        self.assertNotIn("h01", serialized)

    def test_rejects_source_text_fields(self):
        records = self.records()
        records[0]["quoted_text"] = "Nội dung riêng tư"
        with self.assertRaisesRegex(ValueError, "văn bản nguồn"):
            self.evaluate(records)

    def test_rejects_unknown_rule_id_that_could_leak_pii(self):
        records = self.records()
        records[0]["predicted_rule_ids"] = ["PRIVATE CUSTOMER NAME"]
        with self.assertRaisesRegex(ValueError, "rule_id"):
            self.evaluate(records)

    def test_requires_one_language_genre_cohort(self):
        records = self.records()
        records[0].pop("language")
        with self.assertRaisesRegex(ValueError, "language"):
            self.evaluate(records)

        records = self.records()
        records[-1]["genre"] = "research"
        with self.assertRaisesRegex(ValueError, "một cohort"):
            self.evaluate(records)

        with self.assertRaisesRegex(ValueError, "ít nhất một record"):
            self.evaluate([])

    def test_rejects_invalid_label_and_abstention_type(self):
        records = self.records()
        records[0]["label"] = "priority-chek"
        with self.assertRaisesRegex(ValueError, "label"):
            self.evaluate(records)

        records = self.records()
        records[0]["abstained"] = "false"
        with self.assertRaisesRegex(ValueError, "abstained"):
            self.evaluate(records)

    def test_rejects_invalid_span_shapes(self):
        records = self.records()
        records[-1]["expected_spans"] = [[20, 10]]
        with self.assertRaisesRegex(ValueError, "expected_spans"):
            self.evaluate(records)

    def test_output_names_the_single_cohort(self):
        result = self.evaluate(self.records())
        self.assertEqual(result["cohort"], {"language": "vi", "genre": "essay"})


if __name__ == "__main__":
    unittest.main()
