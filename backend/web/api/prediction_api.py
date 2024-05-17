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
    # 这里调用现有的Python程序进行处理
    result = {
        "name": item.name,
        "birthdate": item.birthdate,
        "gender": item.gender,
        "partnerBirthdate": item.partnerBirthdate,
        "marriageDate": item.marriageDate,
        "isBridegroom": item.isBridegroom,
        "addDetails": item.addDetails,
        "enabledFeatures": item.enabledFeatures
    }
    return result
