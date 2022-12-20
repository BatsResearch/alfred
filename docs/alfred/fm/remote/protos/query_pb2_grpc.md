# Query Pb2 Grpc

[alfred Index](../../../../README.md#alfred-index) /
[Alfred](../../../index.md#alfred) /
[Fm](../../index.md#fm) /
[Remote](../index.md#remote) /
[Protos](./index.md#protos) /
Query Pb2 Grpc

> Auto-generated documentation for [alfred.fm.remote.protos.query_pb2_grpc](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py) module.

- [Query Pb2 Grpc](#query-pb2-grpc)
  - [QueryService](#queryservice)
    - [QueryService.DataHeader](#queryservicedataheader)
    - [QueryService.DataReady](#queryservicedataready)
    - [QueryService.Inference](#queryserviceinference)
  - [QueryServiceServicer](#queryserviceservicer)
    - [QueryServiceServicer().DataHeader](#queryserviceservicer()dataheader)
    - [QueryServiceServicer().DataReady](#queryserviceservicer()dataready)
    - [QueryServiceServicer().Inference](#queryserviceservicer()inference)
  - [QueryServiceStub](#queryservicestub)
  - [add_QueryServiceServicer_to_server](#add_queryserviceservicer_to_server)

## QueryService

[Show source in query_pb2_grpc.py:88](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L88)

Missing associated documentation comment in .proto file.

#### Signature

```python
class QueryService(object):
    ...
```

### QueryService.DataHeader

[Show source in query_pb2_grpc.py:143](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L143)

#### Signature

```python
@staticmethod
def DataHeader(
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

### QueryService.DataReady

[Show source in query_pb2_grpc.py:117](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L117)

#### Signature

```python
@staticmethod
def DataReady(
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

### QueryService.Inference

[Show source in query_pb2_grpc.py:91](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L91)

#### Signature

```python
@staticmethod
def Inference(
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



## QueryServiceServicer

[Show source in query_pb2_grpc.py:40](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L40)

Missing associated documentation comment in .proto file.

#### Signature

```python
class QueryServiceServicer(object):
    ...
```

### QueryServiceServicer().DataHeader

[Show source in query_pb2_grpc.py:56](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L56)

Missing associated documentation comment in .proto file.

#### Signature

```python
def DataHeader(self, request, context):
    ...
```

### QueryServiceServicer().DataReady

[Show source in query_pb2_grpc.py:50](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L50)

Missing associated documentation comment in .proto file.

#### Signature

```python
def DataReady(self, request, context):
    ...
```

### QueryServiceServicer().Inference

[Show source in query_pb2_grpc.py:43](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L43)

stream messages

#### Signature

```python
def Inference(self, request, context):
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

[Show source in query_pb2_grpc.py:63](../../../../../alfred/fm/remote/protos/query_pb2_grpc.py#L63)

#### Signature

```python
def add_QueryServiceServicer_to_server(servicer, server):
    ...
```


