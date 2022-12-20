import unittest


from alfred.fm.query import RankedQuery, CompletionQuery
from alfred.template import StringTemplate


class TestDatasetTemplate(unittest.TestCase):

    def test_apply_template_to_datset(self):
        dataset = [{'text': 'This is a test.'},
                   {'text': 'This is another test.'},
                   {'text': 'This is a third test.'}]

        template = StringTemplate("This is a [text]")

        queries = template.apply_to_dataset(dataset)
        queries_ = [template.apply(d) for d in dataset]

        self.assertEqual(len(queries), len(queries_))
        self.assertEqual(len(queries), len(dataset))
        self.assertEqual(queries, queries_)
        self.assertIsInstance(queries[0], CompletionQuery)

        self.assertEqual(queries[0].prompt, "This is a This is a test.")
        self.assertEqual(queries[1].prompt, "This is a This is another test.")

        template = StringTemplate(
            "This is a [text]",
            answer_choices="Yes ||| No",
        )

        ranked_queries = template.apply_to_dataset(dataset)
        ranked_queries_ = [template.apply(data) for data in dataset]

        self.assertEqual(len(ranked_queries), len(dataset))
        self.assertEqual(len(ranked_queries_), len(dataset))
        self.assertEqual(ranked_queries, ranked_queries_)

        self.assertIsInstance(ranked_queries[0], RankedQuery)

        self.assertEqual(ranked_queries[0].prompt, "This is a This is a test.")
        self.assertEqual(ranked_queries[0].candidates, ["Yes", "No"])
