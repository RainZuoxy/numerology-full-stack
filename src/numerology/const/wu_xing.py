from enum import Enum, IntEnum

JIA_ZI = [
    "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥",
    "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未", "甲申", "乙酉", "丙戌", "丁亥",
    "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥",
    "庚子", "辛丑", "壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥",
    "壬子", "癸丑", "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
]


class WuXingRelationshipType(Enum):
    """
    五行关系
    A 生 B: A -> B
    Example:
    水      木    火   土    金
    base -> a -> b -> c -> d
    0: base is supported by base
    1: base is weakened by a
    2: base is consumed by b
    3: base is destroyed by c
    4: base is produced by d

    """
    SUPPORTED = 0
    WEAKENED = 1
    CONSUMED = 2
    DESTROYED = 3
    PRODUCED = 4

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
            WuXingRelationshipType.PRODUCED: {False: cls.ZHENG_YIN, True: cls.XIAO_SHEN},
            WuXingRelationshipType.DESTROYED: {False: cls.ZHENG_GUAN, True: cls.QI_SHA},
            WuXingRelationshipType.CONSUMED: {False: cls.ZHENG_CAI, True: cls.PIAN_CAI},
            WuXingRelationshipType.SUPPORTED: {False: cls.JIE_CAI, True: cls.BI_JIAN},
            WuXingRelationshipType.WEAKENED: {False: cls.SHANG_GUAN, True: cls.SHI_SHEN}
        }

    @classmethod
    def get_relationship(cls, relationship_type: WuXingRelationshipType, is_same: bool):
        relationships = cls.get_relationships()

        if relationship_type not in relationships:
            raise ValueError(f'{relationship_type}不是五行关系类型')

        if not isinstance(is_same, bool):
            raise TypeError('is_same不是bool类型')

        return relationships.get(relationship_type)[is_same]


class Gender(IntEnum):
    MALE = 1
    FEMALE = 0

    @classmethod
    def get_gender_in_cn(cls, value: int) -> str:
        match value:
            case cls.MALE.value:
                return '男'
            case cls.FEMALE.value:
                return '女'
            case _:
                return 'invalid gender'
