import json
import logging
from typing import Optional, List, Any, Union, Tuple

import openai
from openai._exceptions import (
    AuthenticationError,
    APIError,
    APITimeoutError,
    RateLimitError,
    BadRequestError,
    APIConnectionError,
    APIStatusError,
)

from .model import APIAccessFoundationModel
from .response import CompletionResponse, RankedResponse
from .utils import retry

logger = logging.getLogger(__name__)

class OpenLLMModel(APIAccessFoundationModel):
    """
    A wrapper for the OpenLLM Models using OpenAI's Python package
    """

    @retry(
        num_retries=3,
        wait_time=0.1,
        exceptions=(
            AuthenticationError,
            APIConnectionError,
            APITimeoutError,
            RateLimitError,
            APIError,
            BadRequestError,
            APIStatusError,
        ),
    )
    def _api_query(
        self,
        query: Union[str, List, Tuple],
        temperature: float = 0.0,
        max_tokens: int = 64,
        **kwargs: Any,
    ) -> str:
        """
        Run a single query through the foundation model using OpenAI's Python package

        :param query: The prompt to be used for the query
        :type query: Union[str, List, Tuple]
        :param temperature: The temperature of the model
        :type temperature: float
        :param max_tokens: The maximum number of tokens to be returned
        :type max_tokens: int
        :param kwargs: Additional keyword arguments
        :type kwargs: Any
        :return: The generated completion
        :rtype: str
        """
        chat = kwargs.get("chat", False)

        if chat:
            messages = query if isinstance(query, list) else [{"role": "user", "content": query}]
            response = self.openai_client.chat.completions.create(
                model=self.model_string,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content
        else:
            prompt = query[0]['content'] if isinstance(query, list) else query
            response = self.openai_client.completions.create(
                model=self.model_string,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].text

    def __init__(
        self, model_string: str = "", api_key: Optional[str] = None, **kwargs: Any
    ):
        """
        Initialize the OpenLLM API wrapper.

        :param model_string: The model to be used for generating completions.
        :type model_string: str
        :param api_key: The API key to be used for the OpenAI API.
        :type api_key: Optional[str]
        """
        self.model_string = model_string
        base_url = kwargs.get("base_url",  None)
        api_key = api_key or "na"
        self.openai_client = openai.OpenAI(base_url=base_url, api_key=api_key)
        super().__init__(model_string, {"api_key": api_key, "base_url": base_url})

    def _generate_batch(
        self,
        batch_instance: Union[List[str], Tuple],
        **kwargs,
    ) -> List[CompletionResponse]:
        """
        Generate completions for a batch of prompts using the OpenAI API.

        :param batch_instance: A list of prompts for which to generate completions.
        :type batch_instance: List[str] or List[Tuple]
        :param kwargs: Additional keyword arguments to pass to the API.
        :type kwargs: Any
        :return: A list of `CompletionResponse` objects containing the generated completions.
        :rtype: List[CompletionResponse]
        """
        output = []
        for query in batch_instance:
            output.append(
                CompletionResponse(prediction=self._api_query(query, **kwargs))
            )
        return output

    def _score_batch(
        self,
        batch_instance: Union[List[Tuple[str, str]], List[str]],
        scoring_instruction: str = "Instruction: Given the query, choose your answer from [[label_space]]:\nQuery:\n",
        **kwargs,
    ) -> List[RankedResponse]:
        """
        Score candidates using the OpenAI API.

        :param batch_instance: A list of prompts for which to generate candidate preferences.
        :type batch_instance: List[str] or List[Tuple]
        :param scoring_instruction: The instruction prompt for scoring
        :type scoring_instruction: str
        """
        output = []
        for query in batch_instance:
            _scoring_prompt = (
                scoring_instruction.replace(
                    "[[label_space]]", ",".join(query.candidates)
                )
                + query.prompt
            )
            output.append(
                RankedResponse(
                    prediction=self._api_query(_scoring_prompt, **kwargs), scores={}
                )
            )
        return output