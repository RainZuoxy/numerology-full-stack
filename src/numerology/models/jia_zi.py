from typing import List
from datetime import time
from numerology.const.wu_xing import TianGanType, DiZhiType, JIA_ZI
from numerology.models.pillar import PillarElement, PillarEarthElement
from numerology.models.wu_xing import WuXingRegister


class TianGan:

    _tian_gan_list = None

    @classmethod
    def create_tian_gan_list(cls) -> List[PillarElement]:
        return [
            PillarElement(name=TianGanType.JIA.value, positive=True, sequence=1, wu_xing=WuXingRegister.get_wood()),
            PillarElement(name=TianGanType.YI.value, positive=False, sequence=2, wu_xing=WuXingRegister.get_wood()),
            PillarElement(name=TianGanType.BING.value, positive=True, sequence=3, wu_xing=WuXingRegister.get_fire()),
            PillarElement(name=TianGanType.DING.value, positive=False, sequence=4, wu_xing=WuXingRegister.get_fire()),
            PillarElement(name=TianGanType.WU.value, positive=True, sequence=5, wu_xing=WuXingRegister.get_earth()),
            PillarElement(name=TianGanType.JI.value, positive=False, sequence=6, wu_xing=WuXingRegister.get_earth()),
            PillarElement(name=TianGanType.GENG.value, positive=True, sequence=7, wu_xing=WuXingRegister.get_metal()),
            PillarElement(name=TianGanType.XIN.value, positive=False, sequence=8, wu_xing=WuXingRegister.get_metal()),
            PillarElement(name=TianGanType.REN.value, positive=True, sequence=9, wu_xing=WuXingRegister.get_water()),
            PillarElement(name=TianGanType.GUI.value, positive=False, sequence=10, wu_xing=WuXingRegister.get_water())
        ]

    @classmethod
    def get_tian_gan_list(cls):
        if not cls._tian_gan_list:
            cls._tian_gan_list = cls.create_tian_gan_list()

        return cls._tian_gan_list

    @classmethod
    def get_tian_gan_by_index(cls, index: int) -> PillarElement:
        # if not 0 <= index < 11:
        #     raise ValueError('查无此天干, 天干只有10个.')

        return cls.get_tian_gan_list()[index - 1]

    @classmethod
    def get_tian_gan_by_name(cls, tian_gan_name: str) -> PillarElement:
        tian_gan = [item for item in cls.get_tian_gan_list() if item.name == tian_gan_name]

        if len(tian_gan) == 0:
            raise ValueError(f'无法查找天干 - {tian_gan_name}')

        return tian_gan[0]


