from typing import Optional

from pydantic import BaseModel

from backend.web.entity.bone_weight_info import BoneWeightDto
from backend.web.entity.lord_gods_structure_info import LordGodsStructureDto
from backend.web.entity.meta_info import MetaInfoDto, BaZiElementsDto
from backend.web.entity.process_request import QueryDto


class PredictionDto(BaseModel):
    queryDto: QueryDto
    metaInfo: MetaInfoDto
    baziElements: BaZiElementsDto
    boneWeight: Optional[BoneWeightDto] = None
    lordGodsStructure: Optional[LordGodsStructureDto] = None
