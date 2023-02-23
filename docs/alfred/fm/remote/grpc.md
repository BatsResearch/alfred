# Grpc

[Alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Fm](../index.md#fm) /
[Remote](./index.md#remote) /
Grpc

> Auto-generated documentation for [alfred.fm.remote.grpc](../../../../alfred/fm/remote/grpc.py) module.

- [Grpc](#grpc)
  - [gRPCClient](#grpcclient)
    - [gRPCClient().encode](#grpcclient()encode)
    - [gRPCClient().run](#grpcclient()run)
  - [gRPCServer](#grpcserver)
    - [gRPCServer().Encode](#grpcserver()encode)
    - [gRPCServer().Run](#grpcserver()run)
    - [gRPCServer().close](#grpcserver()close)
    - [gRPCServer().restart](#grpcserver()restart)
    - [gRPCServer().serve](#grpcserver()serve)

## gRPCClient

[Show source in grpc.py:25](../../../../alfred/fm/remote/grpc.py#L25)

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

### gRPCClient().encode

[Show source in grpc.py:75](../../../../alfred/fm/remote/grpc.py#L75)

#### Signature

```python
def encode(self, queries: List[str], reduction: str = "mean", **kwargs: Any):
    ...
```

### gRPCClient().run

[Show source in grpc.py:63](../../../../alfred/fm/remote/grpc.py#L63)

#### Signature

```python
def run(self, queries: Union[Iterable[Query], Iterable[str]], **kwargs: Any):
    ...
```



## gRPCServer

[Show source in grpc.py:142](../../../../alfred/fm/remote/grpc.py#L142)

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

### gRPCServer().Encode

[Show source in grpc.py:221](../../../../alfred/fm/remote/grpc.py#L221)

#### Signature

```python
def Encode(self, request_iterator, context):
    ...
```

### gRPCServer().Run

[Show source in grpc.py:178](../../../../alfred/fm/remote/grpc.py#L178)

#### Signature

```python
def Run(self, request_iterator, context):
    ...
```

### gRPCServer().close

[Show source in grpc.py:243](../../../../alfred/fm/remote/grpc.py#L243)

#### Signature

```python
def close(self):
    ...
```

### gRPCServer().restart

[Show source in grpc.py:246](../../../../alfred/fm/remote/grpc.py#L246)

#### Signature

```python
def restart(self):
    ...
```

### gRPCServer().serve

[Show source in grpc.py:158](../../../../alfred/fm/remote/grpc.py#L158)

#### Signature

```python
def serve(self, credentials: Optional[grpc.ServerCredentials] = None):
    ...
```


