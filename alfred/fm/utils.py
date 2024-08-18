import base64
import gc
import logging
from collections import OrderedDict
from typing import List, Union, Optional, Callable, Any
import io

import numpy as np
import torch
import transformers
from PIL import Image

import time

from .query import Query, RankedQuery, CompletionQuery
from .response import RankedResponse

logger = logging.getLogger(__name__)


def clear_cuda_cache():
    """
    Clear cuda cache via garbage collection
    """
    gc.collect()
    torch.cuda.empty_cache()


def normalize_logits(logits: torch.Tensor) -> torch.Tensor:
    """
    Normalize raw logit scores from a foundation model.

    This function normalizes raw logit scores from a foundation model using the softmax function.
    Other normalization methods can be used in the future if needed.

    :param logits: The raw logit scores to be normalized.
    :type logits: torch.Tensor
    :return: The normalized logit scores.
    :rtype: torch.Tensor
    """
    return torch.softmax(logits, dim=-1)


def encode_image(image, type="path"):
    """
    Encode an image file into base64.

    :param image: The image to be encoded.
    :type image: str or bytes or PIL.Image
    :param type: The type of the image. Can be "path", "bytes", or "image".
    :type type: str
    """
    if isinstance(image, str):
        if type == "path":
            with open(image, "rb") as image_file:
                img = image_file.read()
                return base64.b64encode(img).decode("utf-8")
        else:
            return image.decode("utf-8")
    elif isinstance(image, Image.Image):
        buffer = io.BytesIO()
        image.save(buffer, format="png")
        image = buffer.getvalue()
        return base64.b64encode(image).decode("utf-8")


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


def tokenize(inst, tokenizer, max_length=512):
    """
    Tokenize a query instance

    :param inst: A query instance
    :type inst: Union[Query, str]
    :param tokenizer: A tokenizer
    :type tokenizer: transformers.PreTrainedTokenizer
    :param max_length: The maximum length of the tokenized sequence
    :type max_length: int
    :return: A list of token ids
    :rtype: List[int]
    """
    if tokenizer:
        token_ids = tokenizer.encode(
            inst, max_length=max_length, truncation=True, return_tensors="pt"
        )[0]
    else:
        token_ids = inst
    return token_ids, len(token_ids)


def check_pkg_available(pkg_name: str) -> bool:
    """
    Check if a package is available

    :param pkg_name: The name of the package
    :type pkg_name: str
    :return: Whether the package is available
    :rtype: bool
    """
    try:
        __import__(pkg_name)
        return True
    except ImportError:
        raise ImportError(f"Please install {pkg_name} to use this feature")


def type_print(string, interval=0.07, newline=False):
    """
    Print a string word by word to simulate typing
    """
    for word in string.split(" "):
        print(word, end=" ", flush=True)
        time.sleep(interval)
    print("\b", end="", flush=True)
    if newline:
        print("")


def retry(num_retries=3, wait_time=0.1, exceptions=(Exception,)):
    """
    A decorator to retry a function call if it raises an exception.

    Useful for running API-based models that may fail due to network/server issues.

    :param num_retries: The number of retries
    :type num_retries: int
    :param wait_time: The time to wait between retries
    :type wait_time: float
    :param exceptions: The exceptions to catch
    :type exceptions: Tuple[Exception]
    :return: The decorated function
    :rtype: Callable
    """

    def decorator(func):
        # @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(num_retries + 1):
                try:
                    result = func(*args, **kwargs)
                except exceptions as e:
                    if i < num_retries:
                        time.sleep(wait_time)
                        continue
                    else:
                        raise e
                return result

        return wrapper

    return decorator


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def colorize_str(str, color="CYAN"):
    bcolor_ref = {
        "HEADER": bcolors.HEADER,
        "BLUE": bcolors.OKBLUE,
        "CYAN": bcolors.OKCYAN,
        "GREEN": bcolors.OKGREEN,
        "WARNING": bcolors.WARNING,
        "FAIL": bcolors.FAIL,
        "BOLD": bcolors.BOLD,
        "UNDERLINE": bcolors.UNDERLINE,
    }
    return f"{bcolor_ref[color]}{str}{bcolors.ENDC}"
