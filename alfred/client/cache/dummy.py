from typing import Optional, List

from alfred.client.cache.cache import Cache


class DummyCache(Cache):
    """
    A simple in-memory cache implementation. (for testing)

    This class is intended as a dummy implementation of the `Cache` interface for testing purposes. It stores cache entries in a dictionary in memory and does not persist them to disk.
    """

    def __init__(self):
        """
        Initialize the cache as a simple key-value dictionary
        """
        self.cache = {}

    def read(self, prompt: str, metadata: Optional[str] = None) -> List:
        """
        Read the record from the cache by serialized prompt and metadata

        :param prompt: The serialized prompt to search for
        :type prompt: str
        :param metadata: (optional) The metadata to search for, defaults to None
        :type metadata: str
        :return: The response from the cache
        :rtype: List
        """
        try:
            response = [
                {"response": self.cache[prompt + metadata if metadata else prompt]}
            ]
        except KeyError:
            return []
        return response

    def write(self, prompt: str, response: str, metadata: Optional[str] = None):
        """
        Write a prompt-response pair to the cache

        :param prompt: The serialized prompt to write
        :type prompt: str
        :param response: The serialized response to write
        :type response: str
        :param metadata: (optional) The metadata to write, defaults to None
        :type metadata: str
        """
        self.cache[prompt + metadata if metadata else prompt] = response

    def read_by_prompt(self, prompt: str) -> List:
        """
        Read a record from the cache by serialized prompt

        :param prompt: The serialized prompt to search for
        :type prompt: str
        :return: The response from the cache
        :rtype: List
        """
        return self.read(prompt)

    def read_by_prompt_and_metadata(self, prompt: str, metadata: str) -> List:
        """
        Read a record from the cache by serialized prompt and metadata

        :param prompt: The serialized prompt to search for
        :type prompt: str
        :param metadata: The metadata to search for
        :type metadata: str
        :return: The response from the cache
        :rtype: List
        """
        return self.read(prompt, metadata)

    def read_by_metadata(self, metadata: Optional[str] = None) -> List:
        """
        Read a dummy empty list

        :param metadata: (optional) The metadata to search for, defaults to None
        :type metadata: str
        :return: An empty list
        :rtype: list
        """
        return []

    def save(self, path: str) -> str:
        """
        Does not save but return the path argrument

        :param path: The path to save the cache to
        :type path: str
        :return: The path argument
        :rtype: str
        """
        return path

    def to_pandas(self) -> None:
        """
        Does nothing. Return None.

        :return: None
        :rtype: None
        """
        return None
