# Grpc

[alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Fm](../index.md#fm) /
[Remote](./index.md#remote) /
Grpc

> Auto-generated documentation for [alfred.fm.remote.grpc](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/grpc.py) module.

## gRPCClient

[Show source in grpc.py:19](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/grpc.py#L19)

#### Signature

```python
class gRPCClient:
    def __init__(
        self,
        host: str,
        port: int,
        credentials: Optional[Union[grpc.ChannelCredentials, str]] = None,
    ):
        ...
```

### gRPCClient().run

[Show source in grpc.py:53](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/grpc.py#L53)

#### Signature

```python
def run(self, msg: Union[str, Query, Tuple[str, str]], **kwargs):
    ...
```

### gRPCClient().run_dataset

[Show source in grpc.py:77](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/grpc.py#L77)

#### Signature

```python
def run_dataset(
    self,
    dataset: Union[Iterable[Query], Iterable[str], Iterable[Tuple[str, str]]],
    **kwargs
):
    ...
```



## gRPCServer

[Show source in grpc.py:119](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/grpc.py#L119)

Manages connections with gRPCClient

#### Signature

```python
class gRPCServer(query_pb2_grpc.QueryServiceServicer):
    def __init__(
        self,
        model,
        port: int = 10719,
        credentials: Optional[grpc.ServerCredentials] = None,
    ):
        ...
```

### gRPCServer().DataHeader

[Show source in grpc.py:240](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/grpc.py#L240)

#### Signature

```python
def DataHeader(self, request, context):
    ...
```

### gRPCServer().DataReady

[Show source in grpc.py:208](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/grpc.py#L208)

#### Signature

```python
def DataReady(self, request, context):
    ...
```

### gRPCServer().Inference

[Show source in grpc.py:169](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/grpc.py#L169)

#### Signature

```python
def Inference(self, request, context):
    ...
```

### gRPCServer().close

[Show source in grpc.py:246](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/grpc.py#L246)

#### Signature

```python
def close(self):
    ...
```

### gRPCServer.port_finder

[Show source in grpc.py:124](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/grpc.py#L124)

Finds the next available port if given port is not available

#### Signature

```python
@staticmethod
def port_finder(port: int) -> int:
    ...
```

### gRPCServer().restart

[Show source in grpc.py:249](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/grpc.py#L249)

#### Signature

```python
def restart(self):
    ...
```



