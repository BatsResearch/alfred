import json
import logging
import os
from typing import Optional, List, Any, Union, Tuple

import PIL.Image
import torch
import readline

from .model import APIAccessFoundationModel
from .response import CompletionResponse
from .utils import colorize_str, retry, encode_image, type_print

logger = logging.getLogger(__name__)

try:
    import openai
except ModuleNotFoundError:
    logger.warning(
        "OpenAI module not found. Please install it to use the OpenAI model."
    )
    raise ModuleNotFoundError(
        "OpenAI module not found. Please install it to use the OpenAI model."
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

OPENAI_MODELS = (
    "gpt-4",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0613",
    "gpt-4-1106-preview",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k-0613",
    "text-davinci-003",
    "text-davinci-002",
    "text-davinci-001",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
    "code-davinci-002",
)

OPENAI_EMBEDDING_MODELS = (
    "text-davinci-001",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
    "text-embedding-ada-002",
)

OPENAI_VISION_MODELS = ("gpt-4-vision-preview",)


class OpenAIModel(APIAccessFoundationModel):
    """
    A wrapper for the OpenAI API.

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
            if self.model_string in OPENAI_VISION_MODELS:
                img, prompt = query[0], query[1]
                if isinstance(img, PIL.Image.Image):
                    img = encode_image(img, type="image")
                elif isinstance(img, str):
                    img = img
                query = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"{prompt}"},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{img}"},
                            },
                        ],
                    }
                ]
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
    def _openai_embedding_query(
        self,
        query_string: str,
        **kwargs: Any,
    ) -> torch.Tensor:
        """
        Run a single query to get the embedding through the foundation model

        :param query_string: The prompt to be used for the query
        :type query_string: str
        :return: The embeddings
        :rtype: str
        """
        openai_api_key = kwargs.get("openai_api_key", None)
        if openai_api_key is not None:
            openai.api_key = openai_api_key

        return torch.tensor(
            self.openai_client.embeddings.create(
                input=[query_string.replace("\n", " ")], model=self.model_string
            )
            .data[0]
            .embedding
        )

    def __init__(
        self, model_string: str = "text-davinci-002", api_key: Optional[str] = None
    ):
        """
        Initialize the OpenAI API wrapper.

        This function loads the API key for the OpenAI API from an environment variable or a configuration file.
        If neither is found, the user is prompted to enter the API key.
        The available models can be found at https://beta.openai.com/docs/api-reference/completions/create.

        :param model_string: The model to be used for generating completions.
        :type model_string: str
        :param api_key: The API key to be used for the OpenAI API.
        :type api_key: Optional[str]
        """
        assert (
            model_string
            in OPENAI_MODELS + OPENAI_VISION_MODELS + OPENAI_EMBEDDING_MODELS
        ), (
            f"Model {model_string} not found. "
            f"Please choose from {OPENAI_MODELS} or {OPENAI_VISION_MODELS} or {OPENAI_EMBEDDING_MODELS}"
        )

        if "OPENAI_API_KEY" in os.environ:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            logger.log(logging.INFO, f"OpenAI model api key found")
        else:
            logger.log(logging.INFO, f"OpenAI model api key not found in environment")
            if api_key:
                openai.api_key = api_key
            else:
                logger.log(
                    logging.INFO,
                    "OpenAI API key not found in config, Requesting User Input",
                )
                openai.api_key = input("Please enter your OpenAI API key: ")
                logger.log(logging.INFO, f"OpenAI model api key stored")

        self.openai_client = openai.OpenAI(api_key=api_key)
        if model_string in OPENAI_VISION_MODELS:
            self.multimodal_mode = "autoregressive"
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
        if self.model_string not in OPENAI_EMBEDDING_MODELS:
            logger.error(
                f"Model {self.model_string} does not support embedding."
                f"Please choose from {OPENAI_EMBEDDING_MODELS}"
            )
            raise ValueError(
                f"Model {self.model_string} does not support embedding."
                f"Please choose from {OPENAI_EMBEDDING_MODELS}"
            )
        output = []
        for query in batch_instance:
            output.append(self._openai_embedding_query(query, **kwargs))
        return output

    def chat(self, **kwargs: Any):
        """
        Launch an interactive chat session with the OpenAI API.
        """

        def _feedback(feedback: str, no_newline=False):
            print(
                colorize_str("Chat AI: ", "GREEN") + feedback,
                end="\n" if not no_newline else "",
            )

        model = kwargs.get("model", self.model_string)
        c_title = colorize_str("Alfred's OpenAI Chat", "BLUE")
        c_model = colorize_str(model, "WARNING")
        c_exit = colorize_str("exit", "FAIL")
        c_ctrlc = colorize_str("Ctrl+C", "FAIL")

        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 1024)
        log_save_path = kwargs.get("log_save_path", None)
        manual_chat_sequence = kwargs.get("manual_chat_sequence", None)

        print(f"Welcome to the {c_title} session!\nYou are using the {c_model} model.")
        print(f"Type '{c_exit}' or hit {c_ctrlc} to exit the chat session.")

        message_log = [
            {
                "role": "system",
                "content": "You are a intelligent assistant. Please answer the user with professional language.",
            }
        ]

        print()
        print("======== Chat Begin ========")
        print()

        try:
            while True:
                if manual_chat_sequence is not None:
                    query = manual_chat_sequence.pop(0)
                    _feedback(query, no_newline=True)
                    print()
                    if len(manual_chat_sequence) == 0:
                        break
                else:
                    query = input(colorize_str("You: "))
                if query == "exit":
                    _feedback("Goodbye!")
                    break
                message_log.append({"role": "user", "content": query})
                _feedback("", no_newline=True)
                response = []
                for resp in self._openai_query(
                    message_log,
                    chat=True,
                    temperature=temperature,
                    max_tokens=max_tokens,
                ):
                    if resp.choices[0].finish_reason == "stop":
                        break
                    try:
                        txt = resp.choices[0].delta.content
                        type_print(txt)
                    except AttributeError:
                        txt = ""
                    response.append(txt)
                print()
                response = "".join(response).strip()
                response = response.replace("\n", "")
                message_log.append({"role": "assistant", "content": response})
        except KeyboardInterrupt:
            _feedback("Goodbye!")

        print()
        print("======== Chat End ========")
        print()
        print(colorize_str("Thank you for using Alfred!"))

        if log_save_path:
            with open(log_save_path, "w") as f:
                json.dump(message_log, f)
            print(f"Your chat log is saved to {log_save_path}")
