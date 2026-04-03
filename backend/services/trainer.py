from ..training.preprocessing import Preprocessor
from ..training.train import ModelTrainer
from ..utils.config import (
    BATCH_SIZE,
    EMBED_SIZE,
    HIDDEN_SIZE,
    FEATURE_DIM,
    NUM_EPOCHS,
    VOCAB_FREQ_THRESHOLD,
    SAMPLE_CNT_BLEU
)


def start_training_service():
    ## Download, Preprocess and Load data
    preprocessor = Preprocessor()

    dataloader, vocab, transform, image_to_captions, vocab_size = preprocessor.load_data(
        batch_size=BATCH_SIZE,
        vocab_freq_threshold=VOCAB_FREQ_THRESHOLD
    )

    ## Initialize Trainer
    trainer = ModelTrainer(
        dataloader=dataloader,
        vocab=vocab,
        transform=transform,
        # For decoder
        feature_dim=FEATURE_DIM,
        embed_size=EMBED_SIZE,
        hidden_size=HIDDEN_SIZE,
        vocab_size=vocab_size
    )
    
    ## Train the model
    trainer.train(num_epochs=NUM_EPOCHS)

    ## Upload the model to Hugging Face
    trainer.save_model_to_hf("checkpoints/model.pth")

    ## BLUE evaluation
    bleu_beam = trainer.bleu_score(
        image_paths=list(image_to_captions.keys()),
        image_to_captions=image_to_captions,
        inference="beam",
        max_samples=SAMPLE_CNT_BLEU
    )
    bleu_greedy = trainer.bleu_score(
        image_paths=list(image_to_captions.keys()),
        image_to_captions=image_to_captions,
        inference="greedy",
        max_samples=SAMPLE_CNT_BLEU
    )

    return {
        "message": "Training completed",
        "bleu_score_beam": round(bleu_beam, 4),
        "bleu_score_greedy": round(bleu_greedy, 4)
    }