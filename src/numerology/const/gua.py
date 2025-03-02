from abc import ABC, abstractmethod, ABCMeta
from enum import Enum, EnumMeta
from typing import Tuple, Self
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
    def get_base_trigram(cls, value: tuple) -> Self:
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


class TheFirstVolume(Enum):
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

    @classmethod
    def get_trigram64(cls, up_trigram: TrigramType, down_trigram: TrigramType):
        match (up_trigram, down_trigram,):
            case (TrigramType.QIAN, TrigramType.QIAN, ):
                return cls.QIAN
            case (TrigramType.KUN, TrigramType.KUN, ):
                return cls.KUN
            case (TrigramType.KAN, TrigramType.ZHEN, ):
                return cls.ZHUN
            case (TrigramType.GEN, TrigramType.KAN, ):
                return cls.MENG
            case _:
                return None


class Trigram64Type(Enum):

    @classmethod
    def get_trigram64(cls, up_trigram: TrigramType, down_trigram: TrigramType):
        for class_ in [TheFirstVolume]:
            res = class_.get_trigram64(up_trigram=up_trigram, down_trigram=down_trigram)
            if res:
                return res.value
        raise ValueError("No mapping validate trigram")

# for name, member in TheFirstVolume.__members__.items():
#     setattr(Trigram64Type, name, member)
