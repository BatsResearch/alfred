# Cache

[Alfred Index](../../../README.md#alfred-index) / [Alfred](../../index.md#alfred) / [Client](../index.md#client) / [Cache](./index.md#cache) / Cache

> Auto-generated documentation for [alfred.client.cache.cache](../../../../alfred/client/cache/cache.py) module.

- [Cache](#cache)
  - [Cache](#cache-1)
    - [Cache().cached_query](#cache()cached_query)
    - [Cache().load](#cache()load)
    - [Cache().read](#cache()read)
    - [Cache().read_batch](#cache()read_batch)
    - [Cache().read_by_metadata](#cache()read_by_metadata)
    - [Cache().read_by_prompt](#cache()read_by_prompt)
    - [Cache().read_by_prompt_and_metadata](#cache()read_by_prompt_and_metadata)
    - [Cache().read_by_prompts_and_metadata](#cache()read_by_prompts_and_metadata)
    - [Cache().save](#cache()save)
    - [Cache().to_pandas](#cache()to_pandas)
    - [Cache().write](#cache()write)
    - [Cache().write_batch](#cache()write_batch)
  - [from_metadata_string](#from_metadata_string)
  - [to_metadata_string](#to_metadata_string)

## Cache

[Show source in cache.py:38](../../../../alfred/client/cache/cache.py#L38)

Generic Interface for caching operation that wraps certain cache implementation

Currently supported cache implementations:
    - DummyCache: Simple Dict-based
    - SqliteCache: Sqlite3 - based cache
TODO:
    - RedisCache: Redis - based cache

#### Signature

```python
class Cache(abc.ABC): ...
```

### Cache().cached_query

[Show source in cache.py:213](../../../../alfred/client/cache/cache.py#L213)

Decorator function for model queries, fetch from cache db if exist else write into cache_db

#### Arguments

- `model_run` - Model run function
:type model_run: Callable

#### Returns

Decorated function
Type: *Callable*

#### Signature

```python
def cached_query(self, model_run: Callable) -> Callable: ...
```

### Cache().load

[Show source in cache.py:189](../../../../alfred/client/cache/cache.py#L189)

Load the cache from disk to the cache object

#### Arguments

- `path` - Path to the cache file
:type path: str

#### Signature

```python
@abc.abstractmethod
def load(self, path: str): ...
```

### Cache().read

[Show source in cache.py:49](../../../../alfred/client/cache/cache.py#L49)

Read from cache by prompt and metadata

#### Arguments

- `prompt` - Prompt string
:type prompt: str
- `metadata` - (optional) Metadata string
:type metadata: str

#### Returns

List of responses
Type: *list*

#### Signature

```python
@abc.abstractmethod
def read(self, prompt: str, metadata: Optional[str] = None) -> list: ...
```

### Cache().read_batch

[Show source in cache.py:65](../../../../alfred/client/cache/cache.py#L65)

Read a value from the cache by list of serialized prompts and metadata

#### Arguments

- `prompts` - List of serialized prompts
:type prompts: list
- `metadata` - (optional) Metadata string
:type metadata: str

#### Returns

List of serialized responses
Type: *list*

#### Signature

```python
@abc.abstractmethod
def read_batch(
    self, prompts: List[str], metadata: Optional[str] = None
) -> List[str]: ...
```

### Cache().read_by_metadata

[Show source in cache.py:163](../../../../alfred/client/cache/cache.py#L163)

Read the record from the cache by key

#### Arguments

- `metadata` - Metadata string
:type metadata: str

#### Returns

List of records
Type: *list*

#### Signature

```python
@abc.abstractmethod
def read_by_metadata(self, metadata: str) -> List: ...
```

### Cache().read_by_prompt

[Show source in cache.py:117](../../../../alfred/client/cache/cache.py#L117)

Read the record from the cache via serialized prompt

#### Arguments

- `prompt` - Serialized prompt
:type prompt: str

#### Returns

List of records
Type: *list*

#### Signature

```python
@abc.abstractmethod
def read_by_prompt(self, prompt: str) -> List: ...
```

### Cache().read_by_prompt_and_metadata

[Show source in cache.py:131](../../../../alfred/client/cache/cache.py#L131)

Read the record from the cache via serialized prompt and metadata string

#### Arguments

- `prompt` - Serialized prompt
:type prompt: str
- `metadata` - Metadata string
:type metadata: str

#### Returns

List of records
Type: *list*

#### Signature

```python
@abc.abstractmethod
def read_by_prompt_and_metadata(self, prompt: str, metadata: str) -> List: ...
```

### Cache().read_by_prompts_and_metadata

[Show source in cache.py:147](../../../../alfred/client/cache/cache.py#L147)

Read the record from the cache via serialized prompts and metadata string

#### Arguments

- `prompts` - List of serialized prompts
:type prompts: List[str]
- `metadata` - Metadata string
:type metadata: str

#### Returns

List of records
Type: *List*

#### Signature

```python
@abc.abstractmethod
def read_by_prompts_and_metadata(self, prompts: List[str], metadata: str) -> List: ...
```

### Cache().save

[Show source in cache.py:177](../../../../alfred/client/cache/cache.py#L177)

Save the cache to disk

#### Arguments

- `path` - Path to save the cache
:type path: str

#### Signature

```python
@abc.abstractmethod
def save(self, path: str): ...
```

### Cache().to_pandas

[Show source in cache.py:201](../../../../alfred/client/cache/cache.py#L201)

Return the cache db as a pandas dataframe

#### Returns

Pandas dataframe
Type: *pd.DataFrame*

#### Signature

```python
@abc.abstractmethod
def to_pandas(self) -> pd.DataFrame: ...
```

### Cache().write

[Show source in cache.py:83](../../../../alfred/client/cache/cache.py#L83)

Write a value to the cache by serialized prompt, serialized response and metadata

#### Arguments

- `prompt` - Serialized prompt
:type prompt: str
- `response` - Serialized response
:type response: str
- `metadata` - (optional) Metadata string
:type metadata: str

#### Signature

```python
@abc.abstractmethod
def write(self, prompt: str, response: str, metadata: Optional[str] = None): ...
```

### Cache().write_batch

[Show source in cache.py:99](../../../../alfred/client/cache/cache.py#L99)

Write a value to the cache by serialized prompts, serialized responses and metadata in batch

#### Arguments

- `prompts` - List of serialized prompts
:type prompts: List[str]
- `response` - List of serialized responses
:type response: List[str]
- `metadata` - (optional) Metadata string
:type metadata: str

#### Signature

```python
@abc.abstractmethod
def write_batch(
    self, prompts: List[str], response: List[str], metadata: Optional[str] = None
): ...
```



## from_metadata_string

[Show source in cache.py:26](../../../../alfred/client/cache/cache.py#L26)

Convert a string of metadata to a dictionary

#### Arguments

- `metadata_string` - String representation of the metadata from the cache
:type metadata_string: str

#### Returns

Dictionary of metadata
Type: *dict*

#### Signature

```python
def from_metadata_string(metadata_string: str) -> Dict: ...
```



## to_metadata_string

[Show source in cache.py:14](../../../../alfred/client/cache/cache.py#L14)

Convert a dictionary of metadata to a string for storage in the cache

#### Arguments

- `kwargs` - Dictionary of metadata
:type kwargs: dict

#### Returns

String representation of the metadata
Type: *str*

#### Signature

```python
def to_metadata_string(**kwargs: Any) -> str: ...
```