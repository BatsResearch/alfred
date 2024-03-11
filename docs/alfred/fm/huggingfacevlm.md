# Huggingfacevlm

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Fm](./index.md#fm) / Huggingfacevlm

> Auto-generated documentation for [alfred.fm.huggingfacevlm](../../../alfred/fm/huggingfacevlm.py) module.

- [Huggingfacevlm](#huggingfacevlm)
  - [HuggingFaceCLIPModel](#huggingfaceclipmodel)
    - [HuggingFaceCLIPModel()._score_batch](#huggingfaceclipmodel()_score_batch)

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
    ): ...
```

### HuggingFaceCLIPModel()._score_batch

[Show source in huggingfacevlm.py:57](../../../alfred/fm/huggingfacevlm.py#L57)

Scores a batch of instances

#### Arguments

- `batch_instance` - batch of instances
:type batch_instance: Tuple[List[Image.Image], List[str]]
- `kwargs` - (optional) additional arguments
:type kwargs: Dict

#### Returns

list of RankedResponse
Type: *List[RankedResponse]*

#### Signature

```python
def _score_batch(
    self, batch_instance: Tuple[List[Image.Image], List[str]], **kwargs
): ...
```