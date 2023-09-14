# SSHTunnel

[Alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Client](../index.md#client) /
[Ssh](./index.md#ssh) /
SSHTunnel

> Auto-generated documentation for [alfred.client.ssh.sshtunnel](../../../../alfred/client/ssh/sshtunnel.py) module.

- [SSHTunnel](#sshtunnel)
  - [SSHTunnel](#sshtunnel-1)
    - [SSHTunnel.adaptive_handler](#sshtunneladaptive_handler)
    - [SSHTunnel().start](#sshtunnel()start)
    - [SSHTunnel().stop](#sshtunnel()stop)

## SSHTunnel

[Show source in sshtunnel.py:13](../../../../alfred/client/ssh/sshtunnel.py#L13)

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
        key_file: str = "~/.ssh/id_rsa",
        handler: Callable = None,
    ):
        ...
```

### SSHTunnel.adaptive_handler

[Show source in sshtunnel.py:21](../../../../alfred/client/ssh/sshtunnel.py#L21)

Authentication handler for paramiko's interactive authentication

#### Signature

```python
@staticmethod
def adaptive_handler(title, instructions, prompt_list):
    ...
```

### SSHTunnel().start

[Show source in sshtunnel.py:82](../../../../alfred/client/ssh/sshtunnel.py#L82)

Wrapper for _start() with exception handling

#### Signature

```python
def start(self):
    ...
```

### SSHTunnel().stop

[Show source in sshtunnel.py:142](../../../../alfred/client/ssh/sshtunnel.py#L142)

Stop the tunnel

#### Signature

```python
def stop(self):
    ...
```


