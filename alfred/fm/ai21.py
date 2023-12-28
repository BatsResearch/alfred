import logging
from typing import Optional, List, Union, Tuple

import requests

from .model import APIAccessFoundationModel
from .response import CompletionResponse, RankedResponse

logger = logging.getLogger(__name__)

AI21_MODELS = (
    "j1-light",
    "j1-mid",
    "j1-ultra",
)


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
        model: str = "j1-mid",
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
                "temperature": temperature,
            },
        )
        response = response.json()
        try:
            response = response["completions"][0]["data"]["text"]
        except KeyError:
            raise Exception(response["detail"])
        return response

    def __init__(
        self,
        model_string: str = "j1-mid",
        api_key: Optional[str] = None,
    ):
        """
        Initialize the Cohere API wrapper.

        :param model_string: The model to be used for generating completions.
        :type model_string: str
        :param api_key: The API key to be used for accessing the AI21 API.
        :type api_key: Optional[str]
        """
        assert (
            model_string in AI21_MODELS
        ), f"Model {model_string} not found. Please choose from {AI21_MODELS}"
        if api_key is None:
            logger.log(logging.WARNING, "AI21 API key not found, Requesting User Input")
            api_key = input("Please enter your AI21 API key: ")
            logger.log(logging.INFO, f"AI21 model api key stored")
        self.api_key = api_key
        super().__init__(model_string, {"api_key": api_key})

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
                CompletionResponse(
                    prediction=self._ai21_query(
                        query, model=self.model_string, **kwargs
                    )
                )
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
                    prediction=self._ai21_query(
                        _scoring_prompt, model=self.model_string, **kwargs
                    ),
                    scores={},
                )
            )
        return output
