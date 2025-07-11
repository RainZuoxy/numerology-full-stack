from typing import List, Union
from pydantic import BaseModel, ConfigDict
from numerology.const.di_zhi import DiZhiType
from numerology.const.tian_gan import TianGanType
from numerology.const.wu_xing import WuXingType, YinYang


class BaseStem(BaseModel):
    element: Union[TianGanType, DiZhiType]
    yin_yang: YinYang
    sequence: int
    wu_xing: WuXingType

    model_config = ConfigDict(use_enum_values=False)


class HeavenlyStem(BaseStem):
    ...


class EarthlyBranch(BaseStem):
    hidden: List[HeavenlyStem]


# class PillarElement(BaseModel):
#     name: Union[TianGanType, DiZhiType]
#     yin_yang: YinYang
#     sequence: int
#     wu_xing: WuXingType
#
#     model_config = ConfigDict(
#         use_enum_values=False,
#     )
#
#     def get_shi_shen(self, day_master) -> ShiShenType:
#         if not self.shi_shen:
#             relationship = self.wu_xing.get_relationship(day_master.wu_xing)
#             is_same = not (self.yin_yang ^ day_master.yin_yang)
#             self.shi_shen = ShiShenType.get_relationship(relationship_type=relationship, is_same=is_same)
#
#         return self.shi_shen
#
#     def set_wu_xing_positive(self, positive: bool):
#         self.wu_xing.base.yin_yang = positive
#
#     def get_wu_xing_dict(self):
#         return dict(name=self.wu_xing.get_name(), positive=self.yin_yang)
#
#     def get_shi_shen_dict(self):
#         return dict(name=self.shi_shen.value, positive=self.yin_yang)
#
#
# class PillarEarthElement(PillarElement):
#     hidden: List[PillarElement]


class PillarItem(BaseModel):
    name: str
    tian_gan: HeavenlyStem = None
    di_zhi: EarthlyBranch = None

    # def __dict__(self):
    #     return dict(name=self.name, tian_gan=self.tian_gan.__dict__(), di_zhi=self.di_zhi.__dict__())

    def get_wu_xing(self):
        return dict(name=self.name, tian_gan=self.tian_gan.get_wu_xing_dict(), di_zhi=self.di_zhi.get_wu_xing_dict())

    def get_shi_shen(self):
        return dict(name=self.name, tian_gan=self.tian_gan.get_shi_shen_dict(), di_zhi=self.di_zhi.get_shi_shen_dict())
