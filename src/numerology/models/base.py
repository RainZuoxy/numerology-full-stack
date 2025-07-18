from typing import Union
from functools import partial
from pydantic import BaseModel, ConfigDict, Field
from numerology.const import TianGanType, DiZhiType, YinYang, WuXingType, NaYinType

Field = partial(Field, froze=True)


class BaseStem(BaseModel):
    element: Union[TianGanType, DiZhiType] = Field()
    yin_yang: YinYang = Field()
    sequence: int = Field()
    wu_xing: WuXingType = Field()

    model_config = ConfigDict(use_enum_values=False)


class BaseCangGan(BaseModel):
    di_zhi: DiZhiType = Field()
    zhu_qi: TianGanType = Field()
    zhong_qi: TianGanType = Field(default=None)
    yu_qi: TianGanType = Field(default=None)

    def weight(self):
        # todo
        weight_map={...:0.70,...:0.25,...:0.05}
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
