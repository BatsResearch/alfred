# Cohere

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Fm](./index.md#fm) /
Cohere

> Auto-generated documentation for [alfred.fm.cohere](../../../alfred/fm/cohere.py) module.

- [Cohere](#cohere)
  - [CohereModel](#coheremodel)

## CohereModel

[Show source in cohere.py:12](../../../alfred/fm/cohere.py#L12)

A wrapper for the OpenAI API.

This class provides a wrapper for the OpenAI API for generating completions.

#### Signature

```python
class CohereModel(APIAccessFoundationModel):
    def __init__(self, model_string: str = "xlarge", api_key: Optional[str] = None):
        ...
```