import unittest

from alfred.data import from_csv


class TestDataset(unittest.TestCase):
    def test_load_csv(self):
        # download csv dataset and load as an alfred dataset object
        csv_location = (
            "https://raw.githubusercontent.com/dotpyu/seaborn-datasets/master/iris.csv"
        )
        dataset = from_csv(csv_location)
        self.assertEqual(dataset.shape, (150, 5))
        # download csv files as a temp file

    def test_iteration(self):
        # Check dataset can be iterated over
        csv_location = (
            "https://raw.githubusercontent.com/dotpyu/seaborn-datasets/master/iris.csv"
        )
        dataset = from_csv(csv_location)
        for row in dataset:
            self.assertEqual(len(row), 5)


if __name__ == "__main__":
    unittest.main()
