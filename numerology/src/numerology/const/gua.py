from abc import abstractmethod
from enum import Enum
from typing import Tuple
from pydantic import BaseModel

EIGHT_TRIGRAM_TEXT_ICON_QIAN = '☰'
EIGHT_TRIGRAM_TEXT_ICON_KUN = '☷'
EIGHT_TRIGRAM_TEXT_ICON_ZHEN = '☳'
EIGHT_TRIGRAM_TEXT_ICON_XUN = '☴'
EIGHT_TRIGRAM_TEXT_ICON_KAN = '☵'
EIGHT_TRIGRAM_TEXT_ICON_LI = '☲'
EIGHT_TRIGRAM_TEXT_ICON_GEN = '☶'
EIGHT_TRIGRAM_TEXT_ICON_DUI = '☱'


class YaoItem(BaseModel):
    # yin False, yang True
    value: bool


class BaseTrigramItem(BaseModel):
    name: str
    lines: Tuple[YaoItem, YaoItem, YaoItem]  # 自下而上排序
    icon: str


class TrigramType(Enum):
    QIAN = BaseTrigramItem(
        name="乾",
        lines=(YaoItem(value=True), YaoItem(value=True), YaoItem(value=True),),
        icon=EIGHT_TRIGRAM_TEXT_ICON_QIAN
    )
    KUN = BaseTrigramItem(
        name="坤",
        lines=(YaoItem(value=False), YaoItem(value=False), YaoItem(value=False),),
        icon=EIGHT_TRIGRAM_TEXT_ICON_KUN
    )
    ZHEN = BaseTrigramItem(
        name="震",
        lines=(YaoItem(value=True), YaoItem(value=False), YaoItem(value=False),),
        icon=EIGHT_TRIGRAM_TEXT_ICON_ZHEN
    )
    XUN = BaseTrigramItem(
        name="巽",
        lines=(YaoItem(value=False), YaoItem(value=True), YaoItem(value=True),),
        icon=EIGHT_TRIGRAM_TEXT_ICON_XUN
    )
    KAN = BaseTrigramItem(
        name="坎",
        lines=(YaoItem(value=False), YaoItem(value=True), YaoItem(value=False),),
        icon=EIGHT_TRIGRAM_TEXT_ICON_KAN
    )
    LI = BaseTrigramItem(
        name="离",
        lines=(YaoItem(value=True), YaoItem(value=False), YaoItem(value=True),),
        icon=EIGHT_TRIGRAM_TEXT_ICON_LI
    )
    GEN = BaseTrigramItem(
        name="艮",
        lines=(YaoItem(value=False), YaoItem(value=False), YaoItem(value=True),),
        icon=EIGHT_TRIGRAM_TEXT_ICON_GEN
    )
    DUI = BaseTrigramItem(
        name="兑",
        lines=(YaoItem(value=True), YaoItem(value=True), YaoItem(value=False),),
        icon=EIGHT_TRIGRAM_TEXT_ICON_DUI
    )

    @classmethod
    def get_base_trigram(cls, value: tuple):
        match value:
            case (True, True, True, ):
                return cls.QIAN
            case (False, False, False, ):
                return cls.KUN
            case ( True, False, False, ):
                return cls.ZHEN
            case (False, True, True, ):
                return cls.XUN
            case (False, True, False, ):
                return cls.KAN
            case (True, False, True, ):
                return cls.LI
            case (False, False, True, ):
                return cls.GEN
            case (True, True, False, ):
                return cls.DUI


