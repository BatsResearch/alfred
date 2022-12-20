# SSHTunnel

[alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Client](../index.md#client) /
[Ssh](./index.md#ssh) /
SSHTunnel

> Auto-generated documentation for [alfred.client.ssh.sshtunnel](https://github.com/BatsResearch/alfred/blob/main/alfred/client/ssh/sshtunnel.py) module.

## SSHTunnel

[Show source in sshtunnel.py:12](https://github.com/BatsResearch/alfred/blob/main/alfred/client/ssh/sshtunnel.py#L12)

SSH Tunnel implemented with paramiko and supports interactive authentication
This tunnel would be very useful if you have a alfred.fm model on remote server that you want to access
It also supports tunneling via a jump host:
e.g. model on a gpu node of a cluster can use login node as jump
     This will be equivalent to SSH -L commands

#### Signature

```python
class SSHTunnel:
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
        ...
```

### SSHTunnel.adaptive_handler

[Show source in sshtunnel.py:21](https://github.com/BatsResearch/alfred/blob/main/alfred/client/ssh/sshtunnel.py#L21)

Authentication handler for paramiko's interactive authentication

#### Signature

```python
@staticmethod
def adaptive_handler(title, instructions, prompt_list):
    ...
```

### SSHTunnel().start

[Show source in sshtunnel.py:74](https://github.com/BatsResearch/alfred/blob/main/alfred/client/ssh/sshtunnel.py#L74)

Start the tunnel

#### Signature

```python
def start(self):
    ...
```

### SSHTunnel().stop

[Show source in sshtunnel.py:117](https://github.com/BatsResearch/alfred/blob/main/alfred/client/ssh/sshtunnel.py#L117)

Stop the tunnel

#### Signature

```python
def stop(self):
    ...
```



