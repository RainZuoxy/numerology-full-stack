from typing import ClassVar

from pydantic import BaseModel

from numerology.const.wu_xing import WuXingRelationshipType


class WuXingItem(BaseModel):
    name: str
    sheng: str
    ke: str
    hao: str
    xie: str
    zhu: str


class WuXing(BaseModel):
    name: str
    sheng: "WuXing" = None
    ke: "WuXing" = None
    hao: "WuXing" = None
    xie: "WuXing" = None
    zhu: "WuXing" = None

    # def __init__(self, name: str, sheng=None, ke=None, hao=None, xie=None, zhu=None):
    #     super().__init__()
    #     self.name = name
    #     self.sheng, self.ke = sheng, ke
    #     self.hao, self.xie, self.zhu = hao, xie, zhu

    def __repr__(self):
        return self.get_name()

    def get_sheng(self):
        return self.sheng

    def set_sheng(self, sheng):
        self.sheng = sheng

    def get_ke(self):
        return self.ke

    def set_ke(self, ke):
        self.ke = ke

    def get_hao(self):
        return self.hao

    def set_hao(self, hao):
        self.hao = hao

    def get_xie(self):
        return self.xie

    def set_xie(self, xie):
        self.xie = xie

    def get_zhu(self):
        return self.zhu

    def set_zhu(self, zhu):
        self.zhu = zhu

    def get_name(self):
        return self.name

    def get_relationship(self, wu_xing) -> WuXingRelationshipType:
        if not isinstance(wu_xing, WuXing):
            raise ValueError(f'{wu_xing}不是五行类型')

        if self.get_name() == wu_xing.get_sheng().get_name():
            return WuXingRelationshipType.PRODUCE
        elif self.get_name() == wu_xing.get_ke().get_name():
            return WuXingRelationshipType.DESTROY
        elif self.get_name() == wu_xing.get_hao().get_name():
            return WuXingRelationshipType.CONSUME
        elif self.get_name() == wu_xing.get_xie().get_name():
            return WuXingRelationshipType.WEAKEN

        return WuXingRelationshipType.SUPPORT


class WuXingSet:
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
        cls._metal = WuXing(name='金')
        cls._wood = WuXing(name='木')
        cls._water = WuXing(name='水')
        cls._fire = WuXing(name='火')
        cls._earth = WuXing(name='土')

        cls._metal.set_sheng(cls._earth)
        cls._wood.set_sheng(cls._water)
        cls._water.set_sheng(cls._metal)
        cls._fire.set_sheng(cls._wood)
        cls._earth.set_sheng(cls._fire)

        cls._metal.set_ke(cls._fire)
        cls._wood.set_ke(cls._metal)
        cls._water.set_ke(cls._earth)
        cls._fire.set_ke(cls._water)
        cls._earth.set_ke(cls._wood)

        cls._metal.set_hao(cls._wood)
        cls._wood.set_hao(cls._earth)
        cls._water.set_hao(cls._fire)
        cls._fire.set_hao(cls._metal)
        cls._earth.set_hao(cls._water)

        cls._metal.set_xie(cls._water)
        cls._wood.set_xie(cls._fire)
        cls._water.set_xie(cls._wood)
        cls._fire.set_xie(cls._earth)
        cls._earth.set_xie(cls._metal)

        cls._metal.set_zhu(cls._metal)
        cls._wood.set_zhu(cls._wood)
        cls._water.set_zhu(cls._water)
        cls._fire.set_zhu(cls._fire)
        cls._earth.set_zhu(cls._earth)

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
