# RankedResponse

[Alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Fm](../index.md#fm) /
[Response](./index.md#response) /
RankedResponse

> Auto-generated documentation for [alfred.fm.response.ranked_response](../../../../alfred/fm/response/ranked_response.py) module.

- [RankedResponse](#rankedresponse)
  - [RankedResponse](#rankedresponse-1)
    - [RankedResponse().__eq__](#rankedresponse()__eq__)
    - [RankedResponse().embeddings](#rankedresponse()embeddings)
    - [RankedResponse().logits](#rankedresponse()logits)
    - [RankedResponse().prediction](#rankedresponse()prediction)
    - [RankedResponse().scores](#rankedresponse()scores)

## RankedResponse

[Show source in ranked_response.py:9](../../../../alfred/fm/response/ranked_response.py#L9)

A subclass of `Response` that represents a language model response for scoring/ranking.

#### Signature

```python
class RankedResponse(Response):
    def __init__(
        self,
        prediction: str = None,
        scores: Dict = None,
        logits: Optional[Union[torch.Tensor, np.ndarray]] = None,
        embeddings: Optional[Union[torch.Tensor, np.ndarray]] = None,
    ):
        ...
```

### RankedResponse().__eq__

[Show source in ranked_response.py:80](../../../../alfred/fm/response/ranked_response.py#L80)

Determines if two RankedResponse objects are equal.

Two RankedResponse objects are considered equal if their prediction,
score, and embedding attributes are equal. If any of these attributes are not set,
they are considered equal if both are None.

#### Arguments

- `other` - The other RankedResponse object to compare to.
:type other: RankedResponse

#### Returns

True if the two RankedResponse objects are equal, False otherwise.
Type: *bool*

#### Signature

```python
def __eq__(self, other):
    ...
```

### RankedResponse().embeddings

[Show source in ranked_response.py:70](../../../../alfred/fm/response/ranked_response.py#L70)

Get the embedding output by the language model.

#### Returns

The embedding output by the language model
Type: *Union[torch.Tensor, np.ndarray]*

#### Signature

```python
@property
def embeddings(self) -> Union[torch.Tensor, np.ndarray]:
    ...
```

### RankedResponse().logits

[Show source in ranked_response.py:60](../../../../alfred/fm/response/ranked_response.py#L60)

Get the raw logits output by the language model.

#### Returns

The logits output by the language model
Type: *Union[torch.Tensor, np.ndarray]*

#### Signature

```python
@property
def logits(self) -> Union[torch.Tensor, np.ndarray]:
    ...
```

### RankedResponse().prediction

[Show source in ranked_response.py:40](../../../../alfred/fm/response/ranked_response.py#L40)

Get the prediction made by the language model.

#### Returns

The prediction made by the language model
Type: *str*

#### Signature

```python
@property
def prediction(self) -> str:
    ...
```

### RankedResponse().scores

[Show source in ranked_response.py:50](../../../../alfred/fm/response/ranked_response.py#L50)

Get the scores for each candidates in the language model.

#### Returns

A dictionary of scores for each class in the language model
Type: *dict*

#### Signature

```python
@property
def scores(self) -> Dict:
    ...
```


