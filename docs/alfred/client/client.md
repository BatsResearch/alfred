# Client

[alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Client](./index.md#client) /
Client

> Auto-generated documentation for [alfred.client.client](https://github.com/BatsResearch/alfred/blob/main/alfred/client/client.py) module.

## Client

[Show source in client.py:17](https://github.com/BatsResearch/alfred/blob/main/alfred/client/client.py#L17)

Client is the primary user interface that wraps around foundation models.
A client interface for accessing various models, such as those implemented by OpenAI, Hugging Face, etc.
The client can be used to specify the model and how to access it,
and can establish an SSH tunnel to a remote end point for secure access to a remote model.

#### Signature

```python
class Client:
    def __init__(
        self,
        model: Optional[str] = None,
        model_type: Optional[str] = None,
        end_point: Optional[str] = None,
        local_path: Optional[str] = None,
        ssh_tunnel: bool = False,
        ssh_node: Optional[str] = None,
        **kwargs: Any
    ):
        ...
```

### Client().__call__

[Show source in client.py:219](https://github.com/BatsResearch/alfred/blob/main/alfred/client/client.py#L219)

__call__() function to run the model on the queries.
Equivalent to run() function.

#### Arguments

- `queries` - The queries to run the model on.
:type queries: Union[Query, str, List[Query], List[str]]
- `kwargs` - Additional keyword arguments (e.g. repetition_penalty, temperature, etc.)
:type kwargs: Any

#### Returns

The response(s) from the model.
Type: *Union[Response, List[Response]]*

#### Signature

```python
def __call__(
    self, queries: Union[Query, str, List[Query], List[str]], **kwargs: Any
) -> Union[Response, List[Response]]:
    ...
```

### Client().generate

[Show source in client.py:180](https://github.com/BatsResearch/alfred/blob/main/alfred/client/client.py#L180)

Wrapper function to generate the response(s) from the model. (For completion)

#### Arguments

- `query` - The query to generate the response(s) from.
:type query: Union[CompletionQuery, str, List[Union[CompletionQuery, str]]]
- `kwargs` - Additional keyword arguments (e.g. repetition_penalty, temperature, etc.)
:type kwargs: Any

#### Returns

The response(s) from the model.
Type: *Union[Response, List[Response]]*

#### Signature

```python
def generate(
    self,
    query: Union[CompletionQuery, str, List[CompletionQuery], List[str]],
    **kwargs: Any
) -> Union[Response, List[Response]]:
    ...
```

### Client().remote_run

[Show source in client.py:159](https://github.com/BatsResearch/alfred/blob/main/alfred/client/client.py#L159)

Wrapper function for running the model on the queries thru a gRPC Server.

#### Arguments

- `queries` - The queries to run the model on.
:type queries: Union[Query, str, List[Query], List[str]]
- `kwargs` - Additional keyword arguments (e.g. repetition_penalty, temperature, etc.)
:type kwargs: Any

#### Returns

The response(s) from the model.
Type: *Union[Response, List[Response]]*

#### Signature

```python
def remote_run(
    self, queries: Union[Query, str, List[Query], List[str]], **kwargs: Any
) -> Union[Response, List[Response]]:
    ...
```

### Client().run

[Show source in client.py:140](https://github.com/BatsResearch/alfred/blob/main/alfred/client/client.py#L140)

Run the model on the queries.

#### Arguments

- `queries` - The queries to run the model on.
:type queries: Union[Query, str, List[Query], List[str]]
- `kwargs` - Additional keyword arguments (e.g. repetition_penalty, temperature, etc.)
:type kwargs: Any

#### Returns

The response(s) from the model.
Type: *Union[Response, List[Response]]*

#### Signature

```python
def run(
    self, queries: Union[Query, str, List[Query], List[str]], **kwargs: Any
) -> Union[Response, List[Response]]:
    ...
```

### Client().score

[Show source in client.py:196](https://github.com/BatsResearch/alfred/blob/main/alfred/client/client.py#L196)

Wrapper function to score the response(s) from the model. (For ranking)

TODO: Implement Query in the below format:
Query can be in form of a list of ranked query or a dictionary in form of:
{
    "prompt": "query string",
    "candidates": ["candidate 1", "candidate 2", ...]
}

#### Arguments

- `query` - A single query object or a list of query objects
:type query: Union[RankedQuery, Dict, List[RankedQuery], List[str]]
- `kwargs` - Additional keyword arguments
:type kwargs: Any

#### Returns

A single response or a list of responses
Type: *Union[Response, List[Response]]*

#### Signature

```python
def score(
    self, query: Union[RankedQuery, Dict, List[RankedQuery], List[str]], **kwargs: Any
) -> Union[Response, List[Response]]:
    ...
```



