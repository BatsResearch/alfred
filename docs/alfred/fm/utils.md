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
  - [check_pkg_available](#check_pkg_available)
  - [clear_cuda_cache](#clear_cuda_cache)
  - [colorize_str](#colorize_str)
  - [encode_image](#encode_image)
  - [normalize_logits](#normalize_logits)
  - [reorder_array](#reorder_array)
  - [retry](#retry)
  - [tokenize](#tokenize)
  - [type_print](#type_print)

## DynamicBatcher

[Show source in utils.py:318](../../../alfred/fm/utils.py#L318)

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

[Show source in utils.py:447](../../../alfred/fm/utils.py#L447)

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

[Show source in utils.py:363](../../../alfred/fm/utils.py#L363)

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

[Show source in utils.py:406](../../../alfred/fm/utils.py#L406)

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

[Show source in utils.py:241](../../../alfred/fm/utils.py#L241)

A simple embedding cache for VLM models

#### Signature

```python
class EmbeddingCache:
    def __init__(self, max_size: int = 32):
        ...
```

### EmbeddingCache().get

[Show source in utils.py:267](../../../alfred/fm/utils.py#L267)

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

[Show source in utils.py:307](../../../alfred/fm/utils.py#L307)

#### Signature

```python
class TokenizedBatch:
    def __init__(self, token_ids, pad_token_id=0):
        ...
```



## bcolors

[Show source in utils.py:215](../../../alfred/fm/utils.py#L215)

#### Signature

```python
class bcolors:
    ...
```



## batch_multimodal

[Show source in utils.py:111](../../../alfred/fm/utils.py#L111)

Batch RankedQueries with Multimodal Payloads

#### Arguments

- `queries` - A list of multimodal queries
:type queries: List[Query]
- `mode` - The mode of the multimodal query ("autoregressive", "contrastive")
:type mode: str
- `batch_size` - The batch size
:type batch_size: int

#### Returns

A list of batches of multimodal ranked queries
Type: *List[List[Query]]*

#### Signature

```python
def batch_multimodal(queries: List[Query], mode: str, batch_size=64):
    ...
```



## check_pkg_available

[Show source in utils.py:153](../../../alfred/fm/utils.py#L153)

Check if a package is available

#### Arguments

- `pkg_name` - The name of the package
:type pkg_name: str

#### Returns

Whether the package is available
Type: *bool*

#### Signature

```python
def check_pkg_available(pkg_name: str) -> bool:
    ...
```



## clear_cuda_cache

[Show source in utils.py:24](../../../alfred/fm/utils.py#L24)

Clear cuda cache via garbage collection

#### Signature

```python
def clear_cuda_cache():
    ...
```



## colorize_str

[Show source in utils.py:227](../../../alfred/fm/utils.py#L227)

#### Signature

```python
def colorize_str(str, color="CYAN"):
    ...
```



## encode_image

[Show source in utils.py:47](../../../alfred/fm/utils.py#L47)

Encode an image file into base64.

#### Arguments

- `image` - The image to be encoded.
:type image: str or bytes or PIL.Image
- `type` - The type of the image. Can be "path", "bytes", or "image".
:type type: str

#### Signature

```python
def encode_image(image, type="path"):
    ...
```



## normalize_logits

[Show source in utils.py:32](../../../alfred/fm/utils.py#L32)

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

[Show source in utils.py:70](../../../alfred/fm/utils.py#L70)

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



## retry

[Show source in utils.py:180](../../../alfred/fm/utils.py#L180)

A decorator to retry a function call if it raises an exception.

Useful for running API-based models that may fail due to network/server issues.

#### Arguments

- `num_retries` - The number of retries
:type num_retries: int
- `wait_time` - The time to wait between retries
:type wait_time: float
- `exceptions` - The exceptions to catch
:type exceptions: Tuple[Exception]

#### Returns

The decorated function
Type: *Callable*

#### Signature

```python
def retry(num_retries=3, wait_time=0.1, exceptions=(Exception)):
    ...
```



## tokenize

[Show source in utils.py:89](../../../alfred/fm/utils.py#L89)

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



## type_print

[Show source in utils.py:169](../../../alfred/fm/utils.py#L169)

Print a string word by word to simulate typing

#### Signature

```python
def type_print(string, interval=0.07, newline=False):
    ...
```


