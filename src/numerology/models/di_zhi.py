from typing import List, Dict
from datetime import time
from numerology.const import DiZhiType
from numerology.const.wu_xing import WuXingType, YinYang
from numerology.models.base import NumerologyBaseMeta, BaseStem
from numerology.utils.validator import validate_int_range


class DiZhi(metaclass=NumerologyBaseMeta):

    ZI = BaseStem(
        element=DiZhiType.ZI, yin_yang=YinYang.YANG, sequence=1,
        wu_xing=WuXingType.WATER
    )

    CHOU = BaseStem(
        element=DiZhiType.CHOU, yin_yang=YinYang.YIN, sequence=2,
        wu_xing=WuXingType.EARTH
    )
    YIN = BaseStem(
        element=DiZhiType.YIN, yin_yang=YinYang.YANG, sequence=3,
        wu_xing=WuXingType.WOOD
    )
    MAO = BaseStem(
        element=DiZhiType.MAO, yin_yang=YinYang.YIN, sequence=4,
        wu_xing=WuXingType.WOOD
    )
    CHEN = BaseStem(
        element=DiZhiType.CHEN, yin_yang=YinYang.YANG, sequence=5,
        wu_xing=WuXingType.EARTH
    )
    SI = BaseStem(
        element=DiZhiType.SI, yin_yang=YinYang.YIN, sequence=6,
        wu_xing=WuXingType.FIRE
    )
    WU = BaseStem(
        element=DiZhiType.WU, yin_yang=YinYang.YANG, sequence=7,
        wu_xing=WuXingType.FIRE
    )
    WEI = BaseStem(
        element=DiZhiType.WEI, yin_yang=YinYang.YIN, sequence=8,
        wu_xing=WuXingType.EARTH
    )
    SHEN = BaseStem(
        element=DiZhiType.SHEN, yin_yang=YinYang.YANG, sequence=9,
        wu_xing=WuXingType.METAL
    )
    YOU = BaseStem(
        element=DiZhiType.YOU, yin_yang=YinYang.YIN, sequence=10,
        wu_xing=WuXingType.METAL
    )
    XU = BaseStem(
        element=DiZhiType.XU, yin_yang=YinYang.YANG, sequence=11,
        wu_xing=WuXingType.EARTH
    )
    HAI = BaseStem(
        element=DiZhiType.HAI, yin_yang=YinYang.YIN, sequence=12,
        wu_xing=WuXingType.WATER
    )

    _mapping = {
        DiZhiType.ZI: ZI, DiZhiType.CHOU: CHOU,
        DiZhiType.YIN: YIN, DiZhiType.MAO: MAO,
        DiZhiType.CHEN: CHEN, DiZhiType.SI: SI,
        DiZhiType.WU: WU, DiZhiType.WEI: WEI,
        DiZhiType.SHEN: SHEN, DiZhiType.YOU: YOU,
        DiZhiType.XU: XU, DiZhiType.HAI: HAI
    }

    @validate_int_range(min_value=1, max_value=12)
    def __getitem__(self, index: int):

        if index not in self._index_map:
            raise IndexError(f"Index:{index} is not validated.")
        return self._index_map[index]

    @property
    def mapping(self) -> Dict[DiZhiType, BaseStem]:
        return self._mapping

    def get_di_zhi_list(self) -> List[BaseStem]:
        dizhi_list = [item for item in self.mapping.values()]
        dizhi_list.sort(key=lambda item: item.sequence)
        return dizhi_list

    def get_di_zhi_by_hour(self, t: time) -> BaseStem:

        for (start_time, end_time,), dizhi in DiZhiType.get_time_range_list().items():
            if start_time <= t < end_time:
                return self.mapping[dizhi]

        raise ValueError(f'Can not find:{time} in DiZhiType time range list')
