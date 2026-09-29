"""`samples/` — ca mẫu công khai mà `studio.py doctor` kiểm offline.

Ca mẫu là **hợp đồng kỳ vọng**: người mới chạy trục 3 trên `bai-mau.md` rồi so với
`critique.expected.json`. Nếu bản kỳ vọng tự nó sai schema, trỏ tiêu chí không có trong hồ sơ, hay trích
một câu không có trong bài, thì người mới so với một đáp án hỏng — và không ai biết.
"""

import json
import re
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SAMPLES = ROOT / "samples"
SCHEMAS = ROOT / "shared" / "schemas"


def load(name):
    return json.loads((SAMPLES / name).read_text(encoding="utf-8"))


def essay_section_three():
    text = (ROOT / "shared/genres/essay.md").read_text(encoding="utf-8")
    section = text.split("## 3.", 1)[1].split("\n## 4.", 1)[0]
    block = re.search(r"(?ms)^```yaml\r?\n(.*?)^```", section).group(1)
    return yaml.safe_load(block)


def normalise(text):
    return " ".join(text.split())


class SampleShapeTests(unittest.TestCase):
    def test_every_sample_file_exists(self):
        for name in ("README.md", "bai-mau.md", "context.json", "critique.expected.json"):
            with self.subTest(file=name):
                self.assertTrue((SAMPLES / name).is_file())

    def test_context_and_critique_are_valid_against_their_schemas(self):
        for name, schema in (("context.json", "context"), ("critique.expected.json", "critique")):
            with self.subTest(file=name):
                validator = Draft202012Validator(
                    json.loads((SCHEMAS / f"{schema}.schema.json").read_text(encoding="utf-8"))
                )
                errors = [error.message for error in validator.iter_errors(load(name))]
                self.assertEqual(errors, [])

    def test_context_is_resolved_and_uses_the_essay_audience_fields(self):
        context = load("context.json")
        self.assertEqual(context["genre"], "essay")
        self.assertEqual(context["intent"]["unresolved"], [])
        text = (ROOT / "shared/genres/essay.md").read_text(encoding="utf-8")
        fields = yaml.safe_load(re.search(r"(?ms)^```yaml\r?\n(.*?)^```", text).group(1))["audience_fields"]
        self.assertEqual(sorted(context["audience"]), sorted(fields))


class ExpectedCritiqueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.critique = load("critique.expected.json")
        cls.profile = essay_section_three()
        cls.article = normalise((SAMPLES / "bai-mau.md").read_text(encoding="utf-8"))

    def test_scores_cover_every_essay_criterion_and_no_total(self):
        wanted = [row["id"] for row in self.profile["criteria"]]
        self.assertEqual([row["id"] for row in self.critique["criteria_scores"]], wanted)
        self.assertNotIn("total_score", self.critique)

    def test_lenses_run_match_the_enabled_lenses(self):
        self.assertEqual(self.critique["lenses_run"], self.profile["lenses"])

    def test_every_quote_is_really_in_the_article(self):
        for finding in self.critique["findings"]:
            with self.subTest(finding=finding["id"]):
                self.assertIn(normalise(finding["quoted_text"]), self.article)

    def test_must_fix_points_at_existing_findings(self):
        ids = {finding["id"] for finding in self.critique["findings"]}
        for item in self.critique["must_fix"]:
            self.assertIn(item["finding_id"], ids)

    def test_source_check_result_is_stated(self):
        """Luật trục 3: kết quả rà dẫn nguồn phải được nói ra — im lặng không tính là đã rà."""
        self.assertTrue(any("dẫn nguồn" in line for line in self.critique["limitations"]))


if __name__ == "__main__":
    unittest.main()
