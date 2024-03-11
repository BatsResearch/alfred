# Huggingface

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Fm](./index.md#fm) / Huggingface

> Auto-generated documentation for [alfred.fm.huggingface](../../../alfred/fm/huggingface.py) module.

- [Huggingface](#huggingface)
  - [HuggingFaceModel](#huggingfacemodel)
    - [HuggingFaceModel()._encode_batch](#huggingfacemodel()_encode_batch)
    - [HuggingFaceModel()._generate_batch](#huggingfacemodel()_generate_batch)
    - [HuggingFaceModel()._get_hidden_states](#huggingfacemodel()_get_hidden_states)
    - [HuggingFaceModel()._score_batch](#huggingfacemodel()_score_batch)

## HuggingFaceModel

[Show source in huggingface.py:44](../../../alfred/fm/huggingface.py#L44)

The HuggingFaceModel class is a wrapper for HuggingFace models,
including both Seq2Seq (Encoder-Decoder, e.g. T5, T0) and Causal
(Autoregressive, e.g. GPT) Language Models.

This wrapper supports several options for loading models, including
specifying the data type, using a local path for the model hub, using
 a device map for parallelization, applying int8 quantization, and
 using custom tokenization.

The interface includes implementations of the _score_batch method
for ranking candidates and the _generate_batch method for generating prompts.

#### Signature

```python
class HuggingFaceModel(LocalAccessFoundationModel):
    def __init__(
        self,
        model_string: str,
        dtype: str = "auto",
        local_path: Optional[str] = None,
        device_map: Optional[Union[str, dict]] = "auto",
        offload_folder: Optional[str] = None,
        int_8: bool = False,
        trust_remote_code: bool = True,
        tokenizer: Optional[PreTrainedTokenizer] = None,
    ): ...
```

### HuggingFaceModel()._encode_batch

[Show source in huggingface.py:435](../../../alfred/fm/huggingface.py#L435)

Encode given batch of instances.

#### Arguments

- `batch_instance` - A list of raw text prompts.
:type batch_instance: List[str]
- `kwargs` - Additional keyword arguments to pass to the model's `generate` method.
:type kwargs: Any

#### Returns

A list of torch.Tensor objects containing the encoded instances.
Type: *List[torch.Tensor]*

#### Signature

```python
def _encode_batch(self, batch_instance, **kwargs) -> List[torch.Tensor]: ...
```

### HuggingFaceModel()._generate_batch

[Show source in huggingface.py:345](../../../alfred/fm/huggingface.py#L345)

Generate completions for a batch of prompts using the model.

This function takes a batch of prompts and uses the model to generate
completions for each prompt.
The generated completions are then returned in a list of `CompletionResponse` objects.
Currently, only greedy decoding is supported for open completion.

#### Arguments

- `batch` - A list of raw text prompts.
:type batch: List[str]
- `padding` - Whether to pad the batch.
:type padding: bool
- `hidden_state` - Whether to return the (encoder) hidden state.
:type hidden_state: bool
- `allow_grad` - Whether to allow gradient calculations during generation.
:type allow_grad: bool
- `kwargs` - Additional keyword arguments to pass to the model's `generate` method.
:type kwargs: Any

#### Returns

A list of `CompletionResponse` objects containing the generated completions.
Type: *List[CompletionResponse]*

#### Signature

```python
def _generate_batch(
    self,
    batch: List[str],
    padding: bool = True,
    hidden_state: bool = False,
    allow_grad: bool = False,
    tokenized: bool = False,
    **kwargs: Any
) -> List[CompletionResponse]: ...
```

### HuggingFaceModel()._get_hidden_states

[Show source in huggingface.py:170](../../../alfred/fm/huggingface.py#L170)

Get the hidden states of the inputs.
For encoder-decoder models (e.g.) T5, this returns the encoder hidden states.
For causal models (e.g. GPT), this returns the hidden states of the last layer.

#### Arguments

- `inputs` - The inputs to the model
:type inputs: transformers.PreTrainedTokenizer
- `reduction` - (optional) The reduction to apply to the hidden states, options include "mean" and "sum" (default: "mean")
:type reduction: str

#### Returns

The hidden states
Type: *torch.Tensor*

#### Signature

```python
def _get_hidden_states(self, inputs, reduction="mean") -> torch.Tensor: ...
```

### HuggingFaceModel()._score_batch

[Show source in huggingface.py:209](../../../alfred/fm/huggingface.py#L209)

Score a batch of prompts and candidates using the model.

This function takes a batch of prompts and a list of candidates and uses the model to generate
logit scores for the candidates. The raw logit scores are then returned in a list of dictionaries.
If `candidate` is not provided, the function will use the tokenizer's vocabulary as the candidates.
The final (softmax) normalization is done after this function when the scores for one instance
are aggregated.
For one ranked query, this function will be called `len(candidate)` number of times.

#### Arguments

- `batch` - A list of prompts or a list of tuples of prompts and candidates.
:type batch: Union[List[str], List[Tuple[str, str]]]
- `candidate` - A list of candidates to rank. If not provided, the tokenizer's vocabulary is used.
:type candidate: List[str]
- `hidden_state` - Whether to return the encoder hidden state.
:type hidden_state: bool

#### Returns

A list of dictionaries containing the raw logit scores and the encoder/decoder hidden states.
Type: *List[Dict[str, Any]]*

#### Signature

```python
def _score_batch(
    self,
    batch: Union[List[str], List[Tuple[str, str]]],
    candidate: Optional[List[str]] = None,
    hidden_state: bool = False,
    tokenized: bool = False,
    **kwargs: Any
) -> List[Dict[str, Any]]: ...
```