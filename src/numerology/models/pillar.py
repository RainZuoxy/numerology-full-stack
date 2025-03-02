from datetime import time
from typing import Any
from pydantic import BaseModel
from numerology.const.wu_xing import ShiShenType
from numerology.models.wu_xing import WuXing


class PillarElement(BaseModel):
    name: str
    positive: bool
    sequence: int
    wu_xing: WuXing
    shi_shen: ShiShenType = None

    def get_shi_shen(self, pillar) -> ShiShenType:
        if not self.shi_shen:
            relationship = self.wu_xing.get_relationship(pillar.wu_xing)
            same = 1 if self.positive == pillar.positive else 0
            self.shi_shen = ShiShenType.get_relationship(relationship_type=relationship, same=same)

        return self.shi_shen

    # def __dict__(self):
    #     return dict(
    #         name=self.name, positive=self.positive, wu_xing=self.wu_xing.get_name(),
    #         shi_shen=self.shi_shen.value if self.shi_shen else ''
    #     )

    def get_wu_xing_dict(self):
        return dict(name=self.wu_xing.get_name(), positive=self.positive)

    def get_shi_shen_dict(self):
        return dict(name=self.shi_shen.value, positive=self.positive)


class PillarEarthElement(PillarElement):
    start_time: time = None
    end_time: time = None


class PillarItem(BaseModel):
    name: str
    tian_gan: PillarElement = None
    di_zhi: PillarEarthElement = None

    # def __dict__(self):
    #     return dict(name=self.name, tian_gan=self.tian_gan.__dict__(), di_zhi=self.di_zhi.__dict__())

    def get_wu_xing(self):
        return dict(name=self.name, tian_gan=self.tian_gan.get_wu_xing_dict(), di_zhi=self.di_zhi.get_wu_xing_dict())

    def get_shi_shen(self):
        return dict(name=self.name, tian_gan=self.tian_gan.get_shi_shen_dict(), di_zhi=self.di_zhi.get_shi_shen_dict())
