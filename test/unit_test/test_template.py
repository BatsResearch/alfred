import unittest


from alfred.fm.query import CompletionQuery, RankedQuery
from alfred.fm.response import CompletionResponse, RankedResponse
from alfred.template import StringTemplate


class TestTemplate(unittest.TestCase):

    def test_string_template_constructor(self):
        # Test with minimal arguments
        template = StringTemplate("This is a template.")
        self.assertEqual(template._template, "This is a template.")

    def test_string_template_apply(self):
        # Test with minimal arguments
        template = StringTemplate("This is a [data].")
        query = template.apply({"data": "Test data"})
        self.assertIsInstance(query, CompletionQuery)
        self.assertEqual(query.prompt, "This is a Test data.")

        template = StringTemplate("This is a [data].")
        query = template({"data": "Test data"})
        self.assertIsInstance(query, CompletionQuery)
        self.assertEqual(query.prompt, "This is a Test data.")

        # Test with completion template
        template = StringTemplate("This is a [data].",
                                  answer_choices="Yes ||| No")
        query = template.apply({"data": "Test data"})
        self.assertIsInstance(query, RankedQuery)
        self.assertEqual(query.prompt, "This is a Test data.")
        self.assertEqual(query.candidates, ["Yes", "No"])

        # Test with ranked template
        template = StringTemplate("This is a [data].",
                                  answer_choices="Yes ||| No",
                                  label_maps={"Yes": 1, "No": 2})
        query = template.apply({"data": "Test data"})
        self.assertIsInstance(query, RankedQuery)
        self.assertEqual(query.prompt, "This is a Test data.")
        self.assertEqual(query.candidates, ["Yes", "No"])

    def test_string_template_vote(self):
        # Test with completion template
        template = StringTemplate("This is a template.",
                                  answer_choices="Yes ||| No")
        response = CompletionResponse("Yes")
        votes = template.vote(response, label_maps={"Yes": 1, "No": 2})
        print(votes)
        self.assertEqual(len(votes), 1)
        self.assertEqual(votes[0], 1)

        # Test with ranked template
        template = StringTemplate("This is a template.",
                                  answer_choices="Yes ||| No",
                                  label_maps={"Yes": 1, "No": 2})
        response = RankedResponse("Yes", scores={"Yes": 0.9, "No": 0.1})
        votes = template.vote(response, label_maps={"Yes": 1, "No": 2})
        self.assertEqual(len(votes), 1)
        self.assertEqual(votes[0], 1)
