import torch

from ..training.inference import load_model
from ..utils.vocab_utils import load_vocab
from ..utils.config import VOCAB_PATH

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_encoder = None
_decoder = None
_vocab = None

def load_model_and_vocab():
    global _encoder, _decoder, _vocab
    if _encoder is None or _decoder is None or _vocab is None:
        print("Loading model and vocab...")
        _vocab = load_vocab(VOCAB_PATH)
        _encoder, _decoder = load_model(device)
        
    return _encoder, _decoder, _vocab