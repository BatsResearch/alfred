import abc
import ast
import logging
from typing import Optional, List, Callable, Union, Any, Dict

import pandas as pd

from alfred.fm.query import Query
from alfred.fm.response import deserialize, Response

logger = logging.getLogger(__name__)


def to_metadata_string(**kwargs: Any) -> str:
    """
    Convert a dictionary of metadata to a string for storage in the cache

    :param kwargs: Dictionary of metadata
    :type kwargs: dict
    :return: String representation of the metadata
    :rtype: str
    """
    return str(kwargs)


def from_metadata_string(metadata_string: str) -> Dict:
    """
    Convert a string of metadata to a dictionary

    :param metadata_string: String representation of the metadata from the cache
    :type metadata_string: str
    :return: Dictionary of metadata
    :rtype: dict
    """
    return ast.literal_eval(metadata_string)


class Cache(abc.ABC):
    """
    Generic Interface for caching operation that wraps certain cache implementation

    Currently supported cache implementations:
        - DummyCache: Simple Dict-based
        - SqliteCache: Sqlite3 - based cache
    TODO:
        - RedisCache: Redis - based cache
    """
    @abc.abstractmethod
    def read(self, prompt: str, metadata: Optional[str] = None) -> list:
        """
        Read from cache by prompt and metadata

        :param prompt: Prompt string
        :type prompt: str
        :param metadata: (optional) Metadata string
        :type metadata: str
        :return: List of responses
        :rtype: list
        """
        raise NotImplementedError(
            f"read() is not implemented for {self.__class__.__name__}")

    @abc.abstractmethod
    def read_batch(self,
                   prompts: List[str],
                   metadata: Optional[str] = None) -> List[str]:
        """
        Read a value from the cache by list of serialized prompts and metadata

        :param prompts: List of serialized prompts
        :type prompts: list
        :param metadata: (optional) Metadata string
        :type metadata: str
        :return: List of serialized responses
        :rtype: list
        """
        raise NotImplementedError(
            f"read_batch() is not implemented for {self.__class__.__name__}")

    @abc.abstractmethod
    def write(self,
              prompt: str,
              response: str,
              metadata: Optional[str] = None):
        """
        Write a value to the cache by serialized prompt, serialized response and metadata

        :param prompt: Serialized prompt
        :type prompt: str
        :param response: Serialized response
        :type response: str
        :param metadata: (optional) Metadata string
        :type metadata: str
        """
        raise NotImplementedError(
            f"write() is not implemented for {self.__class__.__name__}")

    @abc.abstractmethod
    def write_batch(self,
                    prompts: List[str],
                    response: List[str],
                    metadata: Optional[str] = None):
        """
        Write a value to the cache by serialized prompts, serialized responses and metadata in batch

        :param prompts: List of serialized prompts
        :type prompts: List[str]
        :param response: List of serialized responses
        :type response: List[str]
        :param metadata: (optional) Metadata string
        :type metadata: str
        """
        raise NotImplementedError(
            f"write_batch() is not implemented for {self.__class__.__name__}")

    @abc.abstractmethod
    def read_by_prompt(self, prompt: str) -> List:
        """
        Read the record from the cache via serialized prompt

        :param prompt: Serialized prompt
        :type prompt: str
        :return: List of records
        :rtype: list
        """
        raise NotImplementedError(
            f"read_by_prompt() is not implemented for {self.__class__.__name__}"
        )

    @abc.abstractmethod
    def read_by_prompt_and_metadata(self, prompt: str, metadata: str) -> List:
        """
        Read the record from the cache via serialized prompt and metadata string

        :param prompt: Serialized prompt
        :type prompt: str
        :param metadata: Metadata string
        :type metadata: str
        :return: List of records
        :rtype: list
        """
        raise NotImplementedError(
            f"read_by_prompt_and_metadata() is not implemented for {self.__class__.__name__}"
        )

    @abc.abstractmethod
    def read_by_prompts_and_metadata(self, prompts: List[str],
                                     metadata: str) -> List:
        """
        Read the record from the cache via serialized prompts and metadata string

        :param prompts: List of serialized prompts
        :type prompts: List[str]
        :param metadata: Metadata string
        :type metadata: str
        :return: List of records
        :rtype: List
        """
        raise NotImplementedError(
            f"read_by_prompts_and_metadata() is not implemented for {self.__class__.__name__}"
        )

    @abc.abstractmethod
    def read_by_metadata(self, metadata: str) -> List:
        """
        Read the record from the cache by key

        :param metadata: Metadata string
        :type metadata: str
        :return: List of records
        :rtype: list
        """
        raise NotImplementedError(
            f"read_by_metadata() is not implemented for {self.__class__.__name__}"
        )

    @abc.abstractmethod
    def save(self, path: str):
        """
        Save the cache to disk

        :param path: Path to save the cache
        :type path: str
        """
        raise NotImplementedError(
            f"save() is not implemented for {self.__class__.__name__}")

    @abc.abstractmethod
    def load(self, path: str):
        """
        Load the cache from disk to the cache object

        :param path: Path to the cache file
        :type path: str
        """
        raise NotImplementedError(
            f"load() is not implemented for {self.__class__.__name__}")

    @abc.abstractmethod
    def to_pandas(self) -> pd.DataFrame:
        """
        Return the cache db as a pandas dataframe

        :return: Pandas dataframe
        :rtype: pd.DataFrame
        """
        raise NotImplementedError(
            f"to_pandas() is not implemented for {self.__class__.__name__}")

    def cached_query(self, model_run: Callable) -> Callable:
        """
        Decorator function for model queries, fetch from cache db if exist else write into cache_db

        TODO: [1]standardize serailized prompts str [2] Merge redundent queries

        :param model_run: Model run function
        :type model_run: Callable
        :return: Decorated function
        :rtype: Callable
        """
        def run_query(queries: Union[Response, List[Response], str, List[str]],
                      **kwargs: Any) -> Union[Response, List[Response]]:
            """
            Run query function wrapper that process the queries and
            fetch from cache db if exist else write into cache_db


            :param queries: List of queries
            :type queries: Union[Response, List[Response], str, List[str]]
            :param kwargs: Keyword arguments
            :type kwargs: Any
            :return: List of responses
            :rtype: Union[Response, List[Response]]
            """

            metadata = to_metadata_string(**kwargs)
            list_flag = isinstance(queries, list)
            queries = [queries] if not list_flag else queries

            try:
                # TODO: For now skip read_batch
                raise NotImplementedError
                responses, new_q_idx, _new_queries = self.read_batch(
                    queries, metadata)
                print(
                    f"Found {len(responses) - len(new_q_idx)} responses in cache"
                )
                logger.info(
                    f"Found {len(responses) - len(new_q_idx)} responses in cache"
                )
            except NotImplementedError:
                logger.info(
                    "Batch read not implemented, falling back to single read")
                responses, new_q_idx, new_queries = [], [], []
                for q_idx, query in enumerate(queries):
                    # TODO: Optimize for async reading from DB
                    cached_response = self.read(
                        query.serialize()
                        if isinstance(query, Query) else str(query), metadata)
                    if cached_response:
                        responses.append(deserialize(cached_response))
                    else:
                        responses.append(None)
                        new_q_idx.append(q_idx)
                _new_queries = [queries[idx] for idx in new_q_idx]
            if len(new_q_idx) > 0:
                logger.info(f"Running {len(new_q_idx)} queries")
                _model_responses = model_run(
                    _new_queries[0]
                    if len(_new_queries) == 1 else _new_queries, **kwargs)
                _model_responses = [_model_responses] if not isinstance(
                    _model_responses, list) else _model_responses
                _serialized_responses = [
                    response.serialize() for response in _model_responses
                ]
                _serialized_new_queries = [
                    query.serialize()
                    if isinstance(query, Query) else str(query)
                    for query in _new_queries
                ]
                try:
                    self.write_batch(_serialized_new_queries,
                                     _serialized_responses,
                                     metadata=metadata)
                except NotImplementedError:
                    for query, response in zip(_serialized_new_queries,
                                               _serialized_responses):
                        self.write(query, response, metadata=metadata)

                for idx, q_idx in enumerate(new_q_idx):
                    responses[q_idx] = _model_responses[idx]

            logger.info(f"Returning {len(responses)} responses")

            return responses[0] if not list_flag else responses

        return run_query
