import os
import unittest

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")

from backend.app.domain import IterationLike, drop_one_gpt_for_sentiment_retry, select_sentiment_inputs


class SentimentSelectionTests(unittest.TestCase):
    def test_mention_outputs_are_prioritized(self) -> None:
        outputs = [
            IterationLike(1, "gpt-1", "gem-1", False, False, False, False, None, None, None),
            IterationLike(2, "gpt-2", "gem-2", True, False, False, True, None, None, None),
            IterationLike(3, "gpt-3", "gem-3", False, False, False, False, None, None, None),
        ]

        selected = select_sentiment_inputs(outputs)

        self.assertEqual(
            [(item.provider, item.iteration_number) for item in selected],
            [("gpt", 2), ("gemini", 2), ("gpt", 1), ("gemini", 1)],
        )

    def test_retry_reduction_drops_first_gpt_output(self) -> None:
        outputs = [
            IterationLike(1, "gpt-1", "gem-1", True, False, False, False, None, None, None),
            IterationLike(2, "gpt-2", "gem-2", False, True, False, False, None, None, None),
        ]

        selected = select_sentiment_inputs(outputs)
        reduced = drop_one_gpt_for_sentiment_retry(selected)

        self.assertEqual(
            [(item.provider, item.iteration_number) for item in reduced],
            [("gemini", 2), ("gemini", 1), ("gpt", 2)],
        )


if __name__ == "__main__":
    unittest.main()
