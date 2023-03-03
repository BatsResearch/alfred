import numpy as np

from .labelmodel import LabelModel


class NaiveBayes(LabelModel):
    """
    LabelModel wrapper to perform label modeling for partial labelers on the responses
    """
    def __init__(self, num_classes, num_lfs):
        """Constructor"""
        try:
            from labelmodels import NaiveBayes
        except ImportError:
            raise ImportError(
                "Could not import labelmodel. Please install it from https://github.com/BatsResearch/labelmodels."
            )

        super().__init__(trainable=True)
        self.model = NaiveBayes(
            num_classes=num_classes,
            num_lfs=num_lfs,
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
