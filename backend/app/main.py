# from services.trainer import start_training_service
from ..services.trainer import start_training_service
from ..utils.setup import download_nltk_resources

def main():
    print("Initializing the NLTK resources...")
    download_nltk_resources()
    print("Starting Image Captioning Training Service...")
    result = start_training_service()
    print("Training completed. BLEU Scores:")
    print(f"Beam Search BLEU Score: {result['bleu_score_beam']}")
    print(f"Greedy Search BLEU Score: {result['bleu_score_greedy']}")

if __name__ == "__main__":
    main()