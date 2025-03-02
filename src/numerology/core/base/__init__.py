from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Union
# from numerology.const.wu_xing import BaseWuXing


class BaseRules(ABC):

    def find_by_index(self, index: int):
        tmp = self
        for _ in range(index):
            tmp = tmp.next
        return tmp

    # 生
    @abstractmethod
    def produce(self):
        raise NotImplementedError("Please define 'product'")

    # 克
    @abstractmethod
    def restrain(self):
        raise NotImplementedError("Please define 'restrain'")

    # 耗
    @abstractmethod
    def consume(self):
        raise NotImplementedError("Please define 'consume'")

    # 泄
    @abstractmethod
    def weaken(self):
        raise NotImplementedError("Please define 'weaken'")

    # 助
    @abstractmethod
    def support(self):
        raise NotImplementedError("Please define 'support'")


class Singleton:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            return cls.__instance


class BaseNode:
    def __init__(self, data):
        self.data = data
        self.next = None

    # def __eq__(self, other):
    #     return True if self.data == other.data and self.next == other.next else False
    #
    # def __ne__(self, other):
    #     return True if self.data != other.data or self.next != other.next else False
    #
    # def __lt__(self, other):
    #     return True if other.next == self else False
    #
    # def __gt__(self, other):
    #     return True if self.next == other else False

    # def find_relationship(self, other):
    #     if self.next


class CircularLinkedList(ABC):
    def __init__(self):
        self.head = None

    @abstractmethod
    def get_node_type(self):
        raise NotImplementedError('Please provide node type')

    def append(self, data):
        new_node = self.get_node_type()(data)

        if self.head is None:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next

            new_node.next = current.next
            current.next = new_node

    def get_length(self):
        if self.head is None:
            return 0
        cur = self.head
        if cur.next == self.head:
            return 1

        count = 0
        while cur.next != self.head:
            count += 1
            cur = cur.next
        count += 1
        return count


class BaseProperty(ABC):

    def __init__(self):
        self.names = self.get_circular_linked_list()()
        for item in self.generate_items():
            self.names.append(data=item)

    def current_node(self, name) -> Any:
        count = 0
        cur = self.names.head
        while cur.data != name and count < self.names.get_length():
            cur = cur.next
            count += 1
        return cur

    def get_names(self) -> list:
        if len(self.get_items()) == 0:
            return []
        else:
            return [n.value.name for n in self.get_items()]

    def generate_items(self) -> list:
        return [m.value for m in self.get_items().__members__.values()]

    @abstractmethod
    def get_circular_linked_list(self):
        raise NotImplementedError('Items can not be defined.')

    @abstractmethod
    def get_items(self):
        raise NotImplementedError('Items can not be defined.')


@dataclass
class CellProperty:
    name: str
    yinyang: bool
    wuxing: Union[BaseWuXing, list[BaseWuXing]]

    def __eq__(self, other):
        return True if (
                self.name == other.name and self.yinyang == other.yinyang and self.wuxing == other.wuxing
        ) else False

    def __ne__(self, other):
        return True if (
                self.name != other.name or self.yinyang != other.yinyang or self.wuxing != other.wuxing
        ) else False

    def strengthened_produce(self, other) -> bool:
        return self.yinyang != other.yinyang

    def weakened_produce(self, other) -> bool:
        return self.yinyang == other.yinyang

    def strengthened_restrain(self, other) -> bool:
        return self.yinyang == other.yinyang

    def weakened_restrain(self, other) -> bool:
        return self.yinyang != other.yinyang


# 四柱
@dataclass
class Pillar:
    earthly_branch: CellProperty = ...
    heavenly_stem = ...


# 大运
class MajorLifePeriod:
    interval = 10
    earthly_branch = ...
    heavenly_stem = ...
    started_period = ...


# 流年
class EveryYear:
    earthly_branch = ...
    heavenly_stem = ...


class TenDeities:
    essential_element: CellProperty

    # def match(self, CellProperty):
    #     if
