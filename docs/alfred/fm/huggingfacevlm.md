# Huggingfacevlm

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Fm](./index.md#fm) /
Huggingfacevlm

> Auto-generated documentation for [alfred.fm.huggingfacevlm](../../../alfred/fm/huggingfacevlm.py) module.

- [Huggingfacevlm](#huggingfacevlm)
  - [HuggingFaceCLIPModel](#huggingfaceclipmodel)

## HuggingFaceCLIPModel

[Show source in huggingfacevlm.py:15](../../../alfred/fm/huggingfacevlm.py#L15)

The HuggingFaceModel class is a wrapper for HuggingFace VLM Models
Currently supports CLIP models.

#### Signature

```python
class HuggingFaceCLIPModel(LocalAccessFoundationModel):
    def __init__(
        self,
        model_string: str,
        local_path: Optional[str] = None,
        image_cache_limit: int = 32,
        text_cache_limit: int = 64,
    ):
        ...
```

#### See also

- [LocalAccessFoundationModel](./model.md#localaccessfoundationmodel)


