# Vllm

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Fm](./index.md#fm) /
Vllm

> Auto-generated documentation for [alfred.fm.vllm](../../../alfred/fm/vllm.py) module.

- [Vllm](#vllm)
  - [vLLMModel](#vllmmodel)

## vLLMModel

[Show source in vllm.py:18](../../../alfred/fm/vllm.py#L18)

vLLMModel wraps a vLLM model. vLLM is a fast and easy-to-use library for LLM inference.

source: https://github.com/vllm-project/vllm

#### Signature

```python
class vLLMModel(LocalAccessFoundationModel):
    def __init__(self, model: str, local_dir: str = None, **kwargs: Any):
        ...
```