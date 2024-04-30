from fastapi import APIRouter
from fastapi.logger import logger

from func.lifelong_prediction import LifePrediction
from web.entity.life_prediction_entity import LifePredictionData

app = APIRouter()


@app.post("/predict")
async def predict_life(data: LifePredictionData) -> str:
    logger.info(f"Request data: {data}")
    life = LifePrediction(
        base_datetime=data.birthday,
        meta_info_display=data.meta_info,
        explain_append=data.explain,
        couple_birthday=data.couple_birthday,
        marry_date=data.marry_date,
        ru_zhui=data.ru_zhui,
        enabled_labels=",".join(data.option) if data.option else "core",
    )
    result = life.__str__()
    logger.info(result)
    return result
