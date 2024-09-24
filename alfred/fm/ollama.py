import logging
from typing import List, Any, Dict
import re
from .model import LocalAccessFoundationModel
from .response import CompletionResponse

logger = logging.getLogger(__name__)

try:
    import ollama
except ImportError:
    raise ImportError("Please install Ollama with `pip install ollama`")

class OllamaModel(LocalAccessFoundationModel):
    """
    OllamaModel wraps an Ollama model. Ollama is a library for easy integration with large language models.

    source: https://github.com/ollama/ollama
    """

    def __init__(self, model: str, **kwargs: Any):
        """
        Initialize an Ollama model.

        :param model: The name or path of the model to use.
        :type model: str
        """

        def is_url(string):
            url_pattern = re.compile(
                r'^(?:'
                r'(?:http)s?://' 
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' 
                r'localhost|'  
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                r'(?::\d+)?'  
                r'(?:/?|[/?]\S+)'
                r'|'  
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d+)?' 
                r')$',
                re.IGNORECASE
            )
            return bool(url_pattern.match(string))

        self.model_string = model

        super().__init__(model)
        # if model is ip address then launch host
        if is_url(model):
            self.client = ollama.Client(host=host)
        else:
            self.client = ollama

    def generate_batch(
        self,
        batch_instance: List[str],
        **kwargs: Any,
    ) -> List[CompletionResponse]:
        """
        Generate completions for a batch of queries.

        :param batch_instance: A list of queries.
        :type batch_instance: List[str]
        :param kwargs: Additional keyword arguments.
        :return: A list of `CompletionResponse` objects with the generated content.
        :rtype: List[CompletionResponse]
        """

        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 100)
        top_k = kwargs.get("top_k", 40)
        top_p = kwargs.get("top_p", 0.95)

        responses = []
        for query in batch_instance:
            response = self.client.generate(
                model=self.model_string,
                prompt=query,
                temperature=temperature,
                max_tokens=max_tokens,
                top_k=top_k,
                top_p=top_p
            )
            responses.append(CompletionResponse(prediction=response['response']))

        return responses

    def chat(self, **kwargs: Any):
        """
        Launch an interactive chat session with the Ollama API.
        """

        def _feedback(feedback: str, no_newline=False):
            print(
                colorize_str("Chat AI: ", "GREEN") + feedback,
                end="\n" if not no_newline else "",
            )

        model = kwargs.get("model", self.model_string)
        c_title = colorize_str("Alfred's Ollama Chat", "BLUE")
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
                "content": "You are an intelligent assistant. Please answer the user with professional language.",
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
                if query.lower() == "exit":
                    _feedback("Goodbye!")
                    break
                message_log.append({"role": "user", "content": query})
                _feedback("", no_newline=True)

                response = self.client.chat(
                    model=self.model_string,
                    messages=message_log,
                    stream=True,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                full_response = []
                for chunk in response:
                    try:
                        txt = chunk['message']['content']
                        type_print(txt)
                        full_response.append(txt)
                    except KeyError:
                        pass
                print()

                full_response = "".join(full_response).strip()
                message_log.append({"role": "assistant", "content": full_response})
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