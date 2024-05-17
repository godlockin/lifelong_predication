from pydantic import BaseModel


class MetaInfoDto(BaseModel):
    name: str
    birthdate: str
    lunar_birthday: str
    lunar_birthday_hour: str
    bazi: str
    zodiac: str
    zodiac_cn: str
    year_gan: str
    year_gan_element: str
    year_zhi: str
    year_zhi_element: str
    month_gan: str
    month_gan_element: str
    month_zhi: str
    month_zhi_element: str
    day_gan: str
    day_gan_element: str
    day_zhi: str
    day_zhi_element: str
    hour_gan: str
    hour_gan_element: str


class BaZiElementsDto(BaseModel):
    isStrong: bool
    isPositive: bool
    supportingElements: list[str]
    opposingElements: list[str]
    elementsInfluence: dict[str, str]
    elementsInfluenceWeight: dict[str, float]
