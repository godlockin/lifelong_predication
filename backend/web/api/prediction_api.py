from typing import Dict

from fastapi import APIRouter

from backend.constants.constants import LIFE_PREDICTION_LABELS
from backend.web.entity.process_request import Item

app = APIRouter()


@app.get("/features")
async def get_features() -> Dict[str, str]:
    return LIFE_PREDICTION_LABELS


@app.post("/process")
async def predict_life(item: Item):
    # 这里调用现有的Python程序进行处理
    result = {
        "name": item.name,
        "description": item.description,
        "birthdate": item.birthdate,
        "gender": item.gender,
        "partnerBirthdate": item.partnerBirthdate,
        "marriageDate": item.marriageDate,
        "isBridegroom": item.isBridegroom,
        "addDetails": item.addDetails,
        "enabledFeatures": item.enabledFeatures
    }
    return result
