# Vllm

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Fm](./index.md#fm) / Vllm

> Auto-generated documentation for [alfred.fm.vllm](../../../alfred/fm/vllm.py) module.

- [Vllm](#vllm)
  - [vLLMModel](#vllmmodel)
    - [vLLMModel()._generate_batch](#vllmmodel()_generate_batch)
    - [vLLMModel()._score_batch](#vllmmodel()_score_batch)

## vLLMModel

[Show source in vllm.py:18](../../../alfred/fm/vllm.py#L18)

vLLMModel wraps a vLLM model. vLLM is a fast and easy-to-use library for LLM inference.

source: https://github.com/vllm-project/vllm

#### Signature

```python
class vLLMModel(LocalAccessFoundationModel):
    def __init__(self, model: str, local_path: str = None, **kwargs: Any): ...
```

### vLLMModel()._generate_batch

[Show source in vllm.py:40](../../../alfred/fm/vllm.py#L40)

Generate completions for a batch of queries.

#### Arguments

- `batch_instance` - A list of queries.
:type batch_instance: List[str]
- `kwargs` - Additional keyword arguments.

#### Returns

A list of `CompletionResponse` objects with the same prediction content as the input.
Type: *List[CompletionResponse]*

#### Signature

```python
def _generate_batch(
    self, batch_instance: List[str], **kwargs: Any
) -> List[CompletionResponse]: ...
```

### vLLMModel()._score_batch

[Show source in vllm.py:68](../../../alfred/fm/vllm.py#L68)

Score a batch of prompts and candidates using the vLLM model.

#### Arguments

- `batch` - A list of prompts or a list of tuples of prompts and candidates.
- `candidate` - A list of candidates to rank. If not provided, it's extracted from batch.
- `hidden_state` - Whether to return the encoder hidden state (not supported in vLLM).
- `tokenized` - Whether the input is already tokenized (not supported in vLLM).

#### Returns

A list of dictionaries containing the log probability scores for each candidate.

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