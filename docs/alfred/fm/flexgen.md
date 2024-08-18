# Flexgen

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Fm](./index.md#fm) / Flexgen

> Auto-generated documentation for [alfred.fm.flexgen](../../../alfred/fm/flexgen.py) module.

- [Flexgen](#flexgen)
  - [FlexGenModel](#flexgenmodel)
    - [FlexGenModel()._generate_batch](#flexgenmodel()_generate_batch)

## FlexGenModel

[Show source in flexgen.py:13](../../../alfred/fm/flexgen.py#L13)

FlexGenModel wraps a FlexGen model. FlexGen is used for High-throughput generative inference with single GPU.

Currently, FlexGen supports OPT style models.

source: https://github.com/FMInference/FlexGen
paper: https://arxiv.org/pdf/2303.06865.pdf

#### Signature

```python
class FlexGenModel(LocalAccessFoundationModel):
    def __init__(
        self,
        model: str,
        local_dir: str,
        model_string: str,
        policy: Union[List, Policy] = (100, 0, 100, 0, 100, 0),
        offload_dir: str = "./flexgen_offload_cache",
        **kwargs: Any
    ): ...
```

### FlexGenModel()._generate_batch

[Show source in flexgen.py:73](../../../alfred/fm/flexgen.py#L73)

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