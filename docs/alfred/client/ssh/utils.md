# Utils

[Alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Client](../index.md#client) /
[Ssh](./index.md#ssh) /
Utils

> Auto-generated documentation for [alfred.client.ssh.utils](../../../../alfred/client/ssh/utils.py) module.

- [Utils](#utils)
  - [ForwardServer](#forwardserver)
  - [Handler](#handler)
    - [Handler().handle](#handler()handle)
  - [forward_tunnel](#forward_tunnel)
  - [get_host_port](#get_host_port)
  - [port_finder](#port_finder)

## ForwardServer

[Show source in utils.py:15](../../../../alfred/client/ssh/utils.py#L15)

A simple TCP forwarding server inherited from SocketServer.ThreadingTCPServer

#### Signature

```python
class ForwardServer(SocketServer.ThreadingTCPServer):
    ...
```



## Handler

[Show source in utils.py:24](../../../../alfred/client/ssh/utils.py#L24)

#### Signature

```python
class Handler(SocketServer.BaseRequestHandler):
    ...
```

### Handler().handle

[Show source in utils.py:25](../../../../alfred/client/ssh/utils.py#L25)

#### Signature

```python
def handle(self):
    ...
```



## forward_tunnel

[Show source in utils.py:54](../../../../alfred/client/ssh/utils.py#L54)

#### Signature

```python
def forward_tunnel(local_port, remote_host, remote_port, transport):
    ...
```



## get_host_port

[Show source in utils.py:67](../../../../alfred/client/ssh/utils.py#L67)

parse 'hostname:22' into a host and port, with the port optional

#### Signature

```python
def get_host_port(spec, default_port):
    ...
```



## port_finder

[Show source in utils.py:74](../../../../alfred/client/ssh/utils.py#L74)

Finds the next available port if given port is not available

#### Signature

```python
def port_finder(port: Union[str, int], host: str = "") -> int:
    ...
```