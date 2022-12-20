from typing import List, Union, Tuple

import numpy as np
import torch

from .query import Query


class CompletionQuery(Query):
    """
    A completion query class.

    This is the generic query for any alfred.fm model.
    It mainly contains the prompt, which is the input to the model.

    This class represents a query for completion of a given prompt.
    It is initialized with a prompt, which can be a string, NumPy array,
    list, tuple, or PyTorch tensor.
    """

    def __init__(self,
                 prompt: Union[str, np.ndarray, List, Tuple, torch.Tensor],
                 ):
        """
        Initializes a CompletionQuery class.

        :param prompt: The prompt to be completed.
        :type prompt: Union[str, np.ndarray, List, Tuple, torch.Tensor]
        """
        self._prompt = prompt

    @property
    def prompt(self):
        """returns the raw prompt content"""
        return self._prompt

    def load(self):
        """loads the prompt, this will be convenient for batching the queries"""
        return [self._prompt]

    def __repr__(self):
        """returns the string representation of the query"""
        return f"CompletionQuery(prompt={self._prompt})"

    def __str__(self):
        """returns the string representation of the query"""
        return self.__repr__()

    def __eq__(self, other):
        """returns whether the two queries are equal"""
        return self._prompt == other._prompt

    def __hash__(self):
        """returns the hash of the query"""
        return hash(self._prompt)

    def __len__(self):
        """returns the length of the prompt"""
        return len(self._prompt)

    def __add__(self, other):
        """concatenates the two queries"""
        assert isinstance(
            other, type(
                self._prompt)), f"Cannot add {type(self._prompt)} and {type(other)}"
        return CompletionQuery(self.compose(self._prompt, other._prompt))
