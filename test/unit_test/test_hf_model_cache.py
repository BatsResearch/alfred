import unittest

import os
from alfred.fm.huggingface import HuggingFaceModel

class TestHuggingFaceModelCache(unittest.TestCase):
    def setUp(self):
        # Set up the test environment
        self.test_model_string = "google/t5-efficient-tiny"
        self.test_local_path = "./.pytest_cache/test_local_path"
        os.environ["TRANSFORMERS_CACHE"] = "./.pytest_cache/transformers_cache"

    def test_init(self):
        # Test the initialization of the HuggingFaceModel class
        model = HuggingFaceModel(
            model_string=self.test_model_string,
            local_path=self.test_local_path,
            offload_folder="./.pytest_cache/offload_folder"
        )
        self.assertEqual(model.local_path, self.test_local_path)

    def test_default_local_path(self):
        # Test that the default local path is set correctly
        model = HuggingFaceModel(
            model_string=self.test_model_string,
            offload_folder="./.pytest_cache/offload_folder"
        )
        self.assertEqual(model.local_path, os.environ.get("TRANSFORMERS_CACHE"))
