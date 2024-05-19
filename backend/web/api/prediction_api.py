from typing import Dict

from fastapi import APIRouter

from backend.constants.constants import LIFE_PREDICTION_LABELS
from backend.web.entity.process_request import QueryDto
from backend.web.services.life_predicting_service import LifePredictionOperator

app = APIRouter()


@app.get("/features")
async def get_features() -> Dict[str, str]:
    return LIFE_PREDICTION_LABELS


@app.post("/process")
async def predict_life(item: QueryDto):
    life_prediction = LifePredictionOperator(item)

    return life_prediction.do_predict()
