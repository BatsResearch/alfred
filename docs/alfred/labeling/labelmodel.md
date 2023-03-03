# LabelModel

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Labeling](./index.md#labeling) /
LabelModel

> Auto-generated documentation for [alfred.labeling.labelmodel](../../../alfred/labeling/labelmodel.py) module.

- [LabelModel](#labelmodel)
  - [LabelModel](#labelmodel-1)
    - [LabelModel().__call__](#labelmodel()__call__)
    - [LabelModel().label](#labelmodel()label)

## LabelModel

[Show source in labelmodel.py:5](../../../alfred/labeling/labelmodel.py#L5)

Abstract LabelModel Interface

#### Signature

```python
class LabelModel:
    def __init__(self, config: Optional[Dict] = None, trainable: bool = False):
        ...
```

### LabelModel().__call__

[Show source in labelmodel.py:30](../../../alfred/labeling/labelmodel.py#L30)

functional style of label

#### Signature

```python
def __call__(self, votes):
    ...
```

### LabelModel().label

[Show source in labelmodel.py:26](../../../alfred/labeling/labelmodel.py#L26)

#### Signature

```python
@abc.abstractmethod
def label(self, votes):
    ...
```


