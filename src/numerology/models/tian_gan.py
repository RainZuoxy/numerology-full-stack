from typing import List, Dict
from numerology.const import TianGanType
from numerology.const.wu_xing import WuXingType, YinYang
from numerology.models.base import NumerologyBaseMeta, BaseStem
from numerology.utils.validator import validate_int_range


class TianGan(metaclass=NumerologyBaseMeta):

    JIA = BaseStem(
        element=TianGanType.JIA, yin_yang=YinYang.YANG, sequence=1, wu_xing=WuXingType.WOOD
    )
    YI = BaseStem(
        element=TianGanType.YI, yin_yang=YinYang.YIN, sequence=2, wu_xing=WuXingType.WOOD
    )
    BING = BaseStem(
        element=TianGanType.BING, yin_yang=YinYang.YANG, sequence=3, wu_xing=WuXingType.FIRE
    )
    DING = BaseStem(
        element=TianGanType.DING, yin_yang=YinYang.YIN, sequence=4, wu_xing=WuXingType.FIRE
    )
    WU = BaseStem(
        element=TianGanType.WU, yin_yang=YinYang.YANG, sequence=5, wu_xing=WuXingType.EARTH
    )
    JI = BaseStem(
        element=TianGanType.JI, yin_yang=YinYang.YIN, sequence=6, wu_xing=WuXingType.EARTH
    )
    GENG = BaseStem(
        element=TianGanType.GENG, yin_yang=YinYang.YANG, sequence=7, wu_xing=WuXingType.METAL
    )
    XIN = BaseStem(
        element=TianGanType.XIN, yin_yang=YinYang.YIN, sequence=8, wu_xing=WuXingType.METAL
    )
    REN = BaseStem(
        element=TianGanType.REN, yin_yang=YinYang.YANG, sequence=9, wu_xing=WuXingType.WATER
    )
    GUI = BaseStem(
        element=TianGanType.GUI, yin_yang=YinYang.YIN, sequence=10, wu_xing=WuXingType.WATER
    )

    _mapping = {
        TianGanType.JIA: JIA, TianGanType.YI: YI,
        TianGanType.BING: BING, TianGanType.DING: DING,
        TianGanType.WU: WU, TianGanType.JI: JI,
        TianGanType.GENG: GENG, TianGanType.XIN: XIN,
        TianGanType.REN: REN, TianGanType.GUI: GUI
    }

    @validate_int_range(min_value=1, max_value=10)
    def __getitem__(self, index: int):
        if index not in self._index_map:
            raise IndexError(f"Index:{index} is not validated.")
        return self._index_map[index]

    @property
    def mapping(self) -> Dict[TianGanType, BaseStem]:
        return self._mapping

    def get_tian_gan_list(self) -> List[BaseStem]:
        tiangan_list = [item for item in self.mapping.values()]
        tiangan_list.sort(key=lambda item: item.sequence)
        return tiangan_list
