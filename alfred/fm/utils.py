import base64
import gc
import logging
from collections import OrderedDict
from typing import List, Union, Optional, Callable
import io

import numpy as np
import torch
import transformers
from PIL import Image
from torch.nn.utils.rnn import pad_sequence

import time

from .query import Query, RankedQuery, CompletionQuery
from .response import RankedResponse

logger = logging.getLogger(__name__)

LMT_SIZE_FACTOR = 65536


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


def batch_multimodal(queries: List[Query], mode: str, batch_size=64):
    """
    Batch RankedQueries with Multimodal Payloads

    :param queries: A list of multimodal queries
    :type queries: List[Query]
    :param mode: The mode of the multimodal query ("autoregressive", "contrastive")
    :type mode: str
    :param batch_size: The batch size
    :type batch_size: int
    :return: A list of batches of multimodal ranked queries
    :rtype: List[List[Query]]
    """
    if mode == "contrastive":
        candidates = queries[0].candidates
        batches = []
        batch = []
        for query in queries:
            if len(batch) == batch_size:
                batches.append((batch, candidates))
                batch = []
            batch.append(query.prompt)
        if len(batch) > 0:
            batches.append((batch, candidates))
    elif mode == "autoregressive":
        batches = []
        batch = []
        for query in queries:
            if len(batch) == batch_size:
                batches.append(batch)
                batch = []
            if isinstance(query, Query):
                batch.append(query.prompt)
            else:
                batch.append(query)
        if len(batch) > 0:
            batches.append(batch)
    else:
        raise ValueError(f"Unknown multimodal mode {mode}")
    return batches


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


class EmbeddingCache:
    """
    A simple embedding cache for VLM models
    """

    def __init__(self, max_size: int = 32):
        self.max_size = max_size
        self.cache = {}

    def __contains__(self, key):
        if isinstance(key, Image.Image):
            key = key.tobytes()
        return key in self.cache

    def __getitem__(self, key):
        if isinstance(key, Image.Image):
            key = key.tobytes()
        return self.cache[key]

    def __setitem__(self, key, value):
        if len(self.cache) >= self.max_size:
            self.cache.pop(next(iter(self.cache)))
        if isinstance(key, Image.Image):
            key = key.tobytes()
        self.cache[key] = value

    def get(
        self,
        inputs: Union[List[Image.Image], List[str]],
        embedding_proc: Callable,
    ) -> torch.tensor:
        """
        Process the inputs and retrieve from the cache/embed the inputs

        :param inputs: A list of inputs
        :type inputs: Union[List[Image.Image], List[str]]
        :param embedding_proc: The embedding function
        :type embedding_proc: Callable
        :return: The embeddings
        :rtype: torch.tensor
        """
        cached_embeddings = []
        new_inputs = []

        cached_idx, new_inp_idx = [], []
        for inp_idx, inp in enumerate(inputs):
            if inp in self:
                cached_embeddings.append(self[inp])
                cached_idx.append(inp_idx)
            else:
                new_inputs.append(inp)
                new_inp_idx.append(inp_idx)

        if len(new_inputs) == 0:
            return torch.stack(cached_embeddings)

        new_embeddings = embedding_proc(new_inputs)
        for inp, embedding in zip(new_inputs, new_embeddings):
            self[inp] = embedding
        return torch.stack(
            reorder_array(
                list(new_embeddings) + cached_embeddings, new_inp_idx + cached_idx
            )
        )


class TokenizedBatch:
    def __init__(self, token_ids, pad_token_id=0):
        self.input_ids = pad_sequence(
            token_ids, batch_first=True, padding_value=pad_token_id
        ).long()
        self.attention_mask = (self.input_ids != pad_token_id).long()

    def __len__(self):
        return len(self.input_ids)


