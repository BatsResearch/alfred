'''
Modified with ideas originated from https://github.com/paramiko/paramiko/blob/main/demos/forward.py
'''
import select
import socket
import threading
from typing import Union

try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer


class ForwardServer(SocketServer.ThreadingTCPServer):
    """
    A simple TCP forwarding server inherited from SocketServer.ThreadingTCPServer
    """
    daemon_threads = True
    allow_reuse_address = True


class Handler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            chan = self.ssh_transport.open_channel(
                "direct-tcpip",
                (self.chain_host, self.chain_port),
                self.request.getpeername(),
            )
        except Exception as e:
            return
        if chan is None:
            return

        while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0:
                    break
                self.request.send(data)

        chan.close()
        self.request.close()


def forward_tunnel(local_port, remote_host, remote_port, transport):
    class SubHander(Handler):
        chain_host = remote_host
        chain_port = int(remote_port)
        ssh_transport = transport

    serving_thread = threading.Thread(target=ForwardServer(
        ("127.0.0.1", local_port), SubHander).serve_forever, daemon=True, )
    serving_thread.start()


def get_host_port(spec, default_port):
    "parse 'hostname:22' into a host and port, with the port optional"
    args = (spec.split(":", 1) + [default_port])[:2]
    args[1] = int(args[1])
    return args[0], args[1]


def port_finder(port: Union[str, int],
                host: str = '') -> int:
    """
    Finds the next available port if given port is not available
    """
    port = int(port)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((host, port))
            s.close()
            return port
        except OSError:
            port -= 1
