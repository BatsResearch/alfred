# Model

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Fm](./index.md#fm) / Model

> Auto-generated documentation for [alfred.fm.model](../../../alfred/fm/model.py) module.

- [Model](#model)
  - [APIAccessFoundationModel](#apiaccessfoundationmodel)
  - [FoundationModel](#foundationmodel)
    - [FoundationModel().__call__](#foundationmodel()__call__)
    - [FoundationModel()._encode_batch](#foundationmodel()_encode_batch)
    - [FoundationModel()._generate_batch](#foundationmodel()_generate_batch)
    - [FoundationModel()._score_batch](#foundationmodel()_score_batch)
    - [FoundationModel().encode](#foundationmodel()encode)
    - [FoundationModel().forward](#foundationmodel()forward)
    - [FoundationModel().generate](#foundationmodel()generate)
    - [FoundationModel().run](#foundationmodel()run)
    - [FoundationModel().score](#foundationmodel()score)
  - [LocalAccessFoundationModel](#localaccessfoundationmodel)

## APIAccessFoundationModel

[Show source in model.py:378](../../../alfred/fm/model.py#L378)

#### Signature

```python
class APIAccessFoundationModel(FoundationModel):
    def __init__(self, model_string: str, cfg: Optional[Dict] = None): ...
```

#### See also

- [FoundationModel](#foundationmodel)



## FoundationModel

[Show source in model.py:19](../../../alfred/fm/model.py#L19)

Generic interface for foundation model class

#### Signature

```python
class FoundationModel(abc.ABC): ...
```

### FoundationModel().__call__

[Show source in model.py:356](../../../alfred/fm/model.py#L356)

This function returns the output of the run function when the
 model is called as a function. It can be used as model(queries),
 which is equivalent to model.run(queries).

#### Arguments

- `queries` - A single query or a list of queries
:type queries: Union[Query, str, dict, List[Query], List[str], List[dict]]
- `kwargs` - Additional arguments to pass to the foundation model
:type kwargs: Any

#### Returns

A single response or a list of responses
Type: *Union[str, Response, List[Response]]*

#### Signature

```python
def __call__(
    self,
    queries: Union[
        Query, str, Tuple[str, str], Tuple[Image.Image, str], List[Query], List[str]
    ],
    **kwargs: Any
) -> Union[str, Response, List[Response]]: ...
```

### FoundationModel()._encode_batch

[Show source in model.py:62](../../../alfred/fm/model.py#L62)

For encoding queries into embeddings.

#### Arguments

- `batch_instance` - A batch of query objects or raw query content (e.g. string or embedding arrays)
:type batch_instance: Union[List[RankedQuery], List[str]]

#### Returns

A list of responses
:rtype List[Response]

#### Signature

```python
def _encode_batch(
    self, batch_instance: Union[List[str]], **kwargs: Any
) -> List[torch.Tensor]: ...
```

### FoundationModel()._generate_batch

[Show source in model.py:24](../../../alfred/fm/model.py#L24)

For completing / generating given a batch of queries
Run a batch of queries through the foundation model

#### Arguments

- `batch_instance` - A batch of query objects or raw query content (e.g. string or embedding arrays)
:type batch_instance: Union[List[CompletionQuery], List[str]]
- `kwargs` - Additional arguments to pass to the foundation model
:type batch_instance: Union[List[CompletionQuery], List[str]]

#### Returns

A list of responses
:rtype List[Response]

#### Signature

```python
def _generate_batch(
    self, batch_instance: Union[List[str]], **kwargs
) -> List[Response]: ...
```

### FoundationModel()._score_batch

[Show source in model.py:44](../../../alfred/fm/model.py#L44)

For scoring / ranking candidate queries.
Run a batch of queries through the foundation model.

#### Arguments

- `batch_instance` - A batch of query objects or raw query content (e.g. string or embedding arrays)
:type batch_instance: Union[List[RankedQuery], List[str]]

#### Returns

A list of responses
:rtype List[Response]

#### Signature

```python
def _score_batch(
    self, batch_instance: Union[List[Tuple[str, str]], List[str]], **kwargs
) -> List[Response]: ...
```

### FoundationModel().encode

[Show source in model.py:273](../../../alfred/fm/model.py#L273)

This function is a wrapper around the forward function

#### Arguments

- `queries` - A list of Query or raw query content (as string)
:type queries: Union[List[Query], List[str]]
- `batch_policy` - The batching policy to use. Can be either 'dynamic' or 'static'
:type batch_policy: str
- `batch_size` - The batch size to use for static batching or maximum batch size for dynamic batching
:type batch_size: int
- `reduction` - The reduction method to use for the encoded queries. Can be either 'mean' or 'concat'
:type reduction: str

#### Returns

A list of encoded queries
Type: *List[torch.Tensor]*

#### Signature

```python
def encode(
    self,
    queries: Union[List[Query], List[str]],
    batch_policy: str = "dynamic",
    batch_size: int = 1024,
    reduction: str = "mean",
    **kwargs: Any
) -> List[torch.Tensor]: ...
```

### FoundationModel().forward

[Show source in model.py:79](../../../alfred/fm/model.py#L79)

This function is the main entry point for running queries through the foundation model.
It accepts raw query content and automatically converts it into query objects.
The function then determines whether to run the queries through the _generate_batch
or _score_batch method based on the type of queries. Finally, the function processes
the queries using one of two batching policies (dynamic, static) and passes them
through the foundation model.

#### Arguments

- `queries` - A list of queries
:type queries: Union[List[Query], List[str], List[Tuple[str, str]]]
- `batch_policy` - The batching policy to use. Can be either 'dynamic' or 'static'
:type batch_policy: str
- `batch_size` - The batch size to use for static batching or maximum batch size for dynamic batching
:type batch_size: int
- `mode` - LLM inference mode, choose from ['generate', 'score', 'encode']
:type mode: str
- `pretokenize` - Whether to tokenize the queries while batching
:type pretokenize: bool
- `kwargs` - Additional arguments to pass to the foundation model
:type kwargs: Any

#### Returns

A list of responses
Type: *Union[List[CompletionResponse], List[RankedResponse], List[OrderedDict], List[torch.Tensor]]*

#### Signature

```python
def forward(
    self,
    queries: Union[List[Query], List[str], List[Tuple[str, str]]],
    batch_policy: str = "dynamic",
    batch_size: int = 1024,
    mode: str = "generate",
    pretokenize: bool = True,
    **kwargs
) -> Union[
    List[CompletionResponse], List[RankedResponse], List[OrderedDict], List[torch.Tensor]
]: ...
```

### FoundationModel().generate

[Show source in model.py:222](../../../alfred/fm/model.py#L222)

This function is a wrapper around the forward function for running
CompletionQuery objects through the foundation model. It returns a list
of CompletionResponse objects.

#### Arguments

- `queries` - A list of CompletionQuery or raw query content (as string)
:type queries: Union[List[CompletionQuery], List[str]]
- `batch_policy` - The batching policy to use. Can be either 'dynamic' or 'static'
:type batch_policy: str
- `batch_size` - The batch size to use for static batching or maximum batch size for dynamic batching
:type batch_size: int
- `kwargs` - Additional arguments to pass to the foundation model
:type kwargs: Any

#### Returns

A list of CompletionResponse
Type: *List[CompletionResponse]*

#### Signature

```python
def generate(
    self,
    queries: Union[List[CompletionQuery], List[str]],
    batch_policy: str = "dynamic",
    batch_size: int = 1024,
    **kwargs
) -> List[CompletionResponse]: ...
```

### FoundationModel().run

[Show source in model.py:304](../../../alfred/fm/model.py#L304)

This function is the main entry point for users to run queries through the foundation model.
It accepts raw query content and automatically converts it into query objects.
The function then processes the queries and returns the responses in the appropriate format.
For single instance queries, a single response object is returned.

#### Arguments

- `queries` - A single query or a list of queries
:type queries: Union[Query, str, Tuple[str, str], List[Query], List[str]]
- `kwargs` - Additional arguments to pass to the foundation model
:type kwargs: Any

#### Returns

A single response or a list of responses
Type: *Union[str, Response, List[Response]]*

#### Signature

```python
def run(
    self,
    queries: Union[
        Query, str, Tuple[str, str], Tuple[Image.Image, str], List[Query], List[str]
    ],
    **kwargs: Any
) -> Union[str, Response, List[Response]]: ...
```

### FoundationModel().score

[Show source in model.py:247](../../../alfred/fm/model.py#L247)

This function is a wrapper around the forward function
for running RankedQuery objects through the foundation model.
It returns a list of RankedResponse objects.

#### Arguments

- `queries` - A list of RankedQuery
:type queries: List[RankedQuery]
- `batch_policy` - The batching policy to use. Can be either 'dynamic' or 'static'
:type batch_policy: str
- `batch_size` - The batch size to use for static batching or maximum batch size for dynamic batching
:type batch_size: int
- `kwargs` - Additional arguments to pass to the foundation model
:type kwargs: Any

#### Returns

A list of RankedResponse
Type: *List[RankedResponse]*

#### Signature

```python
def score(
    self,
    queries: List[RankedQuery],
    batch_policy: str = "dynamic",
    batch_size: int = 64,
    **kwargs: Any
) -> List[RankedResponse]: ...
```



## LocalAccessFoundationModel

[Show source in model.py:393](../../../alfred/fm/model.py#L393)

#### Signature

```python
class LocalAccessFoundationModel(FoundationModel):
    def __init__(self, model_string: str, local_path: Optional[str] = None): ...
```

#### See also

- [FoundationModel](#foundationmodel)