import json
from ast import literal_eval

from .completion_response import CompletionResponse
from .ranked_response import RankedResponse
from .response import Response


def from_dict(json_dict: dict) -> Response:
    """
    Converts a JSON dictionary to a Response object.

    :param json_dict: The JSON dictionary to convert.
    :type json_dict: dict
    :return: The Response object.
    :rtype: Responses
    """
    return RankedResponse(
        **json_dict) if 'scores' in json_dict else CompletionResponse(
            **json_dict)


def deserialize(json_str: str) -> Response:
    """
    Deserializes a JSON string into a Response object.

    :param json_str:  The JSON string to deserialize.
    :type json_str: str
    :return: The Response object.
    :rtype: Response
    """
    def dict_clean(it):
        """
        Cleans a dictionary by converting all string values to their literal values.

        :param it: The dictionary to clean.
        :type it: dict
        :return: The cleaned dictionary.
        :rtype: dict
        """
        result = {}
        for key, value in it:
            try:
                str2dict = literal_eval(value)
                value = str2dict
            except (SyntaxError, ValueError):
                pass
            if value == "None":
                value = None
            result[key] = value
        return result

    return from_dict(json.loads(json_str, object_pairs_hook=dict_clean))
