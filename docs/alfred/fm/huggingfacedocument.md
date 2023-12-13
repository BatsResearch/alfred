# Huggingfacedocument

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Fm](./index.md#fm) /
Huggingfacedocument

> Auto-generated documentation for [alfred.fm.huggingfacedocument](../../../alfred/fm/huggingfacedocument.py) module.

- [Huggingfacedocument](#huggingfacedocument)
  - [HuggingFaceDocumentModel](#huggingfacedocumentmodel)

## HuggingFaceDocumentModel

[Show source in huggingfacedocument.py:14](../../../alfred/fm/huggingfacedocument.py#L14)

The HuggingFaceModel class is a wrapper for HuggingFace Document Models
For now, this class serves as an abstraction for DocumentQA-based prompted labelers.

Currently supports:
   - Donut        (MIT License)
   - LayoutLM     (MIT License)
   - LayoutLMv2   (CC BY-NC-SA 4.0)
   - LayoutLMv3   (CC BY-NC-SA 4.0)

#### Signature

```python
class HuggingFaceDocumentModel(LocalAccessFoundationModel):
    def __init__(
        self, model_string: str, local_path: Optional[str] = None, **kwargs: Any
    ):
        ...
```