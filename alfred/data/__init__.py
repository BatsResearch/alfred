from .arrow import IterableArrowDataset, BufferedArrowDataset
from .dataset import Dataset
from pandas import read_csv, read_json, read_sql_table, DataFrame

def from_csv(csv_file: str) -> IterableArrowDataset:
    """
    Load a csv file as a dataset

    :param csv_file: path to csv file / url to csv file
    :type csv_file: str
    :return: IterableArrowDataset object
    :rtype: IterableArrowDataset
    """
    return IterableArrowDataset(read_csv(csv_file))


def from_pandas(df: DataFrame) -> IterableArrowDataset:
    """
    Load a pandas dataframe as a dataset

    :param df: pandas dataframe
    :type df: pandas.DataFrame
    :return: IterableArrowDataset object
    :rtype: IterableArrowDataset
    """
    return IterableArrowDataset(df)


def from_json(json_file: str) -> IterableArrowDataset:
    """
    Load a json file as a dataset

    :param json_file: path to json file / url to json file
    :type json_file: str
    :return: IterableArrowDataset object
    :rtype: IterableArrowDataset
    """
    return IterableArrowDataset(read_json(json_file))


def from_sql_table(sql_table_name, sql_connection_string) -> IterableArrowDataset:
    """
    Load a sql table as a dataset

    :param sql_table_name: name of the table to load
    :type sql_table_name: str
    :param sql_connection_string: connection string to the database
    :type sql_connection_string: str
    :return: IterableArrowDataset object
    :rtype: IterableArrowDataset
    """
    return IterableArrowDataset(
                read_sql_table(
                    sql_table_name,
                    sql_connection_string,
                )
            )
