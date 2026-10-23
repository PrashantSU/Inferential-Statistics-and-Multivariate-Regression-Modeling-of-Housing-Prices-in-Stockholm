from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="Stockholm Housing API", version="1.0.0")

class HouseFeatures(BaseModel):
    region: str
    h_type: str
    balcony: str
    rooms: float
    area: float

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_version": "1.0.0"}

@app.post("/predict")
def predict(features: HouseFeatures):
    B0, SIGMA = 13.8988571, 0.3525
    REGION = {"Northeast": 0.0, "Northwest": 0.1850940, "Southeast": -0.1972418, "Stockholm": 0.3768469, "West": -0.4179828}
    TYPE = {"Apartment": 0.0, "Terrace": -0.0762431, "Villa": 0.1829979}
    BALC = {"No": 0.0, "Yes": -0.0697553}
    B_ROOMS, B_AREA, B_INT = 0.1103812, 0.0138216, -0.0010429

    size_val = B_ROOMS * features.rooms + B_AREA * features.area + B_INT * features.rooms * features.area
    log_price = B0 + REGION[features.region] + TYPE[features.h_type] + BALC[features.balcony] + size_val
    
    price = float(np.exp(log_price))
    lower = float(np.exp(log_price - 1.96 * SIGMA))
    upper = float(np.exp(log_price + 1.96 * SIGMA))

    return {
        "price": price,
        "lower": lower,
        "upper": upper,
        "contributions": {
            "baseline": float(np.exp(B0)),
            "size": float(np.exp(B0 + size_val) - np.exp(B0)),
            "region": float(np.exp(B0 + size_val + REGION[features.region]) - np.exp(B0 + size_val)),
            "type": float(np.exp(B0 + size_val + REGION[features.region] + TYPE[features.h_type]) - np.exp(B0 + size_val + REGION[features.region])),
            "balcony": float(np.exp(log_price) - np.exp(B0 + size_val + REGION[features.region] + TYPE[features.h_type]))
        }
    }