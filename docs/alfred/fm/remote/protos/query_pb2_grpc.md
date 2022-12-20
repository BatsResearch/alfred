# Query Pb2 Grpc

[alfred Index](../../../../README.md#alfred-index) /
[Alfred](../../../index.md#alfred) /
[Fm](../../index.md#fm) /
[Remote](../index.md#remote) /
[Protos](./index.md#protos) /
Query Pb2 Grpc

> Auto-generated documentation for [alfred.fm.remote.protos.query_pb2_grpc](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/protos/query_pb2_grpc.py) module.

## QueryService

[Show source in query_pb2_grpc.py:88](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/protos/query_pb2_grpc.py#L88)

Missing associated documentation comment in .proto file.

#### Signature

```python
class QueryService(object):
    ...
```

### QueryService.DataHeader

[Show source in query_pb2_grpc.py:143](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/protos/query_pb2_grpc.py#L143)

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

[Show source in query_pb2_grpc.py:117](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/protos/query_pb2_grpc.py#L117)

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

[Show source in query_pb2_grpc.py:91](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/protos/query_pb2_grpc.py#L91)

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

[Show source in query_pb2_grpc.py:40](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/protos/query_pb2_grpc.py#L40)

Missing associated documentation comment in .proto file.

#### Signature

```python
class QueryServiceServicer(object):
    ...
```

### QueryServiceServicer().DataHeader

[Show source in query_pb2_grpc.py:56](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/protos/query_pb2_grpc.py#L56)

Missing associated documentation comment in .proto file.

#### Signature

```python
def DataHeader(self, request, context):
    ...
```

### QueryServiceServicer().DataReady

[Show source in query_pb2_grpc.py:50](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/protos/query_pb2_grpc.py#L50)

Missing associated documentation comment in .proto file.

#### Signature

```python
def DataReady(self, request, context):
    ...
```

### QueryServiceServicer().Inference

[Show source in query_pb2_grpc.py:43](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/protos/query_pb2_grpc.py#L43)

stream messages

#### Signature

```python
def Inference(self, request, context):
    ...
```



## QueryServiceStub

[Show source in query_pb2_grpc.py:14](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/protos/query_pb2_grpc.py#L14)

Missing associated documentation comment in .proto file.

#### Signature

```python
class QueryServiceStub(object):
    def __init__(self, channel):
        ...
```



## add_QueryServiceServicer_to_server

[Show source in query_pb2_grpc.py:63](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/remote/protos/query_pb2_grpc.py#L63)

#### Signature

```python
def add_QueryServiceServicer_to_server(servicer, server):
    ...
```



