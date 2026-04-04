from PIL import Image
import torch
import torchvision.transforms as transforms

from ..training.inference import generate_caption_greedy, generate_caption_beam
from ..services.model_loader import load_model_and_vocab
from ..utils.logger import logger

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


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