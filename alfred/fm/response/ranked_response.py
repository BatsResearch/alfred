from typing import Dict, Union, Optional

import numpy as np
import torch

from .response import Response


class RankedResponse(Response):
    """
    A subclass of `Response` that represents a language model response for scoring/ranking.

    """

    def __init__(
            self,
            prediction: str,
            scores: Dict,
            logits: Optional[Union[torch.Tensor, np.ndarray]] = None,
            embeddings: Optional[Union[torch.Tensor, np.ndarray]] = None,
    ):
        """
        Initialize a `RankedResponse` object.

        :param prediction: The prediction made by the language model
        :type prediction: str
        :param scores: A dictionary of scores for each class in the language model
        :type scores: dict
        :param logits: (optional) The logits output by the language model
        :type logits: Union[torch.Tensor, np.ndarray]
        :param embedding: (optional) The embedding output by the language model
        :type embedding: Union[torch.Tensor, np.ndarray]
        """
        super(RankedResponse, self).__init__()
        self['prediction'] = str(prediction)
        self['scores'] = scores
        self['embeddings'] = embeddings
        self['logits'] = logits

    @property
    def prediction(self) -> str:
        """
        Get the prediction made by the language model.

        :returns: The prediction made by the language model
        :rtype: str
        """
        return self['prediction']

    @property
    def scores(self) -> Dict:
        """
        Get the scores for each candidates in the language model.

        :returns: A dictionary of scores for each class in the language model
        :rtype: dict
        """
        return self['scores']

    @property
    def logits(self) -> Union[torch.Tensor, np.ndarray]:
        """
        Get the raw logits output by the language model.

        :returns: The logits output by the language model
        :rtype: Union[torch.Tensor, np.ndarray]
        """
        return self['logits']

    @property
    def embeddings(self) -> Union[torch.Tensor, np.ndarray]:
        """
        Get the embedding output by the language model.

        :returns: The embedding output by the language model
        :rtype: Union[torch.Tensor, np.ndarray]
        """
        return self['embeddings']

    def __eq__(self, other):
        """
        Determines if two RankedResponse objects are equal.

        Two RankedResponse objects are considered equal if their prediction,
        score, and embedding attributes are equal. If any of these attributes are not set,
        they are considered equal if both are None.

        :param other: The other RankedResponse object to compare to.
        :type other: RankedResponse
        :return: True if the two RankedResponse objects are equal, False otherwise.
        :rtype: bool
        """
        if isinstance(other, RankedResponse):
            consistent_flag = self.prediction == other.prediction
            consistent_flag &= (self.scores
                                == other.scores) or (self.scores is None
                                                     and other.scores is None)
            consistent_flag &= (self.logits
                                == other.logits) or (self.logits is None
                                                     and other.logits is None)
            consistent_flag &= (self['embeddings'] == other['embeddings']) or (
                    self['embeddings'] is None and other['embeddings'] is None)
            return consistent_flag
        else:
            return False
