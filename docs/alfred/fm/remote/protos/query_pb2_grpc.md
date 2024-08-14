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
    - [QueryService.Handshake](#queryservicehandshake)
    - [QueryService.Run](#queryservicerun)
  - [QueryServiceServicer](#queryserviceservicer)
    - [QueryServiceServicer().Encode](#queryserviceservicer()encode)
    - [QueryServiceServicer().Handshake](#queryserviceservicer()handshake)
    - [QueryServiceServicer().Run](#queryserviceservicer()run)
  - [QueryServiceStub](#queryservicestub)
  - [add_QueryServiceServicer_to_server](#add_queryserviceservicer_to_server)

## QueryService

[Show source in query_pb2_grpc.py:113](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L113)

Missing associated documentation comment in .proto file.

#### Signature

```python
class QueryService(object):
    ...
```

### QueryService.Encode

[Show source in query_pb2_grpc.py:146](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L146)

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

### QueryService.Handshake

[Show source in query_pb2_grpc.py:116](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L116)

#### Signature

```python
@staticmethod
def Handshake(
    request,
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

[Show source in query_pb2_grpc.py:176](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L176)

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

[Show source in query_pb2_grpc.py:65](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L65)

Missing associated documentation comment in .proto file.

#### Signature

```python
class QueryServiceServicer(object):
    ...
```

### QueryServiceServicer().Encode

[Show source in query_pb2_grpc.py:74](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L74)

Missing associated documentation comment in .proto file.

#### Signature

```python
def Encode(self, request_iterator, context):
    ...
```

### QueryServiceServicer().Handshake

[Show source in query_pb2_grpc.py:68](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L68)

Missing associated documentation comment in .proto file.

#### Signature

```python
def Handshake(self, request, context):
    ...
```

### QueryServiceServicer().Run

[Show source in query_pb2_grpc.py:80](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L80)

Missing associated documentation comment in .proto file.

#### Signature

```python
def Run(self, request_iterator, context):
    ...
```



## QueryServiceStub

[Show source in query_pb2_grpc.py:36](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L36)

Missing associated documentation comment in .proto file.

#### Signature

```python
class QueryServiceStub(object):
    def __init__(self, channel):
        ...
```



## add_QueryServiceServicer_to_server

[Show source in query_pb2_grpc.py:87](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L87)

#### Signature

```python
def add_QueryServiceServicer_to_server(servicer, server):
    ...
```


