# test_sentencepiece_tokenizer_builder.py

import unittest
import os
from amh_tokenizer import SentencePieceTokenizerBuilder

class TestSentencePieceTokenizerBuilder(unittest.TestCase):
    def setUp(self):
        # Set up the output directory
        self.test_model_path = "./tokenizers/test_tokenizer.json"

    def test_train_and_save(self):
        # Create an instance of SentencePieceTokenizerBuilder for testing
        builder = SentencePieceTokenizerBuilder(vocab_size=100, special_tokens=["[UNK]", "[PAD]", "[CLS]"], model_file_path=self.test_model_path)

        # Provide the path to the sample training data for testing
        sample_training_files = ["sample_data.txt"]

        # Run the train_and_save method
        builder.train_and_save(sample_training_files)

        # Assert that the model file is created
        self.assertTrue(os.path.exists(self.test_model_path))

    def tearDown(self):
        # Clean up any resources created during the tests
        if os.path.exists(self.test_model_path):
            os.remove(self.test_model_path)

if __name__ == '__main__':
    unittest.main()