class DynamicBatcher:
    """
    Dynamic Batching Utility
    Maximize GPU Utilization by batching queries of similar sizes
    """

    def __init__(
        self,
        queries: Union[List[Query], List[str]],
        max_batch_size: int = 2048,
        tokenizer: Optional[transformers.PreTrainedTokenizer] = None,
        max_token_length: int = 512,
    ):
        """
        Initialize a DynamicBatcher

        :param queries: A list of queries to be batched
        :type queries: Union[List[Query], List[str]]
        :param max_batch_size: The maximum batch size
        :type max_batch_size: int
        """
        self.len_sorted_idx = None
        self.queries = queries
        self.max_batch_size = max_batch_size

        if torch.cuda.is_available():
            gpu_mem = torch.cuda.get_device_properties(0).total_memory
            free_mem = gpu_mem - torch.cuda.memory_allocated(0)
            self.limit_size = free_mem / LMT_SIZE_FACTOR
        else:
            self.limit_size = LMT_SIZE_FACTOR

        self.max_batch_size = max_batch_size
        self.ranked = False
        self.tokenizer = tokenizer
        if self.tokenizer:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.max_token_length = max_token_length

        if isinstance(self.queries[0], RankedQuery):
            # Enforcing Uniform Candidate sizes and order across one set of RankedQueries
            self.candidates = self.queries[0].candidates
            self.candidate_size = len(self.candidates)
            self.ranked = True

    def merge_rank_response(
        self,
        responses: List[OrderedDict],
        softmax: bool = True,
    ) -> RankedResponse:
        """
        Merge a list of responses with raw logit into a single RankedResponse
        Assumption: Candidate Order is the same across all ranked queries

        :param responses: A list of responses to be merged
        :type responses: List[OrderedDict]
        :param softmax: Whether to apply softmax to the logits
        :type softmax: bool
        :return: A merged response
        :rtype: RankedResponse
        """
        assert self.candidate_size == len(responses)

        scores = torch.empty(self.candidate_size)
        candidates = []
        for response_idx, response in enumerate(responses):
            scores[response_idx] = response["logit"]
            candidates.append(response["candidate"])

        logits = {
            candidate: score.item() for candidate, score in zip(candidates, scores)
        }

        if softmax:
            scores = torch.nn.functional.softmax(scores, dim=0)
        pred = candidates[int(torch.argmax(scores, dim=0))]

        scores = {
            candidate: score.item() for candidate, score in zip(candidates, scores)
        }

        return RankedResponse(
            prediction=pred,
            scores=scores,
            logits=logits,
            embeddings=responses[0]["hidden_state"],
        )

    def reorder(
        self,
        inst: List,
        offset: Optional[int] = None,
    ) -> List:
        """
        Reordering the responses according to the original order of the queries

        :param inst: The list of responses to be reordered
        :type inst: List
        :param offset: The offset of the responses
        :type offset: Optional[int]
        :return: The reordered responses
        :rtype: List of responses
        """

        if len(inst) != len(self.len_sorted_idx):
            if offset:
                _inst = np.empty([len(inst)])
                for idx, i in enumerate(
                    self.len_sorted_idx[offset : offset + len(inst)]
                ):
                    _inst[idx] = inst[i]
                return list(_inst)
            raise ValueError(
                f"Length of inst {len(inst)} does not match length of sorted index {len(self.len_sorted_idx)}"
            )
        if self.len_sorted_idx is None:
            raise ValueError("Batching has not been performed yet")

        reordered_inst = reorder_array(inst, self.len_sorted_idx)

        if self.ranked:
            reordered_inst = [
                self.merge_rank_response(reordered_inst[i : i + self.candidate_size])
                for i in range(0, len(reordered_inst), self.candidate_size)
            ]

        clear_cuda_cache()
        return list(reordered_inst)

    def batch(self) -> List:
        """
        Batch a list of instances into a list of batches.
        If the instances are of different sizes, they will be sorted by size
        and batched accordingly

        :return: A list of batches
        :rtype: List[List[Instance]]
        """

        def _process_batch(batch):
            if self.tokenizer:
                if isinstance(batch[0], tuple):
                    batch, candidate = zip(*batch)
                    return (TokenizedBatch(batch), candidate)
                else:
                    return TokenizedBatch(batch)
            return batch

        logger.info(f"Batching queries with tokenizer? {self.tokenizer is not None}")

        insts = []
        candidates = []
        inst_len = []
        for query in self.queries:
            if isinstance(query, str):
                inst, ilen = tokenize(query, self.tokenizer, self.max_token_length)
                insts.append(inst)
                inst_len.append(ilen)
            elif isinstance(query, CompletionQuery):
                inst, ilen = tokenize(
                    query.load()[0], self.tokenizer, self.max_token_length
                )
                insts.append(inst)
                inst_len.append(ilen)
            elif isinstance(query, RankedQuery):
                inst, ilen = tokenize(
                    query.prompt, self.tokenizer, self.max_token_length
                )
                insts += [inst] * self.candidate_size
                inst_len += [ilen] * self.candidate_size
                candidates += self.candidates
            else:
                logger.error(f"Unknown query type {type(query)}")
                raise ValueError(f"Input type {type(query)} not supported")

        ranked = len(candidates) > 0
        if ranked:
            self.limit_size /= self.candidate_size
        inst_len_sorted, inst_len_sorted_idx = torch.sort(
            torch.tensor(inst_len), descending=True
        )

        self.len_sorted_idx = inst_len_sorted_idx

        curr_batch = []
        curr_max = -1
        curr_batch_sz = 0

        batches = []
        for sorted_idx, index in enumerate(inst_len_sorted_idx):
            inst_len = inst_len_sorted[sorted_idx]
            curr_inst = (insts[index], candidates[index]) if ranked else insts[index]
            curr_max = max(curr_max, inst_len)
            new_sz = curr_max * curr_max * curr_batch_sz
            if new_sz >= self.limit_size or curr_batch_sz >= self.max_batch_size:
                batches.append(_process_batch(curr_batch))
                curr_batch = [curr_inst]
                curr_max = inst_len
                curr_batch_sz = 1
            else:
                curr_batch.append(curr_inst)
                curr_batch_sz += 1

        batches.append(_process_batch(curr_batch))

        clear_cuda_cache()

        return batches


def static_batch(queries: Query, batch_size: int = 1024) -> List[List[Query]]:
    """
    Static Batching Utility
    Batch queries into fixed size batches

    :param queries: A list of queries to be batched
    :type queries: List[Query]
    :param batch_sz: The batch size
    :type batch_sz: int
    :return: A list of batches
    :rtype: List[List[Query]]
    """
    batches = []
    batch = []
    for query in queries:
        if len(batch) == batch_size:
            batches.append(batch)
            batch = []
        if isinstance(query, CompletionQuery):
            _q = query.load()[0]
        elif isinstance(query, RankedQuery):
            _q = query.prompt
        batch.append(_q)
    if len(batch) > 0:
        batches.append(batch)
    return batches
