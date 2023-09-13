# Dummy

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Fm](./index.md#fm) /
Dummy

> Auto-generated documentation for [alfred.fm.dummy](../../../alfred/fm/dummy.py) module.

- [Dummy](#dummy)
  - [DummyModel](#dummymodel)

## DummyModel

[Show source in dummy.py:13](../../../alfred/fm/dummy.py#L13)

A dummy model that returns the input as the output.

This model implements a dummy model that returns the
input as the output for both completion and outputs a raw logit of -1 for scoring.

#### Signature

```python
class DummyModel(LocalAccessFoundationModel):
    def __init__(self, model: Optional[str] = None):
        ...
```

#### See also

- [LocalAccessFoundationModel](./model.md#localaccessfoundationmodel)


