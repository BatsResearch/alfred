# Voter

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Voter](./index.md#voter) /
Voter

> Auto-generated documentation for [alfred.voter.voter](../../../alfred/voter/voter.py) module.

- [Voter](#voter)
  - [Voter](#voter-1)
    - [Voter().clear_calibration](#voter()clear_calibration)
    - [Voter().set_calibration](#voter()set_calibration)
    - [Voter().vote](#voter()vote)

## Voter

[Show source in voter.py:14](../../../alfred/voter/voter.py#L14)

Voter is an actionable objective that translate raw fm responses
to votes. It can also handle calibrations automatically for given template.

#### Signature

```python
class Voter:
    def __init__(
        self,
        label_map: Dict,
        matching_fn: Callable = lambda x, y,: x == y,
        calibration: Optional[Union[List, np.ndarray, Tuple]] = None,
    ):
        ...
```

### Voter().clear_calibration

[Show source in voter.py:144](../../../alfred/voter/voter.py#L144)

Clear calibration weights and biases

#### Signature

```python
def clear_calibration(self):
    ...
```

### Voter().set_calibration

[Show source in voter.py:130](../../../alfred/voter/voter.py#L130)

Set calibration weights and biases

Final calibration would be weights * scores + biases

#### Arguments

- `weights` - weights to apply to the scores
:type weights: Union[List[float], np.ndarray]
- `biases` - biases to apply to the scores
:type biases: Union[List[float], np.ndarray]

#### Signature

```python
def set_calibration(
    self, weights: Union[List[float], np.ndarray], biases: Union[List[float], np.ndarray]
):
    ...
```

### Voter().vote

[Show source in voter.py:52](../../../alfred/voter/voter.py#L52)

Vote for the responses based on the matching function and the label maps

*NOTE*: if label maps contains numerical labels then the vote will be the exact specified value
if not the vote will be the index + 1 of the matched answer choice

*Abstention vote is 0*

*NOTE* on partial labels:

#### Arguments

- `responses` - list of response objects
:type responses: Union[Iterable[str], str, Iterable[Response], Response]
- `matching_function` - (optional) function to match responses against answer choices, defaulting to exact match
                            e.g. lambda x, y: x == y
:type matching_function: Callable
- `label_map` - (optional) label maps that maps responses content to labels
                   label_map specified here will overide the label_map initialized in the template
:type label_map: Dict

#### Returns

numpy ndarray of votes in np.int8
Type: *np.ndarray*

#### Signature

```python
def vote(
    self,
    responses: Union[Iterable[str], str, Iterable[Response], Response],
    matching_function: Optional[Callable] = None,
    label_map: Optional[Dict] = None,
    **kwargs: Any
) -> np.ndarray:
    ...
```

#### See also

- [Response](../fm/response/response.md#response)