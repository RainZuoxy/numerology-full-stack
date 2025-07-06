from datetime import time
from pydantic import BaseModel
from numerology.const.wu_xing import ShiShenType
from numerology.models.wu_xing import WuXing


class PillarElement(BaseModel):
    name: str
    positive: bool
    sequence: int
    wu_xing: WuXing
    shi_shen: ShiShenType = None

    # def model_post_init(self, __context: Any) -> None:
    #     if self.wu_xing.base.positive is None:
    #         self.wu_xing.base.positive = self.positive

    def get_shi_shen(self, day_master: "PillarElement") -> ShiShenType:
        if not self.shi_shen:
            relationship = self.wu_xing.get_relationship(day_master.wu_xing)
            is_same = not (self.positive ^ day_master.positive)
            self.shi_shen = ShiShenType.get_relationship(relationship_type=relationship, is_same=is_same)

        return self.shi_shen

    def set_wu_xing_positive(self, positive: bool):
        self.wu_xing.base.positive = positive

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
