from typing import Union
from numerology.models.pillar import BaseStem

BaseType = Union[BaseStem]


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
            if isinstance(attr_value, BaseType):
                index_map[attr_value.sequence] = attr_value

        new_cls._index_map = index_map
        return new_cls

