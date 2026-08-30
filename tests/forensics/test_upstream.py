import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class UpstreamTests(unittest.TestCase):
    def test_antislop_reference_is_pinned(self):
        data = json.loads((ROOT / "upstream.json").read_text(encoding="utf-8"))
        source = next(x for x in data["sources"] if x["name"] == "SalZaki/antislop")
        self.assertEqual(source["type"], "reference")
        self.assertEqual(source["branch"], "main")
        self.assertEqual(source["baseline"], "b9c5b74dab49d536229e2d5be38b9cd8cfa20d7e")
        self.assertEqual(source["license"], "MIT")
        self.assertTrue(source["took"])

    def test_distill_notes_name_taken_and_rejected_concepts(self):
        notes = (ROOT / "vendor-notes/antislop/DISTILL-NOTES.md").read_text(encoding="utf-8")
        self.assertIn("## Đã chưng cất", notes)
        self.assertIn("## Không mang sang", notes)
        self.assertIn("agent đọc mù", notes)


if __name__ == "__main__":
    unittest.main()
