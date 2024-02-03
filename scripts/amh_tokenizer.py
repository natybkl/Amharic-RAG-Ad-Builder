import time
import os
from tokenizers import Tokenizer, models, pre_tokenizers, processors, trainers

class SentencePieceTokenizerBuilder:
    def __init__(self, vocab_size=50000, special_tokens=None, model_file_path="./tokenizers/tokenizer.json"):
        self.vocab_size = vocab_size
        self.special_tokens = special_tokens or ["[UNK]", "[PAD]", "[CLS]"]
        self.model_file_path = model_file_path

    def build_tokenizer(self):
        tokenizer = Tokenizer(model=models.WordPiece(unk_token="[UNK]"))
        tokenizer.pre_tokenizer = pre_tokenizers.Sequence([pre_tokenizers.Metaspace(),
                                                           pre_tokenizers.Digits(individual_digits=True)])
        tokenizer.post_processor = processors.TemplateProcessing(
            single="[CLS] $A [EOS]",
            special_tokens=[("[CLS]", 1), ("[EOS]", 2)],
        )
        return tokenizer

    def train_and_save(self, training_files):
        sp_tokenizer = self.build_tokenizer()
        trainer = trainers.WordPieceTrainer(vocab_size=self.vocab_size, special_tokens=self.special_tokens)

        t1 = time.time()
        sp_tokenizer.train(files=training_files, trainer=trainer)
        print("en-sentpiece time:", time.time() - t1)

        os.makedirs(os.path.dirname(self.model_file_path), exist_ok=True)
        sp_tokenizer.save(self.model_file_path)

if __name__ == "__main__":
    builder = SentencePieceTokenizerBuilder()
    builder.train_and_save(["All_data.txt"])
