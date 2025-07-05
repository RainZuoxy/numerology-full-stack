from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from numerology.const.wu_xing import WuXingRelationshipType


class WuXingItem(BaseModel):
    name: str
    positive: Optional[bool] = Field(default=None)


class WuXingType(Enum):
    METAL = WuXingItem(name='金')
    WOOD = WuXingItem(name='木')
    WATER = WuXingItem(name='水')
    FIRE = WuXingItem(name='火')
    EARTH = WuXingItem(name='土')


class WuXingBaseRule:
    YANG_METAL = WuXingItem(name='金', positive=True)
    YIN_METAL = WuXingItem(name='金', positive=False)
    YANG_WOOD = WuXingItem(name='木', positive=True)
    YIN_WOOD = WuXingItem(name='木', positive=False)
    YANG_WATER = WuXingItem(name='水', positive=True)
    YIN_WATER = WuXingItem(name='水', positive=False)
    YANG_FIRE = WuXingItem(name='火', positive=True)
    YIN_FIRE = WuXingItem(name='火', positive=False)
    YANG_EARTH = WuXingItem(name='土', positive=True)
    YIN_EARTH = WuXingItem(name='土', positive=False)

    def __init__(self, wuxing_item: WuXingItem):
        self.base = wuxing_item
        self.nature_rule = [wuxing_item]

    def get_wuxing_by_relationship(self, item: WuXingItem):
        ...

    def get_relationship(self, other):
        ...


# class WuXingbak(BaseModel):
#     name: str
#     sheng: Optional["WuXing"] = Field(default=None)
#     ke: Optional["WuXing"] = Field(default=None)
#     hao: Optional["WuXing"] = Field(default=None)
#     xie: Optional["WuXing"] = Field(default=None)
#     zhu: Optional["WuXing"] = Field(default=None)
#
#     def __repr__(self):
#         return self.get_name()
#
#     def set_sheng(self, sheng: "WuXing"):
#         self.sheng = sheng
#
#     def set_ke(self, ke: "WuXing"):
#         self.ke = ke
#
#     def set_hao(self, hao: "WuXing"):
#         self.hao = hao
#
#     def set_xie(self, xie: "WuXing"):
#         self.xie = xie
#
#     def set_zhu(self, zhu: "WuXing"):
#         self.zhu = zhu
#
#     def get_name(self) -> str:
#         return self.name
#
#     def get_relationship(self, wu_xing) -> WuXingRelationshipType:
#         if not isinstance(wu_xing, WuXing):
#             raise ValueError(f'{wu_xing}不是五行类型')
#
#         if self.get_name() == wu_xing.sheng.get_name():
#             return WuXingRelationshipType.PRODUCED
#         elif self.get_name() == wu_xing.ke.get_name():
#             return WuXingRelationshipType.DESTROYED
#         elif self.get_name() == wu_xing.hao.get_name():
#             return WuXingRelationshipType.CONSUMED
#         elif self.get_name() == wu_xing.xie.get_name():
#             return WuXingRelationshipType.WEAKENED
#         elif self.get_name() == wu_xing.zhu.get_name():
#             return WuXingRelationshipType.SUPPORTED
#         else:
#             raise ValueError(f'{wu_xing}不是五行类型')


class WuXing(BaseModel):
    base: WuXingItem
    sheng: Optional["WuXingItem"] = Field(default=None)
    ke: Optional["WuXingItem"] = Field(default=None)
    hao: Optional["WuXingItem"] = Field(default=None)
    xie: Optional["WuXingItem"] = Field(default=None)
    zhu: Optional["WuXingItem"] = Field(default=None)

    def __repr__(self):
        return self.get_name()

    def set_sheng(self, sheng: "WuXingItem"):
        self.sheng = sheng

    def set_ke(self, ke: "WuXingItem"):
        self.ke = ke

    def set_hao(self, hao: "WuXingItem"):
        self.hao = hao

    def set_xie(self, xie: "WuXingItem"):
        self.xie = xie

    def set_zhu(self, zhu: "WuXingItem"):
        self.zhu = zhu

    def get_name(self) -> str:
        return self.base.name

    def get_relationship(self, wu_xing: "WuXing") -> WuXingRelationshipType:
        if not isinstance(wu_xing, WuXing):
            raise ValueError(f'{wu_xing}不是五行类型')

        if self.get_name() == wu_xing.sheng.name:
            return WuXingRelationshipType.PRODUCED
        elif self.get_name() == wu_xing.ke.name:
            return WuXingRelationshipType.DESTROYED
        elif self.get_name() == wu_xing.hao.name:
            return WuXingRelationshipType.CONSUMED
        elif self.get_name() == wu_xing.xie.name:
            return WuXingRelationshipType.WEAKENED
        elif self.get_name() == wu_xing.zhu.name:
            return WuXingRelationshipType.SUPPORTED
        else:
            raise ValueError(f'{wu_xing}不是五行类型')

    def get_wuxing_by_relationship(self, relationship: WuXingRelationshipType) -> "WuXingItem":
        register = {

            WuXingRelationshipType.PRODUCED: self.base.sheng,

            WuXingRelationshipType.DESTROYED: self.base.ke,

            WuXingRelationshipType.CONSUMED: self.base.hao,

            WuXingRelationshipType.WEAKENED: self.base.xie,

            WuXingRelationshipType.SUPPORTED: self.base.zhu,
        }
        return register.get(relationship)


