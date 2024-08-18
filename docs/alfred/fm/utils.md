# Utils

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Fm](./index.md#fm) / Utils

> Auto-generated documentation for [alfred.fm.utils](../../../alfred/fm/utils.py) module.

- [Utils](#utils)
  - [bcolors](#bcolors)
  - [check_pkg_available](#check_pkg_available)
  - [clear_cuda_cache](#clear_cuda_cache)
  - [colorize_str](#colorize_str)
  - [encode_image](#encode_image)
  - [normalize_logits](#normalize_logits)
  - [reorder_array](#reorder_array)
  - [retry](#retry)
  - [tokenize](#tokenize)
  - [type_print](#type_print)

## bcolors

[Show source in utils.py:171](../../../alfred/fm/utils.py#L171)

#### Signature

```python
class bcolors: ...
```



## check_pkg_available

[Show source in utils.py:108](../../../alfred/fm/utils.py#L108)

Check if a package is available

#### Arguments

- `pkg_name` - The name of the package
:type pkg_name: str

#### Returns

Whether the package is available
Type: *bool*

#### Signature

```python
def check_pkg_available(pkg_name: str) -> bool: ...
```



## clear_cuda_cache

[Show source in utils.py:21](../../../alfred/fm/utils.py#L21)

Clear cuda cache via garbage collection

#### Signature

```python
def clear_cuda_cache(): ...
```



## colorize_str

[Show source in utils.py:183](../../../alfred/fm/utils.py#L183)

#### Signature

```python
def colorize_str(str, color="CYAN"): ...
```



## encode_image

[Show source in utils.py:44](../../../alfred/fm/utils.py#L44)

Encode an image file into base64.

#### Arguments

- `image` - The image to be encoded.
:type image: str or bytes or PIL.Image
- `type` - The type of the image. Can be "path", "bytes", or "image".
:type type: str

#### Signature

```python
def encode_image(image, type="path"): ...
```



## normalize_logits

[Show source in utils.py:29](../../../alfred/fm/utils.py#L29)

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
def normalize_logits(logits: torch.Tensor) -> torch.Tensor: ...
```



## reorder_array

[Show source in utils.py:67](../../../alfred/fm/utils.py#L67)

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
) -> Union[np.ndarray, torch.Tensor, list]: ...
```



## retry

[Show source in utils.py:136](../../../alfred/fm/utils.py#L136)

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
def retry(num_retries=3, wait_time=0.1, exceptions=(Exception)): ...
```



## tokenize

[Show source in utils.py:86](../../../alfred/fm/utils.py#L86)

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
def tokenize(inst, tokenizer, max_length=512): ...
```



## type_print

[Show source in utils.py:124](../../../alfred/fm/utils.py#L124)

Print a string word by word to simulate typing

#### Signature

```python
def type_print(string, interval=0.07, newline=False): ...
```