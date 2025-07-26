from numerology.const import TianGanType
from numerology.const.wu_xing import WuXingType, YinYang
from numerology.models.base import NumerologyBaseMeta, BaseStem
from numerology.utils.validator import validate_int_range


class TianGan(metaclass=NumerologyBaseMeta):
    JIA = BaseStem(
        type=TianGanType.JIA, yin_yang=YinYang.YANG, sequence=1, element=WuXingType.WOOD
    )
    YI = BaseStem(
        type=TianGanType.YI, yin_yang=YinYang.YIN, sequence=2, element=WuXingType.WOOD
    )
    BING = BaseStem(
        type=TianGanType.BING, yin_yang=YinYang.YANG, sequence=3, element=WuXingType.FIRE
    )
    DING = BaseStem(
        type=TianGanType.DING, yin_yang=YinYang.YIN, sequence=4, element=WuXingType.FIRE
    )
    WU = BaseStem(
        type=TianGanType.WU, yin_yang=YinYang.YANG, sequence=5, element=WuXingType.EARTH
    )
    JI = BaseStem(
        type=TianGanType.JI, yin_yang=YinYang.YIN, sequence=6, element=WuXingType.EARTH
    )
    GENG = BaseStem(
        type=TianGanType.GENG, yin_yang=YinYang.YANG, sequence=7, element=WuXingType.METAL
    )
    XIN = BaseStem(
        type=TianGanType.XIN, yin_yang=YinYang.YIN, sequence=8, element=WuXingType.METAL
    )
    REN = BaseStem(
        type=TianGanType.REN, yin_yang=YinYang.YANG, sequence=9, element=WuXingType.WATER
    )
    GUI = BaseStem(
        type=TianGanType.GUI, yin_yang=YinYang.YIN, sequence=10, element=WuXingType.WATER
    )

    @validate_int_range(min_value=1, max_value=10)
    def __getitem__(self, index: int):
        if index not in self._index_map:
            raise IndexError(f"Index:{index} is not validated.")
        return self._index_map[index]

    @classmethod
    def get_tian_gan(cls, tian_gan: TianGanType):
        if not isinstance(tian_gan, TianGanType):
            return None
        return getattr(cls, tian_gan.name)
