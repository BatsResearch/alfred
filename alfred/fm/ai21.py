import logging
from typing import Optional, List, Dict
import requests

from .model import APIAccessFoundationModel
from .response import CompletionResponse

logger = logging.getLogger(__name__)



class AI21Model(APIAccessFoundationModel):
    """
    A wrapper for the OpenAI API.

    This class provides a wrapper for the OpenAI API for generating completions.
    """

    def _ai21_query(
            self,
            query_string: str,
            temperature: float = 0.0,
            max_tokens: int = 10,
            model: str = "j1-large",
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
        response = requests.post(
            f"https://api.ai21.com/studio/v1/{model}/complete",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "prompt": query_string,
                "numResults": 1,
                "maxTokens": max_tokens,
                "stopSequences": ["."],
                "topKReturn": 0,
                "temperature": temperature
            }
        )
        return response['completions']['data']['text']

    def __init__(self,
                 api_key: str,
                 model_string: str = "j1-large",
                 cfg: Optional[Dict] = None):
        """
        Initialize the Cohere API wrapper.

        :param model_string: The model to be used for generating completions.
        :type model_string: str
        :param cfg: The configuration dictionary containing the API key and other optional parameters.
        :type cfg: Dict
        """
        self.api_key = api_key
        super().__init__(model_string, cfg)

    def _generate_batch(
            self,
            batch_instance: List[str],
            **kwargs,
    ) -> List[CompletionResponse]:
        """
        Generate completions for a batch of prompts using the AI21 API.

        This function generates completions for a batch of prompts using the AI21 API.
        The generated completions are returned in a list of `CompletionResponse` objects.

        :param batch_instance: A list of prompts for which to generate completions.
        :type batch_instance: List[str]
        :param kwargs: Additional keyword arguments to pass to the OpenAI API.
        :type kwargs: Any
        :return: A list of `CompletionResponse` objects containing the generated completions.
        :rtype: List[CompletionResponse]
        """
        output = []
        for query in batch_instance:
            output.append(
                CompletionResponse(text=self._ai21_query(
                    query, model=self.model_string, **kwargs)))
        return output