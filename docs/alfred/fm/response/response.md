# Response

[Alfred Index](../../../README.md#alfred-index) / [Alfred](../../index.md#alfred) / [Fm](../index.md#fm) / [Response](./index.md#response) / Response

> Auto-generated documentation for [alfred.fm.response.response](../../../../alfred/fm/response/response.py) module.

- [Response](#response)
  - [Response](#response-1)
    - [Response().__repr__](#response()__repr__)
    - [Response().__str__](#response()__str__)
    - [Response().prediction](#response()prediction)
    - [Response().serialize](#response()serialize)

## Response

[Show source in response.py:6](../../../../alfred/fm/response/response.py#L6)

A class that represents a response from a alfred.fm model.
Inherit from OrderedDict.
Inherited by CompletionResponse and RankedResponse.

#### Signature

```python
class Response(OrderedDict): ...
```

### Response().__repr__

[Show source in response.py:44](../../../../alfred/fm/response/response.py#L44)

Get a string representation of the response object.

#### Returns

A string representation of the response
Type: *str*

#### Signature

```python
def __repr__(self): ...
```

### Response().__str__

[Show source in response.py:31](../../../../alfred/fm/response/response.py#L31)

Get a string representation of the response.

#### Returns

A string representation of the response
Type: *str*

#### Signature

```python
def __str__(self): ...
```

### Response().prediction

[Show source in response.py:13](../../../../alfred/fm/response/response.py#L13)

Get the prediction made by the model.

#### Returns

The prediction made by the model

#### Signature

```python
@abc.abstractmethod
def prediction(self): ...
```

### Response().serialize

[Show source in response.py:22](../../../../alfred/fm/response/response.py#L22)

Serialize the response to a JSON string.

#### Returns

The serialized response as a JSON string
Type: *str*

#### Signature

```python
def serialize(self) -> str: ...
```