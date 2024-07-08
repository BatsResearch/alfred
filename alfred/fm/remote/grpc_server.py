import asyncio
import base64
import io
import json
import logging
import uuid
import socket
from typing import Optional

import grpc
from PIL import Image
from tqdm.auto import tqdm

from ..query import RankedQuery, CompletionQuery
from ..remote.protos import query_pb2
from .protos import query_pb2_grpc
from ..remote.utils import tensor_to_bytes
from ..response import RankedResponse, CompletionResponse
from .message_queue import MessageBroker, Message

logger = logging.getLogger(__name__)

IMAGE_SIGNATURE = "[ALFED_IMAGE_BASE64]"


class gRPCServer(query_pb2_grpc.QueryServiceServicer):
    def __init__(
        self,
        model,
        port: int = 10719,
        credentials: Optional[grpc.ServerCredentials] = None,
    ):
        self.model = model
        self.port = port
        self.broker = MessageBroker()
        self.executor = asyncio.get_event_loop()
        self.serve(credentials)

    async def Handshake(self, request, context):
        session_id = str(uuid.uuid4())
        self.broker.sessions[session_id] = asyncio.Queue()
        logger.info(f"New session created: {session_id}")
        return query_pb2.HandshakeResponse(session_id=session_id)

    async def Run(self, request_iterator, context):
        metadata = dict(context.invocation_metadata())
        session_id = metadata.get("session_id")
        if not session_id or session_id not in self.broker.sessions:
            logger.error(f"Invalid session: {session_id}")
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid session")

        self.broker.subscribe("queries", session_id)
        self.broker.subscribe("responses", session_id)

        datasets = []
        kwargs = {}

        async for request in request_iterator:
            instance = request.message
            candidate = request.candidate
            request_kwargs = request.kwargs

            if candidate:
                if instance.startswith(IMAGE_SIGNATURE):
                    instance = Image.open(
                        io.BytesIO(base64.b64decode(instance[len(IMAGE_SIGNATURE) :]))
                    )
            else:
                if IMAGE_SIGNATURE in instance:
                    prompt, img = instance.split(IMAGE_SIGNATURE)
                    img = Image.open(io.BytesIO(base64.b64decode(img)))
                    instance = (img, prompt)

            if request_kwargs:
                kwargs.update(json.loads(request_kwargs))

            if candidate:
                instance = RankedQuery(
                    prompt=instance, candidates=candidate.split("|||")
                )
            else:
                instance = CompletionQuery(instance)

            datasets.append(instance)
            message = Message("queries", instance, session_id)
            await self.broker.publish(message)

        logger.info(f"Received {len(datasets)} queries from session {session_id}")

        responses = self._process_queries(datasets, kwargs)

        for response in responses:
            yield response

    def _process_queries(self, datasets, kwargs):
        responses = self.model.run(datasets, **kwargs)
        for response in tqdm(responses):
            if isinstance(response, CompletionResponse):
                yield query_pb2.RunResponse(
                    message=response.prediction,
                    ranked=False,
                    embedding=tensor_to_bytes(response.embedding),
                )
            elif isinstance(response, RankedResponse):
                yield query_pb2.RunResponse(
                    message=response.prediction,
                    ranked=True,
                    logit=str(response.logits),
                    embedding=tensor_to_bytes(response.embeddings),
                )
            else:
                logger.error(f"Response type {type(response)} not supported")
                raise ValueError("Response type not supported")

    async def Encode(self, request_iterator, context):
        metadata = dict(context.invocation_metadata())
        session_id = metadata.get("session_id")
        if not session_id or session_id not in self.broker.sessions:
            logger.error(f"Invalid session: {session_id}")
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid session")

        self.broker.subscribe("encode_queries", session_id)
        self.broker.subscribe("encode_responses", session_id)

        datasets = []
        reduction = None
        kwargs = {}

        async for request in request_iterator:
            instance = request.message
            reduction = request.reduction
            request_kwargs = request.kwargs

            if request_kwargs:
                kwargs.update(json.loads(request_kwargs))

            datasets.append(instance)
            message = Message("encode_queries", instance, session_id)
            await self.broker.publish(message)

        logger.info(
            f"Received {len(datasets)} queries for embeddings from session {session_id}"
        )

        responses = await self._process_encoding(datasets, reduction, kwargs)

        async for response in responses:
            yield response

    async def _process_encoding(self, datasets, reduction, kwargs):
        responses = self.model.encode(datasets, reduction=reduction, **kwargs)
        async for response in tqdm(responses):
            yield query_pb2.EncodeResponse(
                success=True, embedding=tensor_to_bytes(response)
            )

    def serve(self, credentials):
        server = grpc.aio.server()
        query_pb2_grpc.add_QueryServiceServicer_to_server(self, server)
        if credentials:
            server.add_secure_port(f"[::]:{self.port}", credentials)
        else:
            server.add_insecure_port(f"[::]:{self.port}")

        async def start_server():
            await server.start()
            hostname = socket.gethostname()
            logger.info(f"gRPC server starting at {hostname}:{self.port}")
            await server.wait_for_termination()

        self.executor.run_until_complete(start_server())
