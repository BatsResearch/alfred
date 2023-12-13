# Dummy

[Alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Client](../index.md#client) /
[Cache](./index.md#cache) /
Dummy

> Auto-generated documentation for [alfred.client.cache.dummy](../../../../alfred/client/cache/dummy.py) module.

- [Dummy](#dummy)
  - [DummyCache](#dummycache)
    - [DummyCache().read](#dummycache()read)
    - [DummyCache().read_by_metadata](#dummycache()read_by_metadata)
    - [DummyCache().read_by_prompt](#dummycache()read_by_prompt)
    - [DummyCache().read_by_prompt_and_metadata](#dummycache()read_by_prompt_and_metadata)
    - [DummyCache().save](#dummycache()save)
    - [DummyCache().to_pandas](#dummycache()to_pandas)
    - [DummyCache().write](#dummycache()write)

## DummyCache

[Show source in dummy.py:6](../../../../alfred/client/cache/dummy.py#L6)

A simple in-memory cache implementation. (for testing)

This class is intended as a dummy implementation of the `Cache` interface for testing purposes. It stores cache entries in a dictionary in memory and does not persist them to disk.

#### Signature

```python
class DummyCache(Cache):
    def __init__(self):
        ...
```

#### See also

- [Cache](./cache.md#cache)

### DummyCache().read

[Show source in dummy.py:19](../../../../alfred/client/cache/dummy.py#L19)

Read the record from the cache by serialized prompt and metadata

#### Arguments

- `prompt` - The serialized prompt to search for
:type prompt: str
- `metadata` - (optional) The metadata to search for, defaults to None
:type metadata: str

#### Returns

The response from the cache
Type: *List*

#### Signature

```python
def read(self, prompt: str, metadata: Optional[str] = None) -> List:
    ...
```

### DummyCache().read_by_metadata

[Show source in dummy.py:75](../../../../alfred/client/cache/dummy.py#L75)

Read a dummy empty list

#### Arguments

- `metadata` - (optional) The metadata to search for, defaults to None
:type metadata: str

#### Returns

An empty list
Type: *list*

#### Signature

```python
def read_by_metadata(self, metadata: Optional[str] = None) -> List:
    ...
```

### DummyCache().read_by_prompt

[Show source in dummy.py:51](../../../../alfred/client/cache/dummy.py#L51)

Read a record from the cache by serialized prompt

#### Arguments

- `prompt` - The serialized prompt to search for
:type prompt: str

#### Returns

The response from the cache
Type: *List*

#### Signature

```python
def read_by_prompt(self, prompt: str) -> List:
    ...
```

### DummyCache().read_by_prompt_and_metadata

[Show source in dummy.py:62](../../../../alfred/client/cache/dummy.py#L62)

Read a record from the cache by serialized prompt and metadata

#### Arguments

- `prompt` - The serialized prompt to search for
:type prompt: str
- `metadata` - The metadata to search for
:type metadata: str

#### Returns

The response from the cache
Type: *List*

#### Signature

```python
def read_by_prompt_and_metadata(self, prompt: str, metadata: str) -> List:
    ...
```

### DummyCache().save

[Show source in dummy.py:86](../../../../alfred/client/cache/dummy.py#L86)

Does not save but return the path argrument

#### Arguments

- `path` - The path to save the cache to
:type path: str

#### Returns

The path argument
Type: *str*

#### Signature

```python
def save(self, path: str) -> str:
    ...
```

### DummyCache().to_pandas

[Show source in dummy.py:97](../../../../alfred/client/cache/dummy.py#L97)

Does nothing. Return None.

#### Returns

None
Type: *None*

#### Signature

```python
def to_pandas(self) -> None:
    ...
```

### DummyCache().write

[Show source in dummy.py:38](../../../../alfred/client/cache/dummy.py#L38)

Write a prompt-response pair to the cache

#### Arguments

- `prompt` - The serialized prompt to write
:type prompt: str
- `response` - The serialized response to write
:type response: str
- `metadata` - (optional) The metadata to write, defaults to None
:type metadata: str

#### Signature

```python
def write(self, prompt: str, response: str, metadata: Optional[str] = None):
    ...
```