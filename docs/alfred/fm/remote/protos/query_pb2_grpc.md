# Query Pb2 Grpc

[Alfred Index](../../../../README.md#alfred-index) /
[Alfred](../../../index.md#alfred) /
[Fm](../../index.md#fm) /
[Remote](../index.md#remote) /
[Protos](./index.md#protos) /
Query Pb2 Grpc

> Auto-generated documentation for [alfred.fm.remote.protos.query_pb2_grpc](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py) module.

- [Query Pb2 Grpc](#query-pb2-grpc)
  - [QueryService](#queryservice)
    - [QueryService.Encode](#queryserviceencode)
    - [QueryService.Run](#queryservicerun)
  - [QueryServiceServicer](#queryserviceservicer)
    - [QueryServiceServicer().Encode](#queryserviceservicer()encode)
    - [QueryServiceServicer().Run](#queryserviceservicer()run)
  - [QueryServiceStub](#queryservicestub)
  - [add_QueryServiceServicer_to_server](#add_queryserviceservicer_to_server)

## QueryService

[Show source in query_pb2_grpc.py:70](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L70)

Missing associated documentation comment in .proto file.

#### Signature

```python
class QueryService(object):
    ...
```

### QueryService.Encode

[Show source in query_pb2_grpc.py:72](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L72)

#### Signature

```python
@staticmethod
def Encode(
    request_iterator,
    target,
    options=(),
    channel_credentials=None,
    call_credentials=None,
    insecure=False,
    compression=None,
    wait_for_ready=None,
    timeout=None,
    metadata=None,
):
    ...
```

### QueryService.Run

[Show source in query_pb2_grpc.py:90](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L90)

#### Signature

```python
@staticmethod
def Run(
    request_iterator,
    target,
    options=(),
    channel_credentials=None,
    call_credentials=None,
    insecure=False,
    compression=None,
    wait_for_ready=None,
    timeout=None,
    metadata=None,
):
    ...
```



## QueryServiceServicer

[Show source in query_pb2_grpc.py:34](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L34)

Missing associated documentation comment in .proto file.

#### Signature

```python
class QueryServiceServicer(object):
    ...
```

### QueryServiceServicer().Encode

[Show source in query_pb2_grpc.py:36](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L36)

Missing associated documentation comment in .proto file.

#### Signature

```python
def Encode(self, request_iterator, context):
    ...
```

### QueryServiceServicer().Run

[Show source in query_pb2_grpc.py:42](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L42)

Missing associated documentation comment in .proto file.

#### Signature

```python
def Run(self, request_iterator, context):
    ...
```



## QueryServiceStub

[Show source in query_pb2_grpc.py:14](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L14)

Missing associated documentation comment in .proto file.

#### Signature

```python
class QueryServiceStub(object):
    def __init__(self, channel):
        ...
```



## add_QueryServiceServicer_to_server

[Show source in query_pb2_grpc.py:49](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L49)

#### Signature

```python
def add_QueryServiceServicer_to_server(servicer, server):
    ...
```


