# Dataset

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Data](./index.md#data) /
Dataset

> Auto-generated documentation for [alfred.data.dataset](../../../alfred/data/dataset.py) module.

- [Dataset](#dataset)
  - [Dataset](#dataset-1)
    - [Dataset().__getitem__](#dataset()__getitem__)
    - [Dataset().__iter__](#dataset()__iter__)
    - [Dataset().__len__](#dataset()__len__)
    - [Dataset().__version__](#dataset()__version__)
    - [Dataset().data](#dataset()data)
    - [Dataset().info](#dataset()info)
    - [Dataset.load_from_disk](#datasetload_from_disk)
    - [Dataset.save_to_disk](#datasetsave_to_disk)
    - [Dataset().split](#dataset()split)
    - [Dataset().version](#dataset()version)

## Dataset

[Show source in dataset.py:4](../../../alfred/data/dataset.py#L4)

This is a generic interface for dataset classes that mirrors key interfaces from huggingface datasets. It provides methods for accessing and iterating over the data, as well as for saving and loading the dataset to and from disk.

Properties:

- shape (Tuple[int, int]): The shape of the dataset (number of rows and columns).
- info (DatasetInfo): The metadata of the dataset.
- split (NamedSplit): The information about how the dataset has been split.
- version (str): The version of the dataset.

#### Methods

- `-` *data()* - Return the underlying data.
- `-` *info()* - Return the metadata about the dataset.
- `-` *split()* - Return the information about how the dataset has been split.
- `-` *__len__()* - Return the number of rows in the dataset.
- `-` *__getitem__(uid)* - Return the row with the given unique identifier.
- `-` *__iter__()* - Iterate over the rows of the dataset.
- `-` *__version__()* - Return the version of the dataset.
- `-` *version* - Return the version of the dataset.
- `-` *save_to_disk(path* - str): Save the dataset to disk at the specified path.
- `-` *load_from_disk(path* - str): Load the dataset from disk from the specified path.

#### Signature

```python
class Dataset(abc.ABC):
    ...
```

### Dataset().__getitem__

[Show source in dataset.py:51](../../../alfred/data/dataset.py#L51)

returns the row with the given unique identifier

#### Signature

```python
@abc.abstractmethod
def __getitem__(self, uid, **kawrgs):
    ...
```

### Dataset().__iter__

[Show source in dataset.py:56](../../../alfred/data/dataset.py#L56)

iterates over the rows of the dataset

#### Signature

```python
@abc.abstractmethod
def __iter__(self):
    ...
```

### Dataset().__len__

[Show source in dataset.py:46](../../../alfred/data/dataset.py#L46)

returns the number of rows in the dataset

#### Signature

```python
@abc.abstractmethod
def __len__(self) -> int:
    ...
```

### Dataset().__version__

[Show source in dataset.py:61](../../../alfred/data/dataset.py#L61)

returns the version of the dataset

#### Signature

```python
@abc.abstractmethod
def __version__(self) -> str:
    ...
```

### Dataset().data

[Show source in dataset.py:28](../../../alfred/data/dataset.py#L28)

returns the underlying data

#### Signature

```python
@property
@abc.abstractmethod
def data(self):
    ...
```

### Dataset().info

[Show source in dataset.py:34](../../../alfred/data/dataset.py#L34)

returns the metadata about the dataset

#### Signature

```python
@property
@abc.abstractmethod
def info(self):
    ...
```

### Dataset.load_from_disk

[Show source in dataset.py:76](../../../alfred/data/dataset.py#L76)

loads the dataset from disk from the specified path

#### Signature

```python
@staticmethod
def load_from_disk(self, path: str):
    ...
```

### Dataset.save_to_disk

[Show source in dataset.py:71](../../../alfred/data/dataset.py#L71)

saves the dataset to disk at the specified path

#### Signature

```python
@staticmethod
def save_to_disk(self, path: str):
    ...
```

### Dataset().split

[Show source in dataset.py:40](../../../alfred/data/dataset.py#L40)

returns the information about how the dataset has been split

#### Signature

```python
@property
@abc.abstractmethod
def split(self):
    ...
```

### Dataset().version

[Show source in dataset.py:66](../../../alfred/data/dataset.py#L66)

returns the version of the dataset

#### Signature

```python
@property
def version(self) -> str:
    ...
```


