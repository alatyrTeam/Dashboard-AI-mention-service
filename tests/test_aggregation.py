import os
import unittest

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")

from backend.app.domain import IterationLike, aggregate_outputs, merge_citation_formats, normalize_citation_format


class AggregationTests(unittest.TestCase):
    def test_citation_merge_drops_na_when_real_values_exist(self) -> None:
        self.assertEqual(merge_citation_formats(["N/A", "text", "plain text", "url"]), "text, url")

    def test_citation_merge_returns_na_when_only_na_exists(self) -> None:
        self.assertEqual(merge_citation_formats(["N/A", "n/a"]), "N/A")

    def test_citation_normalization_maps_values_to_allowed_set(self) -> None:
        self.assertEqual(normalize_citation_format("plain text"), "text")
        self.assertEqual(normalize_citation_format("URL/link"), "url")
        self.assertEqual(normalize_citation_format("plain text, https://example.com"), "text, url")

    def test_aggregate_outputs_applies_rules(self) -> None:
        outputs = [
            IterationLike(1, "a", "b", True, False, False, True, 2.0, "Rankberry", "text"),
            IterationLike(2, "c", "d", False, False, True, False, 4.0, "RB, Rankberry", "N/A"),
            IterationLike(3, "e", "f", False, True, False, False, None, None, "url"),
        ]

        result = aggregate_outputs(outputs)

        self.assertTrue(result["gpt_domain_mention"])
        self.assertTrue(result["gem_domain_mention"])
        self.assertTrue(result["gpt_brand_mention"])
        self.assertTrue(result["gem_brand_mention"])
        self.assertEqual(result["response_count_avg"], 3.0)
        self.assertEqual(result["brand_list"], "Rankberry, RB")
        self.assertEqual(result["citation_format"], "text, url")


if __name__ == "__main__":
    unittest.main()
