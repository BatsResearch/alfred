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
    - [StringTemplate().set_chat_template](#stringtemplate()set_chat_template)
    - [StringTemplate.set_global_chat_template](#stringtemplateset_global_chat_template)
    - [StringTemplate().template](#stringtemplate()template)
    - [StringTemplate().type](#stringtemplate()type)
    - [StringTemplate().unset_chat_template](#stringtemplate()unset_chat_template)
    - [StringTemplate.unset_global_chat_template](#stringtemplateunset_global_chat_template)

## StringTemplate

[Show source in string_template.py:20](../../../alfred/template/string_template.py#L20)

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
        chat_template: Optional[Union[str, Dict]] = None,
    ): ...
```

### StringTemplate().__call__

[Show source in string_template.py:402](../../../alfred/template/string_template.py#L402)

A wrapper function to apply the template to a single example

#### Arguments

- `example` - a single example in format of a dictionary
:type example: Dict
- `kwargs` - Additional arguments to pass to apply
:type kwargs: Any

#### Returns

a query object
Type: *Query*

#### Signature

```python
def __call__(self, example: Dict, **kwargs: Any) -> Query: ...
```

### StringTemplate().apply

[Show source in string_template.py:203](../../../alfred/template/string_template.py#L203)

Apply template to an example or a list of examples and returns a query object or a list of queries

#### Arguments

- `example` - list of examples or an example in format of dictionary
:type example: Union[Dict, List[Dict]]
- `kwargs` - "key_translator" for key translation (e.g. for fields key replacements)
:type kwargs: Dict

#### Returns

one or a list of query object (either CompletionQuery or RankedQuery depending on the template type)
Type: *Query or List[Query]*

#### Signature

```python
def apply(
    self, example: Union[Dict, List[Dict]], **kwargs
) -> Union[Query, List[Query]]: ...
```

### StringTemplate().apply_to_dataset

[Show source in string_template.py:293](../../../alfred/template/string_template.py#L293)

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

[Show source in string_template.py:382](../../../alfred/template/string_template.py#L382)

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

### StringTemplate().from_promptsource

[Show source in string_template.py:188](../../../alfred/template/string_template.py#L188)

Update the template from a promptsource template

#### Arguments

- `promptsource_template` - a promptsource template
:type promptsource_template: Dict

#### Signature

```python
def from_promptsource(self, promptsource_template): ...
```

### StringTemplate().get_answer_choices_list

[Show source in string_template.py:311](../../../alfred/template/string_template.py#L311)

Get answer choices list

#### Returns

answer choices list
Type: *List*

#### Signature

```python
def get_answer_choices_list(self) -> List[str]: ...
```

### StringTemplate().id

[Show source in string_template.py:339](../../../alfred/template/string_template.py#L339)

returns the template id

#### Signature

```python
@property
def id(self): ...
```

### StringTemplate().keywords

[Show source in string_template.py:333](../../../alfred/template/string_template.py#L333)

returns the keywords

#### Signature

```python
@property
def keywords(self): ...
```

### StringTemplate().metadata

[Show source in string_template.py:357](../../../alfred/template/string_template.py#L357)

returns the template metadata

#### Signature

```python
@property
def metadata(self): ...
```

### StringTemplate().name

[Show source in string_template.py:345](../../../alfred/template/string_template.py#L345)

returns the template name

#### Signature

```python
@property
def name(self): ...
```

### StringTemplate().reference

[Show source in string_template.py:351](../../../alfred/template/string_template.py#L351)

returns the template reference

#### Signature

```python
@property
def reference(self): ...
```

### StringTemplate().serialize

[Show source in string_template.py:363](../../../alfred/template/string_template.py#L363)

returns the template as a json string of dictionary

#### Returns

json string of dictionary
Type: *str*

#### Signature

```python
def serialize(self): ...
```

### StringTemplate().set_chat_template

[Show source in string_template.py:134](../../../alfred/template/string_template.py#L134)

Set instance-specific chat template, overriding any global template.

#### Arguments

- `chat_template` - chat template to apply

                                - it can either be a model family name (e.g. "llama", "mistral", "gemma", "phi", "qwen", "alpaca")
                                - or a dictionary of chat templates
                                    e.g.
                                    chat_templates = {
                                            "system": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{system_instruction}<|eot_id|>
",
                                            "prefix": " <|start_header_id|>user<|end_header_id|> ",
                                            "suffix": " <|eot_id|>

<|start_header_id|>assistant<|end_header_id|> ",
                                            }
        :type chat_template: Union[str, Dict]

#### Signature

```python
def set_chat_template(self, chat_template: Union[str, Dict]): ...
```

### StringTemplate.set_global_chat_template

[Show source in string_template.py:160](../../../alfred/template/string_template.py#L160)

Set global chat template to apply to all instances of the template.

#### Arguments

- `chat_template` - chat template to apply

                                - it can either be a model family name (e.g. "llama", "mistral", "gemma", "phi", "qwen", "alpaca")
                                - or a dictionary of chat templates
                                    e.g.
                                    chat_templates = {
                                            "system": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{system_instruction}<|eot_id|>
",
                                            "prefix": " <|start_header_id|>user<|end_header_id|> ",
                                            "suffix": " <|eot_id|>

<|start_header_id|>assistant<|end_header_id|> ",
                                            }
        :type chat_template: Union[str, Dict]

#### Signature

```python
@classmethod
def set_global_chat_template(cls, chat_template: Union[str, Dict]): ...
```

### StringTemplate().template

[Show source in string_template.py:321](../../../alfred/template/string_template.py#L321)

returns the template

#### Signature

```python
@property
def template(self): ...
```

### StringTemplate().type

[Show source in string_template.py:327](../../../alfred/template/string_template.py#L327)

returns the template type

#### Signature

```python
@property
def type(self): ...
```

### StringTemplate().unset_chat_template

[Show source in string_template.py:153](../../../alfred/template/string_template.py#L153)

Remove instance-specific chat template, reverting to global template if available.

#### Signature

```python
def unset_chat_template(self): ...
```

### StringTemplate.unset_global_chat_template

[Show source in string_template.py:180](../../../alfred/template/string_template.py#L180)

Remove global chat template.

#### Signature

```python
@classmethod
def unset_global_chat_template(cls): ...
```