import os
import kagglehub
import pandas as pd
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from collections import defaultdict

from data.flickr import FlickrDataset
from data.vocab import Vocabulary
from utils.vocab_utils import save_vocab, load_vocab
from utils.config import DATA_FRACTION, VOCAB_PATH


class Preprocessor:
    def __init__(self) -> None:

        # Download latest version
        DATASET_PATH = kagglehub.dataset_download("adityajn105/flickr8k")

        self.image_dir = "Images"
        self.image_dir = os.path.join(DATASET_PATH, self.image_dir)

        self.caption_file = "captions.txt"
        self.caption_file = os.path.join(DATASET_PATH, self.caption_file)

        ## Image transform
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        self.transform = transform

    def create_dataset(self):
        df = pd.read_csv(self.caption_file)

        ## For fractional use of dataset, uncomment below line
        df = df.sample(frac=DATA_FRACTION, random_state=42).reset_index(drop=True)
        print(f"Using Dataset size: {len(df)}")

        image_paths = []
        captions = []

        for _, row in df.iterrows():
            img_path = os.path.join(self.image_dir, row['image'])
            caption = row['caption']

            image_paths.append(img_path)
            captions.append(caption)

        image_to_captions = defaultdict(list)

        for img_path, cap in zip(image_paths, captions):
            image_to_captions[img_path].append(cap)

        return image_paths, captions, image_to_captions
    
    def load_data(self, batch_size=8, vocab_freq_threshold=2):
        ## download and create dataset
        image_paths, captions, image_to_captions = self.create_dataset()
        
        ## Build Vocab
        self.vocab = Vocabulary(freq_threshold=vocab_freq_threshold)
        self.vocab.build_vocab(captions)

        ## Vocabulary size
        vocab_size = len(self.vocab.stoi)

        ## Dataset and Dataloader
        dataset = FlickrDataset(image_paths, captions, self.vocab, transform=self.transform, max_len=20)
        loader = DataLoader(
            dataset, 
            batch_size=batch_size, 
            shuffle=True,
            num_workers=2,
            pin_memory=True
        )

        ## Save vocab for inference
        # torch.save(self.vocab, "checkpoints/vocab.pth")
        save_vocab(self.vocab, VOCAB_PATH)

        return loader, self.vocab, self.transform, image_to_captions, vocab_size
