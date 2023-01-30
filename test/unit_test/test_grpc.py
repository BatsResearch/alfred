import threading
import unittest

import grpc

import alfred.fm.remote.protos.query_pb2 as query__pb2
import alfred.fm.remote.protos.query_pb2_grpc as query_pb2_grpc
from alfred.client import Client
from alfred.fm.query import CompletionQuery
from alfred.fm.remote.grpc import gRPCServer


class TestGRPCServer(unittest.TestCase):
    def setUp(self):
        def server_starter(server, client, port):
            server(client, port, None)
            print("Server started")

        self.port = 10711
        #
        cli = Client(model_type="dummy")
        # self.server.add_insecure_port(f"127.0.0.1:{self.port}")
        #
        # # Start the gRPC server in a separate thread
        self.server = gRPCServer
        self.server_thread = threading.Thread(target=server_starter,
                                              args=(
                                                  self.server,
                                                  cli,
                                                  self.port,
                                              ),
                                              daemon=True)
        self.server_thread.start()

        self.channel = grpc.insecure_channel(f"localhost:{self.port}")
        self.stub = query_pb2_grpc.QueryServiceStub(self.channel)

    def test_run_single_query(self):
        # Test running a single query using the client
        query = CompletionQuery(prompt="This is a query")
        response = self.stub.Inference(
            query__pb2.InferenceRequest(message=query.prompt))
        self.assertEqual(response.message, query.prompt)

    def test_run_multiple_queries(self):
        # Test running a dataset of queries using the client
        queries = [
            CompletionQuery(prompt="Query 1"),
            CompletionQuery(prompt="Query 2")
        ]

        _ = self.stub.DataHeader(
            query__pb2.DataHeaderRequest(data_size=len(queries)))
        for query in queries:
            _ = self.stub.Inference(
                query__pb2.InferenceRequest(message=query.prompt))
        responses = self.stub.DataReady(
            query__pb2.DataReadySignal(data_size=len(queries)))
        for i, response in enumerate(responses):
            self.assertEqual(response.message, f"Query {i + 1}")
