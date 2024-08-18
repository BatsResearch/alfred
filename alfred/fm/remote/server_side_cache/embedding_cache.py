import torch
from PIL import Image
from typing import List, Callable, Union
import numpy as np


class EmbeddingCache:
    """
    A simple embedding cache for VLM models
    """

    def __init__(self, max_size: int = 32):
        self.max_size = max_size
        self.cache = {}

    def __contains__(self, key):
        if isinstance(key, Image.Image):
            key = key.tobytes()
        return key in self.cache

    def __getitem__(self, key):
        if isinstance(key, Image.Image):
            key = key.tobytes()
        return self.cache[key]

    def __setitem__(self, key, value):
        if len(self.cache) >= self.max_size:
            self.cache.pop(next(iter(self.cache)))
        if isinstance(key, Image.Image):
            key = key.tobytes()
        self.cache[key] = value

    @staticmethod
    def reorder_array(
        arr: Union[np.ndarray, torch.Tensor, list],
        order: Union[np.ndarray, torch.Tensor, list],
    ) -> Union[np.ndarray, torch.Tensor, list]:
        """
        Recover an array according to a given order index.

        This function reorders the elements in an array according to the order specified by a separate array.

        :param arr: The array to be reordered. Can be a NumPy array, PyTorch tensor, or Python list.
        :type arr: Union[np.ndarray, torch.Tensor, list]
        :param order: The order array. Can be a NumPy array, PyTorch tensor, or Python list.
        :type order: Union[np.ndarray, torch.Tensor, list]
        :return: The reordered array. Has the same type as the input `arr`.
        :rtype: Union[np.ndarray, torch.Tensor, list]
        """
        return [x[0] for x in sorted(list(zip(arr, order)), key=lambda x: x[1])]

    def get(
        self,
        inputs: Union[List[Image.Image], List[str]],
        embedding_proc: Callable,
    ) -> torch.tensor:
        """
        Process the inputs and retrieve from the cache/embed the inputs

        :param inputs: A list of inputs
        :type inputs: Union[List[Image.Image], List[str]]
        :param embedding_proc: The embedding function
        :type embedding_proc: Callable
        :return: The embeddings
        :rtype: torch.tensor
        """
        cached_embeddings = []
        new_inputs = []

        cached_idx, new_inp_idx = [], []
        for inp_idx, inp in enumerate(inputs):
            if inp in self:
                cached_embeddings.append(self[inp])
                cached_idx.append(inp_idx)
            else:
                new_inputs.append(inp)
                new_inp_idx.append(inp_idx)

        if len(new_inputs) == 0:
            return torch.stack(cached_embeddings)

        new_embeddings = embedding_proc(new_inputs)
        for inp, embedding in zip(new_inputs, new_embeddings):
            self[inp] = embedding
        return torch.stack(
            self.reorder_array(
                list(new_embeddings) + cached_embeddings, new_inp_idx + cached_idx
            )
        )
