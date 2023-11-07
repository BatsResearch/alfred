import numpy as np
from scipy import stats

from .labelmodel import LabelModel


class MajorityVote(LabelModel):
    """
    LabelModel class to perform majority vote on the responses
    """

    def __init__(self):
        """Constructor"""
        super().__init__()

    def label(self, votes: np.ndarray) -> np.ndarray:
        """returns the majority vote for each response row"""
        return stats.mode(votes, axis=1)[0].flatten()
