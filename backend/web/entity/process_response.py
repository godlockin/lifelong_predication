from pydantic import BaseModel

from backend.web.entity.bone import BoneWeightDto
from backend.web.entity.meta_info import MetaInfoDto, BaZiElementsDto
from backend.web.entity.process_request import QueryDto


class PredictionDto(BaseModel):
    queryDto: QueryDto
    metaInfo: MetaInfoDto
    baziElements: BaZiElementsDto
    boneWeight: BoneWeightDto
