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
  - [TokenizedBatch](#tokenizedbatch)
  - [batch_multimodal](#batch_multimodal)
  - [clear_cuda_cache](#clear_cuda_cache)
  - [normalize_logits](#normalize_logits)
  - [reorder_array](#reorder_array)
  - [tokenize](#tokenize)

## DynamicBatcher

[Show source in utils.py:119](../../../alfred/fm/utils.py#L119)

Dynamic Batching Utility
Maximize GPU Utilization by batching queries of similar sizes

#### Signature

```python
class DynamicBatcher:
    def __init__(
        self,
        queries: Union[List[Query], List[str]],
        max_batch_size: int = 2048,
        tokenizer: Optional[transformers.PreTrainedTokenizer] = None,
        max_token_length: int = 512,
    ):
        ...
```

### DynamicBatcher().batch

[Show source in utils.py:248](../../../alfred/fm/utils.py#L248)

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

[Show source in utils.py:162](../../../alfred/fm/utils.py#L162)

Merge a list of responses with raw logit into a single RankedResponse
Assumption: Candidate Order is the same across all ranked queries

#### Arguments

- `responses` - A list of responses to be merged
:type responses: List[OrderedDict]
- `softmax` - Whether to apply softmax to the logits
:type softmax: bool

#### Returns

A merged response
Type: *RankedResponse*

#### Signature

```python
def merge_rank_response(
    self, responses: List[OrderedDict], softmax: bool = True
) -> RankedResponse:
    ...
```

### DynamicBatcher().reorder

[Show source in utils.py:207](../../../alfred/fm/utils.py#L207)

Reordering the responses according to the original order of the queries

#### Arguments

- `inst` - The list of responses to be reordered
:type inst: List
- `offset` - The offset of the responses
:type offset: Optional[int]

#### Returns

The reordered responses
Type: *List of responses*

#### Signature

```python
def reorder(self, inst: List, offset: Optional[int] = None) -> List:
    ...
```



## TokenizedBatch

[Show source in utils.py:108](../../../alfred/fm/utils.py#L108)

#### Signature

```python
class TokenizedBatch:
    def __init__(self, token_ids, pad_token_id=0):
        ...
```



## batch_multimodal

[Show source in utils.py:84](../../../alfred/fm/utils.py#L84)

Batch RankedQueries with Multimodal Payloads

#### Arguments

- `queries` - A list of multimodal queries
:type queries: List[RankedQuery]
- `batch_size` - The batch size
:type batch_size: int

#### Returns

A list of batches of multimodal ranked queries
Type: *List[List[RankedQuery]]*

#### Signature

```python
def batch_multimodal(queries: List[RankedQuery], batch_size=64):
    ...
```



## clear_cuda_cache

[Show source in utils.py:19](../../../alfred/fm/utils.py#L19)

Clear cuda cache via garbage collection

#### Signature

```python
def clear_cuda_cache():
    ...
```



## normalize_logits

[Show source in utils.py:27](../../../alfred/fm/utils.py#L27)

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

[Show source in utils.py:42](../../../alfred/fm/utils.py#L42)

Recover an array according to a given order index.

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



## tokenize

[Show source in utils.py:61](../../../alfred/fm/utils.py#L61)

Tokenize a query instance

#### Arguments

- `inst` - A query instance
:type inst: Union[Query, str]
- `tokenizer` - A tokenizer
:type tokenizer: transformers.PreTrainedTokenizer
- `max_length` - The maximum length of the tokenized sequence
:type max_length: int

#### Returns

A list of token ids
Type: *List[int]*

#### Signature

```python
def tokenize(inst, tokenizer, max_length=512):
    ...
```


