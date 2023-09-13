# Wrench

[Alfred Index](../../README.md#alfred-index) /
[Alfred](../index.md#alfred) /
[Data](./index.md#data) /
Wrench

> Auto-generated documentation for [alfred.data.wrench](../../../alfred/data/wrench.py) module.

- [Wrench](#wrench)
  - [WrenchBenchmarkDataset](#wrenchbenchmarkdataset)
    - [WrenchBenchmarkDataset().__getattr__](#wrenchbenchmarkdataset()__getattr__)
    - [WrenchBenchmarkDataset().__repr__](#wrenchbenchmarkdataset()__repr__)

## WrenchBenchmarkDataset

[Show source in wrench.py:29](../../../alfred/data/wrench.py#L29)

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

#### Signature

```python
class WrenchBenchmarkDataset(IterableArrowDataset):
    def __init__(
        self, dataset_name: str, split: str = "train", local_path: Optional[str] = None
    ):
        ...
```

### WrenchBenchmarkDataset().__getattr__

[Show source in wrench.py:145](../../../alfred/data/wrench.py#L145)

returns the data instance with the given uid

#### Signature

```python
def __getattr__(self, uid):
    ...
```

### WrenchBenchmarkDataset().__repr__

[Show source in wrench.py:149](../../../alfred/data/wrench.py#L149)

returns the string representation of the dataset

#### Signature

```python
def __repr__(self):
    ...
```


