from pydantic import BaseModel
from numerology.models.base import BaseStem


class PillarItem(BaseModel):
    name: str
    tian_gan: BaseStem = None
    di_zhi: BaseStem = None

    def __repr__(self):
        return f"{self.name}: {self.tian_gan} {self.di_zhi}"

    __str__ = __repr__
