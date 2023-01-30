import unittest

from alfred.fm.query import CompletionQuery, RankedQuery
from alfred.template import StringTemplate


class TestTemplate(unittest.TestCase):
    def test_string_template_constructor(self):
        # Test with minimal arguments
        template = StringTemplate("This is a template.")
        self.assertEqual(template._template, "This is a template.")

    def test_string_template_apply(self):
        # Test with minimal arguments
        template = StringTemplate("This is a [[data]].")
        query = template.apply({"data": "Test data"})
        self.assertIsInstance(query, CompletionQuery)
        self.assertEqual(query.prompt, "This is a Test data.")

        template = StringTemplate("This is a [[data]].")
        query = template({"data": "Test data"})
        self.assertIsInstance(query, CompletionQuery)
        self.assertEqual(query.prompt, "This is a Test data.")

        # Test with completion template
        template = StringTemplate("This is a [[data]].",
                                  answer_choices="Yes ||| No")
        query = template.apply({"data": "Test data"})
        self.assertIsInstance(query, RankedQuery)
        self.assertEqual(query.prompt, "This is a Test data.")
        self.assertEqual(query.candidates, ["Yes", "No"])

        # Test with ranked template
        template = StringTemplate(
            "This is a [[data]].",
            answer_choices="Yes ||| No",
        )
        query = template.apply({"data": "Test data"})
        self.assertIsInstance(query, RankedQuery)
        self.assertEqual(query.prompt, "This is a Test data.")
        self.assertEqual(query.candidates, ["Yes", "No"])
