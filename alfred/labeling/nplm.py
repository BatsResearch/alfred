import numpy as np
import torch

from .labelmodel import LabelModel


class NPLM(LabelModel):
    """
    LabelModel wrapper to perform label modeling for partial labelers on the responses
    """

    def __init__(
        self,
        num_classes,
        label_partition,
        device="cuda:0" if torch.cuda.is_available() else "cpu",
    ):
        """Constructor"""
        try:
            from labelmodels import PartialLabelModel
        except ImportError:
            raise ImportError(
                "Could not import labelmodel. Please install it from https://github.com/BatsResearch/labelmodels."
            )

        super().__init__(trainable=True)
        self.model = PartialLabelModel(
            num_classes=num_classes,
            label_partition=label_partition,
            device=device,
        )

    def label(self, votes: np.ndarray) -> np.ndarray:
        """
        Label the responses using the label model.
        Similar to standard PWS practice, abstention = 0 (i.e. classes are 1-indexed)


        :param votes: The votes from the labelers.
        :type votes: np.ndarray
        :return: The predicted probabilistic labels.
        :rtype: np.ndarray
        """
        self.model.estimate_label_model(votes + 1)
        return self.model.get_label_distribution(votes + 1)
