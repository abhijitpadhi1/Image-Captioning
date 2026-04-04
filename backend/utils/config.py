DATA_FRACTION = 1
BATCH_SIZE = 32
EMBED_SIZE = 256
HIDDEN_SIZE = 512
FEATURE_DIM = 2048
VOCAB_FREQ_THRESHOLD = 2
# VOCAB_SIZE = 5000
LEARNING_RATE = 1e-3
FINETUNING_LR = 1e-4
NUM_EPOCHS = 20
SAMPLE_CNT_BLEU = 1000

CHECKPOINT_PATH = "backend/checkpoints/model.pth"
VOCAB_PATH = "backend/checkpoints/vocab.json"

HF_REPO_ID = "abhijitpadhi1/image-captioning-model"
HF_MODEL_FILENAME = "model.pth"
HF_VOCAB_FILENAME = "vocab.json"
