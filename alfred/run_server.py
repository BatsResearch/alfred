import argparse
import logging
from typing import Any

from alfred.fm.remote.grpc_server import gRPCServer

logging.basicConfig(
    format="ALFRED %(levelname)s: %(asctime)-5s  %(message)s",
    level=logging.NOTSET,
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("Alfred Server")


class ModelServer:
    """
    ModelServer is the server-side interface that wraps a certain alferd.fm class.
    ModelServer is used to launch the specified alferd.fm model as a gRPC Server and find the proper port.
    """

    def __init__(
        self,
        model: str,
        model_type: str,
        port: int = 10719,
        **kwargs: Any,
    ):
        """

        Constructor Alfred ModelServer on the Server Side.
        This ModeServer launches the specified alferd.fm model on the server
        and map the model interfaces to the specified port number.
        If the port given is not available, the server will try to find the next available port.

        :param model: name of the model
        :type model: str
        :param model_type: type of the model. Currently supported: huggingface, openai, dummy
        :type model_type: str
        :param port: port number to launch the server
        :type port: int
        :param kwargs: additional arguments for the model constructor
        :type kwargs: Any
        """
        self.model = model
        self.model_type = model_type.lower()
        assert self.model_type in [
            "huggingface",
            "huggingfacevlm",
            "huggingfacedocument",
            "onnx",
            "tensorrt",
            "openai",
            "anthropic",
            "flexgen",
            "vllm",
            "cohere",
            "ai21",
            "groq",
            "google",
            "torch",
            "ollama",
            "dummy",
        ], f"Invalid model type: {self.model_type}"
        if self.model_type == "huggingface":
            from .fm.huggingface import HuggingFaceModel

            self.model = HuggingFaceModel(self.model, **kwargs)
        elif self.model_type == "huggingfacevlm":
            from .fm.huggingfacevlm import HuggingFaceCLIPModel

            self.model = HuggingFaceCLIPModel(self.model, **kwargs)
        elif self.model_type == "huggingfacedocument":
            from .fm.huggingfacedocument import HuggingFaceDocumentModel

            self.model = HuggingFaceDocumentModel(self.model, **kwargs)
        elif self.model_type == "anthropic":
            from .fm.anthropic import AnthropicModel

            self.model = AnthropicModel(self.model, **kwargs)
        elif self.model_type == "openai":
            from .fm.openai import OpenAIModel

            self.model = OpenAIModel(self.model, **kwargs)
        elif self.model_type == "cohere":
            from .fm.cohere import CohereModel

            self.model = CohereModel(self.model, **kwargs)
        elif self.model_type == "ai21":
            from .fm.ai21 import AI21Model

            self.model = AI21Model(self.model, **kwargs)
        elif self.model_type == "google":
            from .fm.google import GoogleModel

            self.model = GoogleModel(self.model, **kwargs)
        elif self.model_type == "groq":
            from .fm.groq import GroqModel

            self.model = GroqModel(self.model, **kwargs)
        elif self.model_type == "ollama":
            from ..fm.ollama import OllamaModel

            self.model = OllamaModel(self.model)
        elif self.model_type == "dummy":
            from .fm.dummy import DummyModel

            self.model = DummyModel(self.model)
        elif self.model_type == "onnx":
            from .fm.onnx import ONNXModel

            self.model = ONNXModel(self.model, **kwargs)
        elif self.model_type == "flexgen":
            from .fm.flexgen import FlexGenModel

            self.model = FlexGenModel(self.model, **kwargs)
        elif self.model_type == "vllm":
            from .fm.vllm import vLLMModel

            self.model = vLLMModel(self.model, **kwargs)
        elif self.model_type == "tensorrt":
            # self.model = TensorRTModel(self.model, **kwargs)
            raise NotImplementedError
        elif self.model_type == "torch":
            # self.model = TorchModel(self.model, **kwargs)
            raise NotImplementedError
        else:
            logger.error(f"Invalid model type: {self.model_type}")
            raise ValueError(f"Invalid model type: {self.model_type}")
        logger.info(f"Initialized local {self.model_type} model: {self.model}")

        self.server = gRPCServer(self.model, port)
        self.port = self.server.port
        logger.info(f"Initialized gRPC Server on port: {self.port}")


def start_server(args: argparse.Namespace):
    """
    Wrapper function to start gRPC Server.

    :param args: arguments from command line
    :type args: argparse.Namespace
    """
    server = ModelServer(
        args.model,
        args.model_type,
        args.port,
        local_path=args.local_path,
    )


if __name__ == "__main__":
    """
    To Launch from CLI:
    >>> python -m alfred.run_server.py --model_type huggingface --model gpt2 --port 10719


    This is the Main Entry Point for Alfred Server

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=10719)
    parser.add_argument("--credentials", type=str, default=None)

    parser.add_argument("--model", type=str, default="")
    parser.add_argument("--model_type", type=str, default="")
    parser.add_argument("--local_path", type=str, default=None)
    parser.add_argument("--daemon", action="store_true")
    args = parser.parse_args()

    if args.daemon:
        # run start_server in a daemon thread
        import threading

        t = threading.Thread(target=start_server, args=(args,), daemon=True)
        t.start()
    else:
        start_server(args)
