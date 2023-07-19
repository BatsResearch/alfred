# NPLM

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Labeling](./index.md#labeling) /
NPLM

> Auto-generated documentation for [alfred.labeling.nplm](../../../alfred/labeling/nplm.py) module.

- [NPLM](#nplm)
  - [NPLM](#nplm-1)
    - [NPLM().label](#nplm()label)

## NPLM

[Show source in nplm.py:7](../../../alfred/labeling/nplm.py#L7)

LabelModel wrapper to perform label modeling for partial labelers on the responses

#### Signature

```python
class NPLM(LabelModel):
    def __init__(
        self,
        num_classes,
        label_partition,
        device="cuda:0" if torch.cuda.is_available() else "cpu",
    ):
        ...
```

### NPLM().label

[Show source in nplm.py:30](../../../alfred/labeling/nplm.py#L30)

Label the responses using the label model.
Similar to standard PWS practice, abstention = 0 (i.e. classes are 1-indexed)

#### Arguments

- `votes` - The votes from the labelers.
:type votes: np.ndarray

#### Returns

The predicted probabilistic labels.
Type: *np.ndarray*

#### Signature

```python
def label(self, votes: np.ndarray) -> np.ndarray:
    ...
```