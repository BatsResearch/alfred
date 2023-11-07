# Response

[Alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Fm](../index.md#fm) /
Response

> Auto-generated documentation for [alfred.fm.response](../../../../alfred/fm/response/__init__.py) module.

- [Response](#response)
  - [deserialize](#deserialize)
  - [from_dict](#from_dict)
  - [Modules](#modules)

## deserialize

[Show source in __init__.py:25](../../../../alfred/fm/response/__init__.py#L25)

Deserializes a JSON string into a Response object.

#### Arguments

- `json_str` - The JSON string to deserialize.
:type json_str: str

#### Returns

The Response object.
Type: *Response*

#### Signature

```python
def deserialize(json_str: str) -> Response:
    ...
```



## from_dict

[Show source in __init__.py:9](../../../../alfred/fm/response/__init__.py#L9)

Converts a JSON dictionary to a Response object.

#### Arguments

- `json_dict` - The JSON dictionary to convert.
:type json_dict: dict

#### Returns

The Response object.
Type: *Responses*

#### Signature

```python
def from_dict(json_dict: dict) -> Response:
    ...
```



## Modules

- [CompletionResponse](./completion_response.md)
- [RankedResponse](./ranked_response.md)
- [Response](./response.md)