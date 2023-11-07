import unittest

from alfred.fm.query import Query, RankedQuery, CompletionQuery


class TestQuery(unittest.TestCase):
    def test_init(self):
        self.assertTrue(type(RankedQuery("prompt", candidates=["2"])) == RankedQuery)

        self.assertTrue(isinstance(RankedQuery("prompt", candidates=["2"]), Query))

        # empty candidates
        self.assertRaises(AssertionError, RankedQuery, "prompt", candidates=[])
        # mismatch candidate type
        self.assertRaises(AssertionError, RankedQuery, "prompt", candidates=[])

        self.assertTrue(type(CompletionQuery("prompt")) == CompletionQuery)

        self.assertTrue(isinstance(CompletionQuery("prompt"), Query))

    def test_load(self):
        self.assertTrue(type(CompletionQuery("prompt").load()) == list)

        self.assertTrue(len(CompletionQuery("prompt").load()) == 1)

        self.assertTrue(CompletionQuery("prompt").load() == ["prompt"])

        self.assertTrue(
            type(RankedQuery("prompt", candidates=["2", "1"]).load()) == list
        )

        self.assertTrue(len(RankedQuery("prompt", candidates=["2", "1"]).load()) == 2)

        self.assertTrue(
            RankedQuery("prompt", candidates=["2", "1"]).load()
            == [("prompt", "2"), ("prompt", "1")]
        )


if __name__ == "__main__":
    unittest.main()
