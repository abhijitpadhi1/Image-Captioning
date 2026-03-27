import nltk
from collections import Counter


class Vocabulary:
    def __init__(self, freq_threshold=5):
        self.freq_threshold = freq_threshold

        self.itos = {0: "<pad>", 1: "<start>", 2: "<end>", 3: "<unk>"}
        self.stoi = {v: k for k, v in self.itos.items()}

    def tokenizer(self, text):
        return nltk.tokenize.word_tokenize(text.lower())

    def build_vocab(self, sentence_list):
        frequencies = Counter()
        for sentence in sentence_list:
            tokens = self.tokenizer(sentence)
            frequencies.update(tokens)

        idx = 4 # Start index for new words after special tokens

        for word, freq in frequencies.items():
            if freq >= self.freq_threshold:
                self.stoi[word] = idx
                self.itos[idx] = word
                idx += 1

    def numericalize(self, text):
        tokenized_text = self.tokenizer(text)
        return [
            self.stoi.get(token, self.stoi["<unk>"])
            for token in tokenized_text
        ]