# CompletionQuery

[Alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Fm](../index.md#fm) /
[Query](./index.md#query) /
CompletionQuery

> Auto-generated documentation for [alfred.fm.query.completion_query](../../../../alfred/fm/query/completion_query.py) module.

- [CompletionQuery](#completionquery)
  - [CompletionQuery](#completionquery-1)
    - [CompletionQuery().__add__](#completionquery()__add__)
    - [CompletionQuery().__eq__](#completionquery()__eq__)
    - [CompletionQuery().__hash__](#completionquery()__hash__)
    - [CompletionQuery().__len__](#completionquery()__len__)
    - [CompletionQuery().__repr__](#completionquery()__repr__)
    - [CompletionQuery().__str__](#completionquery()__str__)
    - [CompletionQuery().load](#completionquery()load)
    - [CompletionQuery().prompt](#completionquery()prompt)

## CompletionQuery

[Show source in completion_query.py:9](../../../../alfred/fm/query/completion_query.py#L9)

A completion query class.

This is the generic query for any alfred.fm model.
It mainly contains the prompt, which is the input to the model.

In the case of a multimodal completion query, it may take the form of a tuple (e.g. (PIL.Image, str))

This class represents a query for completion of a given prompt.
It is initialized with a prompt, which can be a string, NumPy array,
list, tuple, or PyTorch tensor.

#### Signature

```python
class CompletionQuery(Query):
    def __init__(self, prompt: Union[str, np.ndarray, List, Tuple, torch.Tensor]):
        ...
```

### CompletionQuery().__add__

[Show source in completion_query.py:64](../../../../alfred/fm/query/completion_query.py#L64)

concatenates the two queries

#### Signature

```python
def __add__(self, other):
    ...
```

### CompletionQuery().__eq__

[Show source in completion_query.py:52](../../../../alfred/fm/query/completion_query.py#L52)

returns whether the two queries are equal

#### Signature

```python
def __eq__(self, other):
    ...
```

### CompletionQuery().__hash__

[Show source in completion_query.py:56](../../../../alfred/fm/query/completion_query.py#L56)

returns the hash of the query

#### Signature

```python
def __hash__(self):
    ...
```

### CompletionQuery().__len__

[Show source in completion_query.py:60](../../../../alfred/fm/query/completion_query.py#L60)

returns the length of the prompt

#### Signature

```python
def __len__(self):
    ...
```

### CompletionQuery().__repr__

[Show source in completion_query.py:44](../../../../alfred/fm/query/completion_query.py#L44)

returns the string representation of the query

#### Signature

```python
def __repr__(self):
    ...
```

### CompletionQuery().__str__

[Show source in completion_query.py:48](../../../../alfred/fm/query/completion_query.py#L48)

returns the string representation of the query

#### Signature

```python
def __str__(self):
    ...
```

### CompletionQuery().load

[Show source in completion_query.py:40](../../../../alfred/fm/query/completion_query.py#L40)

loads the prompt, this will be convenient for batching the queries

#### Signature

```python
def load(self):
    ...
```

### CompletionQuery().prompt

[Show source in completion_query.py:35](../../../../alfred/fm/query/completion_query.py#L35)

returns the raw prompt content

#### Signature

```python
@property
def prompt(self):
    ...
```