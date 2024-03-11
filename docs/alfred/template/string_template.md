# StringTemplate

[Alfred Index](../../README.md#alfred-index) / [Alfred](../index.md#alfred) / [Template](./index.md#template) / StringTemplate

> Auto-generated documentation for [alfred.template.string_template](../../../alfred/template/string_template.py) module.

- [StringTemplate](#stringtemplate)
  - [StringTemplate](#stringtemplate-1)
    - [StringTemplate().__call__](#stringtemplate()__call__)
    - [StringTemplate().apply](#stringtemplate()apply)
    - [StringTemplate().apply_to_dataset](#stringtemplate()apply_to_dataset)
    - [StringTemplate().deserialize](#stringtemplate()deserialize)
    - [StringTemplate().from_promptsource](#stringtemplate()from_promptsource)
    - [StringTemplate().get_answer_choices_list](#stringtemplate()get_answer_choices_list)
    - [StringTemplate().id](#stringtemplate()id)
    - [StringTemplate().keywords](#stringtemplate()keywords)
    - [StringTemplate().metadata](#stringtemplate()metadata)
    - [StringTemplate().name](#stringtemplate()name)
    - [StringTemplate().reference](#stringtemplate()reference)
    - [StringTemplate().serialize](#stringtemplate()serialize)
    - [StringTemplate().template](#stringtemplate()template)
    - [StringTemplate().type](#stringtemplate()type)

## StringTemplate

[Show source in string_template.py:15](../../../alfred/template/string_template.py#L15)

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
    Prompt: "Does the [[animal]] have stripes?"

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
        answer_choices: Optional[Union[str, List[str]]] = None,
    ): ...
```

#### See also

- [Template](./template.md#template)

### StringTemplate().__call__

[Show source in string_template.py:290](../../../alfred/template/string_template.py#L290)

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
def __call__(self, example: Dict, **kawrgs: Any) -> Query: ...
```

### StringTemplate().apply

[Show source in string_template.py:123](../../../alfred/template/string_template.py#L123)

Apply template to an example or a list of examples and returns a query object or a list of queries

#### Arguments

- `example` - list of examples or an example in format of dictionary
:type example: Union[Dict, List[Dict]]
- `kawrgs` - "key_translator" for key translation (e.g. for fields key replacements)
:type kawrgs: Dict

#### Returns

one or a list of query object (either CompletionQuery or RankedQuery depending on the template type)
Type: *Query or List[Query]*

#### Signature

```python
def apply(
    self, example: Union[Dict, List[Dict]], **kawrgs
) -> Union[Query, List[Query]]: ...
```

### StringTemplate().apply_to_dataset

[Show source in string_template.py:192](../../../alfred/template/string_template.py#L192)

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

### StringTemplate().deserialize

[Show source in string_template.py:271](../../../alfred/template/string_template.py#L271)

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

### StringTemplate().from_promptsource

[Show source in string_template.py:109](../../../alfred/template/string_template.py#L109)

Update the template from a promptsource template

#### Arguments

- `promptsource_template` - a promptsource template
:type promptsource_template: Dict

#### Signature

```python
def from_promptsource(self, promptsource_template): ...
```

### StringTemplate().get_answer_choices_list

[Show source in string_template.py:209](../../../alfred/template/string_template.py#L209)

Get answer choices list

#### Returns

answer choices list
Type: *List*

#### Signature

```python
def get_answer_choices_list(self) -> List[str]: ...
```

### StringTemplate().id

[Show source in string_template.py:233](../../../alfred/template/string_template.py#L233)

returns the template id

#### Signature

```python
@property
def id(self): ...
```

### StringTemplate().keywords

[Show source in string_template.py:228](../../../alfred/template/string_template.py#L228)

returns the keywords

#### Signature

```python
@property
def keywords(self): ...
```

### StringTemplate().metadata

[Show source in string_template.py:248](../../../alfred/template/string_template.py#L248)

returns the template metadata

#### Signature

```python
@property
def metadata(self): ...
```

### StringTemplate().name

[Show source in string_template.py:238](../../../alfred/template/string_template.py#L238)

returns the template name

#### Signature

```python
@property
def name(self): ...
```

### StringTemplate().reference

[Show source in string_template.py:243](../../../alfred/template/string_template.py#L243)

returns the template reference

#### Signature

```python
@property
def reference(self): ...
```

### StringTemplate().serialize

[Show source in string_template.py:253](../../../alfred/template/string_template.py#L253)

returns the template as a json string of dictionary

#### Returns

json string of dictionary
Type: *str*

#### Signature

```python
def serialize(self): ...
```

### StringTemplate().template

[Show source in string_template.py:218](../../../alfred/template/string_template.py#L218)

returns the template

#### Signature

```python
@property
def template(self): ...
```

### StringTemplate().type

[Show source in string_template.py:223](../../../alfred/template/string_template.py#L223)

returns the template type

#### Signature

```python
@property
def type(self): ...
```