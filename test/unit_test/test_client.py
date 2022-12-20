import unittest

from alfred.client import Client

from alfred.fm.response import CompletionResponse


class TestClientWithDummyModel(unittest.TestCase):
    def setUp(self):
        # Set the model to be a dummy model that returns the input as the output
        self.client = Client(model_type="dummy")

    def test_completion(self):

        # Test that the completion method with return_rank set to True returns the input as the output
        response = self.client("I went to the store")
        self.assertEqual(type(response), CompletionResponse)
        self.assertEqual(response.prediction, "I went to the store")

        response = self.client.run("I went to the store")
        self.assertEqual(type(response), CompletionResponse)
        self.assertEqual(response.prediction, "I went to the store")

        response = self.client.generate("I went to the store")
        self.assertEqual(type(response), CompletionResponse)
        self.assertEqual(response.prediction, "I went to the store")


if __name__ == '__main__':
    unittest.main()
