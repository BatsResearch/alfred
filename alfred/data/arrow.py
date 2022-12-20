from typing import Union, Optional, Dict, Tuple, Iterable, Any, List

import pandas
import pyarrow
from datasets.info import DatasetInfo
from datasets.splits import NamedSplit

from .dataset import Dataset


class IterableArrowDataset(Dataset):
    """
    This class represents a dataset stored in a pyarrow Table or pandas DataFrame. It provides methods for accessing and iterating over the data, as well as for saving and loading the dataset to and from disk.

    Properties:
    - shape (Tuple[int, int]): The shape of the dataset (number of rows and columns).
    - num_rows (int): The number of rows in the dataset.
    - num_cols (int): The number of columns in the dataset.
    - schema (pyarrow.Schema): The schema of the table and its columns.
    - columns (List[pa.ChunkedArray]): A list of all columns in numerical order.

    Methods:
    - data(): Return the underlying pyarrow Table or pandas DataFrame.
    - info(): Return the metadata about the dataset.
    - split(): Return the information about how the dataset has been split.
    - version(): Return the version of the dataset.
    - __len__(): Return the number of rows in the dataset.
    - __getitem__(uid): Return the row with the given unique identifier.
    - itercolumns(*args, **kwargs): Iterate over all columns in their numerical order.
    - __iter__(): Iterate over the rows of the dataset, yielding a dictionary for each row.
    - save_to_disk(path: str): Save the dataset to disk at the specified path.
    - load_from_disk(path: str): Load the dataset from disk from the specified path.
    """

    def __init__(self,
                 table: Union[pyarrow.Table, pandas.DataFrame],
                 info: Optional[DatasetInfo] = None,
                 split: Optional[Union[str, NamedSplit]] = None,
                 ):
        """
        Initialize the dataset with the given table and metadata.

        :param table: The table to store in the dataset.
        :type table: Union[pyarrow.Table, pandas.DataFrame]
        :param info: (optional) The metadata about the dataset, defaults to None
        :type info: Optional[DatasetInfo], optional
        :param split: (optional) The information about how the dataset has been split, defaults to None
        :type split: Optional[Union[str, NamedSplit]], optional
        """

        self._data = table if isinstance(
            table, pyarrow.Table) else pyarrow.Table.from_pandas(table)
        self._info = info
        self._split = split
        self._info = info or DatasetInfo()
        self._split = split

    @staticmethod
    def pyarrow_typer(data: Any) -> pyarrow.DataType:
        """
        Recognize the type of the data and find the according pyarrow type.

        :param data: The data to recognize the type of.
        :type data: Any
        :return: The pyarrow type of the data.
        :rtype: pyarrow.DataType
        """
        if isinstance(data, str):
            return pyarrow.string()
        elif isinstance(data, int):
            return pyarrow.int64()
        elif isinstance(data, float):
            return pyarrow.float64()
        elif isinstance(data, bool):
            return pyarrow.bool()
        else:
            raise ValueError(f"Unsupported type {type(data)}")

    @property
    def shape(self) -> Tuple[int, int]:
        """returns the shape of the dataset (number of rows and columns)"""
        return (self.num_rows, self.num_cols)

    @property
    def num_rows(self) -> int:
        """returns the number of rows in the dataset"""
        return len(self._data)

    @property
    def num_cols(self) -> int:
        """returns the number of columns in the dataset"""
        return len(self._data.columns)

    @property
    def schema(self) -> pyarrow.Schema:
        """
        Schema of the table and its columns.

        :return: The schema of the table and its columns.
        :rtype: pyarrow.Schema
        """
        return self.table.schema

    @property
    def columns(self) -> List[pyarrow.ChunkedArray]:
        """
        Columns of the dataset.

        :return: A list of all columns in numerical order.
        :rtype: List[pyarrow.ChunkedArray]
        """
        return self.table.columns

    def data(self) -> Union[pyarrow.Table, pandas.DataFrame]:
        """
        Return the underlying pyarrow Table or pandas DataFrame.

        :return: The underlying pyarrow Table or pandas DataFrame.
        :rtype: Union[pyarrow.Table, pandas.DataFrame]
        """
        return self._data

    def info(self) -> DatasetInfo:
        """returns the metadata about the dataset"""
        return self._info

    def split(self) -> NamedSplit:
        """returns the information about how the dataset has been split"""
        return self._split

    def version(self) -> str:
        """returns the version of the dataset"""
        return self._info.version

    def __version__(self) -> str:
        """returns the version of the dataset"""
        return self._info.version

    def __len__(self) -> int:
        """returns the number of rows in the dataset"""
        return self.num_rows

    def __getitem__(self, uid: int, **kawrgs: Any) -> Dict[str, Any]:
        """
        Return the row with the given unique identifier.

        :param uid: The unique identifier of the row to return.
        :type uid: int or slice
        :param kawrgs: Additional keyword arguments.
        :type kawrgs: Any
        :return: The row with the given unique identifier.
        :rtype: Dict[str, Any]
        """
        return self._data.to_pandas().iloc[uid]

    def _getitem(self, uid: int) -> Dict[str, Any]:
        """
        Return the row with the given unique identifier.

        :param uid: The unique identifier of the row to return.
        :type uid: int or slice
        :return: The row with the given unique identifier.
        :rtype: Dict[str, Any]
        """
        return self._data.to_pandas().iloc[uid]

    def itercolumns(self, *args: Any, **kwargs: Any) -> Iterable:
        """
        Iterator over all columns in their numerical order.

        :param args: Additional arguments.
        :type args: Any
        :param kwargs: Additional keyword arguments.
        :type kwargs: Any
        """
        return self._data.itercolumns(*args, **kwargs)

    def __iter__(self) -> Iterable[Dict]:
        """
        Iterator over the rows of the dataset, yielding a dictionary for each row.

        :return: An iterator over the rows of the dataset, yielding a dictionary for each row.
        :rtype: Iterable[Dict]
        """
        for batch in self._data.to_batches(max_chunksize=2048):
            for instance in batch.to_pylist():
                yield instance

    def __repr__(self):
        """returns a string representation of the dataset"""
        return f"{self.__class__.__name__}(dataset={self._dataset})"

    def save_to_disk(self, path: str):
        """saves the dataset to disk at the specified path"""
        pass

    def load_from_disk(self, path: str):
        """loads the dataset from disk from the specified path"""
        pass


