import abc


class Dataset(abc.ABC):
    """
    This is a generic interface for dataset classes that mirrors key interfaces from huggingface datasets. It provides methods for accessing and iterating over the data, as well as for saving and loading the dataset to and from disk.

    Properties:

    - shape (Tuple[int, int]): The shape of the dataset (number of rows and columns).
    - info (DatasetInfo): The metadata of the dataset.
    - split (NamedSplit): The information about how the dataset has been split.
    - version (str): The version of the dataset.

    Methods:

    - data(): Return the underlying data.
    - info(): Return the metadata about the dataset.
    - split(): Return the information about how the dataset has been split.
    - __len__(): Return the number of rows in the dataset.
    - __getitem__(uid): Return the row with the given unique identifier.
    - __iter__(): Iterate over the rows of the dataset.
    - __version__(): Return the version of the dataset.
    - version: Return the version of the dataset.
    - save_to_disk(path: str): Save the dataset to disk at the specified path.
    - load_from_disk(path: str): Load the dataset from disk from the specified path.
    """

    @property
    @abc.abstractmethod
    def data(self):
        """returns the underlying data"""
        pass

    @property
    @abc.abstractmethod
    def info(self):
        """returns the metadata about the dataset"""
        pass

    @property
    @abc.abstractmethod
    def split(self):
        """returns the information about how the dataset has been split"""
        pass

    @abc.abstractmethod
    def __len__(self) -> int:
        """returns the number of rows in the dataset"""
        pass

    @abc.abstractmethod
    def __getitem__(self, uid, **kawrgs):
        """returns the row with the given unique identifier"""
        pass

    @abc.abstractmethod
    def __iter__(self):
        """iterates over the rows of the dataset"""
        pass

    @abc.abstractmethod
    def __version__(self) -> str:
        """returns the version of the dataset"""
        pass

    @property
    def version(self) -> str:
        """returns the version of the dataset"""
        pass

    @staticmethod
    def save_to_disk(self, path: str):
        """saves the dataset to disk at the specified path"""
        pass

    @staticmethod
    def load_from_disk(self, path: str):
        """loads the dataset from disk from the specified path"""
        pass
