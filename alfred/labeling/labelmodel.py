import abc
from typing import Optional, Dict


class LabelModel:
    """
    Abstract LabelModel Interface
    """
    def __init__(
        self,
        config: Optional[Dict] = None,
        trainable: bool = False,
    ):
        """
        Constructor

        :param config: (optional) configuration
        :type config: Dict
        :param trainable: (optional) whether the label model is trainable
        :type trainable: bool
        """
        self._config = config
        self._trainable = trainable
        self._trained = False

    @abc.abstractmethod
    def label(self, votes):
        pass

    def __call__(self, votes):
        """functional style of label"""
        return self.label(votes)
