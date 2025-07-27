from pydantic import BaseModel
from numerology.models.base import BaseStem


class PillarItem(BaseModel):
    name: str
    tian_gan: BaseStem = None
    di_zhi: BaseStem = None
