import unittest

from alfred.fm.response import CompletionResponse, RankedResponse
from alfred.template import StringTemplate
from alfred.voter import Voter


class TestVoter(unittest.TestCase):
    def test_vote(self):

        template_voter = Voter(
            label_map={"Yes": 1, "No": 2},
            matching_fn=lambda x, y: x == y
        )
        response = CompletionResponse("Yes")
        votes = template_voter.vote(response)
        self.assertEqual(len(votes), 1)
        self.assertEqual(votes[0], 1)

        response = CompletionResponse("No")
        votes = template_voter.vote(response)
        self.assertEqual(len(votes), 1)
        self.assertEqual(votes[0], 2)

        response = CompletionResponse("no")
        votes = template_voter.vote(response)
        self.assertEqual(len(votes), 1)
        self.assertEqual(votes[0], 0)

        response = CompletionResponse("no")
        votes = template_voter.vote(response, matching_function=lambda x, y: x.lower() == y.lower())
        self.assertEqual(len(votes), 1)
        self.assertEqual(votes[0], 2)

        response = RankedResponse("Yes", scores={"Yes": 0.9, "No": 0.1})
        votes = template_voter.vote(response)
        self.assertEqual(len(votes), 1)
        self.assertEqual(votes[0], 1)

    def test_calibrated_vote(self):
        # Test with completion template
        template_voter = Voter(
            label_map={"Yes": 1, "No": 2},
            matching_fn=lambda x, y: x == y
        )

        response = RankedResponse("Yes", scores={"Yes": 0.9, "No": 0.1})
        votes = template_voter.vote(response)
        self.assertEqual(len(votes), 1)
        self.assertEqual(votes[0], 1)

        template_voter.set_calibration([1, 100],[0,0])
        votes = template_voter.vote(response)
        self.assertEqual(len(votes), 1)
        self.assertEqual(votes[0], 2)

if __name__ == '__main__':
    unittest.main()
