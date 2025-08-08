from abc import ABC, abstractmethod
from typing import TypeVar, Union, Dict
from numerology.const.relationship import WuXingRelationshipType
from numerology.const import WuXingType, ShiShenType
from numerology.models.base import BaseStem

_T = TypeVar('_T', WuXingType, ShiShenType)


class Relationship(ABC):

    @classmethod
    @abstractmethod
    def get_relationships(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_relationship(cls, base: _T, other: _T) -> Union[WuXingRelationshipType, None]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_result_by_relationship(cls, relationship_type: WuXingRelationshipType, **kwargs) -> _T:
        raise NotImplementedError

    @staticmethod
    def is_same_yin_yang(first: BaseStem, second: BaseStem) -> bool:
        return first.yin_yang == second.yin_yang


class WuXingRelationship(Relationship):
    """
    The Base Rule of WuXing
    """

    @classmethod
    def get_relationships(cls) -> Dict[WuXingType, Dict[WuXingRelationshipType, WuXingType]]:
        return {
            WuXingType.WATER: {
                WuXingRelationshipType.PRODUCED: WuXingType.METAL,
                WuXingRelationshipType.CONSUMED: WuXingType.FIRE,
                WuXingRelationshipType.WEAKENED: WuXingType.WOOD,
                WuXingRelationshipType.DESTROYED: WuXingType.EARTH,
                WuXingRelationshipType.SUPPORTED: WuXingType.WATER
            },
            WuXingType.EARTH: {
                WuXingRelationshipType.PRODUCED: WuXingType.FIRE,
                WuXingRelationshipType.CONSUMED: WuXingType.WATER,
                WuXingRelationshipType.WEAKENED: WuXingType.METAL,
                WuXingRelationshipType.DESTROYED: WuXingType.WOOD,
                WuXingRelationshipType.SUPPORTED: WuXingType.EARTH
            },
            WuXingType.METAL: {
                WuXingRelationshipType.PRODUCED: WuXingType.EARTH,
                WuXingRelationshipType.CONSUMED: WuXingType.WOOD,
                WuXingRelationshipType.WEAKENED: WuXingType.WATER,
                WuXingRelationshipType.DESTROYED: WuXingType.FIRE,
                WuXingRelationshipType.SUPPORTED: WuXingType.METAL
            },
            WuXingType.WOOD: {
                WuXingRelationshipType.PRODUCED: WuXingType.WATER,
                WuXingRelationshipType.CONSUMED: WuXingType.EARTH,
                WuXingRelationshipType.WEAKENED: WuXingType.FIRE,
                WuXingRelationshipType.DESTROYED: WuXingType.METAL,
                WuXingRelationshipType.SUPPORTED: WuXingType.WOOD
            },
            WuXingType.FIRE: {
                WuXingRelationshipType.PRODUCED: WuXingType.WOOD,
                WuXingRelationshipType.CONSUMED: WuXingType.METAL,
                WuXingRelationshipType.WEAKENED: WuXingType.EARTH,
                WuXingRelationshipType.DESTROYED: WuXingType.WATER,
                WuXingRelationshipType.SUPPORTED: WuXingType.FIRE
            }
        }

    @classmethod
    def get_result_by_relationship(  # noqa
            cls,
            *,
            relationship_type: WuXingRelationshipType,
            wuxing: WuXingType
    ) -> WuXingType:
        relationships = cls.get_relationships()

        if not isinstance(relationship_type, WuXingRelationshipType):
            raise TypeError('relationship_type is not WuXingRelationshipType')

        if wuxing not in relationships:
            raise ValueError(f'{relationship_type} is not WuXing relationship type')

        return relationships.get(wuxing)[relationship_type]

    @classmethod
    def get_relationship(cls, base: WuXingType, other: WuXingType) -> Union[WuXingRelationshipType, None]:
        for relationship, wuxing in cls.get_relationships()[base].items():
            if wuxing == other:
                return relationship
        return None

    @classmethod
    def get_supported_and_produced(cls):
        return [WuXingRelationshipType.PRODUCED, WuXingRelationshipType.SUPPORTED]


class ShiShenRelationship(Relationship):
    """
    The Base Rule of ShiShen
    """

    @classmethod
    def get_relationships(cls):
        return {
            WuXingRelationshipType.PRODUCED: {False: ShiShenType.ZHENG_YIN, True: ShiShenType.XIAO_SHEN},
            WuXingRelationshipType.DESTROYED: {False: ShiShenType.ZHENG_GUAN, True: ShiShenType.QI_SHA},
            WuXingRelationshipType.CONSUMED: {False: ShiShenType.ZHENG_CAI, True: ShiShenType.PIAN_CAI},
            WuXingRelationshipType.SUPPORTED: {False: ShiShenType.JIE_CAI, True: ShiShenType.BI_JIAN},
            WuXingRelationshipType.WEAKENED: {False: ShiShenType.SHANG_GUAN, True: ShiShenType.SHI_SHEN}
        }

    @classmethod
    def get_result_by_relationship(  # noqa
            cls,
            *,
            relationship_type: WuXingRelationshipType,
            is_yin_yang: bool
    ) -> ShiShenType:
        relationships = cls.get_relationships()

        if relationship_type not in relationships:
            raise ValueError(f'{relationship_type} is not WuXing relationship type')

        if not isinstance(is_yin_yang, bool):
            raise TypeError('is_yinyang is not bool')

        return relationships.get(relationship_type)[is_yin_yang]

    @classmethod
    def get_relationship(cls, base: ShiShenType, other: ShiShenType) -> Union[WuXingRelationshipType, None]:
        for relationship, shishen in cls.get_relationships().items():
            if other in shishen.values():
                return relationship
        return None


def get_shi_shen(day_master: BaseStem, target: BaseStem) -> ShiShenType:
    flag_for_yinyang = WuXingRelationship.is_same_yin_yang(first=day_master, second=target)
    relationship = WuXingRelationship.get_relationship(base=day_master.element, other=target.element)
    return ShiShenRelationship.get_result_by_relationship(
        relationship_type=relationship, is_yin_yang=flag_for_yinyang
    )