class Trigram64Item(BaseModel):
    # first: YaoItem
    # second: YaoItem
    # third: YaoItem
    # forth: YaoItem
    # fifth: YaoItem
    # top: YaoItem
    name: str
    index: int
    icon: str
    up_trigram: TrigramType
    down_trigram: TrigramType

    # @property
    # def up_trigram(self) -> Tuple:
    #     return self.top, self.fifth, self.forth
    #
    # @property
    # def _trigram(self) -> Tuple:
    #     return self.third, self.second, self.first

    # def __repr__(self):
    #     # res.up_trigram.value.value[0].value
    #     {
    #         "卦名": self.name,
    #         "卦序": self.index,
    #         "卦形": self.icon,
    #         "上卦": self.up_trigram.value,
    #         "下卦": self.down_trigram.value,
    #         "上爻": self.up_trigram.value.lines[2].value,
    #         "五爻": self.up_trigram.value.lines[1].value,
    #         "四爻": self.up_trigram.value.lines[0].value,
    #         "三爻": self.down_trigram.value.lines[2].value,
    #         "二爻": self.down_trigram.value.lines[1].value,
    #         "初爻": self.down_trigram.value.lines[0].value
    #     }
    #     return (
    #         f"卦名:{self.name}, 卦序:{self.index}, 卦形：{self.icon},\n"
    #         f"上卦:{self.up_trigram.value}, 下卦:{self.down_trigram.value},\n"
    #         f"上爻:{self.up_trigram.value.lines[2].value},\n"
    #         f"五爻:{self.up_trigram.value.lines[1].value},\n"
    #         f"四爻:{self.up_trigram.value.lines[0].value},\n"
    #         f"三爻:{self.down_trigram.value.lines[2].value},\n"
    #         f"二爻:{self.down_trigram.value.lines[1].value},\n"
    #         f"初爻:{self.down_trigram.value.lines[0].value}\n"
    #     )


# class ABCEnumMeta(ABCMeta, EnumMeta):
#     pass
#
#
# class BaseTrigram64Meta(ABCEnumMeta):
#     registry = []
#
#     def __new__(cls, name, bases, namespace):
#         new_class = super().__new__(cls, name, bases, namespace)
#         cls.registry.append(new_class)
#         return new_class


class BaseTrigram64Type(Enum):
    @classmethod
    @abstractmethod
    def get_trigram64(cls, up_trigram: BaseTrigramItem, down_trigram: BaseTrigramItem) -> Trigram64Item:
        raise NotImplementedError("Need to define")


