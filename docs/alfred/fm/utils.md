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
  - [EmbeddingCache](#embeddingcache)
    - [EmbeddingCache().get](#embeddingcache()get)
  - [TokenizedBatch](#tokenizedbatch)
  - [bcolors](#bcolors)
  - [batch_multimodal](#batch_multimodal)
  - [clear_cuda_cache](#clear_cuda_cache)
  - [colorize_str](#colorize_str)
  - [normalize_logits](#normalize_logits)
  - [reorder_array](#reorder_array)
  - [tokenize](#tokenize)

## DynamicBatcher

[Show source in utils.py:203](../../../alfred/fm/utils.py#L203)

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

[Show source in utils.py:333](../../../alfred/fm/utils.py#L333)

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

[Show source in utils.py:247](../../../alfred/fm/utils.py#L247)

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

[Show source in utils.py:292](../../../alfred/fm/utils.py#L292)

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



## EmbeddingCache

[Show source in utils.py:132](../../../alfred/fm/utils.py#L132)

A simple embedding cache for VLM models

#### Signature

```python
class EmbeddingCache:
    def __init__(self, max_size: int = 32):
        ...
```

### EmbeddingCache().get

[Show source in utils.py:157](../../../alfred/fm/utils.py#L157)

Process the inputs and retrieve from the cache/embed the inputs

#### Arguments

- `inputs` - A list of inputs
:type inputs: Union[List[Image.Image], List[str]]
- `embedding_proc` - The embedding function
:type embedding_proc: Callable

#### Returns

The embeddings
Type: *torch.tensor*

#### Signature

```python
def get(
    self, inputs: Union[List[Image.Image], List[str]], embedding_proc: Callable
) -> torch.tensor:
    ...
```



## TokenizedBatch

[Show source in utils.py:192](../../../alfred/fm/utils.py#L192)

#### Signature

```python
class TokenizedBatch:
    def __init__(self, token_ids, pad_token_id=0):
        ...
```



## bcolors

[Show source in utils.py:108](../../../alfred/fm/utils.py#L108)

#### Signature

```python
class bcolors:
    ...
```



## batch_multimodal

[Show source in utils.py:85](../../../alfred/fm/utils.py#L85)

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

[Show source in utils.py:20](../../../alfred/fm/utils.py#L20)

Clear cuda cache via garbage collection

#### Signature

```python
def clear_cuda_cache():
    ...
```



## colorize_str

[Show source in utils.py:119](../../../alfred/fm/utils.py#L119)

#### Signature

```python
def colorize_str(str, color="CYAN"):
    ...
```



## normalize_logits

[Show source in utils.py:28](../../../alfred/fm/utils.py#L28)

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

[Show source in utils.py:43](../../../alfred/fm/utils.py#L43)

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

[Show source in utils.py:62](../../../alfred/fm/utils.py#L62)

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


