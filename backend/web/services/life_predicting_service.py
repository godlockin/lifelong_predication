from backend.func.lifelong_prediction import LifePrediction
from backend.web.entity.process_request import Item
from backend.func import *


class LifePredictionOperator:
    def __init__(self, item: Item):
        self.item = item
        predict_req = {
            "name": item.name,
            "base_datetime": item.birth,
            "meta_info_display": True,
            "explain_append": item.addDetails,
            "couple_birthday": item.partnerBirth,
            "marry_date": item.marriageDate,
            "ru_zhui": item.isBridegroom,
            "is_male": item.gender == "male",
            "enabled_labels": item.enabledFeatures,
        }
        self.life_prediction = LifePrediction(**predict_req)
