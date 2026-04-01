import nltk
from collections import Counter


class Vocabulary:
    def __init__(self, freq_threshold=5, itos=None, stoi=None):
        self.freq_threshold = freq_threshold

        # Load the vocab if provided
        if itos is not None and stoi is not None:
            self.stoi = stoi
            self.itos = {int(k):v for k,v in itos.items()}
        else:
            self.stoi = {
                "<pad>": 0,
                "<start>": 1,
                "<end>": 2,
                "<unk>": 3
            }
            self.itos = {v:k for k,v in self.stoi.items()}

    def __len__(self):
        return len(self.itos)

    def tokenizer(self, text):
        return nltk.tokenize.word_tokenize(text.lower())

    def build_vocab(self, sentence_list):
        frequencies = Counter()
        for sentence in sentence_list:
            tokens = self.tokenizer(sentence)
            frequencies.update(tokens)

        idx = len(self.stoi)  # Start index for new words after special tokens

        for word, freq in frequencies.items():
            if freq >= self.freq_threshold:
                self.stoi[word] = idx
                self.itos[idx] = word
                idx += 1

    def numericalize(self, text):
        """Convert a sentence into a list of indices based on the vocabulary.
        Words not in the vocabulary are replaced with the index of the <unk> token."""
        tokenized_text = self.tokenizer(text)
        return [
            self.stoi.get(token, self.stoi["<unk>"])
            for token in tokenized_text
        ]
    
    def denumericalize(self, indices):
        """Convert a list of indices back into a sentence based on the vocabulary.
        Indices that do not correspond to any word in the vocabulary are replaced with <unk>."""
        return [
            self.itos.get(idx, "<unk>")
            for idx in indices
        ]

    def to_dict(self):
        """Convert the Vocabulary object into a dictionary format for saving."""
        return {
            "stoi": self.stoi,
            "itos": self.itos
        }
    
    @staticmethod
    def from_dict(data):
        """Create a Vocabulary object from a dictionary."""
        return Vocabulary(
            itos=data.get("itos"),
            stoi=data.get("stoi")
        )