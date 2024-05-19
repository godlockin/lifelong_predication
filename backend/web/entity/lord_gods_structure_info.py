from pydantic import BaseModel


class LordGodsStructureDto(BaseModel):
    structure: str
    structureAppend: str
    structureDescription: str
    structureImagery: str
    comment: str
    isStructurePositive: bool
    structureFix: str