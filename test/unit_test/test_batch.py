import unittest

from alfred.fm.utils import DynamicBatcher

# from torch import cuda


class TestDynamicBatcher(unittest.TestCase):
    def test_init(self):
        queries = ["query 1", "query 2", "query 3"]
        max_batch_size = 10
        batcher = DynamicBatcher(queries, max_batch_size)

        self.assertEqual(batcher.queries, queries)
        self.assertEqual(batcher.max_batch_size, max_batch_size)

        # Test that the maximum batch size is determined by the amount of free GPU memory
        # with patch.object(cuda, 'is_available') as mock_is_available:
        #     mock_is_available.return_value = True
        #     with patch.object(cuda, 'get_device_count') as mock_get_device_count:
        #       mock_get_device_count.return_value = 1
        #     with patch.object(cuda, 'get_device_properties') as mock_get_device_properties:
        #         mock_get_device_properties.return_value.total_memory = 1000000
        #         with patch.object(cuda, 'memory_allocated') as mock_memory_allocated:
        #             mock_memory_allocated.return_value = 500000
        #             batcher = DynamicBatcher(queries)
        #             self.assertEqual(batcher.max_batch_size, int((1000000 - 500000) / 86381))
        #
        #     with patch.object(cuda, 'memory_allocated') as mock_memory_allocated:
        #         mock_memory_allocated.return_value = 1000000
        #         batcher = DynamicBatcher(queries)
        #         self.assertEqual(batcher.max_batch_size, int(1000000 / 86381))
        #
        # # Test that the maximum batch size is set to the default value if no GPU is available
        # with patch.object(cuda, 'is_available') as mock_is_available:
        #     mock_is_available.return_value = False
        #     batcher = DynamicBatcher(queries)
        #     self.assertEqual(batcher.max_batch_size, 2048)

    def test_reorder(self):
        inst = ["query 1", "query 2", "query 3"]
        batcher = DynamicBatcher(inst)
        batches = batcher.batch()

        reordered_inst = list(batcher.reorder(inst))
        self.assertEqual(reordered_inst, inst)

        batcher.len_sorted_idx = [1, 0, 2]
        reordered_inst = batcher.reorder(inst)
        [
            self.assertEqual(x, y)
            for (x, y) in zip(reordered_inst, ["query 2", "query 1", "query 3"])
        ]

    def test_simple_batch(self):
        queries = ["query1", "query2", "query3", "query4", "query5"]

        batcher = DynamicBatcher(queries, max_batch_size=2)

        batches = batcher.batch()
        print(batches)
        self.assertEqual(
            batches, [["query1", "query2"], ["query3", "query4"], ["query5"]]
        )

    def test_batch(self):
        # Figure out how to simulate low GPU memory
        queries = ["query1", "query2", "query3", "query4", "query5"]
        pass
