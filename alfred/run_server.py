import argparse
import logging
from typing import Any

import alfred.fm.remote.grpc as grpc_utils
from alfred.fm.dummy import DummyModel
from alfred.fm.huggingface import HuggingFaceModel
from alfred.fm.openai import OpenAIModel
from alfred.fm.huggingfacevlm import HuggingFaceCLIPModel

logging.basicConfig(
    format='ALFRED %(levelname)s: %(asctime)-5s  %(message)s',
    level=logging.NOTSET,
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger("Alfred Server")


class ModelServer:
    """
    ModelServer is the server-side interface that wraps a certain alfred.fm class.
    ModelServer is used to launch the specified alfred.fm model as a gRPC Server and find the proper port.
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
        This ModeServer launches the specified alfred.fm model on the server
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
            "huggingface", "huggingfacevlm", "openai", "onnx", "tensorrt", "torch", "dummy"
        ], f"Invalid model type: {self.model_type}"
        if self.model_type == "huggingface":
            self.model = HuggingFaceModel(self.model, **kwargs)
        elif self.model_type == "huggingfacevlm":
            self.model = HuggingFaceCLIPModel(self.model, **kwargs)
        elif self.model_type == "openai":
            self.model = OpenAIModel(self.model, **kwargs)
        elif self.model_type == "dummy":
            self.model = DummyModel(self.model)
        else:
            logger.error(f"Invalid model type: {self.model_type}")
            raise ValueError(f"Invalid model type: {self.model_type}")
        logger.info(f"Initialized local {self.model_type} model: {self.model}")

        self.server = grpc_utils.gRPCServer(self.model, port)
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
