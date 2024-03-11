# Huggingfacedocument

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Fm](./index.md#fm) / Huggingfacedocument

> Auto-generated documentation for [alfred.fm.huggingfacedocument](../../../alfred/fm/huggingfacedocument.py) module.

- [Huggingfacedocument](#huggingfacedocument)
  - [HuggingFaceDocumentModel](#huggingfacedocumentmodel)
    - [HuggingFaceDocumentModel()._generate_batch](#huggingfacedocumentmodel()_generate_batch)

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
    ): ...
```

### HuggingFaceDocumentModel()._generate_batch

[Show source in huggingfacedocument.py:70](../../../alfred/fm/huggingfacedocument.py#L70)

Scores a batch of instances

#### Arguments

- `batch_instance` - batch of instances
:type batch_instance: Tuple[List[Image.Image], List[str]]
- `kwargs` - (optional) additional arguments
:type kwargs: Dict

#### Returns

list of CompletionResponse
Type: *List[CompletionResponse]*

#### Signature

```python
def _generate_batch(self, batch_instance: List[Tuple[Image.Image, str]], **kwargs): ...
```