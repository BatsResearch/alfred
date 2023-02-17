import abc
import json
from collections import OrderedDict


class Response(OrderedDict):
    """
    A class that represents a response from a alfred.fm model.
    Inherit from OrderedDict.
    Inherited by CompletionResponse and RankedResponse.
    """

    @abc.abstractmethod
    def prediction(self):
        """
        Get the prediction made by the model.

        :returns: The prediction made by the model
        """
        pass

    def serialize(self) -> str:
        """
        Serialize the response to a JSON string.

        :returns: The serialized response as a JSON string
        :rtype: str
        """
        return json.dumps({k: str(v) for k, v in self.items()}, indent=2)

    def __str__(self):
        """
        Get a string representation of the response.

        :returns: A string representation of the response
        :rtype: str
        """
        ret = f"{self.__class__.__name__}("
        for k, v in self.items():
            ret += f"{str(k)}={str(v)}, "
        ret += ')'
        return ret

    def __repr__(self):
        """
        Get a string representation of the response object.

        :returns: A string representation of the response
        :rtype: str
        """
        return self.prediction
