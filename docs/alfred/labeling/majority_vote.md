# MajorityVote

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Labeling](./index.md#labeling) /
MajorityVote

> Auto-generated documentation for [alfred.labeling.majority_vote](../../../alfred/labeling/majority_vote.py) module.

- [MajorityVote](#majorityvote)
  - [MajorityVote](#majorityvote-1)
    - [MajorityVote().label](#majorityvote()label)

## MajorityVote

[Show source in majority_vote.py:7](../../../alfred/labeling/majority_vote.py#L7)

LabelModel class to perform majority vote on the responses

#### Signature

```python
class MajorityVote(LabelModel):
    def __init__(self):
        ...
```

### MajorityVote().label

[Show source in majority_vote.py:15](../../../alfred/labeling/majority_vote.py#L15)

returns the majority vote for each response row

#### Signature

```python
def label(self, votes: np.ndarray) -> np.ndarray:
    ...
```


