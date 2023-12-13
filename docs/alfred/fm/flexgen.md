# Flexgen

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Fm](./index.md#fm) /
Flexgen

> Auto-generated documentation for [alfred.fm.flexgen](../../../alfred/fm/flexgen.py) module.

- [Flexgen](#flexgen)
  - [FlexGenModel](#flexgenmodel)

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
    ):
        ...
```