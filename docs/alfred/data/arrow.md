# Arrow

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Data](./index.md#data) /
Arrow

> Auto-generated documentation for [alfred.data.arrow](../../../alfred/data/arrow.py) module.

- [Arrow](#arrow)
  - [BufferedArrowDataset](#bufferedarrowdataset)
    - [BufferedArrowDataset().__getitem__](#bufferedarrowdataset()__getitem__)
    - [BufferedArrowDataset().__iter__](#bufferedarrowdataset()__iter__)
    - [BufferedArrowDataset().__len__](#bufferedarrowdataset()__len__)
    - [BufferedArrowDataset().__repr__](#bufferedarrowdataset()__repr__)
    - [BufferedArrowDataset().__version__](#bufferedarrowdataset()__version__)
    - [BufferedArrowDataset().data](#bufferedarrowdataset()data)
    - [BufferedArrowDataset().info](#bufferedarrowdataset()info)
    - [BufferedArrowDataset().load_from_disk](#bufferedarrowdataset()load_from_disk)
    - [BufferedArrowDataset().num_cols](#bufferedarrowdataset()num_cols)
    - [BufferedArrowDataset().num_rows](#bufferedarrowdataset()num_rows)
    - [BufferedArrowDataset().save_to_disk](#bufferedarrowdataset()save_to_disk)
    - [BufferedArrowDataset().shape](#bufferedarrowdataset()shape)
    - [BufferedArrowDataset().split](#bufferedarrowdataset()split)
    - [BufferedArrowDataset().version](#bufferedarrowdataset()version)
  - [IterableArrowDataset](#iterablearrowdataset)
    - [IterableArrowDataset().__getitem__](#iterablearrowdataset()__getitem__)
    - [IterableArrowDataset().__iter__](#iterablearrowdataset()__iter__)
    - [IterableArrowDataset().__len__](#iterablearrowdataset()__len__)
    - [IterableArrowDataset().__repr__](#iterablearrowdataset()__repr__)
    - [IterableArrowDataset().__version__](#iterablearrowdataset()__version__)
    - [IterableArrowDataset().columns](#iterablearrowdataset()columns)
    - [IterableArrowDataset().data](#iterablearrowdataset()data)
    - [IterableArrowDataset().info](#iterablearrowdataset()info)
    - [IterableArrowDataset().itercolumns](#iterablearrowdataset()itercolumns)
    - [IterableArrowDataset().load_from_disk](#iterablearrowdataset()load_from_disk)
    - [IterableArrowDataset().num_cols](#iterablearrowdataset()num_cols)
    - [IterableArrowDataset().num_rows](#iterablearrowdataset()num_rows)
    - [IterableArrowDataset.pyarrow_typer](#iterablearrowdatasetpyarrow_typer)
    - [IterableArrowDataset().save_to_disk](#iterablearrowdataset()save_to_disk)
    - [IterableArrowDataset().schema](#iterablearrowdataset()schema)
    - [IterableArrowDataset().shape](#iterablearrowdataset()shape)
    - [IterableArrowDataset().split](#iterablearrowdataset()split)
    - [IterableArrowDataset().version](#iterablearrowdataset()version)

## BufferedArrowDataset

[Show source in arrow.py:203](../../../alfred/data/arrow.py#L203)

This class represents a dataset stored in a pyarrow buffer.
It provides methods for accessing and iterating over the data,
as well as for saving and loading the dataset to and from disk.

This will be very useful for datasets that are too large to fit into memory.

Properties:

- shape (Tuple[int, int]): The shape of the dataset (number of rows and columns).
- num_rows (int): The number of rows in the dataset.
- num_cols (int): The number of columns in the dataset.

#### Methods

- `-` *data()* - Return the underlying pyarrow Table.
- `-` *info()* - Return the metadata about the dataset.
- `-` *split()* - Return the information about how the dataset has been split.
- `-` *version()* - Return the version of the dataset.
- `-` *__len__()* - Return the number of rows in the dataset.
- `-` *__getitem__(uid)* - Return the row with the given unique identifier.
- `-` *__iter__()* - Iterate over the rows of the dataset, yielding a dictionary for each row.
- `-` *save_to_disk(path* - str): Save the dataset to disk at the specified path.
- `-` *load_from_disk(path* - str): Load the dataset from disk from the specified path.

#### Signature

```python
class BufferedArrowDataset(Dataset):
    def __init__(
        self,
        buffer: pyarrow.Buffer,
        info: Optional[DatasetInfo] = None,
        split: Optional[Union[str, NamedSplit]] = None,
    ):
        ...
```

### BufferedArrowDataset().__getitem__

[Show source in arrow.py:291](../../../alfred/data/arrow.py#L291)

Retuns the row with the given unique identifier.

#### Arguments

- `uid` - The unique identifier of the row to return.
:type uid: int or slice
- `kawrgs` - Additional keyword arguments.
:type kawrgs: Any

#### Returns

The row with the given unique identifier.
Type: *Dict[str, Any]*

#### Signature

```python
def __getitem__(self, uid: int, **kawrgs: Any) -> Dict[str, Any]:
    ...
```

### BufferedArrowDataset().__iter__

[Show source in arrow.py:304](../../../alfred/data/arrow.py#L304)

Iterator over the rows of the dataset, yielding a dictionary for each row.

#### Returns

An iterator over the rows of the dataset, yielding a dictionary for each row.
Type: *Iterable*

#### Signature

```python
def __iter__(self) -> Iterable:
    ...
```

### BufferedArrowDataset().__len__

[Show source in arrow.py:287](../../../alfred/data/arrow.py#L287)

returns the number of rows in the dataset

#### Signature

```python
def __len__(self) -> int:
    ...
```

### BufferedArrowDataset().__repr__

[Show source in arrow.py:315](../../../alfred/data/arrow.py#L315)

returns a string representation of the dataset

#### Signature

```python
def __repr__(self):
    ...
```

### BufferedArrowDataset().__version__

[Show source in arrow.py:283](../../../alfred/data/arrow.py#L283)

returns the version of the dataset

#### Signature

```python
def __version__(self) -> str:
    ...
```

### BufferedArrowDataset().data

[Show source in arrow.py:267](../../../alfred/data/arrow.py#L267)

returns the underlying pyarrow Table

#### Signature

```python
def data(self):
    ...
```

### BufferedArrowDataset().info

[Show source in arrow.py:271](../../../alfred/data/arrow.py#L271)

returns the metadata about the dataset

#### Signature

```python
def info(self):
    ...
```

### BufferedArrowDataset().load_from_disk

[Show source in arrow.py:323](../../../alfred/data/arrow.py#L323)

loads the dataset from disk from the specified path

#### Signature

```python
def load_from_disk(self, path: str):
    ...
```

### BufferedArrowDataset().num_cols

[Show source in arrow.py:262](../../../alfred/data/arrow.py#L262)

returns the number of columns in the dataset

#### Signature

```python
@property
def num_cols(self) -> int:
    ...
```

### BufferedArrowDataset().num_rows

[Show source in arrow.py:257](../../../alfred/data/arrow.py#L257)

returns the number of rows in the dataset

#### Signature

```python
@property
def num_rows(self) -> int:
    ...
```

### BufferedArrowDataset().save_to_disk

[Show source in arrow.py:319](../../../alfred/data/arrow.py#L319)

saves the dataset to disk at the specified path

#### Signature

```python
def save_to_disk(self, path: str):
    ...
```

### BufferedArrowDataset().shape

[Show source in arrow.py:252](../../../alfred/data/arrow.py#L252)

returns the shape of the dataset (number of rows and columns)

#### Signature

```python
@property
def shape(self) -> Tuple[int, int]:
    ...
```

### BufferedArrowDataset().split

[Show source in arrow.py:275](../../../alfred/data/arrow.py#L275)

returns the information about how the dataset has been split

#### Signature

```python
def split(self):
    ...
```

### BufferedArrowDataset().version

[Show source in arrow.py:279](../../../alfred/data/arrow.py#L279)

returns the version of the dataset

#### Signature

```python
def version(self) -> str:
    ...
```



## IterableArrowDataset

[Show source in arrow.py:11](../../../alfred/data/arrow.py#L11)

This class represents a dataset stored in a pyarrow Table or pandas DataFrame. It provides methods for accessing and iterating over the data, as well as for saving and loading the dataset to and from disk.

Properties:
- shape (Tuple[int, int]): The shape of the dataset (number of rows and columns).
- num_rows (int): The number of rows in the dataset.
- num_cols (int): The number of columns in the dataset.
- schema (pyarrow.Schema): The schema of the table and its columns.
- columns (List[pa.ChunkedArray]): A list of all columns in numerical order.

#### Methods

- `-` *data()* - Return the underlying pyarrow Table or pandas DataFrame.
- `-` *info()* - Return the metadata about the dataset.
- `-` *split()* - Return the information about how the dataset has been split.
- `-` *version()* - Return the version of the dataset.
- `-` *__len__()* - Return the number of rows in the dataset.
- `-` *__getitem__(uid)* - Return the row with the given unique identifier.
- itercolumns(*args, **kwargs): Iterate over all columns in their numerical order.
- `-` *__iter__()* - Iterate over the rows of the dataset, yielding a dictionary for each row.
- `-` *save_to_disk(path* - str): Save the dataset to disk at the specified path.
- `-` *load_from_disk(path* - str): Load the dataset from disk from the specified path.

#### Signature

```python
class IterableArrowDataset(Dataset):
    def __init__(
        self,
        table: Union[pyarrow.Table, pandas.DataFrame],
        info: Optional[DatasetInfo] = None,
        split: Optional[Union[str, NamedSplit]] = None,
    ):
        ...
```

### IterableArrowDataset().__getitem__

[Show source in arrow.py:144](../../../alfred/data/arrow.py#L144)

Return the row with the given unique identifier.

#### Arguments

- `uid` - The unique identifier of the row to return.
:type uid: int or slice
- `kawrgs` - Additional keyword arguments.
:type kawrgs: Any

#### Returns

The row with the given unique identifier.
Type: *Dict[str, Any]*

#### Signature

```python
def __getitem__(self, uid: int, **kawrgs: Any) -> Dict[str, Any]:
    ...
```

### IterableArrowDataset().__iter__

[Show source in arrow.py:179](../../../alfred/data/arrow.py#L179)

Iterator over the rows of the dataset, yielding a dictionary for each row.

#### Returns

An iterator over the rows of the dataset, yielding a dictionary for each row.
Type: *Iterable[Dict]*

#### Signature

```python
def __iter__(self) -> Iterable[Dict]:
    ...
```

### IterableArrowDataset().__len__

[Show source in arrow.py:140](../../../alfred/data/arrow.py#L140)

returns the number of rows in the dataset

#### Signature

```python
def __len__(self) -> int:
    ...
```

### IterableArrowDataset().__repr__

[Show source in arrow.py:190](../../../alfred/data/arrow.py#L190)

returns a string representation of the dataset

#### Signature

```python
def __repr__(self):
    ...
```

### IterableArrowDataset().__version__

[Show source in arrow.py:136](../../../alfred/data/arrow.py#L136)

returns the version of the dataset

#### Signature

```python
def __version__(self) -> str:
    ...
```

### IterableArrowDataset().columns

[Show source in arrow.py:105](../../../alfred/data/arrow.py#L105)

Columns of the dataset.

#### Returns

A list of all columns in numerical order.
Type: *List[pyarrow.ChunkedArray]*

#### Signature

```python
@property
def columns(self) -> List[pyarrow.ChunkedArray]:
    ...
```

### IterableArrowDataset().data

[Show source in arrow.py:115](../../../alfred/data/arrow.py#L115)

Return the underlying pyarrow Table or pandas DataFrame.

#### Returns

The underlying pyarrow Table or pandas DataFrame.
Type: *Union[pyarrow.Table, pandas.DataFrame]*

#### Signature

```python
def data(self) -> Union[pyarrow.Table, pandas.DataFrame]:
    ...
```

### IterableArrowDataset().info

[Show source in arrow.py:124](../../../alfred/data/arrow.py#L124)

returns the metadata about the dataset

#### Signature

```python
def info(self) -> DatasetInfo:
    ...
```

### IterableArrowDataset().itercolumns

[Show source in arrow.py:168](../../../alfred/data/arrow.py#L168)

Iterator over all columns in their numerical order.

#### Arguments

- `args` - Additional arguments.
:type args: Any
- `kwargs` - Additional keyword arguments.
:type kwargs: Any

#### Signature

```python
def itercolumns(self, *args: Any, **kwargs: Any) -> Iterable:
    ...
```

### IterableArrowDataset().load_from_disk

[Show source in arrow.py:198](../../../alfred/data/arrow.py#L198)

loads the dataset from disk from the specified path

#### Signature

```python
def load_from_disk(self, path: str):
    ...
```

### IterableArrowDataset().num_cols

[Show source in arrow.py:90](../../../alfred/data/arrow.py#L90)

returns the number of columns in the dataset

#### Signature

```python
@property
def num_cols(self) -> int:
    ...
```

### IterableArrowDataset().num_rows

[Show source in arrow.py:85](../../../alfred/data/arrow.py#L85)

returns the number of rows in the dataset

#### Signature

```python
@property
def num_rows(self) -> int:
    ...
```

### IterableArrowDataset.pyarrow_typer

[Show source in arrow.py:59](../../../alfred/data/arrow.py#L59)

Recognize the type of the data and find the according pyarrow type.

#### Arguments

- [IterableArrowDataset().data](#iterablearrowdatasetdata) - The data to recognize the type of.
:type data: Any

#### Returns

The pyarrow type of the data.
Type: *pyarrow.DataType*

#### Signature

```python
@staticmethod
def pyarrow_typer(data: Any) -> pyarrow.DataType:
    ...
```

### IterableArrowDataset().save_to_disk

[Show source in arrow.py:194](../../../alfred/data/arrow.py#L194)

saves the dataset to disk at the specified path

#### Signature

```python
def save_to_disk(self, path: str):
    ...
```

### IterableArrowDataset().schema

[Show source in arrow.py:95](../../../alfred/data/arrow.py#L95)

Schema of the table and its columns.

#### Returns

The schema of the table and its columns.
Type: *pyarrow.Schema*

#### Signature

```python
@property
def schema(self) -> pyarrow.Schema:
    ...
```

### IterableArrowDataset().shape

[Show source in arrow.py:80](../../../alfred/data/arrow.py#L80)

returns the shape of the dataset (number of rows and columns)

#### Signature

```python
@property
def shape(self) -> Tuple[int, int]:
    ...
```

### IterableArrowDataset().split

[Show source in arrow.py:128](../../../alfred/data/arrow.py#L128)

returns the information about how the dataset has been split

#### Signature

```python
def split(self) -> NamedSplit:
    ...
```

### IterableArrowDataset().version

[Show source in arrow.py:132](../../../alfred/data/arrow.py#L132)

returns the version of the dataset

#### Signature

```python
def version(self) -> str:
    ...
```


