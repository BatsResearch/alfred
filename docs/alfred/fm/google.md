# Google

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Fm](./index.md#fm) /
Google

> Auto-generated documentation for [alfred.fm.google](../../../alfred/fm/google.py) module.

- [Google](#google)
  - [GoogleModel](#googlemodel)
    - [GoogleModel().chat](#googlemodel()chat)

## GoogleModel

[Show source in google.py:33](../../../alfred/fm/google.py#L33)

A wrapper for the Google API.

This class provides a wrapper for the Google API for generating completions.

#### Signature

```python
class GoogleModel(APIAccessFoundationModel):
    def __init__(self, model_string: str = "gemini-pro", api_key: Optional[str] = None):
        ...
```

### GoogleModel().chat

[Show source in google.py:246](../../../alfred/fm/google.py#L246)

Launch an interactive chat session with the Google API.

#### Signature

```python
def chat(self, **kwargs: Any):
    ...
```


