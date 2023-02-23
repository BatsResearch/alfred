import numpy as np
import torch

from .labelmodel import LabelModel

class NPLM(LabelModel):
    """
    LabelModel class to perform majority vote on the responses
    """

    def __init__(self, num_classes, label_partition):
        """Constructor"""
        try:
            from labelmodel import PartialLabelModel
        except ImportError:
            raise ImportError(
                "Could not import labelmodel. Please install it from https://github.com/BatsResearch/labelmodels.")

        super().__init__(trainable=True)
        self.model = PartialLabelModel(
            num_classes=num_classes,
            label_partition=label_partition,
            device = 'cuda:0' if torch.cuda.is_available() else 'cpu',
        )

    def label(self, votes: np.ndarray) -> np.ndarray:
        self.model.estimate_label_model(votes + 1)
        return self.model.get_label_distribution(votes + 1).argmax(axis=1)

