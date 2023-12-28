import json
import logging
import os
import sys
from typing import Optional, List, Any, Union, Tuple

import PIL.Image
import torch

from .model import APIAccessFoundationModel
from .response import CompletionResponse, RankedResponse
from .utils import colorize_str, retry, type_print

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
except ModuleNotFoundError:
    logger.warning(
        "Google GenAI module not found. Please install google-generativeai to use the Google model."
    )
    raise ModuleNotFoundError(
        "Google GenAI module not found. Please install google-generativeai to use the Google model."
    )

GOOGLE_GENAI_MODELS = ("gemini-pro",)

GOOGLE_GENAI_VISION_MODELS = ("gemini-pro-vision",)

GOOGLE_GENAI_EMBEDDING_MODELS = ("embedding-001",)


class GoogleModel(APIAccessFoundationModel):
    """
    A wrapper for the Google API.

    This class provides a wrapper for the Google API for generating completions.
    """

    @retry(
        num_retries=3,
        wait_time=0.1,
        exceptions=(Exception),
    )
    def _google_genai_query(
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
        if self.model_string in GOOGLE_GENAI_VISION_MODELS:
            img, prompt = query[0], query[1]
            if not isinstance(img, PIL.Image.Image):
                raise ValueError(
                    f"Image type {type(img)} not supported. Please use PIL.Image!"
                )
            query = [prompt, img] if len(prompt) > 0 else [img]
        response = self.model.generate_content(
            query,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                stop_sequences=["x"],
                max_output_tokens=max_tokens,
                temperature=temperature,
            ),
        )
        return response.text

    @retry(
        num_retries=3,
        wait_time=0.1,
        exceptions=(Exception),
    )
    def _google_genai_embedding_query(
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

        return torch.tensor(
            genai.embed_content(
                model=f"models/{self.model_string}",
                content=query_string,
                task_type="retrieval_document",
                title="Embedding of single string",
            )
        )

    def __init__(self, model_string: str = "gemini-pro", api_key: Optional[str] = None):
        """
        Initialize the Google API wrapper.

        This function loads the API key for the Google API from an environment variable or a configuration file.
        If neither is found, the user is prompted to enter the API key.
        Note: .genai currently work with python 3.9+

        :param model_string: The model to be used for generating completions.
        :type model_string: str
        :param api_key: The API key to be used for the Google API.
        :type api_key: Optional[str]
        """

        # check python version above 3.9
        if sys.version_info < (3, 9):
            raise RuntimeError("Google GenAI requires Python 3.9+")
        assert (
            model_string
            in GOOGLE_GENAI_MODELS
            + GOOGLE_GENAI_EMBEDDING_MODELS
            + GOOGLE_GENAI_VISION_MODELS
        ), (
            f"Model {model_string} not found. "
            f"Please choose from {GOOGLE_GENAI_MODELS + GOOGLE_GENAI_EMBEDDING_MODELS + GOOGLE_GENAI_VISION_MODELS}"
        )
        if api_key is None:
            if "GOOGLE_API_KEY" in os.environ:
                api_key = os.getenv("GOOGLE_API_KEY")
                logger.log(logging.INFO, f"Google api key found")
            else:
                logger.log(
                    logging.INFO,
                    "Google API key not found in config, Requesting User Input",
                )
                api_key = input("Please enter your Google API key: ")
                logger.log(logging.INFO, f"Google model api key stored")

        genai.configure(api_key=api_key)

        if model_string in GOOGLE_GENAI_VISION_MODELS:
            self.multimodal_mode = "autoregressive"

        self.model = genai.GenerativeModel(model_string)

        super().__init__(model_string, {"api_key": api_key})

    def _generate_batch(
        self,
        batch_instance: Union[List[str], Tuple],
        **kwargs,
    ) -> List[CompletionResponse]:
        """
        Generate completions for a batch of prompts using the Google API.

        This function generates completions for a batch of prompts using the Google API.
        The generated completions are returned in a list of `CompletionResponse` objects.

        :param batch_instance: A list of prompts for which to generate completions.
        :type batch_instance: List[str] or List[Tuple]
        :param kwargs: Additional keyword arguments to pass to the Google API.
        :type kwargs: Any
        :return: A list of `CompletionResponse` objects containing the generated completions.
        :rtype: List[CompletionResponse]
        """
        output = []
        for query in batch_instance:
            output.append(
                CompletionResponse(prediction=self._google_genai_query(query, **kwargs))
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
                    prediction=self._google_genai_query(_scoring_prompt, **kwargs),
                    scores={},
                )
            )
        return output

    def _encode_batch(
        self,
        batch_instance: [List[str]],
        **kwargs,
    ) -> List[torch.Tensor]:
        """
        Generate embeddings for a batch of prompts using the Google API.

        This function generates embeddings for a batch of prompts using the Google API.
        The generated embeddings are returned in a list of `torch.Tensor` objects.

        :param batch_instance: A list of prompts
        :type batch_instance: List[str]
        :param kwargs: Additional keyword arguments to pass to the Google API.
        :type kwargs: Any
        :return: A list of `torch.Tensor` objects containing the generated embeddings.
        :rtype: List[torch.Tensor]
        """
        if self.model_string not in GOOGLE_GENAI_EMBEDDING_MODELS:
            logger.error(
                f"Model {self.model_string} does not support embedding."
                f"Please choose from {GOOGLE_GENAI_EMBEDDING_MODELS}"
            )
            raise ValueError(
                f"Model {self.model_string} does not support embedding."
                f"Please choose from {GOOGLE_GENAI_EMBEDDING_MODELS}"
            )
        output = []
        for query in batch_instance:
            output.append(self._google_genai_embedding_query(query, **kwargs))
        return output

    def chat(self, **kwargs: Any):
        """
        Launch an interactive chat session with the Google API.
        """

        def _feedback(feedback: str, no_newline=False):
            print(
                colorize_str("Chat AI: ", "GREEN") + feedback,
                end="\n" if not no_newline else "",
            )

        model = kwargs.get("model", self.model_string)
        c_title = colorize_str("Alfred's Google Gemini Chat", "BLUE")
        c_model = colorize_str(model, "WARNING")
        c_exit = colorize_str("exit", "FAIL")
        c_ctrlc = colorize_str("Ctrl+C", "FAIL")

        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 1024)
        log_save_path = kwargs.get("log_save_path", None)
        manual_chat_sequence = kwargs.get("manual_chat_sequence", None)
        save_as_markdown = kwargs.get("save_as_markdown", False)

        print(f"Welcome to the {c_title} session!\nYou are using the {c_model} model.")
        print(f"Type '{c_exit}' or hit {c_ctrlc} to exit the chat session.")

        message_log = []
        chat_history = []

        self.chat_client = self.model.start_chat(history=chat_history)

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
                for resp in self.chat_client.send_message(query, stream=True):
                    response.append(resp.text)
                    type_print(resp.text)
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
