import gc
import logging
from collections import OrderedDict
from typing import List, Union, Tuple, Optional

import numpy as np
import torch

from .query import Query, RankedQuery, CompletionQuery
from .response import RankedResponse

logger = logging.getLogger(__name__)

LMT_SIZE_FACTOR = 86381


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


def reorder_array(
    arr: Union[np.ndarray, torch.Tensor,
               list], order: Union[np.ndarray, torch.Tensor, list]
) -> Union[np.ndarray, torch.Tensor, list]:
    """
    Reorder an array according to a given order.

    This function reorders the elements in an array according to the order specified by a separate array.

    :param arr: The array to be reordered. Can be a NumPy array, PyTorch tensor, or Python list.
    :type arr: Union[np.ndarray, torch.Tensor, list]
    :param order: The order array. Can be a NumPy array, PyTorch tensor, or Python list.
    :type order: Union[np.ndarray, torch.Tensor, list]
    :return: The reordered array. Has the same type as the input `arr`.
    :rtype: Union[np.ndarray, torch.Tensor, list]
    """
    if isinstance(arr, list):
        if isinstance(arr[0], torch.Tensor):
            arr = torch.stack(arr)
        else:
            arr = np.array(arr, object)
    if isinstance(order, list):
        order = np.array(order)
    return arr[order]


