# CompletionResponse

[Alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Fm](../index.md#fm) /
[Response](./index.md#response) /
CompletionResponse

> Auto-generated documentation for [alfred.fm.response.completion_response](../../../../alfred/fm/response/completion_response.py) module.

- [CompletionResponse](#completionresponse)
  - [CompletionResponse](#completionresponse-1)
    - [CompletionResponse().__eq__](#completionresponse()__eq__)
    - [CompletionResponse().embedding](#completionresponse()embedding)
    - [CompletionResponse().prediction](#completionresponse()prediction)
    - [CompletionResponse().score](#completionresponse()score)

## CompletionResponse

[Show source in completion_response.py:9](../../../../alfred/fm/response/completion_response.py#L9)

A response class for language model completions.

This class represents a completion response from a language model,
which includes the predicted completion string, a score indicating
the confidence of the prediction, and an optional embedding output.

#### Signature

```python
class CompletionResponse(Response):
    def __init__(
        self,
        prediction: str = None,
        score: Optional[float] = None,
        embedding: Optional[Union[torch.Tensor, np.ndarray]] = None,
    ):
        ...
```

### CompletionResponse().__eq__

[Show source in completion_response.py:69](../../../../alfred/fm/response/completion_response.py#L69)

Determines if two CompletionResponse objects are equal.

Two CompletionResponse objects are considered equal if their prediction,
score, and embedding attributes are equal. If any of these attributes are not set,
they are considered equal if both are None.

#### Arguments

- `other` - The other CompletionResponse object to compare to.
:type other: CompletionResponse

#### Returns

True if the two CompletionResponse objects are equal, False otherwise.
Type: *bool*

#### Signature

```python
def __eq__(self, other):
    ...
```

### CompletionResponse().embedding

[Show source in completion_response.py:59](../../../../alfred/fm/response/completion_response.py#L59)

Returns the embedding of the completion prediction.

#### Returns

The embedding of the completion prediction.
Type: *Union[torch.Tensor, np.ndarray]*

#### Signature

```python
@property
def embedding(self) -> Union[torch.Tensor, np.ndarray]:
    ...
```

### CompletionResponse().prediction

[Show source in completion_response.py:39](../../../../alfred/fm/response/completion_response.py#L39)

Returns the predicted completion string.

#### Returns

The predicted completion string.
Type: *str*

#### Signature

```python
@property
def prediction(self) -> str:
    ...
```

### CompletionResponse().score

[Show source in completion_response.py:49](../../../../alfred/fm/response/completion_response.py#L49)

Returns the score of the completion prediction.

#### Returns

The score of the completion prediction.
Type: *float*

#### Signature

```python
@property
def score(self) -> Dict:
    ...
```


