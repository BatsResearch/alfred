# Grpc

[Alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Fm](../index.md#fm) /
[Remote](./index.md#remote) /
Grpc

> Auto-generated documentation for [alfred.fm.remote.grpc](../../../../alfred/fm/remote/grpc.py) module.

- [Grpc](#grpc)
  - [gRPCClient](#grpcclient)
    - [gRPCClient().run](#grpcclient()run)
    - [gRPCClient().run_dataset](#grpcclient()run_dataset)
  - [gRPCServer](#grpcserver)
    - [gRPCServer().DataHeader](#grpcserver()dataheader)
    - [gRPCServer().DataReady](#grpcserver()dataready)
    - [gRPCServer().Inference](#grpcserver()inference)
    - [gRPCServer().close](#grpcserver()close)
    - [gRPCServer.port_finder](#grpcserverport_finder)
    - [gRPCServer().restart](#grpcserver()restart)

## gRPCClient

[Show source in grpc.py:20](../../../../alfred/fm/remote/grpc.py#L20)

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

[Show source in grpc.py:54](../../../../alfred/fm/remote/grpc.py#L54)

#### Signature

```python
def run(self, msg: Union[str, Query, Tuple[str, str]], **kwargs):
    ...
```

### gRPCClient().run_dataset

[Show source in grpc.py:78](../../../../alfred/fm/remote/grpc.py#L78)

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

[Show source in grpc.py:120](../../../../alfred/fm/remote/grpc.py#L120)

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

[Show source in grpc.py:241](../../../../alfred/fm/remote/grpc.py#L241)

#### Signature

```python
def DataHeader(self, request, context):
    ...
```

### gRPCServer().DataReady

[Show source in grpc.py:209](../../../../alfred/fm/remote/grpc.py#L209)

#### Signature

```python
def DataReady(self, request, context):
    ...
```

### gRPCServer().Inference

[Show source in grpc.py:170](../../../../alfred/fm/remote/grpc.py#L170)

#### Signature

```python
def Inference(self, request, context):
    ...
```

### gRPCServer().close

[Show source in grpc.py:247](../../../../alfred/fm/remote/grpc.py#L247)

#### Signature

```python
def close(self):
    ...
```

### gRPCServer.port_finder

[Show source in grpc.py:125](../../../../alfred/fm/remote/grpc.py#L125)

Finds the next available port if given port is not available

#### Signature

```python
@staticmethod
def port_finder(port: int) -> int:
    ...
```

### gRPCServer().restart

[Show source in grpc.py:250](../../../../alfred/fm/remote/grpc.py#L250)

#### Signature

```python
def restart(self):
    ...
```


