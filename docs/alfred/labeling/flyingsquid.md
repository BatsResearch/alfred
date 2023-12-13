# FlyingSquid

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Labeling](./index.md#labeling) /
FlyingSquid

> Auto-generated documentation for [alfred.labeling.flyingsquid](../../../alfred/labeling/flyingsquid.py) module.

- [FlyingSquid](#flyingsquid)
  - [FlyingSquid](#flyingsquid-1)
    - [FlyingSquid().label](#flyingsquid()label)

## FlyingSquid

[Show source in flyingsquid.py:6](../../../alfred/labeling/flyingsquid.py#L6)

LabelModel class to perform FlyingSquid-based label modeling on the responses

#### Signature

```python
class FlyingSquid(LabelModel):
    def __init__(self, num_lfs):
        ...
```

### FlyingSquid().label

[Show source in flyingsquid.py:22](../../../alfred/labeling/flyingsquid.py#L22)

#### Signature

```python
def label(self, votes: np.ndarray) -> np.ndarray:
    ...
```