class Trigram64Type(Enum):
    QIAN = Trigram64Item(
        name="乾卦", index=1, icon="䷀",
        up_trigram=TrigramType.QIAN, down_trigram=TrigramType.QIAN
    )
    KUN = Trigram64Item(
        name="坤卦", index=2, icon="䷁",
        up_trigram=TrigramType.KUN, down_trigram=TrigramType.KUN
    )
    ZHUN = Trigram64Item(
        name="屯卦", index=3, icon="䷂",
        up_trigram=TrigramType.KAN, down_trigram=TrigramType.ZHEN
    )
    MENG = Trigram64Item(
        name="蒙卦", index=4, icon="䷃",
        up_trigram=TrigramType.GEN, down_trigram=TrigramType.KAN
    )
    XU = Trigram64Item(
        name="需", index=5, icon="䷄",
        up_trigram=TrigramType.KAN, down_trigram=TrigramType.QIAN
    )
    SONG = Trigram64Item(
        name="讼", index=6, icon="䷅",
        up_trigram=TrigramType.QIAN, down_trigram=TrigramType.KAN
    )
    SHI = Trigram64Item(
        name="师", index=7, icon="䷆",
        up_trigram=TrigramType.KUN, down_trigram=TrigramType.KAN
    )
    BI = Trigram64Item(
        name="比", index=8, icon="䷇",
        up_trigram=TrigramType.KAN, down_trigram=TrigramType.KUN
    )
    XIAO_CHU = Trigram64Item(
        name="小畜", index=9, icon="䷈",
        up_trigram=TrigramType.XUN, down_trigram=TrigramType.QIAN
    )
    LV = Trigram64Item(
        name="履", index=10, icon="䷉",
        up_trigram=TrigramType.QIAN, down_trigram=TrigramType.DUI
    )
    TAI = Trigram64Item(
        name="泰", index=11, icon="䷊",
        up_trigram=TrigramType.KUN, down_trigram=TrigramType.QIAN
    )
    PI = Trigram64Item(
        name="否", index=12, icon="䷋",
        up_trigram=TrigramType.QIAN, down_trigram=TrigramType.KUN
    )
    TONG_REN = Trigram64Item(
        name="同人", index=13, icon="䷌",
        up_trigram=TrigramType.QIAN, down_trigram=TrigramType.LI
    )
    DA_YOU = Trigram64Item(
        name="大有", index=14, icon="䷍",
        up_trigram=TrigramType.LI, down_trigram=TrigramType.QIAN
    )
    QIAN1 = Trigram64Item(
        name="谦", index=15, icon="䷎",
        up_trigram=TrigramType.KUN, down_trigram=TrigramType.GEN
    )
    YU = Trigram64Item(
        name="豫", index=16, icon="䷏",
        up_trigram=TrigramType.ZHEN, down_trigram=TrigramType.KUN
    )
    SUI = Trigram64Item(
        name="随", index=17, icon="䷐",
        up_trigram=TrigramType.DUI, down_trigram=TrigramType.ZHEN
    )
    GU = Trigram64Item(
        name="蛊", index=18, icon="䷑",
        up_trigram=TrigramType.GEN, down_trigram=TrigramType.XUN
    )
    LIN = Trigram64Item(
        name="临", index=19, icon="䷒",
        up_trigram=TrigramType.KUN, down_trigram=TrigramType.DUI
    )
    GUAN = Trigram64Item(
        name="观", index=20, icon="䷓",
        up_trigram=TrigramType.XUN, down_trigram=TrigramType.KUN
    )
    SHI_HE = Trigram64Item(
        name="噬嗑", index=21, icon="䷔",
        up_trigram=TrigramType.LI, down_trigram=TrigramType.ZHEN
    )
    BI4 = Trigram64Item(
        name="贲", index=22, icon="䷕",
        up_trigram=TrigramType.GEN, down_trigram=TrigramType.LI
    )
    BO = Trigram64Item(
        name="剥", index=23, icon="䷖",
        up_trigram=TrigramType.GEN, down_trigram=TrigramType.KUN
    )
    FU = Trigram64Item(
        name="复", index=24, icon="䷗",
        up_trigram=TrigramType.KUN, down_trigram=TrigramType.ZHEN
    )

    WU_WANG = Trigram64Item(
        name="无妄", index=25, icon="䷘",
        up_trigram=TrigramType.QIAN, down_trigram=TrigramType.ZHEN
    )
    DA_CHU = Trigram64Item(
        name="大畜", index=26, icon="䷙",
        up_trigram=TrigramType.GEN, down_trigram=TrigramType.QIAN
    )
    YI = Trigram64Item(
        name="颐", index=27, icon="䷚",
        up_trigram=TrigramType.GEN, down_trigram=TrigramType.ZHEN
    )
    DA_GUO = Trigram64Item(
        name="大过", index=28, icon="䷛",
        up_trigram=TrigramType.DUI, down_trigram=TrigramType.XUN
    )
    KAN = Trigram64Item(
        name="坎", index=29, icon="䷜",
        up_trigram=TrigramType.KAN, down_trigram=TrigramType.KAN
    )
    LI = Trigram64Item(
        name="离", index=30, icon="䷝",
        up_trigram=TrigramType.LI, down_trigram=TrigramType.LI
    )
    XIAN = Trigram64Item(
        name="咸", index=31, icon="䷞",
        up_trigram=TrigramType.DUI, down_trigram=TrigramType.GEN
    )
    HENG = Trigram64Item(
        name="恒", index=32, icon="䷟",
        up_trigram=TrigramType.ZHEN, down_trigram=TrigramType.XUN
    )
    DUN = Trigram64Item(
        name="遁", index=33, icon="䷠",
        up_trigram=TrigramType.QIAN, down_trigram=TrigramType.GEN
    )
    DA_ZHUANG = Trigram64Item(
        name="大壮", index=34, icon="䷡",
        up_trigram=TrigramType.ZHEN, down_trigram=TrigramType.QIAN
    )
    JIN = Trigram64Item(
        name="晋", index=35, icon="䷢",
        up_trigram=TrigramType.LI, down_trigram=TrigramType.KUN
    )
    MING_YI = Trigram64Item(
        name="明夷", index=36, icon="䷣",
        up_trigram=TrigramType.KUN, down_trigram=TrigramType.LI
    )
    JIA_REN = Trigram64Item(
        name="家人", index=37, icon="䷤",
        up_trigram=TrigramType.XUN, down_trigram=TrigramType.LI
    )
    KUI = Trigram64Item(
        name="睽", index=38, icon="䷥",
        up_trigram=TrigramType.LI, down_trigram=TrigramType.DUI
    )
    JIAN = Trigram64Item(
        name="蹇", index=39, icon="䷦",
        up_trigram=TrigramType.KAN, down_trigram=TrigramType.GEN
    )
    JIE = Trigram64Item(
        name="解", index=40, icon="䷧",
        up_trigram=TrigramType.ZHEN, down_trigram=TrigramType.KAN
    )
    SUN = Trigram64Item(
        name="损", index=41, icon="䷨",
        up_trigram=TrigramType.GEN, down_trigram=TrigramType.DUI
    )
    YI4 = Trigram64Item(
        name="益", index=42, icon="䷩",
        up_trigram=TrigramType.XUN, down_trigram=TrigramType.ZHEN
    )
    GUAI = Trigram64Item(
        name="夬", index=43, icon="䷪",
        up_trigram=TrigramType.DUI, down_trigram=TrigramType.QIAN
    )
    GOU = Trigram64Item(
        name="姤", index=44, icon="䷫",
        up_trigram=TrigramType.QIAN, down_trigram=TrigramType.XUN
    )
    CUI = Trigram64Item(
        name="萃", index=45, icon="䷬",
        up_trigram=TrigramType.DUI, down_trigram=TrigramType.KUN
    )
    SHENG = Trigram64Item(
        name="升", index=46, icon="䷭",
        up_trigram=TrigramType.KUN, down_trigram=TrigramType.XUN
    )
    KUN4 = Trigram64Item(
        name="困", index=47, icon="䷮",
        up_trigram=TrigramType.DUI, down_trigram=TrigramType.KAN
    )
    JING = Trigram64Item(
        name="井", index=48, icon="䷯",
        up_trigram=TrigramType.KAN, down_trigram=TrigramType.XUN
    )
    GE = Trigram64Item(
        name="革", index=49, icon="䷰",
        up_trigram=TrigramType.DUI, down_trigram=TrigramType.LI
    )
    DING = Trigram64Item(
        name="鼎", index=50, icon="䷱",
        up_trigram=TrigramType.LI, down_trigram=TrigramType.XUN
    )
    ZHEN = Trigram64Item(
        name="震", index=51, icon="䷲",
        up_trigram=TrigramType.ZHEN, down_trigram=TrigramType.ZHEN
    )
    GEN = Trigram64Item(
        name="艮", index=52, icon="䷳",
        up_trigram=TrigramType.GEN, down_trigram=TrigramType.GEN
    )
    JIAN4 = Trigram64Item(
        name="渐", index=53, icon="䷴",
        up_trigram=TrigramType.XUN, down_trigram=TrigramType.GEN
    )
    GUI_MEI = Trigram64Item(
        name="归妹", index=54, icon="䷵",
        up_trigram=TrigramType.ZHEN, down_trigram=TrigramType.DUI
    )
    FENG = Trigram64Item(
        name="丰", index=55, icon="䷶",
        up_trigram=TrigramType.ZHEN, down_trigram=TrigramType.LI
    )
    LV3 = Trigram64Item(
        name="旅", index=56, icon="䷷",
        up_trigram=TrigramType.LI, down_trigram=TrigramType.GEN
    )
    XUN = Trigram64Item(
        name="巽", index=57, icon="䷸",
        up_trigram=TrigramType.XUN, down_trigram=TrigramType.XUN
    )
    DUI = Trigram64Item(
        name="兑", index=58, icon="䷹",
        up_trigram=TrigramType.DUI, down_trigram=TrigramType.DUI
    )
    HUAN = Trigram64Item(
        name="涣", index=59, icon="䷺",
        up_trigram=TrigramType.XUN, down_trigram=TrigramType.KAN
    )
    JIE2 = Trigram64Item(
        name="节", index=60, icon="䷻",
        up_trigram=TrigramType.KAN, down_trigram=TrigramType.DUI
    )
    ZHONG_FU = Trigram64Item(
        name="中孚", index=61, icon="䷼",
        up_trigram=TrigramType.XUN, down_trigram=TrigramType.DUI
    )
    XIAO_GUO = Trigram64Item(
        name="小过", index=62, icon="䷽",
        up_trigram=TrigramType.ZHEN, down_trigram=TrigramType.GEN
    )
    JI_JI = Trigram64Item(
        name="既济", index=63, icon="䷾",
        up_trigram=TrigramType.KAN, down_trigram=TrigramType.LI
    )
    WEI_JI = Trigram64Item(
        name="未济", index=64, icon="䷿",
        up_trigram=TrigramType.LI, down_trigram=TrigramType.KAN
    )

    @classmethod
    def get_mapping(cls):
        EIGHT_TRIGRAM_SYMBOL_QIAN = '天'
        EIGHT_TRIGRAM_SYMBOL_KUN = '地'
        EIGHT_TRIGRAM_SYMBOL_ZHEN = '雷'
        EIGHT_TRIGRAM_SYMBOL_XUN = '风'
        EIGHT_TRIGRAM_SYMBOL_KAN = '水'
        EIGHT_TRIGRAM_SYMBOL_LI = '火'
        EIGHT_TRIGRAM_SYMBOL_GEN = '山'
        EIGHT_TRIGRAM_SYMBOL_DUI = '泽'
        return {
            TrigramType.QIAN:EIGHT_TRIGRAM_SYMBOL_QIAN,
            TrigramType.KUN:EIGHT_TRIGRAM_SYMBOL_KUN,
            TrigramType.ZHEN:EIGHT_TRIGRAM_SYMBOL_ZHEN,
            TrigramType.XUN:EIGHT_TRIGRAM_SYMBOL_XUN,
            TrigramType.KAN:EIGHT_TRIGRAM_SYMBOL_KAN,
            TrigramType.LI:EIGHT_TRIGRAM_SYMBOL_LI,
            TrigramType.GEN:EIGHT_TRIGRAM_SYMBOL_GEN,
            TrigramType.DUI:EIGHT_TRIGRAM_SYMBOL_DUI
        }

    @classmethod
    def get_trigram64(cls, up_trigram: TrigramType, down_trigram: TrigramType):
        for item in cls:
            name, val = item.name, item.value
            if val.up_trigram == up_trigram and val.down_trigram == down_trigram:
                return cls[name]

    # @classmethod
    # def get_trigram64(cls, up_trigram: TrigramType, down_trigram: TrigramType):
    #     match (up_trigram, down_trigram,):
    #         case (TrigramType.QIAN, TrigramType.QIAN, ):
    #             return cls.QIAN
    #         case (TrigramType.KUN, TrigramType.KUN, ):
    #             return cls.KUN
    #         case (TrigramType.KAN, TrigramType.ZHEN, ):
    #             return cls.ZHUN
    #         case (TrigramType.GEN, TrigramType.KAN, ):
    #             return cls.MENG
    #         case _:
    #             return None


# class Trigram64Type(Enum):
#
#     @classmethod
#     def get_trigram64(cls, up_trigram: TrigramType, down_trigram: TrigramType):
#         for class_ in [TheFirstVolume]:
#             res = class_.get_trigram64(up_trigram=up_trigram, down_trigram=down_trigram)
#             if res:
#                 return res.value
#         raise ValueError("No mapping validate trigram")

# for name, member in TheFirstVolume.__members__.items():
#     setattr(Trigram64Type, name, member)
