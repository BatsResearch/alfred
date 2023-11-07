from typing import Dict, Union, Optional

import numpy as np
import torch

from .response import Response


class CompletionResponse(Response):
    """
    A response class for language model completions.

    This class represents a completion response from a language model,
    which includes the predicted completion string, a score indicating
    the confidence of the prediction, and an optional embedding output.
    """

    def __init__(
        self,
        prediction: str,
        score: Optional[float] = None,
        embedding: Optional[Union[torch.Tensor, np.ndarray]] = None,
    ):
        """
        Initializes the CompletionResponse object.

        :param prediction: The predicted completion string.
        :type prediction: str
        :param score: (optional) The confidence score of the prediction.
        :type score: float
        :param embedding: (optional) The embedding of the prediction.
        :type embedding: Union[torch.Tensor, np.ndarray]
        """
        super(CompletionResponse, self).__init__()
        self["prediction"] = str(prediction)
        self["score"] = float(score) if score else None
        self["embedding"] = embedding

    @property
    def prediction(self) -> str:
        """
        Returns the predicted completion string.

        :return: The predicted completion string.
        :rtype: str
        """
        return self["prediction"]

    @property
    def score(self) -> Dict:
        """
        Returns the score of the completion prediction.

        :return: The score of the completion prediction.
        :rtype: float
        """
        return self["score"]

    @property
    def embedding(self) -> Union[torch.Tensor, np.ndarray]:
        """
        Returns the embedding of the completion prediction.

        :return: The embedding of the completion prediction.
        :rtype: Union[torch.Tensor, np.ndarray]
        """
        return self["embedding"]

    def __eq__(self, other):
        """
        Determines if two CompletionResponse objects are equal.

        Two CompletionResponse objects are considered equal if their prediction,
        score, and embedding attributes are equal. If any of these attributes are not set,
        they are considered equal if both are None.

        :param other: The other CompletionResponse object to compare to.
        :type other: CompletionResponse
        :return: True if the two CompletionResponse objects are equal, False otherwise.
        :rtype: bool
        """
        if isinstance(other, CompletionResponse):
            consistent_flag = self.prediction == other.prediction
            consistent_flag &= (self.score == other.score) or (
                self.score is None and other.score is None
            )
            consistent_flag &= (self["embedding"] == other["embedding"]) or (
                self["embedding"] is None and other["embedding"] is None
            )
            return consistent_flag
        else:
            return False
