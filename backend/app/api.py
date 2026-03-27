from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import app as router

app = FastAPI(title="Image Captioning API", description="API for training, predicting captions, and visualizing attention maps for images.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)