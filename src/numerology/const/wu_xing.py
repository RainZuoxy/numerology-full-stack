from enum import Enum
from typing import Union, Any
from dataclasses import dataclass

JIA_ZI = [
    "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥",
    "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未", "甲申", "乙酉", "丙戌", "丁亥",
    "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥",
    "庚子", "辛丑", "壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥",
    "壬子", "癸丑", "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
]


class WuXingRelationshipType(Enum):
    SUPPORT = 0
    WEAKEN = 1
    CONSUME = 2
    DESTROY = 3
    PRODUCE = 4

    @property
    def text(self) -> str:
        relationship_names = {0: '助', 1: '泄', 2: '耗', 3: '克', 4: '生'}
        return relationship_names.get(self.value)


class TianGanType(str, Enum):
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


class DiZhiType(str, Enum):
    ZI = '子'
    CHOU = '丑'
    YIN = '寅'
    MAO = '卯'
    CHEN = '辰'
    SI = '巳'
    WU = '午'
    WEI = '未'
    SHEN = '申'
    YOU = '酉'
    XU = '戌'
    HAI = '亥'

    @classmethod
    def get_list(cls):
        return [
            cls.ZI, cls.CHOU, cls.YIN, cls.MAO, cls.CHEN, cls.SI, cls.WU, cls.WEI, cls.SHEN, cls.YOU, cls.XU, cls.HAI
        ]


class ShiShenType(str, Enum):
    ZHENG_YIN = '正印'
    XIAO_SHEN = '枭神'
    BI_JIAN = '比肩'
    JIE_CAI = '劫财'
    SHI_SHEN = '食神'
    SHANG_GUAN = '伤官'
    ZHENG_CAI = '正财'
    PIAN_CAI = '偏财'
    ZHENG_GUAN = '正官'
    QI_SHA = '七杀'

    @classmethod
    def get_relationships(cls):
        return {
            WuXingRelationshipType.PRODUCE: {0: cls.ZHENG_YIN, 1: cls.XIAO_SHEN},
            WuXingRelationshipType.DESTROY: {0: cls.ZHENG_GUAN, 1: cls.QI_SHA},
            WuXingRelationshipType.CONSUME: {0: cls.ZHENG_CAI, 1: cls.PIAN_CAI},
            WuXingRelationshipType.SUPPORT: {0: cls.JIE_CAI, 1: cls.BI_JIAN},
            WuXingRelationshipType.WEAKEN: {0: cls.SHANG_GUAN, 1: cls.SHI_SHEN}
        }

    @classmethod
    def get_relationship(cls, relationship_type: WuXingRelationshipType, same: int):
        relationships = cls.get_relationships()

        if relationship_type not in relationships:
            return ''

        return relationships.get(relationship_type)[same]


class Gender(Enum):
    MALE = True
    FEMALE = False
