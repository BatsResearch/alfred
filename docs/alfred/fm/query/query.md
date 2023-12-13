# Query

[Alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Fm](../index.md#fm) /
[Query](./index.md#query) /
Query

> Auto-generated documentation for [alfred.fm.query.query](../../../../alfred/fm/query/query.py) module.

- [Query](#query)
  - [Query](#query-1)
    - [Query.compose](#querycompose)
    - [Query().load](#query()load)
    - [Query().serialize](#query()serialize)

## Query

[Show source in query.py:7](../../../../alfred/fm/query/query.py#L7)

Abstract base class for a single query for foundation model interfaces

#### Signature

```python
class Query(abc.ABC):
    ...
```

### Query.compose

[Show source in query.py:12](../../../../alfred/fm/query/query.py#L12)

Compose two strings or lists or tensors or numpy arrays

#### Arguments

- `a` - operand a
:type a: Union[str, List, Tuple, np.ndarray, torch.Tensor]
- `b` - operand b
:type b: Union[str, List, Tuple, np.ndarray, torch.Tensor]
- `strategy` - composition strategy, defaults to None
:type strategy: str, optional

#### Returns

composition of a and b

#### Signature

```python
@staticmethod
def compose(a, b, strategy=None):
    ...
```

### Query().load

[Show source in query.py:50](../../../../alfred/fm/query/query.py#L50)

#### Signature

```python
@abc.abstractmethod
def load(self):
    ...
```

### Query().serialize

[Show source in query.py:41](../../../../alfred/fm/query/query.py#L41)

Serialize query

#### Returns

serialized query
Type: *str*

#### Signature

```python
def serialize(self) -> str:
    ...
```