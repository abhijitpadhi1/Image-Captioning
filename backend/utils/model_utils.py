from huggingface_hub import hf_hub_download, HfApi
import os
import shutil

from utils.config import HF_REPO_ID, HF_MODEL_FILENAME

def get_model_path(local_path="checkpoints/model.pth"):
    # If already exists then use it
    if os.path.exists(local_path):
        return local_path

    print("Downloading model from Hugging Face...")

    downloaded_path = hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=HF_MODEL_FILENAME
    )

    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    shutil.copy(downloaded_path, local_path)

    return local_path

def save_model_to_hf(model_path="checkpoints/model.pth"):
    api = HfApi()
    api.upload_file(
        path_or_fileobj=model_path,
        path_in_repo=HF_MODEL_FILENAME,
        repo_id=HF_REPO_ID,
        repo_type="model",
    )

    print(f"Model uploaded to Hugging Face at repo: {HF_REPO_ID}, filename: {HF_MODEL_FILENAME}")