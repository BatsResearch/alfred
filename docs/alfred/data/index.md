# Data

[alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
Data

> Auto-generated documentation for [alfred.data](https://github.com/BatsResearch/alfred/blob/main/alfred/data/__init__.py) module.

## from_csv

[Show source in __init__.py:5](https://github.com/BatsResearch/alfred/blob/main/alfred/data/__init__.py#L5)

Load a csv file as a dataset

#### Arguments

- `csv_file` - path to csv file / url to csv file
:type csv_file: str

#### Returns

IterableArrowDataset object
Type: *IterableArrowDataset*

#### Signature

```python
def from_csv(csv_file: str) -> IterableArrowDataset:
    ...
```



## from_json

[Show source in __init__.py:29](https://github.com/BatsResearch/alfred/blob/main/alfred/data/__init__.py#L29)

Load a json file as a dataset

#### Arguments

- `json_file` - path to json file / url to json file
:type json_file: str

#### Returns

IterableArrowDataset object
Type: *IterableArrowDataset*

#### Signature

```python
def from_json(json_file: str) -> IterableArrowDataset:
    ...
```



## from_pandas

[Show source in __init__.py:17](https://github.com/BatsResearch/alfred/blob/main/alfred/data/__init__.py#L17)

Load a pandas dataframe as a dataset

#### Arguments

- `df` - pandas dataframe
:type df: pandas.DataFrame

#### Returns

IterableArrowDataset object
Type: *IterableArrowDataset*

#### Signature

```python
def from_pandas(df: DataFrame) -> IterableArrowDataset:
    ...
```



## from_sql_table

[Show source in __init__.py:41](https://github.com/BatsResearch/alfred/blob/main/alfred/data/__init__.py#L41)

Load a sql table as a dataset

#### Arguments

- `sql_table_name` - name of the table to load
:type sql_table_name: str
- `sql_connection_string` - connection string to the database
:type sql_connection_string: str

#### Returns

IterableArrowDataset object
Type: *IterableArrowDataset*

#### Signature

```python
def from_sql_table(sql_table_name, sql_connection_string) -> IterableArrowDataset:
    ...
```



## Modules

- [Arrow](./arrow.md)
- [Dataset](./dataset.md)
- [Wrench](./wrench.md)
