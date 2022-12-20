# Response

[alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Fm](../index.md#fm) /
[Response](./index.md#response) /
Response

> Auto-generated documentation for [alfred.fm.response.response](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/response/response.py) module.

## Response

[Show source in response.py:6](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/response/response.py#L6)

A class that represents a response from a alfred.fm model.
Inherit from OrderedDict.
Inherited by CompletionResponse and RankedResponse.

#### Signature

```python
class Response(OrderedDict):
    ...
```

### Response().__repr__

[Show source in response.py:43](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/response/response.py#L43)

Get a string representation of the response object.

#### Returns

A string representation of the response
Type: *str*

#### Signature

```python
def __repr__(self):
    ...
```

### Response().__str__

[Show source in response.py:30](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/response/response.py#L30)

Get a string representation of the response.

#### Returns

A string representation of the response
Type: *str*

#### Signature

```python
def __str__(self):
    ...
```

### Response().prediction

[Show source in response.py:12](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/response/response.py#L12)

Get the prediction made by the model.

#### Returns

The prediction made by the model

#### Signature

```python
@abc.abstractmethod
def prediction(self):
    ...
```

### Response().serialize

[Show source in response.py:21](https://github.com/BatsResearch/alfred/blob/main/alfred/fm/response/response.py#L21)

Serialize the response to a JSON string.

#### Returns

The serialized response as a JSON string
Type: *str*

#### Signature

```python
def serialize(self) -> str:
    ...
```



