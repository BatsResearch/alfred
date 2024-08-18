# gRPCClient

[Alfred Index](../../../README.md#alfred-index) / [Alfred](../../index.md#alfred) / [Fm](../index.md#fm) / [Remote](./index.md#remote) / gRPCClient

> Auto-generated documentation for [alfred.fm.remote.grpc_client](../../../../alfred/fm/remote/grpc_client.py) module.

- [gRPCClient](#grpcclient)
  - [gRPCClient](#grpcclient-1)
    - [gRPCClient().close](#grpcclient()close)
    - [gRPCClient().encode](#grpcclient()encode)
    - [gRPCClient().handshake](#grpcclient()handshake)
    - [gRPCClient().run](#grpcclient()run)

## gRPCClient

[Show source in grpc_client.py:24](../../../../alfred/fm/remote/grpc_client.py#L24)

#### Signature

```python
class gRPCClient:
    def __init__(
        self,
        host: str,
        port: int,
        credentials: Optional[Union[grpc.ChannelCredentials, str]] = None,
    ): ...
```

### gRPCClient().close

[Show source in grpc_client.py:190](../../../../alfred/fm/remote/grpc_client.py#L190)

#### Signature

```python
def close(self): ...
```

### gRPCClient().encode

[Show source in grpc_client.py:107](../../../../alfred/fm/remote/grpc_client.py#L107)

#### Signature

```python
def encode(self, queries: List[str], reduction: str = "mean", **kwargs: Any): ...
```

### gRPCClient().handshake

[Show source in grpc_client.py:46](../../../../alfred/fm/remote/grpc_client.py#L46)

#### Signature

```python
def handshake(self): ...
```

### gRPCClient().run

[Show source in grpc_client.py:92](../../../../alfred/fm/remote/grpc_client.py#L92)

#### Signature

```python
def run(
    self, queries: Union[Iterable[Query], Iterable[str], Iterable[Tuple]], **kwargs: Any
): ...
```