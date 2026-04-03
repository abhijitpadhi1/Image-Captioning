import json

from ..data.vocab import Vocabulary
    

def save_vocab(vocab, path):
    with open(path, "w") as f:
        json.dump(vocab.to_dict(), f)

def load_vocab(path):
    with open(path, "r") as f:
        vocab_dict = json.load(f)

    vocab = Vocabulary.from_dict(vocab_dict)
    return vocab