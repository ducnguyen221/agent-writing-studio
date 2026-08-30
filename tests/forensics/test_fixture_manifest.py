import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]


class FixtureManifestTests(unittest.TestCase):
    def setUp(self):
        schema = json.loads((ROOT / "fixtures/manifest.schema.json").read_text(encoding="utf-8"))
        self.validator = Draft202012Validator(schema)

    def test_supervised_human_fixture_is_valid(self):
        item = {
            "id": "human-essay-001",
            "provenance": "human",
            "language": "vi",
            "genre": "essay",
            "source_date": "2026-08-01",
            "ground_truth_level": "supervised",
            "evidence": ["observed_writing_session"],
            "split": "test",
        }
        self.assertEqual(list(self.validator.iter_errors(item)), [])

    def test_human_fixture_without_provenance_evidence_is_invalid(self):
        item = {
            "id": "human-essay-002",
            "provenance": "human",
            "language": "vi",
            "genre": "essay",
            "source_date": "2026-08-01",
            "ground_truth_level": "claimed",
            "evidence": [],
            "split": "train",
        }
        self.assertTrue(list(self.validator.iter_errors(item)))

    def test_mixed_fixture_requires_edit_operations_and_spans(self):
        item = {
            "id": "mixed-essay-001",
            "provenance": "mixed",
            "language": "vi",
            "genre": "essay",
            "source_date": "2026-08-01",
            "ground_truth_level": "generated_and_logged",
            "evidence": ["generation_log"],
            "split": "dev",
        }
        self.assertTrue(list(self.validator.iter_errors(item)))


if __name__ == "__main__":
    unittest.main()