class DynamicBatcher:
    """
    Dynamic Batching Utility
    Maximize GPU Utilization by batching queries of similar sizes
    """
    def __init__(
        self,
        queries: Union[List[Query], List[str]],
        max_batch_size: int = 2048,
    ):
        """
        Initialize a DynamicBatcher

        :param queries: A list of queries to be batched
        :type queries: Union[List[Query], List[str]]
        :param max_batch_size: The maximum batch size
        :type max_batch_size: int
        """
        self.queries = queries
        self.max_batch_size = max_batch_size

        if torch.cuda.is_available():
            gpu_mem = torch.cuda.get_device_properties(0).total_memory
            free_mem = gpu_mem - torch.cuda.memory_allocated(0)
        else:
            free_mem = -1

        # Get Approximate Maximum Batch Size
        if free_mem > 0:
            self.max_batch_size = min(int(free_mem / LMT_SIZE_FACTOR),
                                      max_batch_size)
        self.limit_size = LMT_SIZE_FACTOR
        self.ranked = False
        if isinstance(self.queries[0], RankedQuery):
            # Enforcing Uniform Candidate sizes and order across one set of
            # RankedQueries
            self.candidates = self.queries[0].candidates
            self.candidate_size = len(self.candidates)
            self.ranked = True

    def merge_rank_response(
        self,
        responses: List[OrderedDict],
        softmax: bool = True,
        candidate_token_len: Union[List[int], int] = 1,
    ) -> RankedResponse:
        """
        Merge a list of responses with raw logit into a single RankedResponse
        Assumption: Candidate Order is the same across all ranked queries

        :param responses: A list of responses to be merged
        :type responses: List[OrderedDict]
        :param softmax: Whether to apply softmax to the logits
        :type softmax: bool
        :param candidate_token_len: The length of the candidate in terms of tokens
        :type candidate_token_len: Union[List[int], int]
        :return: A merged response
        :rtype: RankedResponse
        """
        if isinstance(candidate_token_len, int):
            candidate_token_len = [candidate_token_len] * len(self.candidates)

        scores = torch.empty(len(candidate_token_len))
        # embeddings = []
        for response_idx, response in enumerate(responses):
            scores[response_idx] = response['logit']
            # embeddings.append(response['hidden_state'])

        if softmax:
            scores = torch.nn.functional.softmax(scores, dim=0)
        pred = self.candidates[int(torch.argmax(scores, dim=0))]

        scores = {
            candidate: score.item()
            for candidate, score in zip(self.candidates, scores)
        }

        # embeddings = {
        #     candidate: embedding
        #     for candidate, embedding in zip(self.candidates, embeddings)
        # }

        return RankedResponse(
            prediction=pred,
            scores=scores,
            embeddings=responses[0]['hidden_state'],
        )

    def reorder(
            self,
            inst: List,
            offset: Optional[int] = None,
            candidate_token_len: Optional[Union[int,
                                                List[int]]] = None) -> List:
        """
        Reordering the responses according to the original order of the queries

        :param inst: The list of responses to be reordered
        :type inst: List
        :param offset: The offset of the responses
        :type offset: Optional[int]
        :param candidate_token_len: The length of the candidate in terms of tokens
        :type candidate_token_len: Optional[Union[int, List[int]]]
        :return: The reordered responses
        :rtype: List of responses
        """

        if len(inst) != len(self.len_sorted_idx):
            if offset:
                _inst = np.empty([len(inst)])
                for idx, i in enumerate(self.len_sorted_idx[offset:offset +
                                                            len(inst)]):
                    _inst[idx] = inst[i]
                return list(_inst)
            raise ValueError(
                f"Length of inst {len(inst)} does not match length of sorted index {len(self.len_sorted_idx)}"
            )
        if self.len_sorted_idx is None:
            raise ValueError("Batching has not been performed yet")

        reordered_inst = reorder_array(inst, self.len_sorted_idx)

        if self.ranked:
            assert len(candidate_token_len) == len(
                self.candidates
            ), f"Length of candidate_token_len {len(candidate_token_len)} does not match length of candidates {len(self.candidates)}"
            reordered_inst = [
                self.merge_rank_response(reordered_inst[i:i +
                                                        self.candidate_size])
                for i in range(0, len(reordered_inst), self.candidate_size)
            ]

        clear_cuda_cache()
        return list(reordered_inst)

    def batch(self) -> List:
        '''
        Batch a list of instances into a list of batches.
        If the instances are of different sizes, they will be sorted by size
        and batched accordingly

        :return: A list of batches
        :rtype: List[List[Instance]]
        '''
        insts = []
        candidates = []
        for query in self.queries:
            if isinstance(query, str):
                insts.append(query)
            elif isinstance(query, CompletionQuery):
                insts += query.load()
            elif isinstance(query, RankedQuery):
                insts += [query.prompt] * len(query.candidates)
                candidates += query.candidates
            elif isinstance(query, Tuple):
                insts.append(query[0])
                candidates.append(query[1])
            else:
                logger.error(f"Unknown query type {type(query)}")
                raise ValueError(f"Input type {type(query)} not supported")

        ranked = len(candidates) > 0
        if ranked:
            self.limit_size /= self.candidate_size
        inst_len = [len(inst) for inst in insts]
        inst_len_sorted, inst_len_sorted_idx = torch.sort(
            torch.tensor(inst_len), descending=True)

        self.len_sorted_idx = inst_len_sorted_idx

        curr_batch = []
        curr_sz = 0
        curr_max = -1
        curr_batch_sz = 0

        batches = []
        for sorted_idx, index in enumerate(inst_len_sorted_idx):
            inst_len = inst_len_sorted[sorted_idx]
            curr_inst = (insts[index],
                         candidates[index]) if ranked else insts[index]
            if curr_sz < self.limit_size and curr_batch_sz < self.max_batch_size:
                curr_max = max(curr_max, inst_len)
                new_sz = curr_max * curr_batch_sz
                if new_sz >= self.limit_size or curr_batch_sz >= self.max_batch_size:
                    batches.append(curr_batch)
                    curr_batch = [curr_inst]
                    curr_sz = inst_len
                    curr_max = inst_len
                    curr_batch_sz = 1
                else:
                    curr_batch.append(curr_inst)
                    curr_batch_sz += 1
                    curr_sz = new_sz
            else:
                batches.append(curr_batch)
                curr_batch = [curr_inst]
                curr_sz = inst_len
                curr_max = inst_len
                curr_batch_sz = 1
        batches.append(curr_batch)

        clear_cuda_cache()

        return batches