class DiZhi:

    _di_zhi_list = None

    @classmethod
    def create_di_zhi_list(cls) -> List[PillarEarthElement]:
        return [
            PillarEarthElement(
                name=DiZhiType.ZI.value, positive=True, sequence=0,
                start_time=time(23, 0, 0), end_time=time(23, 59, 59), wu_xing=WuXingRegister.get_water()
            ),
            PillarEarthElement(
                name=DiZhiType.ZI.value, positive=True, sequence=1,
                start_time=time(0, 0, 0), end_time=time(0, 59, 59), wu_xing=WuXingRegister.get_water()
            ),
            PillarEarthElement(
                name=DiZhiType.CHOU.value, positive=False, sequence=2,
                start_time=time(1, 0, 0), end_time=time(2, 59, 59), wu_xing=WuXingRegister.get_earth()
            ),
            PillarEarthElement(
                name=DiZhiType.YIN.value, positive=True, sequence=3,
                start_time=time(3, 0, 0), end_time=time(4, 59, 59), wu_xing=WuXingRegister.get_wood()
            ),
            PillarEarthElement(
                name=DiZhiType.MAO.value, positive=False, sequence=4,
                start_time=time(5, 0, 0), end_time=time(6, 59, 59), wu_xing=WuXingRegister.get_wood()
            ),
            PillarEarthElement(
                name=DiZhiType.CHEN.value, positive=True, sequence=5,
                start_time=time(7, 0, 0), end_time=time(8, 59, 59), wu_xing=WuXingRegister.get_earth()
            ),
            PillarEarthElement(
                name=DiZhiType.SI.value, positive=False, sequence=6,
                start_time=time(9, 0, 0), end_time=time(10, 59, 59), wu_xing=WuXingRegister.get_fire()
            ),
            PillarEarthElement(
                name=DiZhiType.WU.value, positive=True, sequence=7,
                start_time=time(11, 0, 0), end_time=time(12, 59, 59), wu_xing=WuXingRegister.get_fire()
            ),
            PillarEarthElement(
                name=DiZhiType.WEI.value, positive=False, sequence=8,
                start_time=time(13, 0, 0), end_time=time(14, 59, 59), wu_xing=WuXingRegister.get_earth()
            ),
            PillarEarthElement(
                name=DiZhiType.SHEN.value, positive=True, sequence=9,
                start_time=time(15, 0, 0), end_time=time(16, 59, 59), wu_xing=WuXingRegister.get_metal()
            ),
            PillarEarthElement(
                name=DiZhiType.YOU.value, positive=False, sequence=10,
                start_time=time(17, 0, 0), end_time=time(18, 59, 59), wu_xing=WuXingRegister.get_metal()
            ),
            PillarEarthElement(
                name=DiZhiType.XU.value, positive=True, sequence=11,
                start_time=time(19, 0, 0), end_time=time(20, 59, 59), wu_xing=WuXingRegister.get_earth()
            ),
            PillarEarthElement(
                name=DiZhiType.HAI.value, positive=False, sequence=12,
                start_time=time(21, 0, 0), end_time=time(22, 59, 59), wu_xing=WuXingRegister.get_water()
            )
        ]

    @classmethod
    def get_di_zhi_list(cls):
        if not cls._di_zhi_list:
            cls._di_zhi_list = cls.create_di_zhi_list()

        return cls._di_zhi_list

    @classmethod
    def get_di_zhi_by_index(cls, index: int) -> PillarEarthElement:
        # if not 0 <= index < 13:
        #     raise ValueError('查无此地支, 地支只有12个.')

        return cls.get_di_zhi_list()[index - 1]

    @classmethod
    def get_di_zhi_by_name(cls, di_zhi_name: str) -> PillarEarthElement:
        di_zhi = [item for item in cls.get_di_zhi_list() if item.name == di_zhi_name]

        if len(di_zhi) == 0:
            raise ValueError(f'无法查找地支 - {di_zhi_name}')

        return di_zhi[0]

    @classmethod
    def get_di_zhi_by_hour(cls, t: time) -> PillarEarthElement:

        for item in cls.get_di_zhi_list():
            if item.start_time <= t < item.end_time:
                return item

        raise ValueError(f'无法查找{time}时辰的地支')


class JiaZi:

    _jia_zi_list = None

    @classmethod
    def get_jia_zi_list(cls):
        if not cls._jia_zi_list:
            cls._jia_zi_list = JIA_ZI

        return cls._jia_zi_list

    @classmethod
    def get_jia_zi_by_index(cls, tian_gan_index: int, di_zhi_index: int) -> str:
        if not 0 <= tian_gan_index < 6:
            raise ValueError('一个甲子只有5个天干系列')

        if not 0 <= di_zhi_index < 13:
            raise ValueError('一个甲子只包含12个地支')

        return cls.get_jia_zi_list()[((tian_gan_index - 1) * 12 + di_zhi_index) - 1]

    @classmethod
    def parse_pillar_string(cls, pillar_string: str) -> [PillarElement, PillarEarthElement]:
        if len(pillar_string) != 2:
            raise ValueError('天干地支柱内容长度不匹配')

        tian_gan, di_zhi = pillar_string[0], pillar_string[1]
        return TianGan.get_tian_gan_by_name(tian_gan_name=tian_gan), DiZhi.get_di_zhi_by_name(di_zhi_name=di_zhi)
