# Vllm

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Fm](./index.md#fm) / Vllm

> Auto-generated documentation for [alfred.fm.vllm](../../../alfred/fm/vllm.py) module.

- [Vllm](#vllm)
  - [vLLMModel](#vllmmodel)
    - [vLLMModel()._generate_batch](#vllmmodel()_generate_batch)

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