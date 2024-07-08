# RankedQuery

[Alfred Index](../../../README.md#alfred-index) / [Alfred](../../index.md#alfred) / [Fm](../index.md#fm) / [Query](./index.md#query) / RankedQuery

> Auto-generated documentation for [alfred.fm.query.ranked_query](../../../../alfred/fm/query/ranked_query.py) module.

- [RankedQuery](#rankedquery)
  - [RankedQuery](#rankedquery-1)
    - [RankedQuery().__add__](#rankedquery()__add__)
    - [RankedQuery().__eq__](#rankedquery()__eq__)
    - [RankedQuery().__hash__](#rankedquery()__hash__)
    - [RankedQuery().__len__](#rankedquery()__len__)
    - [RankedQuery().__repr__](#rankedquery()__repr__)
    - [RankedQuery().__str__](#rankedquery()__str__)
    - [RankedQuery().candidates](#rankedquery()candidates)
    - [RankedQuery().get_answer_choices_str](#rankedquery()get_answer_choices_str)
    - [RankedQuery().load](#rankedquery()load)
    - [RankedQuery().prompt](#rankedquery()prompt)

## RankedQuery

[Show source in ranked_query.py:16](../../../../alfred/fm/query/ranked_query.py#L16)

Ranked Query Class encompasses query terms that operate in
scoring scheme with FM interfaces

#### Examples

```python
>>> from alfred.fm.query import RankedQuery
>>> query = RankedQuery("What is the answer of 1+1?", candidates=["2", "1"])
Then you can call either alfred.client or alfred.fm to get the RankedResponse
>>> from alfred.client import Client
>>> client = Client()
>>> response = client(query)
or
>>> from alfred.fm.x import XFM
>>> fm = XFM()
>>> response = fm(query)
```

#### Signature

```python
class RankedQuery(Query):
    def __init__(
        self,
        prompt: Union[str, np.ndarray, Image.Image, Tuple, torch.Tensor],
        candidates: Union[List, Tuple, np.ndarray, torch.Tensor],
    ): ...
```

### RankedQuery().__add__

[Show source in ranked_query.py:108](../../../../alfred/fm/query/ranked_query.py#L108)

concatenates the two queries

#### Signature

```python
def __add__(self, other): ...
```

### RankedQuery().__eq__

[Show source in ranked_query.py:93](../../../../alfred/fm/query/ranked_query.py#L93)

returns whether the two queries are equal

#### Signature

```python
def __eq__(self, other): ...
```

### RankedQuery().__hash__

[Show source in ranked_query.py:100](../../../../alfred/fm/query/ranked_query.py#L100)

returns the hash of the query

#### Signature

```python
def __hash__(self): ...
```

### RankedQuery().__len__

[Show source in ranked_query.py:104](../../../../alfred/fm/query/ranked_query.py#L104)

returns the length of the query

#### Signature

```python
def __len__(self): ...
```

### RankedQuery().__repr__

[Show source in ranked_query.py:85](../../../../alfred/fm/query/ranked_query.py#L85)

returns the string representation of the query

#### Signature

```python
def __repr__(self): ...
```

### RankedQuery().__str__

[Show source in ranked_query.py:89](../../../../alfred/fm/query/ranked_query.py#L89)

returns the string representation of the query

#### Signature

```python
def __str__(self): ...
```

### RankedQuery().candidates

[Show source in ranked_query.py:52](../../../../alfred/fm/query/ranked_query.py#L52)

returns the raw candidates content

#### Signature

```python
@property
def candidates(self): ...
```

### RankedQuery().get_answer_choices_str

[Show source in ranked_query.py:62](../../../../alfred/fm/query/ranked_query.py#L62)

get the raw candidates as jinja strings (deliminated by '|||')

#### Signature

```python
def get_answer_choices_str(self): ...
```

### RankedQuery().load

[Show source in ranked_query.py:66](../../../../alfred/fm/query/ranked_query.py#L66)

Load prompt and candidates

#### Arguments

- `composition_fn` - function to compose prompt and candidates
:type composition_fn: Callable

#### Returns

composed prompt and candidates as a list of different prompt queries
Type: *List*

#### Signature

```python
def load(self, composition_fn: Callable = None) -> List: ...
```

### RankedQuery().prompt

[Show source in ranked_query.py:57](../../../../alfred/fm/query/ranked_query.py#L57)

returns the raw prompt content

#### Signature

```python
@property
def prompt(self): ...
```