import ast
import base64
import io
import json
import logging
import torch
import torch.nn.functional as F
from typing import Optional, Union, Iterable, Tuple, Any, List

import grpc
from PIL import Image

from ..query import Query, RankedQuery, CompletionQuery
from ..remote.protos import query_pb2
from .protos import query_pb2_grpc
from ..remote.utils import bytes_to_tensor
from ..response import RankedResponse, CompletionResponse

logger = logging.getLogger(__name__)

IMAGE_SIGNATURE = "[ALFED_IMAGE_BASE64]"


class gRPCClient:
    def __init__(
        self,
        host: str,
        port: int,
        credentials: Optional[Union[grpc.ChannelCredentials, str]] = None,
    ):
        self.host = host
        self.port = port
        self.session_id = None

        if credentials:
            self.channel = grpc.secure_channel(f"{self.host}:{self.port}", credentials)
        else:
            self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")

        try:
            self.stub = query_pb2_grpc.QueryServiceStub(self.channel)
        except Exception as e:
            logger.error(f"Failed to connect to {self.host}:{self.port}")
            raise e

    def handshake(self):
        try:
            response = self.stub.Handshake(query_pb2.HandshakeRequest())
            self.session_id = response.session_id
            logger.info(f"Handshake completed. Session ID: {self.session_id}")
        except Exception as e:
            logger.error(f"Handshake failed: {e}")
            raise e

    @staticmethod
    def _interpret_msg(msg):
        candidate = None
        if isinstance(msg, CompletionQuery):
            msg = msg.load()[0]
            if isinstance(msg, Tuple):
                img, prompt = msg[0], msg[1]
                io_output = io.BytesIO()
                img.save(io_output, format="png")
                msg = (
                    prompt
                    + IMAGE_SIGNATURE
                    + base64.b64encode(io_output.getvalue()).decode("UTF-8")
                )
        elif isinstance(msg, RankedQuery):
            msg, candidate = msg.prompt, msg.get_answer_choices_str()
            if isinstance(msg, Image.Image):
                io_output = io.BytesIO()
                msg.save(io_output, format="png")
                msg = IMAGE_SIGNATURE + base64.b64encode(io_output.getvalue()).decode(
                    "UTF-8"
                )
        elif isinstance(msg, Tuple):
            msg, candidate = msg[0], msg[1]
            if isinstance(msg, Image.Image):
                img, prompt = msg, candidate
                io_output = io.BytesIO()
                img.save(io_output, format="png")
                msg = (
                    prompt
                    + IMAGE_SIGNATURE
                    + base64.b64encode(io_output.getvalue()).decode("UTF-8")
                )
                candidate = None

        return msg, candidate

    def run(
        self,
        queries: Union[Iterable[Query], Iterable[str], Iterable[Tuple]],
        **kwargs: Any,
    ):
        if not self.session_id:
            self.handshake()

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
        if not self.session_id:
            self.handshake()

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
                yield query_pb2.RunRequest(
                    message=msg, candidate=candidate, kwargs=kwargs
                )

        metadata = (("session_id", self.session_id),)
        output = []
        for response in self.stub.Run(_run_req_gen(), metadata=metadata):
            if response.ranked:
                logits = ast.literal_eval(response.logit)
                candidates = list(logits.keys())
                logit_values = torch.tensor(list(logits.values()))
                probabilities = F.softmax(logit_values, dim=0)
                scores = {
                    candidate: prob.item()
                    for candidate, prob in zip(candidates, probabilities)
                }
                output.append(
                    RankedResponse(
                        **{
                            "prediction": response.message,
                            "scores": scores,
                            "logits": logits,
                            "embeddings": bytes_to_tensor(response.embedding),
                        }
                    )
                )
            else:
                output.append(
                    CompletionResponse(
                        response.message, embedding=bytes_to_tensor(response.embedding)
                    )
                )
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
                yield query_pb2.EncodeRequest(
                    message=query, reduction=reduction, kwargs=kwargs
                )

        metadata = (("session_id", self.session_id),)
        output = []
        for response in self.stub.Encode(_encode_req_gen(), metadata=metadata):
            if response.success:
                output.append(bytes_to_tensor(response.embedding))
            else:
                output.append(None)
        return output

    def close(self):
        self.channel.close()
