# Model

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Fm](./index.md#fm) /
Model

> Auto-generated documentation for [alfred.fm.model](../../../alfred/fm/model.py) module.

- [Model](#model)
  - [APIAccessFoundationModel](#apiaccessfoundationmodel)
  - [FoundationModel](#foundationmodel)
    - [FoundationModel().__call__](#foundationmodel()__call__)
    - [FoundationModel().forward](#foundationmodel()forward)
    - [FoundationModel().generate](#foundationmodel()generate)
    - [FoundationModel().run](#foundationmodel()run)
    - [FoundationModel().score](#foundationmodel()score)
  - [LocalAccessFoundationModel](#localaccessfoundationmodel)

## APIAccessFoundationModel

[Show source in model.py:250](../../../alfred/fm/model.py#L250)

#### Signature

```python
class APIAccessFoundationModel(FoundationModel):
    def __init__(self, model_string: str, cfg: Optional[Dict] = None):
        ...
```

#### See also

- [FoundationModel](#foundationmodel)



## FoundationModel

[Show source in model.py:18](../../../alfred/fm/model.py#L18)

Generic interface for foundation model class

#### Signature

```python
class FoundationModel(abc.ABC):
    ...
```

### FoundationModel().__call__

[Show source in model.py:230](../../../alfred/fm/model.py#L230)

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
    queries: Union[Query, str, Tuple[str, str], List[Query], List[str]],
    **kwargs: Any
) -> Union[str, Response, List[Response]]:
    ...
```

### FoundationModel().forward

[Show source in model.py:59](../../../alfred/fm/model.py#L59)

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
- [FoundationModel().score](#foundationmodelscore) - Whether to run the queries through the _score_batch() method
:type score: bool
- `kwargs` - Additional arguments to pass to the foundation model
:type kwargs: Any

#### Returns

A list of responses
Type: *Union[List[CompletionResponse], List[RankedResponse], List[OrderedDict]]*

#### Signature

```python
def forward(
    self,
    queries: Union[List[Query], List[str], List[Tuple[str, str]]],
    batch_policy: str = "dynamic",
    batch_size: int = 1024,
    score: bool = False,
    **kwargs
) -> Union[List[CompletionResponse], List[RankedResponse], List[OrderedDict]]:
    ...
```

### FoundationModel().generate

[Show source in model.py:141](../../../alfred/fm/model.py#L141)

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
) -> List[CompletionResponse]:
    ...
```

### FoundationModel().run

[Show source in model.py:195](../../../alfred/fm/model.py#L195)

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
    queries: Union[Query, str, Tuple[str, str], List[Query], List[str]],
    **kwargs: Any
) -> Union[str, Response, List[Response]]:
    ...
```

### FoundationModel().score

[Show source in model.py:165](../../../alfred/fm/model.py#L165)

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
    batch_size: int = 1024,
    **kwargs: Any
) -> List[RankedResponse]:
    ...
```



## LocalAccessFoundationModel

[Show source in model.py:267](../../../alfred/fm/model.py#L267)

#### Signature

```python
class LocalAccessFoundationModel(FoundationModel):
    def __init__(self, model_string: str, local_path: Optional[str] = None):
        ...
```

#### See also

- [FoundationModel](#foundationmodel)


