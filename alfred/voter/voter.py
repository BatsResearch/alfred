import logging
from typing import Dict, Callable, Union, List, Any, Iterable, Optional, Tuple

import numpy as np
from tqdm.auto import tqdm

from alfred.fm.response.completion_response import CompletionResponse
from alfred.fm.response.ranked_response import RankedResponse
from alfred.fm.response.response import Response

logger = logging.getLogger(__name__)


class Voter:
    """

    Voter is an actionable objective that translate raw fm responses
    to votes. It can also handle calibrations automatically for given template.


    """

    def __init__(
            self,
            label_map: Dict,
            matching_fn: Callable = lambda x, y: x == y,
            calibration: Optional[Union[List, np.ndarray, Tuple]] = None,
    ):
        """
        Initialize a voter


        :param label_map: There are 2 scenario each corresponding to ranked scoring scheme and completion scheme.
                            1. Ranked Scoring Scheme:
                                A dictionary of *labels* that maps to numerical vote/labels.
                                To use when the given answer_choices is out of order.
                                e.g. {"dog": 1, "cat": 2}
                            2. Completion Scheme:
                                A dictionary that maps *completions* to numerical values for votes.
                                e.g. {"cat": 1, "kitten": 1, "dog": 2, "puppy": 2}
        :type label_map: Dict
        :param matching_fn: (optional) function to match responses against answer choices, defaulting to exact match
                            e.g. lambda x, y: x == y
        :type matching_fn: Callable
        :param calibration: (optional) calibration weights to apply to the voter
        :type calibration: Optional[Union[List, np.ndarray]]
        """

        self._label_map = label_map
        self._matching_fn = matching_fn
        self._calibration = calibration

    def vote(self,
             responses: Union[Iterable[str], str, Iterable[Response],
             Response],
             matching_function: Optional[Callable] = None,
             label_map: Optional[Dict] = None,
             **kwargs: Any) -> np.ndarray:
        """
        Vote for the responses based on the matching function and the label maps

        *NOTE*: if label maps contains numerical labels then the vote will be the exact specified value
        if not the vote will be the index + 1 of the matched answer choice


        *Abstention vote is 0*

        *NOTE* on partial labels:

        :param responses: list of response objects
        :type responses: Union[Iterable[str], str, Iterable[Response], Response]
        :param matching_function: (optional) function to match responses against answer choices, defaulting to exact match
                                    e.g. lambda x, y: x == y
        :type matching_function: Callable
        :param label_map: (optional) label maps that maps responses content to labels
                           label_map specified here will overide the label_map initialized in the template
        :type label_map: Dict
        :return: numpy ndarray of votes in np.int8
        :rtype: np.ndarray
        """
        label_map = self._label_map if label_map is None else label_map
        matching_function = self._matching_fn if matching_function is None else matching_function

        if isinstance(responses, str) or isinstance(responses, Response):
            responses = [responses]

        if label_map is None:
            logger.warning(
                "No answer label map found, voting will not be done")
            raise ValueError(
                "No answer label map found, voting will not be done")

        no_tqdm = kwargs.get('no_tqdm', True)
        abstention = kwargs.get('abstention', 0)

        votes = np.ones(len(responses)) * abstention
        for idx, response in enumerate(tqdm(responses, disable=no_tqdm)):
            if type(response) == CompletionResponse:
                response = response.prediction
            elif type(response) == RankedResponse:
                if self._calibration:
                    scores = np.array(list(response.scores.values()))
                    labels = np.array(list(response.scores.keys()))
                    if type(self._calibration) == tuple:
                        weights, biases = self._calibration
                        calibrated_scores = scores @ weights + biases
                    elif type(self._calibration) in [list, np.ndarray]:
                        calibrated_scores = scores @ self._calibration
                    response = labels[np.argmax(calibrated_scores)]
                else:
                    response = response.prediction
            elif isinstance(response, str):
                pass
            else:
                logger.error(f"Unsupported response type: {type(response)}")
                raise ValueError(
                    f"Unsupported response type: {type(response)}")

            if isinstance(label_map, dict):
                for k_idx, key in enumerate(label_map.keys()):
                    if matching_function(response, key):
                        votes[idx] = label_map[key] if isinstance(
                            label_map[key], int) else k_idx + 1
            else:
                if matching_function(response, label_map):
                    votes[idx] = 1
        return votes

    def set_calibration(self, weights: Union[List[float], np.ndarray],
                        biases: Union[List[float], np.ndarray]):
        """
        Set calibration weights and biases

        Final calibration would be weights * scores + biases

        :param weights: weights to apply to the scores
        :type weights: Union[List[float], np.ndarray]
        :param biases: biases to apply to the scores
        :type biases: Union[List[float], np.ndarray]
        """
        self._calibration = (weights, biases)

    def clear_calibration(self):
        """
        Clear calibration weights and biases
        """
        self._calibration = None
