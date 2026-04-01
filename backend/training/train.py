from json import decoder

from tqdm import tqdm
from PIL import Image
from nltk.translate.bleu_score import corpus_bleu
import torch
import torch.nn as nn

from model.decoder import DecoderWithAttention
from model.encoder import EncoderCNN
from training.inference import generate_caption_greedy, generate_caption_beam
from utils.model_utils import save_model_to_hf
from utils.config import CHECKPOINT_PATH, EMBED_SIZE, FEATURE_DIM, HIDDEN_SIZE

class ModelTrainer:
    def __init__(self, dataloader, vocab, transform, feature_dim = 2048, embed_size = 256, hidden_size = 256, vocab_size = 5000):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.embed_size = embed_size
        self.hidden_size = hidden_size
        self.vocab_size = vocab_size
        self.dataloader = dataloader
        self.transform = transform

        self.encoder = EncoderCNN().to(self.device)
        self.decoder = DecoderWithAttention(
            feature_dim=feature_dim,
            embed_size=embed_size,
            hidden_size=hidden_size,
            vocab_size=vocab_size
        ).to(self.device)

        ## Loss and Optimizer
        self.vocab = vocab
        pad_idx = self.vocab.stoi["<pad>"]

        self.criterion = nn.CrossEntropyLoss(ignore_index=pad_idx)

        params = list(self.decoder.parameters())
        self.optimizer = torch.optim.Adam(params, lr=1e-3)


    def train_one_epoch(self, encoder, decoder, dataloader, optimizer, criterion, device):
        encoder.train()
        decoder.train()

        total_loss = 0

        loop = tqdm(dataloader, desc="Training", leave=False)

        for images, captions_input, captions_target in loop:
            images = images.to(device)
            captions_input = captions_input.to(device)
            captions_target = captions_target.to(device)

            # Forward pass
            features = encoder(images)                     # (B, 49, 2048)
            outputs, alphas = decoder(features, captions_input)

            # Reshape for loss
            outputs = outputs.reshape(-1, outputs.shape[2])
            captions_target = captions_target.reshape(-1)

            loss = criterion(outputs, captions_target)

            # Backprop
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

            # Update tqdm live
            loop.set_postfix(loss=loss.item())

        return total_loss / len(dataloader)

    def train(self, num_epochs=10):
        best_loss = float('inf')
        if self.device.type == 'cuda':
            print("Using GPU for training")
        else:
            print("Using CPU for training. Consider using a GPU for faster training.")
        ## Training with fine-tuneing encoder
        for epoch in range(num_epochs):
            # Fine-tune encoder AFTER 5 epochs
            if epoch == 5:
                print("Unfreezing encoder...")

                for param in self.encoder.resnet.parameters():
                    param.requires_grad = True

                # Recreate optimizer
                self.optimizer = torch.optim.Adam(
                    list(self.decoder.parameters()) + list(self.encoder.parameters()),
                    lr=1e-4
                )

                # Debug: Check trainable parameters
                # for name, param in self.encoder.named_parameters():
                #     if param.requires_grad:
                #         print("Trainable:", name)

            print(f"Epoch {epoch+1}/{num_epochs}")

            loss = self.train_one_epoch(
                self.encoder, self.decoder, self.dataloader, self.optimizer, self.criterion, self.device
            )

            if loss < best_loss:
                best_loss = loss
                print(f"New best loss: {best_loss:.4f}. Saving model...")
                torch.save({
                    "config": {
                        "embed_size": EMBED_SIZE,
                        "hidden_size": HIDDEN_SIZE,
                        "feature_dim": FEATURE_DIM,
                        "vocab_size": self.vocab_size
                    },
                    "encoder": self.encoder.state_dict(),
                    "decoder": self.decoder.state_dict()
                }, CHECKPOINT_PATH)

            print(f"Epoch {epoch+1}, Loss: {loss:.4f}")

    def save_model_to_hf(self, model_path="checkpoints/model.pth"):
        save_model_to_hf(model_path)

    def bleu_score(self, image_paths, image_to_captions, inference, max_samples=1000):
        self.encoder.eval()
        self.decoder.eval()

        references = []
        candidates = []

        loop = tqdm(image_paths[:max_samples], desc="Evaluating BLEU")

        with torch.no_grad():
            for img_path in loop:
                # Load image
                image = Image.open(img_path).convert("RGB")
                image_tensor = self.transform(image).to(self.device)

                # Generate caption
                if inference == "greedy":
                    pred = generate_caption_greedy(self.encoder, self.decoder, image_tensor, self.vocab, self.device)
                elif inference == "beam":
                    pred = generate_caption_beam(self.encoder, self.decoder, image_tensor, self.vocab, self.device, beam_width=3)
                else:
                    raise ValueError(f"Unknown inference method: {inference}")

                pred_tokens = pred.split()

                # Get ALL reference captions
                ref_caps = image_to_captions[img_path]

                ref_tokens = []
                for cap in ref_caps:
                    tokens = self.vocab.tokenizer(cap)

                    # Remove special tokens if present
                    tokens = [t for t in tokens if t not in ["<start>", "<end>"]]

                    ref_tokens.append(tokens)

                references.append(ref_tokens)
                candidates.append(pred_tokens)

                # Optional live BLEU
                if len(candidates) > 50:
                    partial_bleu = corpus_bleu(references, candidates)
                    loop.set_postfix(bleu=round(partial_bleu, 4))

        bleu = corpus_bleu(references, candidates)
        return bleu