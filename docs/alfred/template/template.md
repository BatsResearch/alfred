# Template

[Alfred Index](../../README.md#alfred-index) /
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
    - [Template().keywords](#template()keywords)
    - [Template().metadata](#template()metadata)
    - [Template().name](#template()name)
    - [Template().reference](#template()reference)
    - [Template().serialize](#template()serialize)
    - [Template().template](#template()template)
    - [Template().type](#template()type)

## Template

[Show source in template.py:4](../../../alfred/template/template.py#L4)

Generic interface for prompt template

The class mirrors main functionality of promptsource's template
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

[Show source in template.py:83](../../../alfred/template/template.py#L83)

returns the template applied to the example, this allows a functional style

#### Signature

```python
def __call__(self, example):
    ...
```

### Template().apply

[Show source in template.py:68](../../../alfred/template/template.py#L68)

returns the template applied to the example

#### Signature

```python
@abc.abstractmethod
def apply(self, example):
    ...
```

### Template().deserialize

[Show source in template.py:78](../../../alfred/template/template.py#L78)

returns the deserialized version of the template

#### Signature

```python
@abc.abstractmethod
def deserialize(self, json_str):
    ...
```

### Template().get_answer_choices_list

[Show source in template.py:63](../../../alfred/template/template.py#L63)

returns the answer choices list of the template

#### Signature

```python
@abc.abstractmethod
def get_answer_choices_list(self, example):
    ...
```

### Template().id

[Show source in template.py:39](../../../alfred/template/template.py#L39)

returns the id of the template

#### Signature

```python
@property
@abc.abstractmethod
def id(self):
    ...
```

### Template().keywords

[Show source in template.py:33](../../../alfred/template/template.py#L33)

returns the keywords of the template

#### Signature

```python
@property
@abc.abstractmethod
def keywords(self):
    ...
```

### Template().metadata

[Show source in template.py:57](../../../alfred/template/template.py#L57)

returns the metadata of the template

#### Signature

```python
@property
@abc.abstractmethod
def metadata(self):
    ...
```

### Template().name

[Show source in template.py:45](../../../alfred/template/template.py#L45)

returns the name of the template

#### Signature

```python
@property
@abc.abstractmethod
def name(self):
    ...
```

### Template().reference

[Show source in template.py:51](../../../alfred/template/template.py#L51)

returns the reference of the template

#### Signature

```python
@property
@abc.abstractmethod
def reference(self):
    ...
```

### Template().serialize

[Show source in template.py:73](../../../alfred/template/template.py#L73)

returns the serialized version of the template

#### Signature

```python
@abc.abstractmethod
def serialize(self):
    ...
```

### Template().template

[Show source in template.py:21](../../../alfred/template/template.py#L21)

returns the template string

#### Signature

```python
@property
@abc.abstractmethod
def template(self):
    ...
```

### Template().type

[Show source in template.py:27](../../../alfred/template/template.py#L27)

returns the type of the template

#### Signature

```python
@property
@abc.abstractmethod
def type(self):
    ...
```