import io
import logging
import socket
import torch
import urllib.request

logger = logging.getLogger(__name__)


def get_ip(ipv4=True):
    """
    Returns the Public IP address of the current machine.

    :param ipv4: If True, returns the IPv4 address. If False, returns the IPv6 address.
    :type ipv4: bool
    :return: The Public IP address of the current machine.
    :rtype: str
    """
    prefix = 'v4' if ipv4 else 'v6'
    external_ip = urllib.request.urlopen(
        f"https://{prefix}.ident.me").read().decode('utf8')
    return external_ip.strip()


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
            logger.warning(f"Port {port + 1} is not available, trying {port}")


def tensor_to_bytes(tensor):
    try:
        buffer = io.BytesIO()
        torch.save(tensor, buffer)
        res = buffer.getvalue()
        return res
    except Exception as e:
        return bytes('error', 'utf-8')


def bytes_to_tensor(bytes):
    try:
        buffer = io.BytesIO(bytes)
        res = torch.load(buffer)
        return res
    except Exception as e:
        return None
