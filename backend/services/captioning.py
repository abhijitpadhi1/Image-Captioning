from PIL import Image
import torch
import torchvision.transforms as transforms

from training.inference import generate_caption_greedy, load_model, generate_caption_beam
from utils.config import VOCAB_PATH
from utils.vocab_utils import load_vocab
from utils.logger import logger

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Global cache for vocab and model to avoid reloading on every request
_encoder = None
_decoder = None
_vocab = None

# Load the vocab and model at startup
def load_model_and_vocab():
    global _encoder, _decoder, _vocab
    if _encoder is None or _decoder is None or _vocab is None:
        print("Loading model and vocab...")
        _vocab = load_vocab(VOCAB_PATH)
        _encoder, _decoder = load_model(device)
        print("Model and vocab loaded.")
        logger.info("Model and vocab loaded.")
    return _encoder, _decoder, _vocab


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


async def predict_caption_service(file, method="beam"):
    image = Image.open(file.file).convert("RGB")
    image_tensor = transform(image)
    encoder, decoder, vocab = load_model_and_vocab()

    if method == "beam":
        caption = generate_caption_beam(
            encoder, decoder, image_tensor, vocab, device
        )
    elif method == "greedy":
        caption = generate_caption_greedy(
            encoder, decoder, image_tensor, vocab, device
        )
    else:
        raise ValueError(f"Unknown method: {method}")
    
    logger.info(f"Generated caption using {method} search: {caption}")

    return {
        "caption": caption,
        "method": method
    }