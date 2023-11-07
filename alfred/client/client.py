import logging
from typing import Any, List, Optional, Union, Dict, Tuple

import numpy as np
import torch
from grpc import FutureTimeoutError

from .cache import Cache, DummyCache, SQLiteCache
from .ssh.sshtunnel import SSHTunnel
from ..fm.query import CompletionQuery, Query, RankedQuery
from ..fm.remote.grpc import gRPCClient
from ..fm.response import Response
from ..template import StringTemplate, Template
from ..voter.voter import Voter

logger = logging.getLogger(__name__)

NULL_INPUT_TOKENS = ["N/A", "ε", "[MASK]", "NULL", "<|endoftext|>"]


class Client:
    """
    Client is the primary user interface that wraps around foundation models.
    A client interface for accessing various models, such as those implemented by OpenAI, Hugging Face, etc.
    The client can be used to specify the model and how to access it,
    and can establish an SSH tunnel to a remote end point for secure access to a remote model.
    """

    def __init__(
        self,
        model: Optional[str] = None,
        model_type: Optional[str] = None,
        end_point: Optional[str] = None,
        local_path: Optional[str] = None,
        ssh_tunnel: bool = False,
        ssh_pk: str = "~/.ssh/id_rsa",
        ssh_node: Optional[str] = None,
        cache: Optional[Cache] = None,
        **kwargs: Any,
    ):
        """
        Initialize a Client class.

        :param model: (optional) The name of the model. (e.g. bigscience/T0pp or text-davinci-003)
        :type model: str
        :param model_type: (optional) The type of the model. (e.g. "openai", "huggingface", "dummy")
        :type model_type: str
        :param end_point: (optional) The end point of the model with username and port. (e.g. "user@localhost:50051")
        :type end_point: str
        :param local_path: (optional) The local path of the model. (e.g. "/home/user/.cache/model")
        :param ssh_tunnel: Whether to establish an SSH tunnel to the end point.
        :type ssh_tunnel: bool
        :param ssh_pk: ssh RSA key location
        :type ssh_pk: str
        :param ssh_node: (optional) The final SSH node to establish the SSH tunnel. (e.g. gpu node on a cluster with login node as jump)
        :type ssh_node: str
        :param cache: (optional) The cache to use. (e.g. "SQLite", "Dummy")
        :type cache: Cache Object
        :param kwargs: Additional keyword arguments
        :type kwargs: Any
        """

        self.model = model
        self.model_type = model_type

        if self.model_type:
            self.model_type = model_type.lower()
            assert self.model_type in [
                "huggingface",
                "huggingfacevlm",
                "huggingfacedocument",
                "onnx",
                "tensorrt",
                "flexgen",
                "vllm",
                "openai",
                "anthropic",
                "cohere",
                "ai21",
                "torch",
                "dummy",
            ], f"Invalid model type: {self.model_type}"
        else:
            if end_point is None:
                logger.error(
                    "Model type is not specified. Please specify model type or end point"
                )
                raise ValueError(
                    "Model type is not specified. Please specify model/model_type or end_point"
                )

        if cache:
            if cache == "SQLite":
                self.cache = SQLiteCache()
            elif cache == "Dummy":
                self.cache = DummyCache()
            self.run = self.cache.cached_query(self.run)

        self.grpcClient = None
        if end_point:
            end_point_pieces = end_point.split(":")
            self.end_point_ip, self.end_point_port = (
                "".join(end_point_pieces[:-1]),
                end_point_pieces[-1],
            )

            if ssh_tunnel:
                try:
                    user_name, host_name = self.end_point_ip.split("@")
                except ValueError:
                    logger.warning(
                        "Invalid end point format, please use user_name@host_name:port, prompting for username and "
                        "password"
                    )
                    user_name = input("Username: ")
                    host_name = self.end_point_ip

                logger.info(
                    f"Trying to connect to {user_name}@{host_name}:{self.end_point_port} via {ssh_node}"
                )

                tunnel = SSHTunnel(
                    remote_host=host_name,
                    remote_port=self.end_point_port,
                    remote_node_address=ssh_node,
                    username=user_name,
                    key_file=ssh_pk,
                )

                tunnel.start()

                logger.info(
                    f"SSH tunnel bound to {self.end_point_ip}:{self.end_point_port} established at localhost:{tunnel.local_port}"
                )

                self.end_point_ip = "127.0.0.1"
                self.end_point_port = tunnel.local_port

            logger.info(
                f"Connecting to remote end point: {end_point}, looking for model: {model}"
            )

            try:
                logger.info(
                    f"Connecting to remote end point: {self.end_point_ip}:{self.end_point_port}, looking for model: {model}"
                )
                self.grpcClient = gRPCClient(self.end_point_ip, self.end_point_port)
                logger.info(f"Connected to remote end point: {end_point}")
            except FutureTimeoutError:
                logger.error(f"Cannot connect to remote end point: {end_point}")
                raise ConnectionError(
                    f"Cannot connect to remote end point: {end_point}"
                )
        else:
            if self.model_type == "huggingface":
                from ..fm.huggingface import HuggingFaceModel

                self.model = HuggingFaceModel(
                    self.model, local_path=local_path, **kwargs
                )
            elif self.model_type == "huggingfacevlm":
                from ..fm.huggingfacevlm import HuggingFaceCLIPModel

                self.model = HuggingFaceCLIPModel(
                    self.model, local_path=local_path, **kwargs
                )
            elif self.model_type == "huggingfacedocument":
                from ..fm.huggingfacedocument import HuggingFaceDocumentModel

                self.model = HuggingFaceDocumentModel(
                    self.model, local_path=local_path, **kwargs
                )
            elif self.model_type == "anthropic":
                from ..fm.anthropic import AnthropicModel

                self.model = AnthropicModel(self.model, **kwargs)
            elif self.model_type == "openai":
                from ..fm.openai import OpenAIModel

                self.model = OpenAIModel(self.model, **kwargs)
            elif self.model_type == "cohere":
                from ..fm.cohere import CohereModel

                self.model = CohereModel(self.model, **kwargs)
            elif self.model_type == "ai21":
                from ..fm.ai21 import AI21Model

                self.model = AI21Model(self.model, **kwargs)
            elif self.model_type == "dummy":
                from ..fm.dummy import DummyModel

                self.model = DummyModel(self.model)
            elif self.model_type == "onnx":
                from ..fm.onnx import ONNXModel

                self.model = ONNXModel(self.model, **kwargs)
            elif self.model_type == "flexgen":
                from ..fm.flexgen import FlexGenModel

                self.model = FlexGenModel(self.model, **kwargs)
            elif self.model_type == "vllm":
                from ..fm.vllm import vLLMModel

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
            logger.info(f"Connected to local {self.model_type} model: {self.model}")

    def run(
        self,
        queries: Union[Query, str, List[Query], List[str]],
        **kwargs: Any,
    ) -> Union[Response, List[Response]]:
        """
        Run the model on the queries.

        :param queries: The queries to run the model on.
        :type queries: Union[Query, str, List[Query], List[str]]
        :param kwargs: Additional keyword arguments (e.g. repetition_penalty, temperature, etc.)
        :type kwargs: Any
        :return: The response(s) from the model.
        :rtype: Union[Response, List[Response]]
        """
        if self.grpcClient:
            return self.remote_run(queries, **kwargs)
        else:
            return self.model.run(queries, **kwargs)

    def remote_run(
        self,
        queries: Union[Query, str, List[Query], List[str]],
        **kwargs: Any,
    ) -> Union[Response, List[Response]]:
        """
        Wrapper function for running the model on the queries thru a gRPC Server.

        :param queries: The queries to run the model on.
        :type queries: Union[Query, str, List[Query], List[str]]
        :param kwargs: Additional keyword arguments (e.g. repetition_penalty, temperature, etc.)
        :type kwargs: Any
        :return: The response(s) from the model.
        :rtype: Union[Response, List[Response]]
        """
        single_query = False
        if (
            isinstance(queries, str)
            or isinstance(queries, Query)
            or isinstance(queries, Tuple)
        ):
            single_query = True
            queries = [queries]
        responses = self.grpcClient.run(queries, **kwargs)
        return responses[0] if single_query else responses

    def generate(
        self,
        query: Union[CompletionQuery, str, List[CompletionQuery], List[str]],
        **kwargs: Any,
    ) -> Union[Response, List[Response]]:
        """
        Wrapper function to generate the response(s) from the model. (For completion)

        :param query: The query to generate the response(s) from.
        :type query: Union[CompletionQuery, str, List[Union[CompletionQuery, str]]]
        :param kwargs: Additional keyword arguments (e.g. repetition_penalty, temperature, etc.)
        :type kwargs: Any
        :return: The response(s) from the model.
        :rtype: Union[Response, List[Response]]
        """
        return self(query, **kwargs)

    def score(
        self,
        query: Union[RankedQuery, Dict, List[RankedQuery], List[str]],
        **kwargs: Any,
    ) -> Union[Response, List[Response]]:
        """
        Wrapper function to score the response(s) from the model. (For ranking)

        TODO: Implement Query in the below format:
        Query can be in form of a list of ranked query or a dictionary in form of:
        {
            "prompt": "query string",
            "candidates": ["candidate 1", "candidate 2", ...]
        }

        :param query: A single query object or a list of query objects
        :type query: Union[RankedQuery, Dict, List[RankedQuery], List[str]]
        :param kwargs: Additional keyword arguments
        :type kwargs: Any
        :return: A single response or a list of responses
        :rtype: Union[Response, List[Response]]
        """
        return self(query, **kwargs)

    def __call__(
        self, queries: Union[Query, str, List[Query], List[str]], **kwargs: Any
    ) -> Union[Response, List[Response]]:
        """
        __call__() function to run the model on the queries.
        Equivalent to run() function.

        :param queries: The queries to run the model on.
        :type queries: Union[Query, str, List[Query], List[str]]
        :param kwargs: Additional keyword arguments (e.g. repetition_penalty, temperature, etc.)
        :type kwargs: Any
        :return: The response(s) from the model.
        :rtype: Union[Response, List[Response]]
        """
        return self.run(queries, **kwargs)

    def calibrate(
        self,
        template: Union[str, Template],
        voter: Optional[Voter] = None,
        null_tokens: Optional[Union[List[str], str]] = None,
        candidates: Optional[Union[List[str], str]] = None,
        strategy: int = 1,
    ):
        """
        calibrate are used to calibrate foundation models contextually given the template.
        A voter class may be passed to calibrate the model with a specific voter.
        If a voter is set, the calibrated weights will be stored in the voter
        calibrate() function will return the calibration weights and biases otherwise.

        There are two strategies for calibration:
        1.  W = diag(p)^-1, b = 0
        2.  W = eye, b = -p

        For reference, please refer to:
            Zhao, Z., Wallace, E., Feng, S., Klein, D., & Singh, S. (2021, July).
            Calibrate before use: Improving few-shot performance of language models.
            In International Conference on Machine Learning (pp. 12697-12706). PMLR.

        :param template: The template to calibrate the model with.
        :type template: Union[str, Template]
        :param voter: The voter to calibrate the model with.
        :type voter: Optional[Voter]
        :param null_tokens: The null tokens to calibrate the model with.
        :type null_tokens: Optional[Union[List[str], str]]
        :param candidates: The candidates to calibrate the model with.
        :type candidates: Optional[Union[List[str], str]]
        :param strategy: The strategy to calibrate the model with. default to 1
        :type strategy: int
        """
        if null_tokens is None:
            null_tokens = NULL_INPUT_TOKENS
        if isinstance(null_tokens, str):
            null_tokens = [null_tokens]

        candidates = candidates or template._answer_candidates
        if candidates is None:
            logger.error("No candidates provided for calibration.")
            raise ValueError("No answer candidates provided for calibration.")

        template = StringTemplate(template) if isinstance(template, str) else template

        # identify the keywords in template_str
        keywords = template.keywords
        weights = np.empty([len(null_tokens), len(candidates), len(candidates)])
        biases = np.empty([len(null_tokens), len(candidates)])
        scores = np.empty((len(null_tokens), len(candidates)))
        for null_token_id, null_token in enumerate(null_tokens):
            null_instance = dict(((k, null_token) for k in keywords))
            query = template.apply(null_instance)
            query._candidates = candidates
            p = np.array(list(self.score(query, no_tqdm=True).scores.values()))
            scores[null_token_id, :] = p
            if strategy == 1:
                weights[null_token_id, :, :] = np.linalg.inv(np.diag(p))
                biases[null_token_id, :] = np.zeros(len(candidates))
            elif strategy == 2:
                weights[null_token_id, :, :] = np.eye(len(candidates))
                biases[null_token_id, :] = -p

        ensembled_weights = weights.mean(axis=0)
        ensembled_biases = biases.mean(axis=0)

        if voter is None:
            return ensembled_weights, ensembled_biases

        voter.set_calibration(ensembled_weights, ensembled_biases)

    def encode(
        self,
        queries: Union[str, List[str]],
        reduction: str = "mean",
    ) -> Union[torch.Tensor, List[torch.Tensor]]:
        """
        embed() function to embed the queries.

        :param queries: The queries to embed.
        :type queries: Union[str, List[str]]
        :param reduction: The reduction method to use on word embeddings. default to 'mean'
                          choose from ['mean', 'sum', 'none']
        :type reduction: str
        """
        is_single = False
        if isinstance(queries, str) or isinstance(queries, Query):
            queries = [queries]
            is_single = True

        if self.grpcClient:
            output = self.grpcClient.encode(queries, reduction=reduction)
        else:
            output = self.model.encode(queries, reduction=reduction)

        return output[0] if is_single else output

    def chat(self, log_save_path: Optional[str] = None, **kwargs: Any):
        """
        Chat with the model APIs.
        Currently, Alfred supports Chat APIs from Anthropic and OpenAI

        :param log_save_path: The file to save the chat logs.
        :type log_save_path: Optional[str]
        """
        if self.model_type in ["openai", "anthropic"]:
            self.model.chat(log_save_path=log_save_path, **kwargs)
        else:
            logger.error(
                "Chat APIs are only supported for Anthropic and OpenAI models."
            )
            raise NotImplementedError(
                "Currently Chat are only supported for Anthropic and OpenAI models."
            )
