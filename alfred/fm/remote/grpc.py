import ast
import json
import logging
import socket
import sys
from concurrent import futures
from typing import Optional, Union, Iterable, Tuple

import grpc

from alfred.fm.query import Query, RankedQuery, CompletionQuery
from alfred.fm.remote.protos import query_pb2
from alfred.fm.remote.protos import query_pb2_grpc
from alfred.fm.remote.utils import get_ip
from alfred.fm.response import RankedResponse, CompletionResponse

logger = logging.getLogger(__name__)


class gRPCClient:

    def __init__(self,
                 host: str,
                 port: int,
                 credentials: Optional[Union[grpc.ChannelCredentials, str]] = None,
                 ):
        self.host = host
        self.port = port

        if credentials:
            self.channel = grpc.secure_channel(
                f"{self.host}:{self.port}", credentials)
        else:
            self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")

        try:
            grpc.channel_ready_future(self.channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            sys.exit('Error connecting to server')
        else:
            self.stub = query_pb2_grpc.QueryServiceStub(self.channel)

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

    def run(self,
            msg: Union[str, Query, Tuple[str, str]],
            **kwargs,
            ):

        kwargs = json.dumps(kwargs)
        msg, candidate = self._interpret_msg(msg)
        response = self.stub.Inference(
            query_pb2.InferenceRequest(
                message=msg,
                candidate=candidate,
                kwargs=kwargs))
        if candidate:
            resp = self.stub.DataReady(
                query_pb2.DataReadySignal(
                    data_size=1, kwargs=kwargs))
            for response in resp:
                # Only supposed to run once
                response = RankedResponse(
                    **{"prediction": response.message, "scores": ast.literal_eval(response.logit)})
        else:
            response = CompletionResponse(response.message)
        return response

    def run_dataset(self,
                    dataset: Union[Iterable[Query],
                    Iterable[str],
                    Iterable[Tuple[str,
                    str]]],
                    **kwargs,
                    ):
        try:
            data_size = len(dataset)
        except TypeError:
            data_size = -1

        kwargs = json.dumps(kwargs)

        self.stub.DataHeader(query_pb2.DataHeaderRequest(data_size=data_size))

        candidate = None

        for msg in dataset:
            msg, candidate = self._interpret_msg(msg)
            self.stub.Inference(
                query_pb2.InferenceRequest(
                    message=msg, candidate=candidate))

        responses = []
        for response in self.stub.DataReady(
                query_pb2.DataReadySignal(
                    data_size=data_size,
                    kwargs=kwargs)):
            if candidate:
                response = {
                    "prediction": response.message,
                    "scores": ast.literal_eval(
                        response.logit)}
                response = RankedResponse(**response)
            else:
                response = CompletionResponse(response.message)
            responses.append(response)

        return responses


class gRPCServer(query_pb2_grpc.QueryServiceServicer):
    """
    Manages connections with gRPCClient
    """

    @staticmethod
    def port_finder(port: int) -> int:
        """
        Finds the next available port if given port is not available
        """
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(('', port))
                s.close()
                return port
            except OSError:
                port -= 1
                logger.warning(
                    f"Port {port + 1} is not available, trying {port}")

    def __init__(self,
                 model,
                 port: int = 10719,
                 credentials: Optional[grpc.ServerCredentials] = None,
                 ):
        self.model = model
        self.port = self.port_finder(port)

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        query_pb2_grpc.add_QueryServiceServicer_to_server(self, self.server)

        if credentials:
            self.server.add_secure_port(f"[::]:{self.port}", credentials)
        else:
            self.server.add_insecure_port(f"[::]:{self.port}")

        self.group_infer_flag = False
        self.group_ranked_flag = False
        self.dataset = []
        self.candidates = []

        my_ip = get_ip()
        hostname = socket.gethostname()
        # Will not work if the port is not visible to the outside world
        logger.info(
            f"gRPC server starting at {hostname}:{self.port} or {my_ip}:{self.port}")
        self.server.start()
        self.server.wait_for_termination()

    def Inference(self, request, context):
        instance = request.message
        candidate = request.candidate
        kwargs = request.kwargs

        # kwargs is optional
        if kwargs:
            kwargs = json.loads(kwargs)
        else:
            kwargs = {}

        if candidate:
            instance = RankedQuery(
                prompt=instance,
                candidates=candidate.split("|||"))
            self.group_ranked_flag = True
            self.group_infer_flag = True
        else:
            self.group_ranked_flag = False

        if self.group_infer_flag:
            self.dataset.append(instance)
            return query_pb2.InferenceResponse(message="", success=True)
        else:
            try:
                logger.info(
                    f"Received inference request: {instance} with kwargs: {kwargs}")
                response = self.model.run(instance, **kwargs)
                response = response.prediction
                logger.info(f"Sending inference response: {response}")
                # TODO: Take advantage of serialization of Responses
                return query_pb2.InferenceResponse(
                    message=response, ranked=False, success=True)
            except Exception as e:
                message = f"Error: {e}"
                logger.error(message)
                return query_pb2.InferenceResponse(
                    message=message, ranked=False, success=False)

    def DataReady(self, request, context):
        dataset_size = request.data_size
        kwargs = request.kwargs

        # kwargs is optional
        if kwargs:
            kwargs = json.loads(kwargs)
        else:
            kwargs = {}
        logger.info(f"Received {dataset_size} queries")
        if len(self.dataset) != dataset_size:
            logger.warning(
                f"Dataset size mismatch, expected {dataset_size} but got {len(self.dataset)}")

        logger.info(f"Running {dataset_size} queries")
        # edge case for 1 rankequery
        for response in self.model.run(self.dataset, **kwargs):
            # TODO: Take advantage of serialization of Responses
            if isinstance(response, RankedResponse):
                yield query_pb2.InferenceResponse(message=response.prediction,
                                                  logit=str(
                                                      response.scores) if response.scores else None,
                                                  ranked=response.scores is not None, success=True)
            elif isinstance(response, CompletionResponse):
                yield query_pb2.InferenceResponse(message=response.prediction, ranked=False, success=True)
            else:
                yield query_pb2.InferenceResponse(message=response, ranked=False, success=True)
        logger.info(f"Finished running {dataset_size} queries")
        self.group_infer_flag, self.group_ranked_flag = False, False
        self.dataset = []
        logger.info(f"Resetting dataset")

    def DataHeader(self, request, context):
        self.group_infer_flag = True
        self.dataset = []
        dataset_size = request.data_size
        return query_pb2.DataHeaderResponse(data_size=dataset_size)

    def close(self):
        self.server.stop(0)

    def restart(self):
        self.close()
        self.__init__(self.port)
