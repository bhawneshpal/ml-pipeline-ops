import json
import logging

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

# Setup structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger("ml-service")

app = FastAPI(title="ML Pipeline Ops")

# Load active model based on metadata
def load_active_model():
    with open("model/metadata.json", "r") as f:
        metadata = json.load(f)
    active_version = metadata["active_version"]
    model_path = metadata["versions"][active_version]["file"]
    model = joblib.load(model_path)
    logger.info(f"Loaded active model: {active_version}")
    return model, active_version

model, active_version = load_active_model()

# Request schema with validation (this is our "bad input protection")
class PredictRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    @field_validator("sepal_length", "sepal_width", "petal_length", "petal_width")
    @classmethod
    def must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Measurement must be a positive number")
        return value


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "active_version": active_version
    }


@app.post("/predict")
def predict(request: PredictRequest):
    try:
        features = [[
            request.sepal_length,
            request.sepal_width,
            request.petal_length,
            request.petal_width
        ]]
        prediction = model.predict(features)[0]
        logger.info(f"Prediction made using {active_version}: class={int(prediction)}")
        return {
            "prediction": int(prediction),
            "model_version": active_version
        }
    except (ValueError, RuntimeError) as e:
        logger.error(f"Prediction failed: {e!s}")
    raise HTTPException(status_code=500, detail="Prediction failed")