import logging
from typing import Optional, List, Union, Tuple, Any, Dict
import json

from .utils import colorize_str, type_print

try:
    from groq import Groq
except ImportError:
    raise ImportError(
        "The 'groq' package is required to use the GroqModel. Please install it using 'pip install groq'."
    )

from .model import APIAccessFoundationModel
from .response import CompletionResponse, RankedResponse

logger = logging.getLogger(__name__)

GROQ_MODELS = (
    "llama3-8b-8192",
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "gemma-7b-it",
)


class GroqModel(APIAccessFoundationModel):
    """
    A wrapper for the OpenAI API.

    This class provides a wrapper for the OpenAI API for generating completions.
    """

    def _groq_query(
        self,
        query_string: Union[str, List[Dict]],
        temperature: float = 0.0,
        max_tokens: int = 10,
        model: Optional[str] = None,
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
        model = self.model_string if model is None else model
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": query_string,
                }
            ]
            if isinstance(query_string, str)
            else query_string,
            model=model,
        )
        try:
            response = response.choices[0].message.content
        except KeyError:
            raise Exception(f"Error: {response}")
        return response

    def __init__(
        self,
        model_string: str = "llama3-8b-8192",
        api_key: Optional[str] = None,
    ):
        """
        Initialize the Cohere API wrapper.

        :param model_string: The model to be used for generating completions.
        :type model_string: str
        :param api_key: The API key to be used for accessing the Groq API.
        :type api_key: Optional[str]
        """
        if model_string not in GROQ_MODELS:
            logger.log(
                f"Model {model_string} not in supported models {GROQ_MODELS}, please check the Groq API documentation for supported models"
            )

        if api_key is None:
            logger.log(logging.WARNING, "Groq API key not found, Requesting User Input")
            api_key = input("Please enter your Groq API key: ")
            logger.log(logging.INFO, f"Groq model api key stored")

        self.client = Groq(api_key=api_key)
        self.api_key = api_key
        super().__init__(model_string, {"api_key": api_key})

    def _generate_batch(
        self,
        batch_instance: List[str],
        **kwargs,
    ) -> List[CompletionResponse]:
        """
        Generate completions for a batch of prompts using the Groq API.

        This function generates completions for a batch of prompts using the Groq API.
        The generated completions are returned in a list of `CompletionResponse` objects.

        :param batch_instance: A list of prompts for which to generate completions.
        :type batch_instance: List[str]
        :param kwargs: Additional keyword arguments to pass to the Groq API.
        :type kwargs: Any
        :return: A list of `CompletionResponse` objects containing the generated completions.
        :rtype: List[CompletionResponse]
        """
        output = []
        for query in batch_instance:
            output.append(
                CompletionResponse(prediction=self._groq_query(query, **kwargs))
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
                    prediction=self._groq_query(
                        _scoring_prompt, model=self.model_string, **kwargs
                    ),
                    scores={},
                )
            )
        return output

    def chat(self, **kwargs: Any):
        """
        Launch an interactive chat session with the Anthropic API.
        """

        def _feedback(feedback: str, no_newline=False, override=False):
            if override:
                print("\r", end="")
            print(
                colorize_str("Chat AI: ", "GREEN"),
                end="",
            )
            type_print(feedback)
            print(
                "",
                end="\n" if not no_newline else "",
            )

        model = kwargs.get("model", self.model_string)
        c_title = colorize_str("Alfred's Anthropic Chat", "BLUE")
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
                "content": "You are a helpful assistant to the user. Answer their questions as accurately as possible.",
            },
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
                print(
                    colorize_str("Chat AI: ", "GREEN"),
                    end="",
                )
                response = self._groq_query(
                    message_log,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    model=model,
                )
                print(response)
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
