from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Item(BaseModel):
    name: str
    birthdate: datetime
    gender: Optional[str] = None
    partnerBirthdate: Optional[datetime] = None
    marriageDate: Optional[datetime] = None
    isBridegroom: Optional[bool] = False
    addDetails: Optional[bool] = False
    enabledFeatures: List[str]
