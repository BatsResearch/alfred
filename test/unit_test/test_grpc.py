import threading
import time
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
        self.server_thread = threading.Thread(
            target=server_starter,
            args=(
                self.server,
                cli,
                self.port,
            ),
            daemon=True,
        )
        self.server_thread.start()

        self.channel = grpc.insecure_channel(f"localhost:{self.port}")
        self.stub = query_pb2_grpc.QueryServiceStub(self.channel)
        time.sleep(2)

    def test_run_single_query(self):
        # Test running a single query using the client
        query = CompletionQuery(prompt="This is a query")

        def _run_req_gen():
            yield query__pb2.RunRequest(message=query.prompt)

        response = self.stub.Run(_run_req_gen())
        response = response.next()
        self.assertEqual(response.message, query.prompt)

    def test_run_multiple_queries(self):
        # Test running a dataset of queries using the client
        queries = [CompletionQuery(prompt="Query 1"), CompletionQuery(prompt="Query 2")]

        def _run_req_gen():
            for query in queries:
                yield query__pb2.RunRequest(message=query.prompt)

        responses = self.stub.Run(_run_req_gen())

        for i, response in enumerate(responses):
            self.assertEqual(response.message, f"Query {i + 1}")
