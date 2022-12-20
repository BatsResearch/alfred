# StringTemplate

[alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Template](./index.md#template) /
StringTemplate

> Auto-generated documentation for [alfred.template.string_template](../../../alfred/template/string_template.py) module.

- [StringTemplate](#stringtemplate)
  - [StringTemplate](#stringtemplate-1)
    - [StringTemplate().__call__](#stringtemplate()__call__)
    - [StringTemplate().apply](#stringtemplate()apply)
    - [StringTemplate().apply_to_dataset](#stringtemplate()apply_to_dataset)
    - [StringTemplate().deserialize](#stringtemplate()deserialize)
    - [StringTemplate().get_answer_choices_list](#stringtemplate()get_answer_choices_list)
    - [StringTemplate().id](#stringtemplate()id)
    - [StringTemplate().metadata](#stringtemplate()metadata)
    - [StringTemplate().name](#stringtemplate()name)
    - [StringTemplate().reference](#stringtemplate()reference)
    - [StringTemplate().serialize](#stringtemplate()serialize)
    - [StringTemplate().template](#stringtemplate()template)
    - [StringTemplate().type](#stringtemplate()type)
    - [StringTemplate().vote](#stringtemplate()vote)

## StringTemplate

[Show source in string_template.py:16](../../../alfred/template/string_template.py#L16)

Prompt Template Class for Common Static Templates

The class handles ranked scoring and completion queries for static templates.

.. note

```python
On partial label integration:
Partial Label vote is implicitly integrated in the template.
Users will need to specify the label maps for the partial label group numbers.
    e.g.
    Rule: Predict "stripe" attributes for labels [zebra, tigers].
    Label Numerical: {"zebra": 1, "tiger": 2, "horse": 3}
    Prompt: "Does the [animal] have stripes?"

    answer_choices: "yes|||no"
    labels_map: {"yes": 2, "no": 1}

    The partial label partition would be: [[3], [1,2]]
```

#### Methods

- `apply` - apply template to an example and returns a query object
- `vote` - vote for the responses based on the matching function and the label maps
- `update_template` - update template

Properties:
    - `template` - template
    - `type` - type of the template
    - `id` - id of the template
    - `name` - name of the template
    - `reference` - reference
    - `metadata` - metadata

#### Signature

```python
class StringTemplate(Template):
    def __init__(
        self,
        template: str,
        id: Optional[str] = None,
        name: Optional[str] = None,
        reference: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        answer_choices: Optional[str] = None,
        label_maps: Optional[Dict] = None,
        matching_fn: Optional[Callable] = lambda x, y,: x == y,
    ):
        ...
```

#### See also

- [Template](./template.md#template)

### StringTemplate().__call__

[Show source in string_template.py:327](../../../alfred/template/string_template.py#L327)

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
def __call__(self, example: Dict, **kawrgs: Any) -> Query:
    ...
```

### StringTemplate().apply

[Show source in string_template.py:112](../../../alfred/template/string_template.py#L112)

Apply template to an example and returns a query object

#### Arguments

- `example` - an example in format of dictionary
:type example: Dict
- `kawrgs` - "key_translator" for key translation (e.g. for fields key replacements)
:type kawrgs: Dict

#### Returns

query object (either CompletionQuery or RankedQuery depending on the template type)
Type: *Query*

#### Signature

```python
def apply(self, example: Dict, **kawrgs) -> Query:
    ...
```

### StringTemplate().apply_to_dataset

[Show source in string_template.py:174](../../../alfred/template/string_template.py#L174)

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
def apply_to_dataset(self, dataset: Iterable[Dict], **kwargs: Any) -> Iterable[Query]:
    ...
```

### StringTemplate().deserialize

[Show source in string_template.py:308](../../../alfred/template/string_template.py#L308)

returns a template object from a json string of dictionary

#### Arguments

- `json_str` - json string of dictionary to deserialize a string template
:type json_str: str

#### Returns

template object

#### Signature

```python
def deserialize(self, json_str: str) -> Template:
    ...
```

#### See also

- [Template](./template.md#template)

### StringTemplate().get_answer_choices_list

[Show source in string_template.py:256](../../../alfred/template/string_template.py#L256)

Get answer choices list

#### Returns

answer choices list
Type: *List*

#### Signature

```python
def get_answer_choices_list(self) -> List[str]:
    ...
```

### StringTemplate().id

[Show source in string_template.py:273](../../../alfred/template/string_template.py#L273)

returns the template id

#### Signature

```python
def id(self):
    ...
```

### StringTemplate().metadata

[Show source in string_template.py:285](../../../alfred/template/string_template.py#L285)

returns the template metadata

#### Signature

```python
def metadata(self):
    ...
```

### StringTemplate().name

[Show source in string_template.py:277](../../../alfred/template/string_template.py#L277)

returns the template name

#### Signature

```python
def name(self):
    ...
```

### StringTemplate().reference

[Show source in string_template.py:281](../../../alfred/template/string_template.py#L281)

returns the template reference

#### Signature

```python
def reference(self):
    ...
```

### StringTemplate().serialize

[Show source in string_template.py:289](../../../alfred/template/string_template.py#L289)

returns the template as a json string of dictionary

#### Returns

json string of dictionary
Type: *str*

#### Signature

```python
def serialize(self):
    ...
```

### StringTemplate().template

[Show source in string_template.py:265](../../../alfred/template/string_template.py#L265)

returns the template

#### Signature

```python
def template(self):
    ...
```

### StringTemplate().type

[Show source in string_template.py:269](../../../alfred/template/string_template.py#L269)

returns the template type

#### Signature

```python
def type(self):
    ...
```

### StringTemplate().vote

[Show source in string_template.py:190](../../../alfred/template/string_template.py#L190)

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
- `label_maps` - (optional) label maps that maps responses content to labels
                   label_maps specified here will overide the label_maps initialized in the template
:type label_maps: Dict

#### Returns

numpy ndarray of votes in np.int8
Type: *np.ndarray*

#### Signature

```python
def vote(
    self,
    responses: Union[Iterable[str], str, Iterable[Response], Response],
    matching_function: Callable = lambda x, y,: x == y,
    label_maps: Optional[Dict] = None,
    **kwargs: Any
) -> np.ndarray:
    ...
```


