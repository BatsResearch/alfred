# Utils

[Alfred Index](../../README.md#alfred-index) /
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

[Show source in utils.py:61](../../../alfred/fm/utils.py#L61)

Dynamic Batching Utility
Maximize GPU Utilization by batching queries of similar sizes

#### Signature

```python
class DynamicBatcher:
    def __init__(
        self, queries: Union[List[Query], List[str]], max_batch_size: int = 2048
    ):
        ...
```

### DynamicBatcher().batch

[Show source in utils.py:177](../../../alfred/fm/utils.py#L177)

Batch a list of instances into a list of batches.
If the instances are of different sizes, they will be sorted by size
and batched accordingly

#### Returns

A list of batches
Type: *List[List[Instance]]*

#### Signature

```python
def batch(self) -> List:
    ...
```

### DynamicBatcher().merge_rank_response

[Show source in utils.py:101](../../../alfred/fm/utils.py#L101)

Merge a list of responses with raw logit into a single RankedResponse
Assumption: Candidate Order is the same across all ranked queries

#### Arguments

- `responses` - A list of responses to be merged
:type responses: List[OrderedDict]
- `softmax` - Whether to apply softmax to the logits
:type softmax: bool
- `candidate_token_len` - The length of the candidate in terms of tokens
:type candidate_token_len: Union[List[int], int]

#### Returns

A merged response
Type: *RankedResponse*

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

[Show source in utils.py:136](../../../alfred/fm/utils.py#L136)

Reordering the responses according to the original order of the queries

#### Arguments

- `inst` - The list of responses to be reordered
:type inst: List
- `offset` - The offset of the responses
:type offset: Optional[int]
- `candidate_token_len` - The length of the candidate in terms of tokens
:type candidate_token_len: Optional[Union[int, List[int]]]

#### Returns

The reordered responses
Type: *List of responses*

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

[Show source in utils.py:17](../../../alfred/fm/utils.py#L17)

Clear cuda cache via garbage collection

#### Signature

```python
def clear_cuda_cache():
    ...
```



## normalize_logits

[Show source in utils.py:25](../../../alfred/fm/utils.py#L25)

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

[Show source in utils.py:40](../../../alfred/fm/utils.py#L40)

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


