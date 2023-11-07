import abc

import numpy as np
import torch


class Query(abc.ABC):
    """
    Abstract base class for a single query for foundation model interfaces
    """

    @staticmethod
    def compose(a, b, strategy=None):
        """
        Compose two strings or lists or tensors or numpy arrays

        :param a: operand a
        :type a: Union[str, List, Tuple, np.ndarray, torch.Tensor]
        :param b: operand b
        :type b: Union[str, List, Tuple, np.ndarray, torch.Tensor]
        :param strategy: composition strategy, defaults to None
        :type strategy: str, optional
        :return: composition of a and b
        """
        assert isinstance(a, type(b)), f"Cannot compose {type(a)} and {type(b)}"

        if strategy is None:
            if isinstance(a, str) or isinstance(a, list):
                return a + b
            elif isinstance(a, np.ndarray):
                return np.concatenate([a, b])
            elif isinstance(a, torch.Tensor):
                return torch.cat([a, b])
            else:
                raise NotImplementedError(
                    f"Type {type(a)} not supported for composition"
                )
        elif strategy == "ranked":
            return (a.strip(), b.strip())

    def serialize(self) -> str:
        """
        Serialize query

        :return: serialized query
        :rtype: str
        """
        return self.__repr__()

    @abc.abstractmethod
    def load(self):
        pass
