# Template

[alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Template](./index.md#template) /
Template

> Auto-generated documentation for [alfred.template.template](../../../alfred/template/template.py) module.

- [Template](#template)
  - [Template](#template-1)
    - [Template().__call__](#template()__call__)
    - [Template().apply](#template()apply)
    - [Template().deserialize](#template()deserialize)
    - [Template().get_answer_choices_list](#template()get_answer_choices_list)
    - [Template().id](#template()id)
    - [Template().metadata](#template()metadata)
    - [Template().name](#template()name)
    - [Template().reference](#template()reference)
    - [Template().serialize](#template()serialize)
    - [Template().template](#template()template)
    - [Template().type](#template()type)
    - [Template().vote](#template()vote)

## Template

[Show source in template.py:7](../../../alfred/template/template.py#L7)

Generic interface for prompt template

The class mirros main functionality of promptsource's template
Please see https://github.com/bigscience-workshop/promptsource for more details

@misc{bach2022promptsource,
  title={PromptSource: An Integrated Development Environment and Repository for Natural Language Prompts},
  author={Stephen H. Bach and Victor Sanh and Zheng-Xin Yong and Albert Webson and Colin Raffel and Nihal V. Nayak and Abheesht Sharma and Taewoon Kim and M Saiful Bari and Thibault Fevry and Zaid Alyafeai and Manan Dey and Andrea Santilli and Zhiqing Sun and Srulik Ben-David and Canwen Xu and Gunjan Chhablani and Han Wang and Jason Alan Fries and Maged S. Al-shaibani and Shanya Sharma and Urmish Thakker and Khalid Almubarak and Xiangru Tang and Xiangru Tang and Mike Tian-Jian Jiang and Alexander M. Rush},
  year={2022},
  eprint={2202.01279},
  archivePrefix={arXiv},
  primaryClass={cs.LG}
}

#### Signature

```python
class Template(abc.ABC):
    ...
```

### Template().__call__

[Show source in template.py:100](../../../alfred/template/template.py#L100)

returns the template applied to the example, this allows a functional style

#### Signature

```python
def __call__(self, example):
    ...
```

### Template().apply

[Show source in template.py:85](../../../alfred/template/template.py#L85)

returns the template applied to the example

#### Signature

```python
@abc.abstractmethod
def apply(self, example):
    ...
```

### Template().deserialize

[Show source in template.py:95](../../../alfred/template/template.py#L95)

returns the deserialized version of the template

#### Signature

```python
@abc.abstractmethod
def deserialize(self, json_str):
    ...
```

### Template().get_answer_choices_list

[Show source in template.py:80](../../../alfred/template/template.py#L80)

returns the answer choices list of the template

#### Signature

```python
@abc.abstractmethod
def get_answer_choices_list(self, example):
    ...
```

### Template().id

[Show source in template.py:36](../../../alfred/template/template.py#L36)

returns the id of the template

#### Signature

```python
@property
@abc.abstractmethod
def id(self):
    ...
```

### Template().metadata

[Show source in template.py:54](../../../alfred/template/template.py#L54)

returns the metadata of the template

#### Signature

```python
@property
@abc.abstractmethod
def metadata(self):
    ...
```

### Template().name

[Show source in template.py:42](../../../alfred/template/template.py#L42)

returns the name of the template

#### Signature

```python
@property
@abc.abstractmethod
def name(self):
    ...
```

### Template().reference

[Show source in template.py:48](../../../alfred/template/template.py#L48)

returns the reference of the template

#### Signature

```python
@property
@abc.abstractmethod
def reference(self):
    ...
```

### Template().serialize

[Show source in template.py:90](../../../alfred/template/template.py#L90)

returns the serialized version of the template

#### Signature

```python
@abc.abstractmethod
def serialize(self):
    ...
```

### Template().template

[Show source in template.py:24](../../../alfred/template/template.py#L24)

returns the template string

#### Signature

```python
@property
@abc.abstractmethod
def template(self):
    ...
```

### Template().type

[Show source in template.py:30](../../../alfred/template/template.py#L30)

returns the type of the template

#### Signature

```python
@property
@abc.abstractmethod
def type(self):
    ...
```

### Template().vote

[Show source in template.py:60](../../../alfred/template/template.py#L60)

returns the vote of the template based on the responses with
the label maps and matching function

#### Arguments

- `responses` - the responses to be voted on
:type responses: Union[Response, str]
- `matching_function` - the matching function to be used
:type matching_function: Callable
- `label_maps` - (optional) the label maps to be used, this will overide the
                    default label maps of the template if it is initialized with one
:type label_maps: Dict

#### Signature

```python
@abc.abstractmethod
def vote(
    self,
    responses: Union[Response, str],
    matching_function: Callable,
    label_maps: Optional[Dict] = None,
):
    ...
```


