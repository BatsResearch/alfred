import logging
import os
import torch
from typing import Optional, List, Dict, Any

from .model import APIAccessFoundationModel
from .response import CompletionResponse

logger = logging.getLogger(__name__)


class CohereModel(APIAccessFoundationModel):
    """
    A wrapper for the OpenAI API.

    This class provides a wrapper for the OpenAI API for generating completions.
    """

    def _cohere_query(
            self,
            query_string: str,
            temperature: float = 0.0,
            max_tokens: int = 10,
            model: str = "xlarge",
            **kwargs: Any,
    ) -> str:
        """
        Run a single query through the foundation model

        :param query_string: The prompt to be used for the query
        :type query_string: str
        :param temperature: The temperature of the model
        :type temperature: float
        :param max_tokens: The maximum number of tokens to be returned
        :type max_tokens: int
        :param model: The model to be used
        :type model: str
        :return: The generated completion
        :rtype: str
        """
        response = self.model(prompt=query_string,
                              model=model,
                              max_tokens=max_tokens,
                              temperature=temperature,
                              **kwargs)
        return response.generations[0].text

    def _cohere_embedding_query(
            self,
            query_string: str,
    ) -> torch.Tensor:
        """
        Encode a single query to get the embedding through the foundation model

        :param query_string: The prompt to be used for the query
        :type query_string: str
        :return: The embeddings
        :rtype: str
        """
        return self.model.embed(texts=[query_string]).embeddings

    def __init__(self,
                 api_key: str,
                 model_string: str = "xlarge",
                 cfg: Optional[Dict] = None):
        """
        Initialize the Cohere API wrapper.

        :param model_string: The model to be used for generating completions.
        :type model_string: str
        :param cfg: The configuration dictionary containing the API key and other optional parameters.
        :type cfg: Dict
        """
        try:
            import cohere
        except ModuleNotFoundError:
            raise ModuleNotFoundError("cohere module not found. Please install it.")
        self.model = cohere.Client(api_key)
        super().__init__(model_string, cfg)

    def _generate_batch(
            self,
            batch_instance: List[str],
            **kwargs,
    ) -> List[CompletionResponse]:
        """
        Generate completions for a batch of prompts using the Cohere API.

        This function generates completions for a batch of prompts using the Cohere API.
        The generated completions are returned in a list of `CompletionResponse` objects.

        :param batch_instance: A list of prompts for which to generate completions.
        :type batch_instance: List[str]
        :param kwargs: Additional keyword arguments to pass to the Cohere API.
        :type kwargs: Any
        :return: A list of `CompletionResponse` objects containing the generated completions.
        :rtype: List[CompletionResponse]
        """
        output = []
        for query in batch_instance:
            output.append(
                CompletionResponse(text=self._cohere_query(
                    query, model=self.model_string, **kwargs)))
        return output

    def _encode_batch(
            self,
            batch_instance: [List[str]],
            **kwargs,
    ) -> List[torch.Tensor]:
        """
        Generate embeddings for a batch of prompts using the Cohere API.

        This function generates embeddings for a batch of prompts using the Cohere API.
        The generated embeddings are returned in a list of `torch.Tensor` objects.

        :param batch_instance: A list of prompts
        :type batch_instance: List[str]
        :param kwargs: Additional keyword arguments to pass to the Cohere API.
        :type kwargs: Any
        :return: A list of `torch.Tensor` objects containing the generated embeddings.
        :rtype: List[torch.Tensor]
        """
        output = []
        for query in batch_instance:
            output.append(
                self._cohere_embedding_query(query))
        return output
