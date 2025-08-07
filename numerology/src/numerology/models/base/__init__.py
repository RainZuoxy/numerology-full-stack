from typing import Union, Tuple
from functools import partial
from pydantic import BaseModel, ConfigDict, Field
from numerology.const import TianGanType, DiZhiType, YinYang, WuXingType, NaYinType, ShiShenType

Field = partial(Field, froze=True)
CG_TYPE = Union[TianGanType, ShiShenType]


class BaseStem(BaseModel):
    type: Union[TianGanType, DiZhiType] = Field()
    yin_yang: YinYang = Field()
    sequence: int = Field()
    element: WuXingType = Field()

    model_config = ConfigDict(use_enum_values=False)

    def __str__(self):
        return f"{self.type.value}({self.yin_yang.value}-{self.element.value})"


class BaseCangGan(BaseModel):
    di_zhi: DiZhiType = Field()
    zhu_qi: CG_TYPE = Field()
    zhong_qi: CG_TYPE = Field(default=None)
    yu_qi: CG_TYPE = Field(default=None)

    def get_qis(self) -> Tuple[CG_TYPE, ...]:
        return (self.zhu_qi, self.zhong_qi, self.yu_qi,)

    def weight(self):
        # todo
        weight_map = {...: 0.70, ...: 0.25, ...: 0.05}
        return


class BaseNaYin(BaseModel):
    na_yin: NaYinType
    desc: str


class NumerologyBaseMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def __new__(cls, name, bases, namespace):

        new_cls = super().__new__(cls, name, bases, namespace)

        index_map = {}
        for attr_name, attr_value in namespace.items():
            if isinstance(attr_value, BaseStem):
                index_map[attr_value.sequence] = attr_value

        new_cls._index_map = index_map
        return new_cls
