import logging
import os
from typing import Optional, List, Dict, Any

import torch

from .model import APIAccessFoundationModel
from .response import CompletionResponse

logger = logging.getLogger(__name__)

OPENAI_MODELS = (
    "text-davinci-003"
    "text-davinci-002",
    "text-davinci-001",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
)
try:
    import openai
except ModuleNotFoundError:
    logger.info("OpenAI module not found. Skipping OpenAI-based Models.")
    pass


class OpenAIModel(APIAccessFoundationModel):
    """
    A wrapper for the OpenAI API.

    This class provides a wrapper for the OpenAI API for generating completions.
    """
    @staticmethod
    def _openai_query(
        query_string: str,
        temperature: float = 0.0,
        max_tokens: int = 3,
        model: str = "text-davinci-002",
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
        :param model: The model to be used (choose from https://beta.openai.com/docs/api-reference/completions/create)
        :type model: str
        :return: The generated completion
        :rtype: str
        """
        openai_api_key = kwargs.get("openai_api_key", None)
        if openai_api_key is not None:
            openai.api_key = openai_api_key

        response = openai.Completion.create(
            model=model,
            prompt=query_string,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response

    @staticmethod
    def _openai_embedding_query(
        query_string: str,
        model: str = "text-davinci-002",
        **kwargs: Any,
    ) -> torch.Tensor:
        """
        Run a single query to get the embedding through the foundation model

        :param query_string: The prompt to be used for the query
        :type query_string: str
        :param model: The model to be used (choose from https://beta.openai.com/docs/api-reference/completions/create)
        :type model: str
        :return: The embeddings
        :rtype: str
        """
        try:
            import openai
        except ImportError:
            raise ImportError(
                "OpenAI module not found. Please install openai.")
        openai_api_key = kwargs.get("openai_api_key", None)
        if openai_api_key is not None:
            openai.api_key = openai_api_key
        return torch.tensor(
            openai.Embedding.create(input=[query_string.replace("\n", " ")],
                                    model=model)['data'][0]['embedding'])

    def __init__(self,
                 model_string: str = "text-davinci-002",
                 cfg: Optional[Dict] = None):
        """
        Initialize the OpenAI API wrapper.

        This function loads the API key for the OpenAI API from an environment variable or a configuration file.
        If neither is found, the user is prompted to enter the API key.
        The available models can be found at https://beta.openai.com/docs/api-reference/completions/create.

        :param model_string: The model to be used for generating completions.
        :type model_string: str
        :param cfg: The configuration dictionary containing the API key and other optional parameters.
        :type cfg: Dict
        """

        # Load your API key from an environment variable or secret management
        # service
        if "OPENAI_API_KEY" in os.environ:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            logger.log(logging.INFO, f"OpenAI model api key found")
        else:
            logger.log(logging.WARNING,
                       f"OpenAI model api key not found in environment")
            try:
                # Load your API key from a configuration file
                openai.api_key = cfg['api_key']
                logger.log(logging.INFO,
                           f"OpenAI model api key found in config")
            except KeyError or TypeError:
                logger.log(
                    logging.WARNING,
                    "OpenAI API key not found in config, Requesting User Input"
                )
                openai.api_key = input("Please enter your OpenAI API key: ")
                logger.log(logging.INFO, f"OpenAI model api key stored")
        assert model_string in OPENAI_MODELS, f"Model {model_string} not found. Please choose from {OPENAI_MODELS}"

        self.parallel = cfg.get("parallel", False)
        super().__init__(model_string, cfg)

    def _generate_batch(
        self,
        batch_instance: List[str],
        **kwargs,
    ) -> List[CompletionResponse]:
        """
        Generate completions for a batch of prompts using the OpenAI API.

        This function generates completions for a batch of prompts using the OpenAI API.
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
                CompletionResponse(text=self._openai_query(
                    query, model=self.model_string, **kwargs)))
        return output

    def _encode_batch(
        self,
        batch_instance: [List[str]],
        **kwargs,
    ) -> List[torch.Tensor]:
        """
        Generate embeddings for a batch of prompts using the OpenAI API.

        This function generates embeddings for a batch of prompts using the OpenAI API.
        The generated embeddings are returned in a list of `torch.Tensor` objects.

        :param batch_instance: A list of prompts
        :type batch_instance: List[str]
        :param kwargs: Additional keyword arguments to pass to the OpenAI API.
        :type kwargs: Any
        :return: A list of `torch.Tensor` objects containing the generated embeddings.
        :rtype: List[torch.Tensor]
        """
        output = []
        for query in batch_instance:
            output.append(
                self._openai_embedding_query(query,
                                             model=self.model_string,
                                             **kwargs))
        return output
