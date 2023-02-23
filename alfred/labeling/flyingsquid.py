import numpy as np
import torch

from .labelmodel import LabelModel

class FlyingSquid(LabelModel):
    """
    LabelModel class to perform majority vote on the responses
    """

    def __init__(self, num_lfs):
        """Constructor"""
        try:
            from flyingsquid.label_model import LabelModel as FSLM
        except ImportError:
            raise ImportError(
                "Could not import flyingsquid. Please install it from https://github.com/HazyResearch/flyingsquid.")
        super().__init__(trainable=True)
        self.model = FSLM(num_lfs)

    def label(self, votes: np.ndarray) -> np.ndarray:
        self.model.fit(votes)
        return self.model.predict(votes).flatten()

