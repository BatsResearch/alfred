# gRPCServer

[Alfred Index](../../../README.md#alfred-index) / [Alfred](../../index.md#alfred) / [Fm](../index.md#fm) / [Remote](./index.md#remote) / gRPCServer

> Auto-generated documentation for [alfred.fm.remote.grpc_server](../../../../alfred/fm/remote/grpc_server.py) module.

- [gRPCServer](#grpcserver)
  - [gRPCServer](#grpcserver-1)
    - [gRPCServer().Encode](#grpcserver()encode)
    - [gRPCServer().Handshake](#grpcserver()handshake)
    - [gRPCServer().Run](#grpcserver()run)
    - [gRPCServer().serve](#grpcserver()serve)

## gRPCServer

[Show source in grpc_server.py:26](../../../../alfred/fm/remote/grpc_server.py#L26)

#### Signature

```python
class gRPCServer(query_pb2_grpc.QueryServiceServicer):
    def __init__(
        self,
        model,
        port: int = 10719,
        credentials: Optional[grpc.ServerCredentials] = None,
    ): ...
```

### gRPCServer().Encode

[Show source in grpc_server.py:115](../../../../alfred/fm/remote/grpc_server.py#L115)

#### Signature

```python
async def Encode(self, request_iterator, context): ...
```

### gRPCServer().Handshake

[Show source in grpc_server.py:39](../../../../alfred/fm/remote/grpc_server.py#L39)

#### Signature

```python
async def Handshake(self, request, context): ...
```

### gRPCServer().Run

[Show source in grpc_server.py:45](../../../../alfred/fm/remote/grpc_server.py#L45)

#### Signature

```python
async def Run(self, request_iterator, context): ...
```

### gRPCServer().serve

[Show source in grpc_server.py:157](../../../../alfred/fm/remote/grpc_server.py#L157)

#### Signature

```python
def serve(self, credentials): ...
```