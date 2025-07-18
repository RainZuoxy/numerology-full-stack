from enum import Enum
from numerology.utils.validator import validate_int_range


class TianGanType(Enum):
    JIA = '甲'
    YI = '乙'
    BING = '丙'
    DING = '丁'
    WU = '戊'
    JI = '己'
    GENG = '庚'
    XIN = '辛'
    REN = '壬'
    GUI = '癸'

    @classmethod
    def get_list(cls):
        return [cls.JIA, cls.YI, cls.BING, cls.DING, cls.WU, cls.JI, cls.GENG, cls.XIN, cls.REN, cls.GUI]

    @classmethod
    @validate_int_range(param="index", min_value=0, max_value=9)
    def get_di_zhi_by_index(cls, index: int) -> "TianGanType":
        return cls.get_list()[index]
