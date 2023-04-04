# Client

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Client](./index.md#client) /
Client

> Auto-generated documentation for [alfred.client.client](../../../alfred/client/client.py) module.

- [Client](#client)
  - [Client](#client-1)
    - [Client().__call__](#client()__call__)
    - [Client().calibrate](#client()calibrate)
    - [Client().chat](#client()chat)
    - [Client().encode](#client()encode)
    - [Client().generate](#client()generate)
    - [Client().remote_run](#client()remote_run)
    - [Client().run](#client()run)
    - [Client().score](#client()score)

## Client

[Show source in client.py:21](../../../alfred/client/client.py#L21)

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
        cache: Optional[Cache] = None,
        **kwargs: Any
    ):
        ...
```

### Client().__call__

[Show source in client.py:260](../../../alfred/client/client.py#L260)

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

### Client().calibrate

[Show source in client.py:275](../../../alfred/client/client.py#L275)

calibrate are used to calibrate foundation models contextually given the template.
A voter class may be passed to calibrate the model with a specific voter.
If a voter is set, the calibrated weights will be stored in the voter
calibrate() function will return the calibration weights and biases otherwise.

There are two strategies for calibration:
1.  W = diag(p)^-1, b = 0
2.  W = eye, b = -p

For reference, please refer to:
    Zhao, Z., Wallace, E., Feng, S., Klein, D., & Singh, S. (2021, July).
    Calibrate before use: Improving few-shot performance of language models.
    In International Conference on Machine Learning (pp. 12697-12706). PMLR.

#### Arguments

- `template` - The template to calibrate the model with.
:type template: Union[str, Template]
- `voter` - The voter to calibrate the model with.
:type voter: Optional[Voter]
- `null_tokens` - The null tokens to calibrate the model with.
:type null_tokens: Optional[Union[List[str], str]]
- `candidates` - The candidates to calibrate the model with.
:type candidates: Optional[Union[List[str], str]]
- `strategy` - The strategy to calibrate the model with. default to 1
:type strategy: int

#### Signature

```python
def calibrate(
    self,
    template: Union[str, Template],
    voter: Optional[Voter] = None,
    null_tokens: Optional[Union[List[str], str]] = None,
    candidates: Optional[Union[List[str], str]] = None,
    strategy: int = 1,
):
    ...
```

### Client().chat

[Show source in client.py:377](../../../alfred/client/client.py#L377)

Chat with the model APIs.
Currently, Alfred supports Chat APIs from Anthropic and OpenAI

#### Arguments

- `log_save_path` - The file to save the chat logs.
:type log_save_path: Optional[str]

#### Signature

```python
def chat(self, log_save_path: Optional[str] = None, **kwargs: Any):
    ...
```

### Client().encode

[Show source in client.py:351](../../../alfred/client/client.py#L351)

embed() function to embed the queries.

#### Arguments

- `queries` - The queries to embed.
:type queries: Union[str, List[str]]
- `reduction` - The reduction method to use on word embeddings. default to 'mean'
                  choose from ['mean', 'sum', 'none']
:type reduction: str

#### Signature

```python
def encode(
    self, queries: Union[str, List[str]], reduction: str = "mean"
) -> Union[torch.Tensor, List[torch.Tensor]]:
    ...
```

### Client().generate

[Show source in client.py:219](../../../alfred/client/client.py#L219)

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

[Show source in client.py:197](../../../alfred/client/client.py#L197)

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

[Show source in client.py:177](../../../alfred/client/client.py#L177)

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

[Show source in client.py:236](../../../alfred/client/client.py#L236)

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


