import unittest

from alfred.fm.response import (
    Response,
    CompletionResponse,
    RankedResponse,
    deserialize,
    from_dict,
)


class TestResponse(unittest.TestCase):
    def test_init(self):
        self.assertTrue(type(CompletionResponse("text")) == CompletionResponse)

        self.assertTrue(isinstance(CompletionResponse("text"), Response))

        self.assertTrue(
            type(RankedResponse("prediction", scores={"1": 0.1})) == RankedResponse
        )

        self.assertTrue(
            isinstance(RankedResponse("prediction", scores={"1": 0.1}), Response)
        )

        self.assertTrue(
            RankedResponse("prediction", scores={"1": 0.1}).prediction == "prediction"
        )

        self.assertTrue(
            RankedResponse("prediction", scores={"1": 0.1}).scores == {"1": 0.1}
        )

        self.assertTrue(CompletionResponse("text").prediction == "text")

        self.assertTrue(
            CompletionResponse("text").prediction
            == CompletionResponse("text")["prediction"]
        )

        self.assertTrue(
            RankedResponse("text", scores={"1": 0.1}).scores
            == RankedResponse("text", scores={"1": 0.1})["scores"]
        )

        self.assertTrue(
            RankedResponse("text", scores={"1": 0.1}).prediction
            == RankedResponse("text", scores={"1": 0.1})["prediction"]
        )

    def test_init_from_dict(self):
        self.assertTrue(type(from_dict({"prediction": "text"})) == CompletionResponse)

        self.assertTrue(isinstance(from_dict({"prediction": "text"}), Response))

        self.assertTrue(
            type(from_dict({"prediction": "prediction", "scores": {"1": 0.1}}))
            == RankedResponse
        )

        self.assertTrue(
            isinstance(
                from_dict({"prediction": "text", "scores": {"1": 0.1}}), Response
            )
        )

        self.assertTrue(
            CompletionResponse(**{"prediction": "text"}).prediction == "text"
        )

        self.assertTrue(from_dict({"prediction": "text"}).prediction == "text")

        self.assertTrue(
            RankedResponse(**{"prediction": "text", "scores": {"1": 0.1}}).prediction
            == "text"
        )

        self.assertTrue(
            from_dict({"prediction": "text", "scores": {"1": 0.1}}).prediction == "text"
        )

    def test_serialization(self):
        completion_response = CompletionResponse("text")
        self.assertTrue(
            deserialize(completion_response.serialize()) == completion_response
        )

        ranked_response = RankedResponse("prediction", scores={"1": 0.1})
        print(type(deserialize(ranked_response.serialize()).scores))
        self.assertTrue(deserialize(ranked_response.serialize()) == ranked_response)


if __name__ == "__main__":
    unittest.main()
