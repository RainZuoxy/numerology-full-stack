import math
from datetime import datetime
from typing import Iterator, Tuple, Union

from numerology.const import DiZhiType, Gender, ShiShenType
from numerology.core.relationship import WuXingRelationship, ShiShenRelationship
from numerology.models import TianGan, TIAN_GAN, DI_ZHI
from numerology.core.ganzhi_calendar import GanZhiCalendar
from numerology.models.base import BaseStem
from numerology.models.cang_gan import CangGan
# from numerology.models.chart import MainDestinyChart
from numerology.models.pillar import PillarItem
from numerology.utils.validator import convert_tian_gan_index, convert_di_zhi_index

SS_TYPE = Union[ShiShenType, None]


class BaZiChartGenerateMixin:

    @staticmethod
    def get_chinese_zodiac(type_: DiZhiType) -> str:
        return type_.get_chinese_zodiac()

    @staticmethod
    def get_day_master(day_pillar: PillarItem) -> BaseStem:
        return day_pillar.tian_gan

    def check_de_ling(self, day_master: BaseStem, month_di_zhi: BaseStem) -> bool:
        relationship = WuXingRelationship.get_relationship(base=day_master.element, other=month_di_zhi.element)
        if relationship in WuXingRelationship.get_supported_and_produced():
            return True
        return False

    @classmethod
    def get_flag_for_gender_and_chinese_zodiac(cls, gender: Gender, dizhi_year: BaseStem) -> bool:
        return (
                (gender.value == 1 and dizhi_year.yin_yang.value == "阳") or
                (gender.value == 0 and dizhi_year.yin_yang.value == "阴")
        )

    @staticmethod
    def get_start_age(dob: datetime, flag_for_gender_and_chinese_zodiac: bool) -> float:
        step = 'backward' if flag_for_gender_and_chinese_zodiac else "forward"
        diff = GanZhiCalendar(dob=dob).get_days_until_nearest_solar_term(orient=step)
        start_age = diff.days / 3
        return start_age

    @staticmethod
    def standard_start_age(start_age: float) -> str:
        month, year = math.modf(start_age)
        return f"{int(year)}岁{int(month * 12):02d}个月"

    @classmethod
    def get_main_destiny(
            cls,
            month_pillar: PillarItem,
            flag_for_gender_and_chinese_zodiac: bool,
            num: int
    ) -> Iterator[Tuple[BaseStem, BaseStem]]:
        tg_md_index = month_pillar.tian_gan.sequence
        dz_md_index = month_pillar.di_zhi.sequence

        step = 1 if flag_for_gender_and_chinese_zodiac else -1

        for i in range(num):
            tg_md_index += step
            tg_md_index = convert_tian_gan_index(index=tg_md_index)

            dz_md_index += step
            dz_md_index = convert_di_zhi_index(index=dz_md_index)

            yield TIAN_GAN[tg_md_index], DI_ZHI[dz_md_index]


class ShiShenGenerateMixin:

    @staticmethod
    def get_shi_shen(day_master: BaseStem, target: BaseStem) -> SS_TYPE:
        if not (day_master and target):
            return None
        flag_for_yinyang = WuXingRelationship.is_same_yin_yang(first=day_master, second=target)
        relationship = WuXingRelationship.get_relationship(base=day_master.element, other=target.element)
        return ShiShenRelationship.get_result_by_relationship(
            relationship_type=relationship, is_yin_yang=flag_for_yinyang
        )

    @classmethod
    def get_shi_shen_by_cang_gan(cls, day_master: BaseStem, di_zhi: DiZhiType) -> Tuple[ShiShenType, SS_TYPE, SS_TYPE]:
        zhu_qi, zhonq_qi, yu_qi = CangGan.get_cang_gan(di_zhi=di_zhi).value.get_qis()

        return (
            cls.get_shi_shen(day_master=day_master, target=TianGan.get_tian_gan(zhu_qi)),
            cls.get_shi_shen(day_master=day_master, target=TianGan.get_tian_gan(zhonq_qi)),
            cls.get_shi_shen(day_master=day_master, target=TianGan.get_tian_gan(yu_qi)),
        )

    # @classmethod
    # def get_shi_shen_by_main_destiny(cls, day_master: BaseStem, main_destiny:MainDestinyChart):
    #     tmp = []
    #     for item in main_destiny.items:


