# Openai

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Fm](./index.md#fm) /
Openai

> Auto-generated documentation for [alfred.fm.openai](../../../alfred/fm/openai.py) module.

- [Openai](#openai)
  - [OpenAIModel](#openaimodel)
    - [OpenAIModel().chat](#openaimodel()chat)

## OpenAIModel

[Show source in openai.py:50](../../../alfred/fm/openai.py#L50)

A wrapper for the OpenAI API.

This class provides a wrapper for the OpenAI API for generating completions.

#### Signature

```python
class OpenAIModel(APIAccessFoundationModel):
    def __init__(
        self, model_string: str = "text-davinci-002", api_key: Optional[str] = None
    ):
        ...
```

### OpenAIModel().chat

[Show source in openai.py:229](../../../alfred/fm/openai.py#L229)

Launch an interactive chat session with the OpenAI API.

#### Signature

```python
def chat(self, **kwargs: Any):
    ...
```


