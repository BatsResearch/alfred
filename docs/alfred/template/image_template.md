# ImageTemplate

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Template](./index.md#template) / ImageTemplate

> Auto-generated documentation for [alfred.template.image_template](../../../alfred/template/image_template.py) module.

- [ImageTemplate](#imagetemplate)
  - [ImageTemplate](#imagetemplate-1)
    - [ImageTemplate().__call__](#imagetemplate()__call__)
    - [ImageTemplate().apply](#imagetemplate()apply)
    - [ImageTemplate().apply_to_dataset](#imagetemplate()apply_to_dataset)
    - [ImageTemplate().deserialize](#imagetemplate()deserialize)
    - [ImageTemplate().get_answer_choices_list](#imagetemplate()get_answer_choices_list)
    - [ImageTemplate().id](#imagetemplate()id)
    - [ImageTemplate().keywords](#imagetemplate()keywords)
    - [ImageTemplate().metadata](#imagetemplate()metadata)
    - [ImageTemplate().name](#imagetemplate()name)
    - [ImageTemplate().reference](#imagetemplate()reference)
    - [ImageTemplate().serialize](#imagetemplate()serialize)
    - [ImageTemplate().template](#imagetemplate()template)
    - [ImageTemplate().type](#imagetemplate()type)

## ImageTemplate

[Show source in image_template.py:15](../../../alfred/template/image_template.py#L15)

Template Class for Image data

The class generates queries for image data.

#### Signature

```python
class ImageTemplate(Template):
    def __init__(
        self,
        candidate_replacement: dict,
        template: str = "A photo of [[label]]",
        id: Optional[str] = None,
        name: Optional[str] = None,
        reference: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ): ...
```

#### See also

- [Template](./template.md#template)

### ImageTemplate().__call__

[Show source in image_template.py:204](../../../alfred/template/image_template.py#L204)

A wrapper function to apply the template to a single example

#### Arguments

- `example` - a single example in format of a dictionary
:type example: Dict
- `kawrgs` - Additional arguments to pass to apply
:type kawrgs: Any

#### Returns

a query object
Type: *Query*

#### Signature

```python
def __call__(
    self,
    example: Union[Image.Image, torch.tensor, np.ndarray, str, tuple],
    **kawrgs: Any
) -> Query: ...
```

### ImageTemplate().apply

[Show source in image_template.py:73](../../../alfred/template/image_template.py#L73)

Apply the template to a single image example

#### Arguments

- `example` - a single example in format of a dictionary
:type example: PIL Image, torch.tensor, numpy.ndarray, str, tuple
- `kwargs` - Additional arguments to pass to apply
:type kwargs: Any

#### Returns

a RankedQuery object
Type: *RankedQuery*

#### Signature

```python
def apply(
    self,
    example: Union[Image.Image, torch.tensor, np.ndarray, str, tuple],
    keyword: str = "image_path",
    **kwargs: Any
) -> RankedQuery: ...
```

### ImageTemplate().apply_to_dataset

[Show source in image_template.py:106](../../../alfred/template/image_template.py#L106)

A wrapper function to apply the template to a dataset iteratively

#### Arguments

- `dataset` - a dataset in format of a iterable of dictionary
:type dataset: Iterable[Dict]
- `kwargs` - Additional arguments to pass to apply
:type kwargs: Any

#### Returns

an iterable of query objects
Type: *Iterable[Query]*

#### Signature

```python
def apply_to_dataset(
    self, dataset: Iterable[Dict], **kwargs: Any
) -> Iterable[Query]: ...
```

### ImageTemplate().deserialize

[Show source in image_template.py:185](../../../alfred/template/image_template.py#L185)

returns a template object from a json string of dictionary

#### Arguments

- `json_str` - json string of dictionary to deserialize a string template
:type json_str: str

#### Returns

template object

#### Signature

```python
def deserialize(self, json_str: str) -> Template: ...
```

#### See also

- [Template](./template.md#template)

### ImageTemplate().get_answer_choices_list

[Show source in image_template.py:123](../../../alfred/template/image_template.py#L123)

Get answer choices list

#### Returns

answer choices list
Type: *List*

#### Signature

```python
def get_answer_choices_list(self) -> List[str]: ...
```

### ImageTemplate().id

[Show source in image_template.py:147](../../../alfred/template/image_template.py#L147)

returns the template id

#### Signature

```python
@property
def id(self): ...
```

### ImageTemplate().keywords

[Show source in image_template.py:142](../../../alfred/template/image_template.py#L142)

returns the keywords

#### Signature

```python
@property
def keywords(self): ...
```

### ImageTemplate().metadata

[Show source in image_template.py:162](../../../alfred/template/image_template.py#L162)

returns the template metadata

#### Signature

```python
@property
def metadata(self): ...
```

### ImageTemplate().name

[Show source in image_template.py:152](../../../alfred/template/image_template.py#L152)

returns the template name

#### Signature

```python
@property
def name(self): ...
```

### ImageTemplate().reference

[Show source in image_template.py:157](../../../alfred/template/image_template.py#L157)

returns the template reference

#### Signature

```python
@property
def reference(self): ...
```

### ImageTemplate().serialize

[Show source in image_template.py:167](../../../alfred/template/image_template.py#L167)

returns the template as a json string of dictionary

#### Returns

json string of dictionary
Type: *str*

#### Signature

```python
def serialize(self): ...
```

### ImageTemplate().template

[Show source in image_template.py:132](../../../alfred/template/image_template.py#L132)

returns the template

#### Signature

```python
@property
def template(self): ...
```

### ImageTemplate().type

[Show source in image_template.py:137](../../../alfred/template/image_template.py#L137)

returns the template type

#### Signature

```python
@property
def type(self): ...
```