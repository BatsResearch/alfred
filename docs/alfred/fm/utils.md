# Utils

[alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Fm](./index.md#fm) /
Utils

> Auto-generated documentation for [alfred.fm.utils](../../../alfred/fm/utils.py) module.

- [Utils](#utils)
  - [DynamicBatcher](#dynamicbatcher)
    - [DynamicBatcher().batch](#dynamicbatcher()batch)
    - [DynamicBatcher().merge_rank_response](#dynamicbatcher()merge_rank_response)
    - [DynamicBatcher().reorder](#dynamicbatcher()reorder)
  - [clear_cuda_cache](#clear_cuda_cache)
  - [normalize_logits](#normalize_logits)
  - [reorder_array](#reorder_array)

## DynamicBatcher

[Show source in utils.py:59](../../../alfred/fm/utils.py#L59)

#### Signature

```python
class DynamicBatcher:
    def __init__(
        self, queries: Union[List[Query], List[str]], max_batch_size: int = 2048
    ):
        ...
```

### DynamicBatcher().batch

[Show source in utils.py:156](../../../alfred/fm/utils.py#L156)

Batch a list of instances into a list of batches

#### Signature

```python
def batch(self):
    ...
```

### DynamicBatcher().merge_rank_response

[Show source in utils.py:96](../../../alfred/fm/utils.py#L96)

Assumption: Candidate Order is the same across all ranked queries

#### Arguments

- `responses` - A list of responses to be merged
- `softmax` - Whether to apply softmax to the logits
- `candidate_token_len` - The length of the candidate in terms of tokens

#### Returns

A merged response

#### Signature

```python
def merge_rank_response(
    self,
    responses: List[OrderedDict],
    softmax: bool = True,
    candidate_token_len: Union[List[int], int] = 1,
) -> RankedResponse:
    ...
```

### DynamicBatcher().reorder

[Show source in utils.py:127](../../../alfred/fm/utils.py#L127)

#### Signature

```python
def reorder(
    self,
    inst: List,
    offset: Optional[int] = None,
    candidate_token_len: Optional[Union[int, List[int]]] = None,
) -> List:
    ...
```



## clear_cuda_cache

[Show source in utils.py:15](../../../alfred/fm/utils.py#L15)

Clear cuda cache via garbage collection

#### Signature

```python
def clear_cuda_cache():
    ...
```



## normalize_logits

[Show source in utils.py:23](../../../alfred/fm/utils.py#L23)

Normalize raw logit scores from a foundation model.

This function normalizes raw logit scores from a foundation model using the softmax function.
Other normalization methods can be used in the future if needed.

#### Arguments

- `logits` - The raw logit scores to be normalized.
:type logits: torch.Tensor

#### Returns

The normalized logit scores.
Type: *torch.Tensor*

#### Signature

```python
def normalize_logits(logits: torch.Tensor) -> torch.Tensor:
    ...
```



## reorder_array

[Show source in utils.py:38](../../../alfred/fm/utils.py#L38)

Reorder an array according to a given order.

This function reorders the elements in an array according to the order specified by a separate array.

#### Arguments

- `arr` - The array to be reordered. Can be a NumPy array, PyTorch tensor, or Python list.
:type arr: Union[np.ndarray, torch.Tensor, list]
- `order` - The order array. Can be a NumPy array, PyTorch tensor, or Python list.
:type order: Union[np.ndarray, torch.Tensor, list]

#### Returns

The reordered array. Has the same type as the input `arr`.
Type: *Union[np.ndarray, torch.Tensor, list]*

#### Signature

```python
def reorder_array(
    arr: Union[np.ndarray, torch.Tensor, list],
    order: Union[np.ndarray, torch.Tensor, list],
) -> Union[np.ndarray, torch.Tensor, list]:
    ...
```


