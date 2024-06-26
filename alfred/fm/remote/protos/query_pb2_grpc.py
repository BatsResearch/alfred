# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""

import grpc

from . import query_pb2 as query__pb2


class QueryServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Encode = channel.stream_stream(
            "/unary.QueryService/Encode",
            request_serializer=query__pb2.EncodeRequest.SerializeToString,
            response_deserializer=query__pb2.EncodeResponse.FromString,
        )
        self.Run = channel.stream_stream(
            "/unary.QueryService/Run",
            request_serializer=query__pb2.RunRequest.SerializeToString,
            response_deserializer=query__pb2.RunResponse.FromString,
        )


class QueryServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Encode(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Run(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_QueryServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "Encode": grpc.stream_stream_rpc_method_handler(
            servicer.Encode,
            request_deserializer=query__pb2.EncodeRequest.FromString,
            response_serializer=query__pb2.EncodeResponse.SerializeToString,
        ),
        "Run": grpc.stream_stream_rpc_method_handler(
            servicer.Run,
            request_deserializer=query__pb2.RunRequest.FromString,
            response_serializer=query__pb2.RunResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "unary.QueryService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class QueryService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Encode(
        request_iterator,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            "/unary.QueryService/Encode",
            query__pb2.EncodeRequest.SerializeToString,
            query__pb2.EncodeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def Run(
        request_iterator,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            "/unary.QueryService/Run",
            query__pb2.RunRequest.SerializeToString,
            query__pb2.RunResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
