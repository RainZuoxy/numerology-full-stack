from datetime import datetime
from typing import Any

from pydantic import BaseModel

from numerology.const.tian_gan import TianGanType
from numerology.core.rule import get_pillar_year_index, get_pillar_month_index, get_pillar_day_index
from numerology.models.wu_xing import WuXingRegister
from numerology.models import TIAN_GAN, DI_ZHI
from numerology.models.pillar import PillarItem
from numerology.models.jia_zi import JiaZi


class BaZiChart(BaseModel):
    lunar_dob_time: datetime
    day_master: TianGanType = None
    year_pillar: PillarItem = None
    month_pillar: PillarItem = None
    day_pillar: PillarItem = None
    hour_pillar: PillarItem = None

    def get_lunar_dob_time(self):
        return self.lunar_dob_time

    def get_pillars(self):
        return [self.year_pillar, self.month_pillar, self.day_pillar, self.hour_pillar]

    def analysis(self):
        self.year_pillar = self.compute_year_pillar(year=self.get_lunar_dob_time().year)
        self.month_pillar = self.compute_month_pillar(
            year=self.get_lunar_dob_time().year, month=self.get_lunar_dob_time().month
        )
        self.day_pillar = self.compute_day_pillar(solar_dt=self.get_dob_time())
        self.hour_pillar = self.compute_hour_pillar(dt=self.get_dob_time())
        self.day_master = self.day_pillar.tian_gan.name
        self.analysis_shi_shen()

    '''
        年份干支口诀:
        天干: (阴历年份-3)/10取余
        地支: (阴历年份-3)/12取余
    '''

    @classmethod
    def compute_year_pillar(cls, year: int) -> PillarItem:
        tiangan_index, dizhi_index = get_pillar_year_index(dob_year=year)
        return PillarItem(
            name='年柱', tian_gan=TIAN_GAN[tiangan_index], di_zhi=DI_ZHI[dizhi_index]
        )

    '''
    月份干支口诀:
    天干:
    凡甲年己年, 一月天干为丙, 二月天干为丁, 其余顺推;
    凡乙年庚年, 一月天干为戊, 二月天干为己, 其余顺推;
    凡丙年辛年, 一月天干为庚, 二月天干为辛, 其余顺推;
    凡丁年壬年, 一月天干为壬, 二月天干为癸, 其余顺推;
    凡戊年癸年, 一月天干为甲, 二月天干为乙, 其余顺推;
    地支:
    每月的地支是固定的, 正月为寅, 二月为卯, 三月为辰, 四月为巳, 五月为午, 六月为未,
    七月为申, 八月为酉, 九月为戌, 十月为亥, 十一月为子, 十二月为丑.
    '''

    @classmethod
    def compute_month_pillar(cls, year: int, month: int) -> PillarItem:
        start_pillars = {1: 3, 2: 5, 3: 7, 4: 9, 0: 9}
        year_pillar = cls.compute_year_pillar(year=year)
        tiangan_index,dizhi_index=get_pillar_month_index(
            sequence_year_tiangan=year_pillar.tian_gan.sequence, month=month
        )
        return PillarItem(
            name='月柱',
            tian_gan=TIAN_GAN[tiangan_index],
            di_zhi=DI_ZHI[dizhi_index]
        )

    '''
    日柱干支口诀:
    ((公元年数 - 1) * 5 + (公元年数 - 1) / 4 + 当天是当年的第几日) / 60 取余数
    天干: 余数 % 10取余
    地支: 余数 % 12取余
    '''

    @classmethod
    def compute_day_pillar(cls, solar_dt: datetime) -> PillarItem:
        tiangan_index,dizhi_index=get_pillar_day_index(dt=solar_dt)

        return PillarItem(
            name='日柱', tian_gan=TIAN_GAN[tiangan_index],
            di_zhi=DI_ZHI[dizhi_index]
        )

    '''
    时柱干支口诀:
    天干:
    甲日或己日, 子时则配甲, 即甲子, 丑时则顺排, 配乙, 即乙丑, 其余顺推;
    乙日或庚日, 子时则配丙, 即丙子, 丑时则顺排, 配丁, 即丁丑, 其余顺推;
    丙日或辛日, 子时则配戊, 即戊子, 丑时则顺排, 配己, 即己丑, 其余顺推;
    丁日或壬日, 子时则配庚, 即庚子, 其余顺排.
    戊日或癸日, 子时则配壬, 即壬子, 其余顺排.

    地支：
    子时: 23点--凌晨1点 - 丑时: 1点--凌晨3点
    寅时: 3点--凌晨5点 - 卯时: 5点--早晨7点
    辰时: 7点--上午9点 - 巳时: 9点--中午11点
    午时: 11点--下午13点 - 未时: 13点--下午15点
    申时: 15点--下午17点 - 酉时: 17点--下午19点
    戌时: 19点--晚上21点 - 亥时: 21点--晚上23点
    '''

    @classmethod
    def compute_hour_pillar(cls, dt: datetime) -> PillarItem:
        day_pillar = cls.compute_day_pillar(solar_dt=dt)
        tian_gan_index = day_pillar.tian_gan.sequence % 5
        di_zhi = DiZhi.get_di_zhi_by_hour(dt.time())
        jia_zi = JiaZi.get_jia_zi_by_index(tian_gan_index=tian_gan_index, di_zhi_index=di_zhi.sequence)
        tian_gan, _ = JiaZi.parse_pillar_string(jia_zi)

        return PillarItem(name='时柱', tian_gan=tian_gan, di_zhi=di_zhi)

    def analysis_shi_shen(self):
        self.year_pillar.tian_gan.get_shi_shen(day_master=self.day_pillar.tian_gan)
        self.year_pillar.di_zhi.get_shi_shen(day_master=self.day_pillar.tian_gan)
        self.month_pillar.tian_gan.get_shi_shen(day_master=self.day_pillar.tian_gan)
        self.month_pillar.di_zhi.get_shi_shen(day_master=self.day_pillar.tian_gan)
        self.day_pillar.di_zhi.get_shi_shen(day_master=self.day_pillar.tian_gan)
        self.hour_pillar.tian_gan.get_shi_shen(day_master=self.day_pillar.tian_gan)
        self.hour_pillar.di_zhi.get_shi_shen(day_master=self.day_pillar.tian_gan)


if __name__ == '__main__':
    print(2022 % 12)
