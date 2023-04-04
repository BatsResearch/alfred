import json
import logging
import os
from typing import Optional, List, Any, Union, Tuple, Dict

import torch
import readline

from .model import APIAccessFoundationModel
from .response import CompletionResponse
from .utils import colorize_str

logger = logging.getLogger(__name__)

ANTHROPIC_MODELS = (
    "claude-v1",
    "claude-v1.0",
    "claude-v1.2",
    "claude-instant-v1",
    "claude-instant-v1.0",
)

try:
    import anthropic
except ModuleNotFoundError:
    logger.warning("Anthropic module not found. Please install it from https://github.com/anthropics/anthropic-sdk-python")
    raise ModuleNotFoundError("Anthropic module not found. Please install it from https://github.com/anthropics/anthropic-sdk-python")


class AnthropicModel(APIAccessFoundationModel):
    """
    A wrapper for the anthropic API.

    This class provides a wrapper for the anthropic API for generating completions.
    """
    def _anthropic_query(
        self,
        query: Union[str, List],
        temperature: float = 0.0,
        max_tokens: int = 3,
        model: str = "claude-v1",
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
        :param model: The model to be used
        :type model: str
        :param kwargs: Additional keyword arguments
        :type kwargs: Any
        :return: The generated completion
        :rtype: str
        """
        chat = kwargs.get("chat", False)
        api_key = kwargs.get("api_key", None)

        if api_key is not None:
            anthropic.api_key = api_key

        if chat:
            return self._anthropic_client.completion_stream(
                model=model,
                prompt=f"{anthropic.HUMAN_PROMPT} {query}{anthropic.AI_PROMPT}",
                max_tokens_to_sample=max_tokens,
                temperature=temperature,
                stream=True,
            )
        else:
            response = self._anthropic_client.completion(
                prompt=f"{anthropic.HUMAN_PROMPT} {query}{anthropic.AI_PROMPT}",
                model="claude-v1",
                max_tokens_to_sample=max_tokens,
                temperature=temperature,
            )
            return response["completion"]

    def __init__(self,
                 model_string: str = "claude-v1",
                 api_key: Optional[str] = None):
        """
        Initialize the Anthropic API wrapper.

        This function loads the API key for the anthropic API from an environment variable or a configuration file.
        If neither is found, the user is prompted to enter the API key.
        The available models can be found at https://beta.anthropic.com/docs/api-reference/completions/create.

        :param model_string: The model to be used for generating completions.
        :type model_string: str
        :param api_key: The API key to be used for the anthropic API.
        :type api_key: Optional[str]
        """
        assert model_string in ANTHROPIC_MODELS, f"Model {model_string} not found. Please choose from {ANTHROPIC_MODELS}"

        if "ANTHROPIC_API_KEY" in os.environ:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            logger.log(logging.INFO, f"Anthropic model api key found")
        else:
            logger.log(logging.INFO,
                       f"Anthropic model api key not found in environment")
            if api_key:
                api_key = api_key
            else:
                logger.log(
                    logging.INFO,
                    "Anthropic API key not found in config, Requesting User Input"
                )
                api_key = input("Please enter your anthropic API key: ")
                logger.log(logging.INFO, f"Anthropic model api key stored")

        self._anthropic_client = anthropic.Client(api_key)
        super().__init__(model_string, {"api_key": api_key})

    def _generate_batch(
        self,
        batch_instance: List[str],
        **kwargs,
    ) -> List[CompletionResponse]:
        """
        Generate completions for a batch of prompts using the anthropic API.

        This function generates completions for a batch of prompts using the anthropic API.
        The generated completions are returned in a list of `CompletionResponse` objects.

        :param batch_instance: A list of prompts for which to generate completions.
        :type batch_instance: List[str]
        :param kwargs: Additional keyword arguments to pass to the anthropic API.
        :type kwargs: Any
        :return: A list of `CompletionResponse` objects containing the generated completions.
        :rtype: List[CompletionResponse]
        """
        output = []
        for query in batch_instance:
            output.append(
                CompletionResponse(prediction=self._anthropic_query(
                    query, model=self.model_string, **kwargs)))
        return output

    def chat(self, **kwargs: Any):
        """
        Launch an interactive chat session with the Anthropic API.
        """
        def _feedback(feedback: str, no_newline=False, override=False):
            if override: print("\r", end="")
            print(colorize_str("Chat AI: ", "GREEN") + feedback,
                  end="\n" if not no_newline else "")

        model = kwargs.get("model", self.model_string)
        c_title = colorize_str("Alfred's Anthropic Chat", "BLUE")
        c_model = colorize_str(model, "WARNING")
        c_exit = colorize_str("exit", "FAIL")
        c_ctrlc = colorize_str("Ctrl+C", "FAIL")

        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 1024)
        log_save_path = kwargs.get("log_save_path", None)
        manual_chat_sequence = kwargs.get("manual_chat_sequence", None)

        print(
            f"Welcome to the {c_title} session!\nYou are using the {c_model} model."
        )
        print(f"Type '{c_exit}' or hit {c_ctrlc} to exit the chat session.")

        message_log = []

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
                response = []
                for resp in self._anthropic_query(query,
                                               chat=True,
                                               model=model,
                                               temperature=temperature,
                                               max_tokens=max_tokens):
                    if resp["stop_reason"] in ["stop", "stop_sequence"]:
                        break
                    try:
                        txt = resp["completion"]
                        _feedback(txt, no_newline=True, override=True)
                    except AttributeError:
                        txt = ''
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
