from fastapi.routing import APIRouter

from backend.web.api.health_check import app as health_check_api
from backend.web.api.prediction_api import app as prediction_api

api_router = APIRouter()

api_router.include_router(health_check_api, prefix="")
api_router.include_router(prediction_api, prefix="/prediction")
