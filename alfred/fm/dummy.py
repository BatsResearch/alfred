import logging
import torch
from typing import Optional, List, Union, Any

from alfred.fm.model import LocalAccessFoundationModel
from .query import Query
from .response import CompletionResponse, Response

logger = logging.getLogger(__name__)


class DummyModel(LocalAccessFoundationModel):
    """
    A dummy model that returns the input as the output.

    This model implements a dummy model that returns the
    input as the output for both completion and outputs a raw logit of -1 for scoring.
    """

    def __init__(self, model: Optional[str] = None):
        """
        Initialize a `DummyModel` object.

        :param model: (optional) The path to the model.
        :type model: str
        """
        super().__init__("dummy model")
        self.model = model

    def _generate_batch(
            self,
            batch_instance: Union[List[Query], List[str]],
            **kwargs: Any,
    ) -> List[Response]:
        """
        Generate completions for a batch of queries.

        This function returns the same output as the input queries but returns a `Response` object.

        :param batch_instance: A list of queries.
        :type batch_instance: List[Query]
        :param kwargs: Additional keyword arguments.
        :return: A list of `Response` objects with the same prediction content as the input.
        :rtype: List[Response]
        """
        return [
            CompletionResponse(
                content.load()[0] if isinstance(content, Query) else content)
            for content in batch_instance
        ]

    def _encode_batch(
            self,
            batch_instance: Union[List[Query], List[str]],
            **kwargs: Any,
    ) -> List[torch.Tensor]:
        """
        Encode a batch of queries.

        This function returns a zero vector of size 512 for all queries.

        :param batch_instance: A list of queries.
        :type batch_instance: List[Query]
        :param reduction: The reduction method to use.
        :type reduction: str
        :param kwargs: Additional keyword arguments.
        :return: A list of `torch.Tensor` objects with the same prediction content as the input.
        :rtype: List[torch.Tensor]
        """
        return [torch.zeros([512]) for _ in batch_instance]

    def _score_batch(
            self,
            batch_instance: Union[List[Query], List[str]],
            **kwargs,
    ) -> List[dict]:
        """
        Score a batch of queries.

        This function returns a logit score of -1 for all candidates.

        :param batch_instance: A list of queries.
        :type batch_instance: List[Query]
        :param kwargs: Additional keyword arguments.
        :type kwargs: Any
        :return: A list of logit scores in the form of a dictionary.
        :rtype: List[dict]
        """

        return [{'logits': 1.} for _ in range(len(batch_instance))]
