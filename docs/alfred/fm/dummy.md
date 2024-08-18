# Dummy

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Fm](./index.md#fm) / Dummy

> Auto-generated documentation for [alfred.fm.dummy](../../../alfred/fm/dummy.py) module.

- [Dummy](#dummy)
  - [DummyModel](#dummymodel)
    - [DummyModel()._encode_batch](#dummymodel()_encode_batch)
    - [DummyModel()._generate_batch](#dummymodel()_generate_batch)
    - [DummyModel()._score_batch](#dummymodel()_score_batch)

## DummyModel

[Show source in dummy.py:13](../../../alfred/fm/dummy.py#L13)

A dummy model that returns the input as the output.

This model implements a dummy model that returns the
input as the output for both completion and outputs a raw logit of -1 for scoring.

#### Signature

```python
class DummyModel(LocalAccessFoundationModel):
    def __init__(self, model: Optional[str] = None): ...
```

### DummyModel()._encode_batch

[Show source in dummy.py:54](../../../alfred/fm/dummy.py#L54)

Encode a batch of queries.

This function returns a zero vector of size 512 for all queries.

#### Arguments

- `batch_instance` - A list of queries.
:type batch_instance: List[Query]
- `reduction` - The reduction method to use.
:type reduction: str
- `kwargs` - Additional keyword arguments.

#### Returns

A list of `torch.Tensor` objects with the same prediction content as the input.
Type: *List[torch.Tensor]*

#### Signature

```python
def _encode_batch(
    self, batch_instance: Union[List[Query], List[str]], **kwargs: Any
) -> List[torch.Tensor]: ...
```

### DummyModel()._generate_batch

[Show source in dummy.py:31](../../../alfred/fm/dummy.py#L31)

Generate completions for a batch of queries.

This function returns the same output as the input queries but returns a `Response` object.

#### Arguments

- `batch_instance` - A list of queries.
:type batch_instance: List[Query]
- `kwargs` - Additional keyword arguments.

#### Returns

A list of `Response` objects with the same prediction content as the input.
Type: *List[Response]*

#### Signature

```python
def _generate_batch(
    self, batch_instance: Union[List[Query], List[str]], **kwargs: Any
) -> List[Response]: ...
```

### DummyModel()._score_batch

[Show source in dummy.py:74](../../../alfred/fm/dummy.py#L74)

Score a batch of queries.

This function returns a logit score of -1 for all candidates.

#### Arguments

- `batch_instance` - A list of queries.
:type batch_instance: List[Query]
- `kwargs` - Additional keyword arguments.
:type kwargs: Any

#### Returns

A list of logit scores in the form of a dictionary.
Type: *List[dict]*

#### Signature

```python
def _score_batch(
    self, batch_instance: Union[List[Query], List[str]], **kwargs
) -> List[dict]: ...
```