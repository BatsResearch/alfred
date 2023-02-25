# Run Server

[Alfred Index](../README.md#alfred-index) /
[Alfred](./index.md#alfred) /
Run Server

> Auto-generated documentation for [alfred.run_server](../../alfred/run_server.py) module.

- [Run Server](#run-server)
  - [ModelServer](#modelserver)
  - [start_server](#start_server)

## ModelServer

[Show source in run_server.py:20](../../alfred/run_server.py#L20)

ModelServer is the server-side interface that wraps a certain alfred.fm class.
ModelServer is used to launch the specified alfred.fm model as a gRPC Server and find the proper port.

#### Signature

```python
class ModelServer:
    def __init__(self, model: str, model_type: str, port: int = 10719, **kwargs: Any):
        ...
```



## start_server

[Show source in run_server.py:72](../../alfred/run_server.py#L72)

Wrapper function to start gRPC Server.

#### Arguments

- [args](#run-server) - arguments from command line
:type args: argparse.Namespace

#### Signature

```python
def start_server(args: argparse.Namespace):
    ...
```


