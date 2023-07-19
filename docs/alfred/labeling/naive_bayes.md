# NaiveBayes

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Labeling](./index.md#labeling) /
NaiveBayes

> Auto-generated documentation for [alfred.labeling.naive_bayes](../../../alfred/labeling/naive_bayes.py) module.

- [NaiveBayes](#naivebayes)
  - [NaiveBayes](#naivebayes-1)
    - [NaiveBayes().label](#naivebayes()label)

## NaiveBayes

[Show source in naive_bayes.py:6](../../../alfred/labeling/naive_bayes.py#L6)

LabelModel wrapper to perform label modeling for partial labelers on the responses

#### Signature

```python
class NaiveBayes(LabelModel):
    def __init__(self, num_classes, num_lfs):
        ...
```

### NaiveBayes().label

[Show source in naive_bayes.py:25](../../../alfred/labeling/naive_bayes.py#L25)

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