import os
import json
import shutil
from huggingface_hub import hf_hub_download, HfApi

from ..utils.config import HF_REPO_ID, HF_VOCAB_FILENAME

from ..data.vocab import Vocabulary
    
def upload_vocab(path="checkpoints/vocab.json"):
    api = HfApi()
    api.upload_file(
        path_or_fileobj=path,
        path_in_repo=HF_VOCAB_FILENAME,
        repo_id=HF_REPO_ID,
        repo_type="model",
    )

    print(f"Vocabulary uploaded to Hugging Face at repo: {HF_REPO_ID}, filename: {HF_VOCAB_FILENAME}")

def save_vocab(vocab, path):
    with open(path, "w") as f:
        json.dump(vocab.to_dict(), f)

    upload_vocab(path)

def load_vocab(path="checkpoints/vocab.json"):
    print("Downloading vocabulary from Hugging Face...")
    shutil.rmtree("/root/.cache/huggingface", ignore_errors=True)
    downloaded_path = hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=HF_VOCAB_FILENAME,
        force_download=True
    )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    shutil.copy(downloaded_path, path)

    with open(path, "r") as f:
        vocab_dict = json.load(f)
        voc = Vocabulary.from_dict(vocab_dict)
        print(f"Vocabulary loaded from {path}, size: {len(voc.itos)}")
        return voc
    
