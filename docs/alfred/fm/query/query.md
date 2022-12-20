# Query

[alfred Index](../../../README.md#alfred-index) /
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
- `b` - operand b

#### Returns

composition of a and b

#### Signature

```python
@staticmethod
def compose(a, b, strategy=None):
    ...
```

### Query().load

[Show source in query.py:46](../../../../alfred/fm/query/query.py#L46)

#### Signature

```python
@abc.abstractmethod
def load(self):
    ...
```

### Query().serialize

[Show source in query.py:37](../../../../alfred/fm/query/query.py#L37)

Serialize query

#### Returns

serialized query
Type: *str*

#### Signature

```python
def serialize(self) -> str:
    ...
```


