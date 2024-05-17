from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class QueryDto(BaseModel):
    name: str
    selfBirthday: datetime
    gender: Optional[str] = None
    partnerBirthday: Optional[datetime] = None
    marriageDate: Optional[datetime] = None
    isBridegroom: Optional[bool] = False
    addDetails: Optional[bool] = False
    enabledFeatures: List[str]