class BufferedArrowDataset(Dataset):
    """
    This class represents a dataset stored in a pyarrow buffer.
    It provides methods for accessing and iterating over the data,
    as well as for saving and loading the dataset to and from disk.

    This will be very useful for datasets that are too large to fit into memory.

    Properties:

    - shape (Tuple[int, int]): The shape of the dataset (number of rows and columns).
    - num_rows (int): The number of rows in the dataset.
    - num_cols (int): The number of columns in the dataset.

    Methods:

    - data(): Return the underlying pyarrow Table.
    - info(): Return the metadata about the dataset.
    - split(): Return the information about how the dataset has been split.
    - version(): Return the version of the dataset.
    - __len__(): Return the number of rows in the dataset.
    - __getitem__(uid): Return the row with the given unique identifier.
    - __iter__(): Iterate over the rows of the dataset, yielding a dictionary for each row.
    - save_to_disk(path: str): Save the dataset to disk at the specified path.
    - load_from_disk(path: str): Load the dataset from disk from the specified path.
    """

    def __init__(self,
                 buffer: pyarrow.Buffer,
                 info: Optional[DatasetInfo] = None,
                 split: Optional[Union[str, NamedSplit]] = None,
                 ):
        """
        Initializes a  BufferedArrowDataset class.

        :param buffer: The pyarrow buffer containing the dataset.
        :type buffer: pyarrow.Buffer
        :param info: The metadata about the dataset.
        :type info: Optional[DatasetInfo]
        :param split: The information about how the dataset has been split.
        :type split: Optional[Union[str, NamedSplit]]
        """
        self._stream = pyarrow.BufferReader(buffer)
        o_stream = pyarrow.ipc.open_stream(self._stream)
        self._data = o_stream.read_all()
        self._info = info or DatasetInfo()
        self._split = split

    @property
    def shape(self) -> Tuple[int, int]:
        """returns the shape of the dataset (number of rows and columns)"""
        return (self.num_rows, self.num_columns)

    @property
    def num_rows(self) -> int:
        """returns the number of rows in the dataset"""
        return len(self._data)

    @property
    def num_cols(self) -> int:
        """returns the number of columns in the dataset"""
        return len(self._data.columns)

    def data(self):
        """returns the underlying pyarrow Table"""
        return self._data

    def info(self):
        """returns the metadata about the dataset"""
        return self._info

    def split(self):
        """returns the information about how the dataset has been split"""
        return self._split

    def version(self) -> str:
        """returns the version of the dataset"""
        return self._info.version

    def __version__(self) -> str:
        """returns the version of the dataset"""
        return self._info.version

    def __len__(self) -> int:
        """returns the number of rows in the dataset"""
        return self.num_rows

    def __getitem__(self, uid: int, **kawrgs: Any) -> Dict[str, Any]:
        """
        Retuns the row with the given unique identifier.

        :param uid: The unique identifier of the row to return.
        :type uid: int or slice
        :param kawrgs: Additional keyword arguments.
        :type kawrgs: Any
        :return: The row with the given unique identifier.
        :rtype: Dict[str, Any]
        """
        return self._dataset[uid]

    def __iter__(self) -> Iterable:
        """
        Iterator over the rows of the dataset, yielding a dictionary for each row.

        :return: An iterator over the rows of the dataset, yielding a dictionary for each row.
        :rtype: Iterable
        """
        for batch in self._data.to_batches(max_chunksize=2048):
            for instance in batch.to_pylist():
                yield instance

    def __repr__(self):
        """returns a string representation of the dataset"""
        return f"{self.__class__.__name__}(dataset={self._dataset})"

    def save_to_disk(self, path: str):
        """saves the dataset to disk at the specified path"""
        pass

    def load_from_disk(self, path: str):
        """loads the dataset from disk from the specified path"""
        pass
