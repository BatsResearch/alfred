"""

 Wrench Dataset Class is a dataset wrapper for Wrench, a weak supervision benchmark testbed.

"""
import json
import logging
import os
from typing import Optional

import pyarrow
from datasets.info import DatasetInfo

from .arrow import IterableArrowDataset

logger = logging.getLogger(__name__)

try:
    from wrench.dataset import get_data_home, get_dataset_type

    WRENCH_AVAILABLE = True
except ModuleNotFoundError:
    logger.warning(
        "Wrench is not installed. Will only be able to load from local storage."
    )
    WRENCH_AVAILABLE = False


class WrenchBenchmarkDataset(IterableArrowDataset):
    """
    Dataset wrapper for Wrench Dataset.
    This wrapper class inherits from IterableArrowDataset


    Wrench is a benchmark platform containing diverse weak supervision tasks.

    @inproceedings{
        zhang2021wrench,
        title={{WRENCH}: A Comprehensive Benchmark for Weak Supervision},
        author={Jieyu Zhang and Yue Yu and Yinghao Li and Yujing Wang and Yaming Yang and Mao Yang and Alexander Ratner},
        booktitle={Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track},
        year={2021},
        url={https://openreview.net/forum?id=Q9SKS5k8io}
    }
    """
    def __init__(self,
                 dataset_name: str,
                 split: str = "train",
                 local_path: Optional[str] = None):
        """
        Initialize the Wrench Dataset class.

        :param dataset_name: The name of the dataset to load.
        :type dataset_name: str
        :param split: The split to load, defaults to "train"
        :type split: str
        :param local_path: (Optional) The local path to load the dataset from.
                            If the wrench dataset is installed as a package then
                            it is totally fine to leave it as None.
        :type local_path: str
        """

        if split not in ["train", "valid", "test"]:
            logger.error(f"Invalid split: {split}")
            raise ValueError(
                f"Invalid split: {split}, please choose from ['train', 'valid', 'test']!"
            )
        if WRENCH_AVAILABLE:
            local_path = local_path or get_data_home()
            logger.log(
                logging.INFO,
                f"Loading wrench dataset {dataset_name} from {local_path}")

        else:
            if local_path is None:
                logging.error("No local path for wrench dataset is provided.")
                raise ValueError(
                    "local_path must be specified if wrench is not installed.")

        try:
            with open(os.path.join(local_path, dataset_name,
                                   split + '.json')) as f:
                raw_data = json.load(f)
        except FileNotFoundError:
            warn_msg = f"No {split} data found under {local_path} for {dataset_name}."
            logger.warning(warn_msg)
            if WRENCH_AVAILABLE:
                warn_msg += "\nPlease check if you have downloaded the dataset. You can download wrench datasets from https://drive.google.com/drive/folders/1v55IKG2JN9fMtKJWU48B_5_DcPWGnpTq"
            raise FileNotFoundError(warn_msg)

        self.uid2label = {}
        self.labels = []
        # Strong assumption: every data has the same fields!!!
        _inst = list(raw_data.values())[0]['data']
        self.valid_field = {
            key: self.pyarrow_typer(value)
            for key, value in _inst.items()
            if type(value) in [str, int, float]
        }
        self.uid2idx = {}
        self.data_list = []
        for idx, (uid, inst) in enumerate(raw_data.items()):
            lean_data = {
                key: inst['data'][key]
                for key in self.valid_field.keys()
            }
            lean_data = {
                **{
                    'uid': uid
                },
                **lean_data,
                **{
                    'label': inst['label']
                }
            }
            self.data_list.append(lean_data)

            self.uid2label[uid] = inst['label']
            self.labels.append(inst['label'])
            self.uid2idx[uid] = idx

        self.uids = list(self.uid2label.keys())

        info = DatasetInfo(
            description=f"Wrench Dataset: {dataset_name}, {split} split",
            version="0.0.0",
        )

        schema = pyarrow.schema({
            **{
                "uid": self.pyarrow_typer(self.uids[0])
            },
            **self.valid_field,
            **{
                "label": self.pyarrow_typer(self.uid2label[self.uids[0]])
            }
        })

        _data = pyarrow.Table.from_pylist(self.data_list, schema=schema)

        self.dataset_name = dataset_name

        super().__init__(_data, info=info, split=split)

    def __getattr__(self, uid):
        """returns the data instance with the given uid"""
        return self.data_list[self.uid2idx[uid]]

    def __repr__(self):
        """returns the string representation of the dataset"""
        return f"{self.__class__.__name__}(Wrench Dataset: {self.dataset_name})"
