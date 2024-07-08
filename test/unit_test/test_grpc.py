import threading
import time
import unittest
import asyncio

from alfred.client import Client
from alfred.fm.query import CompletionQuery
from alfred.fm.remote.grpc_server import gRPCServer
from alfred.fm.remote.grpc_client import gRPCClient


class TestGRPCServer(unittest.TestCase):
    def setUp(self):
        self.port = 10711
        self.model = Client(model_type="dummy")

        def server_starter(server, model, port):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(server(model=model, port=port))

        self.server_thread = threading.Thread(
            target=server_starter,
            args=(
                gRPCServer,
                self.model,
                self.port,
            ),
            daemon=True,
        )
        self.server_thread.start()

        time.sleep(1)

        self.client = gRPCClient("localhost", self.port)

    def test_handshake(self):
        # Test the handshake process
        self.client.handshake()
        self.assertIsNotNone(self.client.session_id)

    def test_run_single_query(self):
        # Test running a single query using the client
        query = CompletionQuery(prompt="This is a query")
        responses = self.client.run([query])

        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0].prediction, query.prompt)

    def test_run_multiple_queries(self):
        queries = [CompletionQuery(prompt="Query 1"), CompletionQuery(prompt="Query 2")]
        responses = self.client.run(queries)

        self.assertEqual(len(responses), 2)
        for i, response in enumerate(responses):
            self.assertEqual(response.prediction, f"Query {i + 1}")

    def tearDown(self):
        self.client.close()


if __name__ == "__main__":
    unittest.main()
