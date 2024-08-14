# Anthropic

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Fm](./index.md#fm) /
Anthropic

> Auto-generated documentation for [alfred.fm.anthropic](../../../alfred/fm/anthropic.py) module.

- [Anthropic](#anthropic)
  - [AnthropicModel](#anthropicmodel)
    - [AnthropicModel().chat](#anthropicmodel()chat)

## AnthropicModel

[Show source in anthropic.py:41](../../../alfred/fm/anthropic.py#L41)

A wrapper for the anthropic API.

This class provides a wrapper for the anthropic API for generating completions.

#### Signature

```python
class AnthropicModel(APIAccessFoundationModel):
    def __init__(
        self, model_string: str = "claude-3-opus-20240229", api_key: Optional[str] = None
    ):
        ...
```

### AnthropicModel().chat

[Show source in anthropic.py:206](../../../alfred/fm/anthropic.py#L206)

Launch an interactive chat session with the Anthropic API.

#### Signature

```python
def chat(self, **kwargs: Any):
    ...
```


