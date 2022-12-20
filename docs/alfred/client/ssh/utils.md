# Utils

[alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Client](../index.md#client) /
[Ssh](./index.md#ssh) /
Utils

> Auto-generated documentation for [alfred.client.ssh.utils](https://github.com/BatsResearch/alfred/blob/main/alfred/client/ssh/utils.py) module.

## ForwardServer

[Show source in utils.py:15](https://github.com/BatsResearch/alfred/blob/main/alfred/client/ssh/utils.py#L15)

A simple TCP forwarding server inherited from SocketServer.ThreadingTCPServer

#### Signature

```python
class ForwardServer(SocketServer.ThreadingTCPServer):
    ...
```



## Handler

[Show source in utils.py:23](https://github.com/BatsResearch/alfred/blob/main/alfred/client/ssh/utils.py#L23)

#### Signature

```python
class Handler(SocketServer.BaseRequestHandler):
    ...
```

### Handler().handle

[Show source in utils.py:24](https://github.com/BatsResearch/alfred/blob/main/alfred/client/ssh/utils.py#L24)

#### Signature

```python
def handle(self):
    ...
```



## forward_tunnel

[Show source in utils.py:53](https://github.com/BatsResearch/alfred/blob/main/alfred/client/ssh/utils.py#L53)

#### Signature

```python
def forward_tunnel(local_port, remote_host, remote_port, transport):
    ...
```



## get_host_port

[Show source in utils.py:64](https://github.com/BatsResearch/alfred/blob/main/alfred/client/ssh/utils.py#L64)

parse 'hostname:22' into a host and port, with the port optional

#### Signature

```python
def get_host_port(spec, default_port):
    ...
```



## port_finder

[Show source in utils.py:71](https://github.com/BatsResearch/alfred/blob/main/alfred/client/ssh/utils.py#L71)

Finds the next available port if given port is not available

#### Signature

```python
def port_finder(port: Union[str, int], host: str = "") -> int:
    ...
```