# class WuXingRegisterbak:
#     _metal = None
#     _wood = None
#     _water = None
#     _fire = None
#     _earth = None
#
#     def __init__(self):
#         super().__init__()
#         self._load_wu_xing_relationships()
#
#     @classmethod
#     def init(cls):
#         cls._load_wu_xing_relationships()
#
#     @classmethod
#     def _load_wu_xing_relationships(cls):
#         cls._metal = WuXing(name='金')
#         cls._wood = WuXing(name='木')
#         cls._water = WuXing(name='水')
#         cls._fire = WuXing(name='火')
#         cls._earth = WuXing(name='土')
#
#         cls._metal.set_sheng(cls._earth)
#         cls._wood.set_sheng(cls._water)
#         cls._water.set_sheng(cls._metal)
#         cls._fire.set_sheng(cls._wood)
#         cls._earth.set_sheng(cls._fire)
#
#         cls._metal.set_ke(cls._fire)
#         cls._wood.set_ke(cls._metal)
#         cls._water.set_ke(cls._earth)
#         cls._fire.set_ke(cls._water)
#         cls._earth.set_ke(cls._wood)
#
#         cls._metal.set_hao(cls._wood)
#         cls._wood.set_hao(cls._earth)
#         cls._water.set_hao(cls._fire)
#         cls._fire.set_hao(cls._metal)
#         cls._earth.set_hao(cls._water)
#
#         cls._metal.set_xie(cls._water)
#         cls._wood.set_xie(cls._fire)
#         cls._water.set_xie(cls._wood)
#         cls._fire.set_xie(cls._earth)
#         cls._earth.set_xie(cls._metal)
#
#         cls._metal.set_zhu(cls._metal)
#         cls._wood.set_zhu(cls._wood)
#         cls._water.set_zhu(cls._water)
#         cls._fire.set_zhu(cls._fire)
#         cls._earth.set_zhu(cls._earth)
#
#     @property
#     def metal(self) -> str:
#         return self._metal.name
#
#     @property
#     def wood(self) -> str:
#         return self._wood.name
#
#     @property
#     def water(self) -> str:
#         return self._water.name
#
#     @property
#     def fire(self) -> str:
#         return self._fire.name
#
#     @property
#     def earth(self) -> str:
#         return self._earth.name
#
#     @classmethod
#     def get_metal(cls) -> WuXing:
#         return cls._metal
#
#     @classmethod
#     def get_wood(cls) -> WuXing:
#         return cls._wood
#
#     @classmethod
#     def get_water(cls) -> WuXing:
#         return cls._water
#
#     @classmethod
#     def get_fire(cls) -> WuXing:
#         return cls._fire
#
#     @classmethod
#     def get_earth(cls) -> WuXing:
#         return cls._earth

class WuXingRegister:
    _metal = None
    _wood = None
    _water = None
    _fire = None
    _earth = None

    def __init__(self):
        super().__init__()
        self._load_wu_xing_relationships()

    @classmethod
    def init(cls):
        cls._load_wu_xing_relationships()

    @classmethod
    def _load_wu_xing_relationships(cls):
        cls._metal = WuXing(base=WuXingType.METAL.value)
        cls._wood = WuXing(base=WuXingType.WOOD.value)
        cls._water = WuXing(base=WuXingType.WATER.value)
        cls._fire = WuXing(base=WuXingType.FIRE.value)
        cls._earth = WuXing(base=WuXingType.EARTH.value)

        cls._metal.set_sheng(cls._earth.base)
        cls._wood.set_sheng(cls._water.base)
        cls._water.set_sheng(cls._metal.base)
        cls._fire.set_sheng(cls._wood.base)
        cls._earth.set_sheng(cls._fire.base)

        cls._metal.set_ke(cls._fire.base)
        cls._wood.set_ke(cls._metal.base)
        cls._water.set_ke(cls._earth.base)
        cls._fire.set_ke(cls._water.base)
        cls._earth.set_ke(cls._wood.base)

        cls._metal.set_hao(cls._wood.base)
        cls._wood.set_hao(cls._earth.base)
        cls._water.set_hao(cls._fire.base)
        cls._fire.set_hao(cls._metal.base)
        cls._earth.set_hao(cls._water.base)

        cls._metal.set_xie(cls._water.base)
        cls._wood.set_xie(cls._fire.base)
        cls._water.set_xie(cls._wood.base)
        cls._fire.set_xie(cls._earth.base)
        cls._earth.set_xie(cls._metal.base)

        cls._metal.set_zhu(cls._metal.base)
        cls._wood.set_zhu(cls._wood.base)
        cls._water.set_zhu(cls._water.base)
        cls._fire.set_zhu(cls._fire.base)
        cls._earth.set_zhu(cls._earth.base)

    @property
    def metal(self) -> str:
        return self._metal.name

    @property
    def wood(self) -> str:
        return self._wood.name

    @property
    def water(self) -> str:
        return self._water.name

    @property
    def fire(self) -> str:
        return self._fire.name

    @property
    def earth(self) -> str:
        return self._earth.name

    @classmethod
    def get_metal(cls) -> WuXing:
        return cls._metal

    @classmethod
    def get_wood(cls) -> WuXing:
        return cls._wood

    @classmethod
    def get_water(cls) -> WuXing:
        return cls._water

    @classmethod
    def get_fire(cls) -> WuXing:
        return cls._fire

    @classmethod
    def get_earth(cls) -> WuXing:
        return cls._earth


WuXingRegister.init()
