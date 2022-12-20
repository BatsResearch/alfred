import abc
import logging
import os
from contextlib import nullcontext
from typing import List, Optional, Dict, Union, Tuple, OrderedDict, Any

import numpy as np
import torch
from tqdm.auto import tqdm

from .query import Query, RankedQuery, CompletionQuery
from .response import Response, CompletionResponse, RankedResponse
from .utils import DynamicBatcher

logger = logging.getLogger(__name__)


class FoundationModel(abc.ABC):
    """
    Generic interface for foundation model class
    """

    @abc.abstractmethod
    def _generate_batch(self,
                        batch_instance: Union[List[str]],
                        **kwargs,
                        ) -> List[Response]:
        """
        For completing / generating given a batch of queries
        Run a batch of queries through the foundation model

        :param batch_instance: A batch of query objects or raw query content (e.g. string or embedding arrays)
        :type batch_instance: Union[List[CompletionQuery], List[str]]
        :param kwargs: Additional arguments to pass to the foundation model
        :type batch_instance: Union[List[CompletionQuery], List[str]]
        :return: A list of responses
        :rtype List[Response]
        """
        raise NotImplementedError(
            f"_infer_batch() is not implemented for {self.__class__.__name__}")

    @abc.abstractmethod
    def _score_batch(self,
                     batch_instance: Union[List[Tuple[str, str]], List[str]],
                     **kwargs,
                     ) -> List[Response]:
        """
        For scoring / ranking candidate queries.
        Run a batch of queries through the foundation model.

        :param batch_instance: A batch of query objects or raw query content (e.g. string or embedding arrays)
        :type batch_instance: Union[List[RankedQuery], List[str]]
        :return: A list of responses
        :rtype List[Response]
        """
        raise NotImplementedError(
            f"_score_batch() is not implemented for {self.__class__.__name__}")

    def forward(self,
                queries: Union[List[Query],
                List[str],
                List[Tuple[str, str]]],
                batch_policy: str = 'dynamic',
                batch_size: int = 1024,
                score: bool = False,
                **kwargs,
                ) -> Union[List[CompletionResponse],
    List[RankedResponse],
    List[OrderedDict]]:
        """
        This function is the main entry point for running queries through the foundation model.
        It accepts raw query content and automatically converts it into query objects.
        The function then determines whether to run the queries through the _generate_batch
        or _score_batch method based on the type of queries. Finally, the function processes
        the queries using one of two batching policies (dynamic, static) and passes them
        through the foundation model.

        :param queries: A list of queries
        :type queries: Union[List[Query], List[str], List[Tuple[str, str]]]
        :param batch_policy: The batching policy to use. Can be either 'dynamic' or 'static'
        :type batch_policy: str
        :param batch_size: The batch size to use for static batching or maximum batch size for dynamic batching
        :type batch_size: int
        :param score: Whether to run the queries through the _score_batch() method
        :type score: bool
        :param kwargs: Additional arguments to pass to the foundation model
        :type kwargs: Any
        :return: A list of responses
        :rtype: Union[List[CompletionResponse], List[RankedResponse], List[OrderedDict]]
        """

        with_grad = kwargs.get('with_grad', False)
        no_tqdm = kwargs.get('no_tqdm', False)

        if type(queries[0]) in [RankedQuery, tuple]:
            score = True

        if batch_policy == 'static':
            # To near equally sized batches
            batched_queries = np.array_split(
                queries, len(queries) // batch_size
            )
        elif batch_policy == 'dynamic':
            DB = DynamicBatcher(queries, max_batch_size=batch_size)
            batched_queries = DB.batch()
        else:
            raise ValueError(f"batch_policy {batch_policy} not supported")

        inferece_fn = self._score_batch if score else self._generate_batch
        logger.log(logging.INFO, f"Inferring {len(batched_queries)} batches")

        with nullcontext() if with_grad else torch.no_grad():
            responses = []
            for batch_id, batch in enumerate(
                    tqdm(batched_queries, disable=no_tqdm)):
                responses += inferece_fn(batch, **kwargs)

        if score:
            # Assuming candidates are the same for all queries for one
            # run/batch
            try:
                candidate_token_len = [
                    len(x) for x in self.model.tokenizer(
                        list(
                            queries[0].candidates),
                        padding=True,
                        add_special_tokens=False).input_ids]
            except BaseException:
                logger.info(
                    "Unable to get candidate token length, defaulting to token length of 1")
                candidate_token_len = [1] * len(queries[0].candidates)
        else:
            candidate_token_len = None

        if batch_policy == 'dynamic':
            responses = DB.reorder(
                responses, candidate_token_len=candidate_token_len)

        return list(responses)

    def generate(self,
                 queries: Union[List[CompletionQuery], List[str]],
                 batch_policy: str = 'dynamic',
                 batch_size: int = 1024,
                 **kwargs,
                 ) -> List[CompletionResponse]:
        """
        This function is a wrapper around the forward function for running
        CompletionQuery objects through the foundation model. It returns a list
        of CompletionResponse objects.

        :param queries:  A list of CompletionQuery or raw query content (as string)
        :type queries: Union[List[CompletionQuery], List[str]]
        :param batch_policy: The batching policy to use. Can be either 'dynamic' or 'static'
        :type batch_policy: str
        :param batch_size: The batch size to use for static batching or maximum batch size for dynamic batching
        :type batch_size: int
        :param kwargs: Additional arguments to pass to the foundation model
        :type kwargs: Any
        :return: A list of CompletionResponse
        :rtype: List[CompletionResponse]
        """
        return self.forward(queries, batch_policy, batch_size, **kwargs)

    def score(self,
              queries: List[RankedQuery],
              batch_policy: str = 'dynamic',
              batch_size: int = 1024,
              **kwargs: Any,
              ) -> List[RankedResponse]:
        """
        This function is a wrapper around the forward function
        for running RankedQuery objects through the foundation model.
        It returns a list of RankedResponse objects.

        :param queries:  A list of RankedQuery
        :type queries: List[RankedQuery]
        :param batch_policy: The batching policy to use. Can be either 'dynamic' or 'static'
        :type batch_policy: str
        :param batch_size: The batch size to use for static batching or maximum batch size for dynamic batching
        :type batch_size: int
        :param kwargs: Additional arguments to pass to the foundation model
        :type kwargs: Any
        :return: A list of RankedResponse
        :rtype: List[RankedResponse]
        """

        return self.forward(
            queries,
            batch_policy,
            batch_size,
            score=True,
            **kwargs)

    def run(self,
            queries: Union[Query, str, Tuple[str, str], List[Query], List[str]],
            **kwargs: Any,
            ) -> Union[str, Response, List[Response]]:
        """
        This function is the main entry point for users to run queries through the foundation model.
        It accepts raw query content and automatically converts it into query objects.
        The function then processes the queries and returns the responses in the appropriate format.
        For single instance queries, a single response object is returned.

        :param queries: A single query or a list of queries
        :type queries: Union[Query, str, Tuple[str, str], List[Query], List[str]]
        :param kwargs: Additional arguments to pass to the foundation model
        :type kwargs: Any
        :return: A single response or a list of responses
        :rtype: Union[str, Response, List[Response]]
        """
        if isinstance(queries, list):
            if type(queries[0]) in [tuple, RankedQuery]:
                score = True
            elif type(queries[0]) in [str, CompletionQuery]:
                score = False
            else:
                raise ValueError(f"Unsupported query type {type(queries[0])}")
            return self.forward(queries, score=score, **kwargs)
        elif isinstance(queries, RankedQuery) or isinstance(queries, tuple):
            return self.forward([queries], score=True, **kwargs)[0]
        elif isinstance(queries, CompletionQuery) or isinstance(queries, str):
            return self._generate_batch(queries.load() if isinstance(
                queries, CompletionQuery) else [queries], **kwargs)[0]
        else:
            logger.warning(
                f"Unsupported query type {type(queries)}, Attempting to run")
            return self.forward(queries, **kwargs)

    def __call__(self,
                 queries: Union[Query, str, Tuple[str, str], List[Query], List[str]],
                 **kwargs: Any,
                 ) -> Union[str, Response, List[Response]]:
        """
        This function returns the output of the run function when the
         model is called as a function. It can be used as model(queries),
         which is equivalent to model.run(queries).

        :param queries: A single query or a list of queries
        :type queries: Union[Query, str, dict, List[Query], List[str], List[dict]]
        :param kwargs: Additional arguments to pass to the foundation model
        :type kwargs: Any
        :return: A single response or a list of responses
        :rtype: Union[str, Response, List[Response]]
        """

        return self.run(queries)


