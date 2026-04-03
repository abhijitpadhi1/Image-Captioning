from PIL import Image
import torch
import torchvision.transforms as transforms

from ..training.inference import load_model
from ..utils.vocab_utils import load_vocab
from ..utils.config import VOCAB_PATH

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
    return _encoder, _decoder, _vocab

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


def generate_caption_with_attention(encoder, decoder, image, vocab, device, max_len=20):
    with torch.no_grad():
        image = image.to(device).unsqueeze(0)
        features = encoder(image)

        h = torch.zeros(1, decoder.lstm.hidden_size).to(device)
        c = torch.zeros(1, decoder.lstm.hidden_size).to(device)

        inputs = torch.tensor([vocab.stoi["<start>"]]).to(device)

        caption = []
        attention_maps = []

        for _ in range(max_len):
            embedding = decoder.embedding(inputs)

            context, alpha = decoder.attention(features, h)

            lstm_input = torch.cat((embedding.squeeze(1), context), dim=1)

            h, c = decoder.lstm(lstm_input, (h, c))

            output = decoder.fc(h)

            predicted = output.argmax(1)
            word = vocab.itos[predicted.item()]

            if word == "<end>":
                break

            caption.append(word)
            attention_maps.append(alpha.cpu().tolist())

            inputs = predicted

    return caption, attention_maps


async def visualize_attention_service(file):
    image = Image.open(file.file).convert("RGB")
    image_tensor = transform(image)
    encoder, decoder, vocab = load_model_and_vocab()

    caption, attention = generate_caption_with_attention(
        encoder, decoder, image_tensor, vocab, device
    )

    return {
        "caption": caption,
        "attention_maps": attention
    }