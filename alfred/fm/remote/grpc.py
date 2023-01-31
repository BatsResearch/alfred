import ast
import asyncio
import json
import logging
import socket
from tqdm.auto import tqdm
from concurrent import futures
from typing import Optional, Union, Iterable, Tuple, Any, List

import grpc

from alfred.fm.query import Query, RankedQuery, CompletionQuery
from alfred.fm.remote.protos import query_pb2
from alfred.fm.remote.protos import query_pb2_grpc
from alfred.fm.remote.utils import get_ip, tensor_to_bytes, bytes_to_tensor, port_finder
from alfred.fm.response import RankedResponse, CompletionResponse

logger = logging.getLogger(__name__)


class gRPCClient:
    def __init__(
        self,
        host: str,
        port: int,
        credentials: Optional[Union[grpc.ChannelCredentials, str]] = None,
    ):
        self.host = host
        self.port = port

        if credentials:
            self.channel = grpc.secure_channel(f"{self.host}:{self.port}",
                                               credentials)
        else:
            self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")

        try:
            self.stub = query_pb2_grpc.QueryServiceStub(self.channel)
        except Exception as e:
            logger.error(f"Failed to connect to {self.host}:{self.port}")
            raise e

    @staticmethod
    def _interpret_msg(msg):
        candidate = None
        if isinstance(msg, CompletionQuery):
            msg = msg.load()[0]
        elif isinstance(msg, RankedQuery):
            msg, candidate = msg.prompt, msg.get_answer_choices_str()
        elif isinstance(msg, Tuple):
            msg, candidate = msg[0], msg[1]
        return msg, candidate

    def run(
        self,
        queries: Union[Iterable[Query], Iterable[str]],
        **kwargs: Any,
    ):
        try:
            output = self._run(queries, **kwargs)
        except Exception as e:
            logger.error(f"Failed to run queries: {e}")
            raise e
        return output

    def encode(
        self,
        queries: List[str],
        reduction: str = "mean",
        **kwargs: Any,
    ):
        try:
            output = self._encode(queries, reduction, **kwargs)
        except Exception as e:
            logger.error(f"Failed to encode queries: {e}")
            raise e
        return output

    def _run(
        self,
        queries: Union[Iterable[Query], Iterable[str]],
        **kwargs: Any,
    ):
        kwargs = json.dumps(kwargs)

        def _run_req_gen():
            for query in queries:
                msg, candidate = self._interpret_msg(query)
                yield query_pb2.RunRequest(message=msg,
                                           candidate=candidate,
                                           kwargs=kwargs)

        output = []
        for response in self.stub.Run(_run_req_gen()):
            if response.ranked:
                output.append(
                    RankedResponse(
                        **{
                            "prediction": response.message,
                            "scores": ast.literal_eval(response.logit),
                            "embeddings": bytes_to_tensor(response.embedding)
                        }))
            else:
                output.append(
                    CompletionResponse(response.message,
                                       embedding=bytes_to_tensor(
                                           response.embedding)))
        return output

    def _encode(
        self,
        queries: List[str],
        reduction: str = "mean",
        **kwargs: Any,
    ):
        kwargs = json.dumps(kwargs)

        def _encode_req_gen():
            for query in queries:
                yield query_pb2.EncodeRequest(message=query,
                                              reduction=reduction,
                                              kwargs=kwargs)

        output = []
        for response in self.stub.Encode(_encode_req_gen()):
            if response.success:
                output.append(bytes_to_tensor(response.embedding))
            else:
                output.append(None)
        return output


class gRPCServer(query_pb2_grpc.QueryServiceServicer):
    """
    Manages connections with gRPCClient
    """
    def __init__(
        self,
        model,
        port: int = 10719,
        credentials: Optional[grpc.ServerCredentials] = None,
    ):
        self.model = model
        self.port = port_finder(port)

        self.serve(credentials)

    def serve(self, credentials: Optional[grpc.ServerCredentials] = None):

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        query_pb2_grpc.add_QueryServiceServicer_to_server(self, self.server)

        if credentials:
            self.server.add_secure_port(f"[::]:{self.port}", credentials)
        else:
            self.server.add_insecure_port(f"[::]:{self.port}")

        my_ip = get_ip()
        hostname = socket.gethostname()
        # Will not work if the port is not visible to the outside world
        logger.info(
            f"gRPC server starting at {hostname}:{self.port} or {my_ip}:{self.port}"
        )

        self.server.start()
        self.server.wait_for_termination()

    def Run(self, request_iterator, context):
        logger.info("Received request")
        datasets = []
        for request in request_iterator:
            instance = request.message
            candidate = request.candidate
            kwargs = request.kwargs

            if kwargs:
                kwargs = json.loads(kwargs)
            else:
                kwargs = {}
            if candidate:
                instance = RankedQuery(prompt=instance,
                                       candidates=candidate.split("|||"))
            else:
                instance = CompletionQuery(instance)
            datasets.append(instance)

        logger.info(f"Received {len(datasets)} queries")

        responses = self.model.run(datasets, **kwargs)
        for response in tqdm(responses):
            if isinstance(response, CompletionResponse):
                yield query_pb2.RunResponse(message=response.prediction,
                                            ranked=False,
                                            embedding=tensor_to_bytes(
                                                response.embedding))
            elif isinstance(response, RankedResponse):
                yield query_pb2.RunResponse(message=response.prediction,
                                            ranked=True,
                                            logit=str(response.scores),
                                            embedding=tensor_to_bytes(
                                                response.embeddings))
            else:
                logger.error(f"Response type {type(response)} not supported")
                raise ValueError("Response type not supported")

    def Encode(self, request_iterator, context):
        logger.info("Received request")
        datasets = []
        for request in request_iterator:
            instance = request.message
            reduction = request.reduction
            kwargs = request.kwargs

            if kwargs:
                kwargs = json.loads(kwargs)
            else:
                kwargs = {}

            datasets.append(instance)

        logger.info(f"Received {len(datasets)} queries for embeddings")

        for response in tqdm(
                self.model.encode(datasets, reduction=reduction, **kwargs)):
            yield query_pb2.EncodeResponse(success=True,
                                           embedding=tensor_to_bytes(response))

    def close(self):
        self.server.stop(0)

    def restart(self):
        self.close()
        self.__init__(self.port)
