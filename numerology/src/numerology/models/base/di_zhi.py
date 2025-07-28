from datetime import time
from numerology.const import DiZhiType
from numerology.const.wu_xing import WuXingType, YinYang
from numerology.models.base import NumerologyBaseMeta, BaseStem
from numerology.utils.validator import validate_int_range


class DiZhi(metaclass=NumerologyBaseMeta):
    ZI = BaseStem(
        type=DiZhiType.ZI, yin_yang=YinYang.YANG, sequence=1,
        element=WuXingType.WATER
    )

    CHOU = BaseStem(
        type=DiZhiType.CHOU, yin_yang=YinYang.YIN, sequence=2,
        element=WuXingType.EARTH
    )
    YIN = BaseStem(
        type=DiZhiType.YIN, yin_yang=YinYang.YANG, sequence=3,
        element=WuXingType.WOOD
    )
    MAO = BaseStem(
        type=DiZhiType.MAO, yin_yang=YinYang.YIN, sequence=4,
        element=WuXingType.WOOD
    )
    CHEN = BaseStem(
        type=DiZhiType.CHEN, yin_yang=YinYang.YANG, sequence=5,
        element=WuXingType.EARTH
    )
    SI = BaseStem(
        type=DiZhiType.SI, yin_yang=YinYang.YIN, sequence=6,
        element=WuXingType.FIRE
    )
    WU = BaseStem(
        type=DiZhiType.WU, yin_yang=YinYang.YANG, sequence=7,
        element=WuXingType.FIRE
    )
    WEI = BaseStem(
        type=DiZhiType.WEI, yin_yang=YinYang.YIN, sequence=8,
        element=WuXingType.EARTH
    )
    SHEN = BaseStem(
        type=DiZhiType.SHEN, yin_yang=YinYang.YANG, sequence=9,
        element=WuXingType.METAL
    )
    YOU = BaseStem(
        type=DiZhiType.YOU, yin_yang=YinYang.YIN, sequence=10,
        element=WuXingType.METAL
    )
    XU = BaseStem(
        type=DiZhiType.XU, yin_yang=YinYang.YANG, sequence=11,
        element=WuXingType.EARTH
    )
    HAI = BaseStem(
        type=DiZhiType.HAI, yin_yang=YinYang.YIN, sequence=12,
        element=WuXingType.WATER
    )

    @validate_int_range(min_value=1, max_value=12)
    def __getitem__(self, index: int):

        if index not in self._index_map:
            raise IndexError(f"Index:{index} is not validated.")
        return self._index_map[index]

    @classmethod
    def get_di_zhi(cls, di_zhi: DiZhiType) -> BaseStem:
        if not isinstance(di_zhi, DiZhiType):
            return None
        return getattr(cls, di_zhi.name)

    def get_di_zhi_by_hour(self, t: time) -> BaseStem:

        for (start_time, end_time,), dizhi in DiZhiType.get_time_range_list().items():
            if start_time <= t < end_time:
                return self.get_di_zhi(di_zhi=dizhi)

        raise ValueError(f'Can not find:{time} in DiZhiType time range list')
