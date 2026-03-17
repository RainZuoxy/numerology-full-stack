from typing import Tuple

from pydantic import BaseModel

from numerology.models.pillar import PillarItem


class MainDestinyItem(BaseModel):
    schedule: Tuple[float, float]
    origin_item: PillarItem
    shi_shen:Tuple[str,Tuple]


    def get_schedule(self):
        return f"{self.schedule[0]} ~ {self.schedule[1]}"

    def get_shi_shen(self):
        dz = ','.join([i.value if i else '_' for i in self.shi_shen[1]])
        return f"{self.shi_shen[0]}-{dz}"
