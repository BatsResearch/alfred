"""

Ranked Query Class encompasses query tem

"""
import numpy as np
import torch
from PIL import Image
from typing import List, Union, Tuple, Callable

from .query import Query


class RankedQuery(Query):
    """
    Ranked Query Class encompasses query terms that operate in
    scoring scheme with FM interfaces

    Example:
        >>> from alfred.fm.query import RankedQuery
        >>> query = RankedQuery("What is the answer of 1+1?", candidates=["2", "1"])
        Then you can call either alfred.client or alfred.fm to get the RankedResponse
        >>> from alfred.client import Client
        >>> client = Client()
        >>> response = client(query)
        or
        >>> from alfred.fm.x import XFM
        >>> fm = XFM()
        >>> response = fm(query)
    """

    def __init__(
            self,
            prompt: Union[str, np.ndarray, Image.Image, Tuple, torch.Tensor],
            candidates: Union[List, Tuple, np.ndarray, torch.Tensor],
    ):
        """
        Initializes a RankedQuery class.

        :param prompt: query prompt
        :type prompt: Union[str, np.ndarray, List, Tuple, torch.Tensor]
        :param candidates: list of candidates for appending to prompt
        :type candidates: Union[List, Tuple, np.ndarray, torch.Tensor]
        """
        assert len(candidates) > 0, \
            "Candidates cannot be empty"
        self._prompt = prompt
        self._candidates = candidates
        self.composition_strategy = "ranked"

    @property
    def candidates(self):
        """returns the raw candidates content"""
        return self._candidates

    @property
    def prompt(self):
        """returns the raw prompt content"""
        return self._prompt

    def get_answer_choices_str(self):
        """get the raw candidates as jinja strings (deliminated by '|||')"""
        return "|||".join(self._candidates)

    def load(
            self,
            composition_fn: Callable = None,
    ) -> List:
        """
        Load prompt and candidates

        :param composition_fn: function to compose prompt and candidates
        :type composition_fn: Callable
        :return: composed prompt and candidates as a list of different prompt queries
        :rtype: List
        """
        composition_fn = composition_fn or self.compose

        return [
            composition_fn(self._prompt,
                           candidate,
                           strategy=self.composition_strategy)
            for candidate in self._candidates
        ]

    def __repr__(self):
        """returns the string representation of the query"""
        return f"RankedQuery(content={self._prompt}, candidates={self._candidates}, composition_strategy={self.composition_strategy})"

    def __str__(self):
        """returns the string representation of the query"""
        return self.__repr__()

    def __eq__(self, other):
        """returns whether the two queries are equal"""
        assert isinstance(
            other, Query), f"Cannot compare {type(self)} and {type(other)}"
        return self._prompt == other._prompt

    def __hash__(self):
        """returns the hash of the query"""
        return hash(self._prompt)

    def __len__(self):
        """returns the length of the query"""
        return len(self._prompt)

    def __add__(self, other):
        """concatenates the two queries"""
        assert isinstance(
            other, type(self._prompt)
        ), f"Cannot add {type(self._prompt)} and {type(other)}"
        return RankedQuery(self.compose(self._prompt, other), self._candidates)
