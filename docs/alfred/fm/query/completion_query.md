# CompletionQuery

[alfred Index](../../../README.md#alfred-index) /
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

[Show source in completion_query.py:61](../../../../alfred/fm/query/completion_query.py#L61)

concatenates the two queries

#### Signature

```python
def __add__(self, other):
    ...
```

### CompletionQuery().__eq__

[Show source in completion_query.py:49](../../../../alfred/fm/query/completion_query.py#L49)

returns whether the two queries are equal

#### Signature

```python
def __eq__(self, other):
    ...
```

### CompletionQuery().__hash__

[Show source in completion_query.py:53](../../../../alfred/fm/query/completion_query.py#L53)

returns the hash of the query

#### Signature

```python
def __hash__(self):
    ...
```

### CompletionQuery().__len__

[Show source in completion_query.py:57](../../../../alfred/fm/query/completion_query.py#L57)

returns the length of the prompt

#### Signature

```python
def __len__(self):
    ...
```

### CompletionQuery().__repr__

[Show source in completion_query.py:41](../../../../alfred/fm/query/completion_query.py#L41)

returns the string representation of the query

#### Signature

```python
def __repr__(self):
    ...
```

### CompletionQuery().__str__

[Show source in completion_query.py:45](../../../../alfred/fm/query/completion_query.py#L45)

returns the string representation of the query

#### Signature

```python
def __str__(self):
    ...
```

### CompletionQuery().load

[Show source in completion_query.py:37](../../../../alfred/fm/query/completion_query.py#L37)

loads the prompt, this will be convenient for batching the queries

#### Signature

```python
def load(self):
    ...
```

### CompletionQuery().prompt

[Show source in completion_query.py:32](../../../../alfred/fm/query/completion_query.py#L32)

returns the raw prompt content

#### Signature

```python
@property
def prompt(self):
    ...
```


