import os
import unittest

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")

from backend.app.domain import detect_mentions, normalize_domain_variations, split_brand_variations


class DomainLogicTests(unittest.TestCase):
    def test_brand_variations_are_trimmed_and_deduplicated(self) -> None:
        self.assertEqual(
            split_brand_variations(" Rankberry,rankberry , RB , , rb "),
            ["Rankberry", "RB"],
        )

    def test_domain_normalization_includes_expected_variants(self) -> None:
        self.assertEqual(
            normalize_domain_variations("https://www.Example.com/path"),
            ["https://www.example.com/path", "www.example.com/path", "example.com/path", "www.example.com", "example.com"],
        )

    def test_mentions_are_detected_case_insensitively(self) -> None:
        domain_match, brand_match = detect_mentions(
            "Visit WWW.EXAMPLE.COM and compare it against rankberry.",
            "https://www.example.com",
            "Rankberry, RB",
        )
        self.assertTrue(domain_match)
        self.assertTrue(brand_match)


if __name__ == "__main__":
    unittest.main()
