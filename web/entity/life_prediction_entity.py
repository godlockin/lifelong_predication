from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class LifePredictionData(BaseModel):
    birthday: datetime = Field(..., description="The birthday of yourself, in the format of 'YYYY-MM-DD HH:MM:SS'")
    meta_info: bool = Field(True, description="The bazi info for yourself, default as True")
    gander: bool = Field(True, description="The gander of yourself, default as male")
    explain: bool = Field(False, description="To check whether append explain details on different attributes")
    couple_birthday: datetime = Field(..., description="The birthday of your couple, in the format of 'YYYY-MM-DD HH:MM:SS'")
    marry_date: Optional[datetime] = Field(None, description="The date which you couples prepare to get marriage, in the format of 'YYYY-MM-DD HH:MM:SS'")
    ru_zhui: bool = Field(False, description="Set male as primary info to do calculation, and there were a special case on male's marriage is [ru zhui]")
    option: List[str] = Field(['core'], description='Choose an option from: bone_weight, zodiac_explain, lord_gods, lord_gods_structure, demigods, family_support, life_stages_luck, ten_years_luck, yearly_luck, intermarriage, potential_couple. Default is ["core"].')

    class Config:
        schema_extra = {
            "example": {
                "birthday": "1996-01-01 16:00:00",
                "gander": True,
                "explain": True,
                "couple_birthday": "1996-01-01 14:15:00",
                "marry_date": "2024-08-29 05:20:00",
                "ru_zhui": False,
                "option": ["core"],
                "display": False
            }
        }