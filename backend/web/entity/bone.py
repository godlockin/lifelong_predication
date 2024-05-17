from pydantic import BaseModel


class BoneWeightDto(BaseModel):
    boneWeight: float
    description: str
    details: dict[str, float]
