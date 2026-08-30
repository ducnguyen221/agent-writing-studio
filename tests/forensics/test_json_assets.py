import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]


class JsonAssetTests(unittest.TestCase):
    def test_all_json_files_parse(self):
        failures = []
        for path in ROOT.rglob("*.json"):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                failures.append(f"{path.relative_to(ROOT)}: {error}")
        self.assertEqual(failures, [], "JSON không hợp lệ:\n" + "\n".join(failures))

    def test_all_json_schemas_are_valid_draft_2020_12(self):
        failures = []
        for path in ROOT.rglob("*.schema.json"):
            try:
                schema = json.loads(path.read_text(encoding="utf-8"))
                Draft202012Validator.check_schema(schema)
            except Exception as error:  # jsonschema exposes several schema-error subclasses
                failures.append(f"{path.relative_to(ROOT)}: {error}")
        self.assertEqual(failures, [], "JSON Schema không hợp lệ:\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
