from itertools import islice
from typing import List, Union, Optional, Any

import torch
import transformers
import logging

from ..response import RankedResponse
from ..query import Query, RankedQuery, CompletionQuery

logger = logging.getLogger(__name__)


class StaticBatcher:
    """
    Static Batching Utility
    Batch queries into fixed size batches
    """

    def __init__(
        self,
        queries: Union[List[Query], List[str]],
        max_batch_size: int = 512,
        tokenizer: Optional[transformers.PreTrainedTokenizer] = None,
        max_token_length: int = 512,
    ):
        """
        Initialize a StaticBatcher

        :param queries: A list of queries to be batched
        :type queries: Union[List[Query], List[str]]
        :param max_batch_size: The maximum batch size
        :type max_batch_size: int
        :param tokenizer: Optional tokenizer for processing queries
        :type tokenizer: Optional[transformers.PreTrainedTokenizer]
        :param max_token_length: Maximum token length for tokenization
        :type max_token_length: int
        """
        self.queries = queries
        self.max_batch_size = max_batch_size
        self.tokenizer = tokenizer
        if self.tokenizer:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.max_token_length = max_token_length

        self.ranked = False
        self.candidates = None
        self.candidate_size = 0

        if isinstance(self.queries[0], RankedQuery):
            self.ranked = True
            self.candidates = self.queries[0].candidates
            self.candidate_size = len(self.candidates)

    def batch(self) -> List[List[Any]]:
        """
        Batch a list of instances into a list of batches.

        :return: A list of batches
        :rtype: List[List[Any]]
        """

        def query_generator(queries):
            for query in queries:
                if isinstance(query, CompletionQuery):
                    yield query.load()[0]
                elif isinstance(query, RankedQuery):
                    for candidate in query.candidates:
                        yield (query.prompt, candidate)
                elif isinstance(query, str):
                    yield query
                else:
                    raise ValueError(f"Unknown query type {type(query)}")

        iterator = query_generator(self.queries)
        batches = []

        while True:
            batch = list(islice(iterator, self.max_batch_size))
            if not batch:
                break
            if self.tokenizer:
                batch = self._tokenize_batch(batch)
            batches.append(batch)

        return batches

    def _tokenize_batch(self, batch):
        tokenized_batch = []
        for item in batch:
            if isinstance(item, tuple):
                prompt, candidate = item
                tokenized = self.tokenizer(
                    prompt,
                    candidate,
                    max_length=self.max_token_length,
                    truncation=True,
                    padding="max_length",
                    return_tensors="pt",
                )
            else:
                tokenized = self.tokenizer(
                    item,
                    max_length=self.max_token_length,
                    truncation=True,
                    padding="max_length",
                    return_tensors="pt",
                )
            tokenized_batch.append(tokenized)
        return tokenized_batch

    def reorder(self, inst: List) -> List:
        """
        Reordering the responses according to the original order of the queries

        :param inst: The list of responses to be reordered
        :type inst: List
        :param offset: The offset of the responses
        :type offset: Optional[int]
        :return: The reordered responses
        :rtype: List
        """
        if self.ranked:
            inst = [
                self.merge_rank_response(inst[i : i + self.candidate_size])
                for i in range(0, len(inst), self.candidate_size)
            ]

        return inst

    def merge_rank_response(self, responses: List[dict]) -> RankedResponse:
        """
        Merge a list of responses with raw logit into a single ranked response

        :param responses: A list of responses to be merged
        :type responses: List[dict]
        :return: A merged response
        :rtype: RankedResponse
        """
        if not responses:
            raise ValueError("Empty response list")

        scores = torch.tensor([r["logit"] for r in responses])
        candidates = [r["candidate"] for r in responses]

        logits = {
            candidate: score.item() for candidate, score in zip(candidates, scores)
        }
        scores = torch.nn.functional.softmax(scores, dim=0)

        pred_index = int(torch.argmax(scores, dim=0))
        prediction = candidates[pred_index]

        normalized_scores = {
            candidate: score.item() for candidate, score in zip(candidates, scores)
        }

        return RankedResponse(
            prediction=prediction,
            scores=normalized_scores,
            logits=logits,
            embeddings=responses[0]["hidden_state"]
            if "hidden_state" in responses[0]
            else None,
        )