class APIAccessFoundationModel(FoundationModel):
    def __init__(self,
                 model_string: str,
                 cfg: Optional[Dict] = None):
        """
        Initializes the APIAccessFoundationModel class,
        which wraps API-based models such as OpenAI GPT-3, Cohere, and AI21 etc.

        :param model_string: The model string to use (e.g. text-davinci-003 for OpenAI GPT-3)
        :type model_string: str
        :param cfg: (optional) A dictionary containing configuration options for the model
        :type cfg: Dict
        """
        self.cfg = cfg
        self.model_string = model_string


class LocalAccessFoundationModel(FoundationModel):
    def __init__(self,
                 model_string: str,
                 local_path: Optional[str] = None):
        """
        Initializes the LocalAccessFoundationModel class,
         which wraps a local serving model such as PyTorch or HuggingFace.

        :param model_string: The model string that defines the model type
                                (e.g. gpt2 for HuggingFace GPT-2)
        :type model_string: str
        :param local_path: (optional) The path to the local model directories.
               If not provided, the default path ~/.model_cache/{model_string} will be used.
        :type local_path: str
        """
        self.local_path = local_path
        if local_path is None:
            self.local_path = os.path.join(
                os.path.expanduser('~'), '.model_cache', model_string)
        self.model_string = model_string
