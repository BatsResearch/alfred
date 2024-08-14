# Groq

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Fm](./index.md#fm) /
Groq

> Auto-generated documentation for [alfred.fm.groq](../../../alfred/fm/groq.py) module.

- [Groq](#groq)
  - [GroqModel](#groqmodel)
    - [GroqModel().chat](#groqmodel()chat)

## GroqModel

[Show source in groq.py:27](../../../alfred/fm/groq.py#L27)

A wrapper for the OpenAI API.

This class provides a wrapper for the OpenAI API for generating completions.

#### Signature

```python
class GroqModel(APIAccessFoundationModel):
    def __init__(
        self, model_string: str = "llama3-8b-8192", api_key: Optional[str] = None
    ):
        ...
```

### GroqModel().chat

[Show source in groq.py:157](../../../alfred/fm/groq.py#L157)

Launch an interactive chat session with the Anthropic API.

#### Signature

```python
def chat(self, **kwargs: Any):
    ...
```


