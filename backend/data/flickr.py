import torch
from torch.utils.data import Dataset
from PIL import Image

class FlickrDataset(Dataset):
    def __init__(self, image_paths, captions, vocab, transform=None, max_len=20):
        self.image_paths = image_paths
        self.captions = captions
        self.vocab = vocab
        self.transform = transform
        self.max_len = max_len

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert("RGB")

        if self.transform:
            image = self.transform(image)

        caption = self.captions[idx]

        # Numericalize
        numericalized = [self.vocab.stoi["<start>"]]
        numericalized += self.vocab.numericalize(caption)
        numericalized.append(self.vocab.stoi["<end>"])

        # Padding
        if len(numericalized) < self.max_len:
            numericalized += [self.vocab.stoi["<pad>"]] * (self.max_len - len(numericalized))
        else:
            numericalized = numericalized[:self.max_len]

        # Create input and target
        caption_input = torch.tensor(numericalized[:-1])
        caption_target = torch.tensor(numericalized[1:])

        return image, caption_input, caption_target