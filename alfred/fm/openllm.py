import json
import logging
import os
from typing import Optional, List, Any, Union, Tuple

import PIL.Image
import torch

from .model import APIAccessFoundationModel
from .response import CompletionResponse, RankedResponse
from .utils import colorize_str, retry, encode_image, type_print

logger = logging.getLogger(__name__)

try:
    import openai
except ModuleNotFoundError:
    logger.warning(
        "OpenAI module not found. Please install it to use the OpenAI model or connect to OpenLLM Server."
    )
    raise ModuleNotFoundError(
        "OpenAI module not found. Please install it to use the OpenAI model or connect to OpenLLM Server."
    )

from openai._exceptions import (
    AuthenticationError,
    APIError,
    APITimeoutError,
    RateLimitError,
    BadRequestError,
    APIConnectionError,
    APIStatusError,
)



class OpenLLMModel(APIAccessFoundationModel):
    """
    A wrapper for the OpenAI API for OpenLLM Models

    This class provides a wrapper for the OpenAI API for generating completions.
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
    def _openai_query(
        self,
        query: Union[str, List, Tuple],
        temperature: float = 0.0,
        max_tokens: int = 64,
        **kwargs: Any,
    ) -> str:
        """
        Run a single query through the foundation model

        :param query: The prompt to be used for the query
        :type query: Union[str, List]
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
        openai_api_key = kwargs.get("openai_api_key", None)
        if openai_api_key is not None:
            openai.api_key = openai_api_key

        if chat:
            return self.openai_client.chat.completions.create(
                model=self.model_string,
                messages=query,
                max_tokens=max_tokens,
                stop=None,
                temperature=temperature,
                stream=True,
            )
        else:
            query = [{"role": "user", "content": query}]
            response = self.openai_client.chat.completions.create(
                messages=query,
                model=self.model_string,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content

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

    def __init__(
        self, model_string: str = "", api_key: Optional[str] = None, **kwargs: Any
    ):
        """
        Initialize the OpenAI API wrapper.

        :param model_string: The model to be used for generating completions.
        :type model_string: str
        :param api_key: The API key to be used for the OpenAI API.
        :type api_key: Optional[str]
        """
        base_url = kwargs.get("base_url", None)
        if not api_key:
            api_key = "na"
        self.openai_client = openai.OpenAI(base_url=base_url if base_url else model_string)
        super().__init__(model_string, {"api_key": openai.api_key})

    def _generate_batch(
        self,
        batch_instance: Union[List[str], Tuple],
        **kwargs,
    ) -> List[CompletionResponse]:
        """
        Generate completions for a batch of prompts using the OpenAI API.

        This function generates completions for a batch of prompts using the OpenAI API.
        The generated completions are returned in a list of `CompletionResponse` objects.

        :param batch_instance: A list of prompts for which to generate completions.
        :type batch_instance: List[str] or List[Tuple]
        :param kwargs: Additional keyword arguments to pass to the OpenAI API.
        :type kwargs: Any
        :return: A list of `CompletionResponse` objects containing the generated completions.
        :rtype: List[CompletionResponse]
        """
        output = []
        for query in batch_instance:
            output.append(
                CompletionResponse(prediction=self._openai_query(query, **kwargs))
            )
        return output

    def _score_batch(
        self,
        batch_instance: Union[List[Tuple[str, str]], List[str]],
        scoring_instruction: str = "Instruction: Given the query, choose your answer from [[label_space]]:\nQuery:\n",
        **kwargs,
    ) -> List[RankedResponse]:
        """
        Tentative solution for scoring candidates.

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
                    prediction=self._openai_query(_scoring_prompt, **kwargs), scores={}
                )
            )
        return output
