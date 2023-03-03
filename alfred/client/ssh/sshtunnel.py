import getpass
import logging
from typing import Optional, Union, Callable

import paramiko

from alfred.client.ssh.utils import port_finder, forward_tunnel

logger = logging.getLogger(__name__)


class SSHTunnel:
    """
    SSH Tunnel implemented with paramiko and supports interactive authentication
    This tunnel would be very useful if you have a alfred.fm model on remote server that you want to access
    It also supports tunneling via a jump host:
    e.g. model on a gpu node of a cluster can use login node as jump
         This will be equivalent to SSH -L commands
    """
    @staticmethod
    def adaptive_handler(title, instructions, prompt_list):
        """Authentication handler for paramiko's interactive authentication"""
        print(title)
        print(instructions)
        user_input = []
        for (prompt, echo) in prompt_list:
            if echo:
                res = input(prompt)
            else:
                res = getpass.getpass(prompt)
            user_input.append(res)
        return user_input

    def __init__(
        self,
        remote_host: str,
        remote_port: Union[int, str],
        local_port: Union[int, str] = 10705,
        username: Optional[str] = None,
        remote_node_address: Optional[str] = None,
        remote_bind_port: Optional[Union[int, str]] = 443,
        handler: Callable = None,
    ):
        """
        Initialize the SSH Tunnel

        :param remote_host: The remote host to connect to
        :type remote_host: str
        :param remote_port: The remote port to connect to
        :type remote_port: Union[int, str]
        :param local_port: The local port to bind to, defaults to 10705
        :type local_port: Union[int, str], optional
        :param username: (optional) The username to connect with, defaults to None
        :type username: str
        :param remote_node_address: (optional) The remote node address to connect to, defaults to None
        :type remote_node_address: str
        :param remote_bind_port: (optional) The remote bind port to connect to, defaults to 443
        :type remote_bind_port: Optional[Union[int, str]], optional
        :param handler: The handler for interactive authentication, defaults to adaptive handler
        :type handler: Callable, optional
        """

        self.local_port = port_finder(local_port)
        logger.info(f"Local port: {self.local_port}")

        self.remote_port = remote_port
        self.remote_host = remote_host

        self.username = username or input("Username: ")
        self.remote_node_address = remote_node_address
        self.remote_bind_port = remote_bind_port
        self.handler = handler or self.adaptive_handler

    def start(self):
        """Wrapper for _start() with exception handling"""
        attempts = 0
        while attempts < 3:
            try:
                self._start()
                break
            except Exception as e:
                logger.error(e)
                attempts += 1
                logger.warning(f"Attempt {attempts} failed, retrying...")
        logger.info("Tunnel started")

    def _start(self):
        """Start the tunnel"""

        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.WarningPolicy())

        try:
            self.client.connect(self.remote_host, username=self.username)
        except paramiko.ssh_exception.SSHException:
            pass

        try:
            self.client.get_transport().auth_interactive(
                username=self.username, handler=self.handler)
        except paramiko.ssh_exception.AuthenticationException:
            logger.error("Wrong Password, Please restart the Tunnel")
            raise paramiko.ssh_exception.AuthenticationException
        logger.log(logging.INFO, f"Connected to {self.remote_host} @ port 22")

        port = self.client.get_transport().sock.getsockname()[1]
        logger.debug(f"Underlying port: {port}")

        if not self.remote_node_address:
            self.remote_bind_port = port_finder(self.remote_bind_port,
                                                self.remote_host)
            self.remote_node_address = "127.0.0.1"
        else:
            self.remote_bind_port = self.remote_port

        logger.info(f"Remote bind port: {self.remote_bind_port}")

        forward_tunnel(int(self.local_port), self.remote_node_address,
                       int(self.remote_port), self.client.get_transport())
        logger.info(f"Forward SSH Tunnel started on port {self.local_port}")

        logger.info(
            f"Forwarding {self.remote_host}->{self.remote_node_address}:{self.remote_bind_port} to localhost:{self.local_port}"
        )

    def stop(self):
        """Stop the tunnel"""
        self.client = None
