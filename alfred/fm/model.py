import abc
import logging
import numpy as np
import os
import torch
from contextlib import nullcontext
from tqdm.auto import tqdm
from typing import List, Optional, Dict, Union, Tuple, OrderedDict, Any

from .query import Query, RankedQuery, CompletionQuery
from .response import Response, CompletionResponse, RankedResponse
from .utils import DynamicBatcher, clear_cuda_cache, batch_multimodal

logger = logging.getLogger(__name__)


class FoundationModel(abc.ABC):
    """
    Generic interface for foundation model class
    """

    def _generate_batch(
            self,
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

    def _score_batch(
            self,
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

    def _encode_batch(
            self,
            batch_instance: Union[List[str]],
            **kwargs: Any,
    ) -> List[torch.Tensor]:
        """
        For encoding queries into embeddings.

        :param batch_instance: A batch of query objects or raw query content (e.g. string or embedding arrays)
        :type batch_instance: Union[List[RankedQuery], List[str]]
        :return: A list of responses
        :rtype List[Response]
        """
        raise NotImplementedError(
            f"_encode_batch() is not implemented for {self.__class__.__name__}"
        )

    def forward(
            self,
            queries: Union[List[Query], List[str], List[Tuple[str, str]]],
            batch_policy: str = 'dynamic',
            batch_size: int = 1024,
            mode: str = 'generate',
            pretokenize: bool = True,
            **kwargs,
    ) -> Union[List[CompletionResponse], List[RankedResponse],
    List[OrderedDict], List[torch.Tensor]]:
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
        :param mode: LLM inference mode, choose from ['generate', 'score', 'encode']
        :type mode: str
        :param pretokenize: Whether to tokenize the queries while batching
        :type pretokenize: bool
        :param kwargs: Additional arguments to pass to the foundation model
        :type kwargs: Any
        :return: A list of responses
        :rtype: Union[List[CompletionResponse], List[RankedResponse], List[OrderedDict], List[torch.Tensor]]
        """
        with_grad = kwargs.get('with_grad', False)
        no_tqdm = kwargs.get('no_tqdm', False)

        if type(queries[0]) in [RankedQuery, tuple]:
            mode = 'score'

        if mode == 'generate':
            inferece_fn = self._generate_batch
        elif mode == 'score':
            inferece_fn = self._score_batch
        elif mode == 'encode':
            inferece_fn = self._encode_batch
        else:
            raise ValueError(f"mode {mode} not supported")

        if isinstance(self, LocalAccessFoundationModel):
            try:
                if self.processor:
                    batch_policy = 'static'
                    batched_queries = batch_multimodal(queries,
                                                       batch_size=batch_size)
                    pretokenized = False
                    inferece_fn = self._score_batch
            except AttributeError:
                if batch_policy == 'static':
                    # To near equally sized batches
                    batched_queries = np.array_split(
                        queries,
                        len(queries) // batch_size)
                    pretokenized = False
                elif batch_policy == 'dynamic':
                    if pretokenize:
                        pretokenized = True
                        try:
                            tokenizer = self.tokenizer
                        except AttributeError:
                            logger.error(
                                "Tokenizer not found. Please set the tokenizer attribute for the model"
                            )
                            tokenizer = None
                            pretokenized = False
                    else:
                        pretokenized = False
                        tokenizer = None
                    DB = DynamicBatcher(queries,
                                        tokenizer=tokenizer,
                                        max_batch_size=batch_size)
                    batched_queries = DB.batch()
                else:
                    raise ValueError(
                        f"batch_policy {batch_policy} not supported")
        else:
            batch_policy = 'static'
            batched_queries = np.array_split(queries, len(queries))
            pretokenized = False

        logger.log(logging.INFO, f"Inferring {len(batched_queries)} batches")

        attempts = 0
        while attempts < 3:
            try:
                with nullcontext() if with_grad else torch.no_grad():
                    responses = []
                    for batch_id, batch in enumerate(
                            tqdm(batched_queries, disable=no_tqdm)):
                        responses += inferece_fn(batch,
                                                 tokenized=pretokenized,
                                                 **kwargs)
                    break
            except RuntimeError as e:
                attempts += 1
                if "out of memory" in str(e):
                    logger.log(
                        logging.INFO,
                        "WARNING: out of memory, trying to allocate a new batch",
                    )
                    clear_cuda_cache()
                    if batch_policy == 'static':
                        batch_size = int(batch_size * 0.8)
                        batched_queries = np.array_split(
                            queries,
                            len(queries) // batch_size)
                        logging.info(f"New batch size: {batch_size}")
                    elif batch_policy == 'dynamic':
                        DB.limit_size = int(DB.limit_size * 0.9)
                        DB.max_batch_size = int(DB.max_batch_size * 0.9)
                        batched_queries = DB.batch()
                        logging.info(
                            f"New lmt_sz, bs: {DB.limit_size}, {DB.max_batch_size}"
                        )
                else:
                    raise e

        if batch_policy == 'dynamic':
            responses = DB.reorder(responses)

        return list(responses)

    def generate(
            self,
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

    def score(
            self,
            queries: List[RankedQuery],
            batch_policy: str = 'dynamic',
            batch_size: int = 64,
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

        return self.forward(queries,
                            batch_policy,
                            batch_size,
                            mode="score",
                            **kwargs)

    def encode(
            self,
            queries: Union[List[Query], List[str]],
            batch_policy: str = 'dynamic',
            batch_size: int = 1024,
            reduction: str = 'mean',
            **kwargs: Any,
    ) -> List[torch.Tensor]:
        """
        This function is a wrapper around the forward function

        :param queries:  A list of Query or raw query content (as string)
        :type queries: Union[List[Query], List[str]]
        :param batch_policy: The batching policy to use. Can be either 'dynamic' or 'static'
        :type batch_policy: str
        :param batch_size: The batch size to use for static batching or maximum batch size for dynamic batching
        :type batch_size: int
        :param reduction: The reduction method to use for the encoded queries. Can be either 'mean' or 'concat'
        :type reduction: str
        :return: A list of encoded queries
        :rtype: List[torch.Tensor]
        """
        return self.forward(queries,
                            batch_policy,
                            batch_size,
                            mode="encode",
                            reduction=reduction,
                            **kwargs)

    def run(
            self,
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
                mode = 'score'
            elif type(queries[0]) in [str, CompletionQuery]:
                mode = 'generate'
            else:
                raise ValueError(f"Unsupported query type {type(queries[0])}")
            return self.forward(queries, mode=mode, **kwargs)
        elif isinstance(queries, RankedQuery) or isinstance(queries, tuple):
            return self.forward([queries], mode="score", **kwargs)[0]
        elif isinstance(queries, CompletionQuery) or isinstance(queries, str):
            return self._generate_batch(
                queries.load() if isinstance(queries, CompletionQuery) else
                [queries], **kwargs)[0]
        else:
            logger.warning(
                f"Unsupported query type {type(queries)}, Attempting to run")
            return self.forward(queries, **kwargs)

    def __call__(
            self,
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
    def __init__(self, model_string: str, cfg: Optional[Dict] = None):
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
    def __init__(self, model_string: str, local_path: Optional[str] = None):
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
            self.local_path = os.path.join(os.path.expanduser('~'),
                                           '.model_cache', model_string)
        self.model_string = model_string
