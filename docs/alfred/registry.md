# Registry

[Alfred Index](../README.md#alfred-index) /
[Alfred](./index.md#alfred) /
Registry

> Auto-generated documentation for [alfred.registry](../../alfred/registry.py) module.

- [Registry](#registry)
  - [Registry](#registry-1)
    - [Registry().register](#registry()register)
    - [Registry().templates](#registry()templates)
    - [Registry().unregister](#registry()unregister)
    - [Registry().voters](#registry()voters)
  - [register](#register)
  - [templates](#templates)
  - [unregister](#unregister)
  - [voters](#voters)

## Registry

[Show source in registry.py:8](../../alfred/registry.py#L8)

#### Signature

```python
class Registry:
    def __init__(self):
        ...
```

### Registry().register

[Show source in registry.py:14](../../alfred/registry.py#L14)

#### Signature

```python
def register(self, cls: Union[Voter, Template]):
    ...
```

#### See also

- [Template](template/template.md#template)
- [Voter](voter/voter.md#voter)

### Registry().templates

[Show source in registry.py:38](../../alfred/registry.py#L38)

#### Signature

```python
@property
def templates(self):
    ...
```

### Registry().unregister

[Show source in registry.py:24](../../alfred/registry.py#L24)

#### Signature

```python
def unregister(self, cls: Union[Voter, Template]):
    ...
```

#### See also

- [Template](template/template.md#template)
- [Voter](voter/voter.md#voter)

### Registry().voters

[Show source in registry.py:34](../../alfred/registry.py#L34)

#### Signature

```python
@property
def voters(self):
    ...
```



## register

[Show source in registry.py:44](../../alfred/registry.py#L44)

#### Signature

```python
def register(cls: Union[Voter, Template]):
    ...
```

#### See also

- [Template](template/template.md#template)
- [Voter](voter/voter.md#voter)



## templates

[Show source in registry.py:56](../../alfred/registry.py#L56)

#### Signature

```python
def templates() -> List[Template]:
    ...
```



## unregister

[Show source in registry.py:48](../../alfred/registry.py#L48)

#### Signature

```python
def unregister(cls: Union[Voter, Template]):
    ...
```

#### See also

- [Template](template/template.md#template)
- [Voter](voter/voter.md#voter)



## voters

[Show source in registry.py:52](../../alfred/registry.py#L52)

#### Signature

```python
def voters() -> List[Voter]:
    ...
```


