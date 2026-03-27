from training.preprocessing import Preprocessor
from training.train import ModelTrainer


def start_training_service():
    ## Download, Preprocess and Load data
    preprocessor = Preprocessor()

    dataloader, vocab, transform, image_to_captions, vocab_size = preprocessor.load_data(
        batch_size=8,
        vocab_freq_threshold=2
    )

    ## Initialize Trainer
    trainer = ModelTrainer(
        dataloader=dataloader,
        vocab=vocab,
        transform=transform,
        # For decoder
        feature_dim=2048,
        embed_size=256,
        hidden_size=256,
        vocab_size=vocab_size
    )
    
    ## Train the model
    trainer.train(num_epochs=10)

    ## BLUE evaluation
    bleu_beam = trainer.bleu_score(
        image_paths=list(image_to_captions.keys()),
        image_to_captions=image_to_captions,
        inference="beam"
    )
    bleu_greedy = trainer.bleu_score(
        image_paths=list(image_to_captions.keys()),
        image_to_captions=image_to_captions,
        inference="greedy"
    )

    return {
        "message": "Training completed",
        "bleu_score_beam": round(bleu_beam, 4),
        "bleu_score_greedy": round(bleu_greedy, 4)
    }