from fastapi import FastAPI, UploadFile, File

from services.trainer import start_training_service
from services.captioning import predict_caption_service
from services.visualize import visualize_attention_service
from utils.logger import logger

app = FastAPI()


@app.get("/")
def home():
    logger.info("API Root accessed")
    return {"message": "Image Captioning API Running"}


# Training trigger
@app.post("/train")
def train():
    return start_training_service()


# Caption prediction
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    return predict_caption_service(file)


# Attention visualization
@app.post("/visualize")
async def visualize(file: UploadFile = File(...)):
    return await visualize_attention_service(file)