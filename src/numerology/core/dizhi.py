from enum import Enum

from numerology.core.base import CellProperty, Singleton, BaseProperty
from numerology.core.base.dizhi import DiZhiCircularLinkedList
from numerology.const.wu_xing import BaseWuXing


class DiZhiItems(Enum):
    ZI = CellProperty(name='子', yinyang=True, wuxing=BaseWuXing.WATER)
    CHOU = CellProperty(name='丑', yinyang=False, wuxing=BaseWuXing.EARTH)
    YIN = CellProperty(name='寅', yinyang=True, wuxing=BaseWuXing.WOOD)
    MAO = CellProperty(name='卯', yinyang=False, wuxing=BaseWuXing.WOOD)
    CHEN = CellProperty(name='辰', yinyang=True, wuxing=BaseWuXing.EARTH)
    SI = CellProperty(name='巳', yinyang=False, wuxing=BaseWuXing.FIRE)
    WU = CellProperty(name='午', yinyang=True, wuxing=BaseWuXing.FIRE)
    WEI = CellProperty(name='未', yinyang=False, wuxing=BaseWuXing.EARTH)
    SHEN = CellProperty(name='申', yinyang=True, wuxing=BaseWuXing.METAL)
    YOU = CellProperty(name='酉', yinyang=False, wuxing=BaseWuXing.METAL)
    XU = CellProperty(name='戌', yinyang=True, wuxing=BaseWuXing.EARTH)
    HAI = CellProperty(name='亥', yinyang=False, wuxing=BaseWuXing.WATER)


class DiZhi(Singleton, BaseProperty):
    def current_node(self, name):
        count = 0
        cur = self.names.head
        while cur.data.name != name and count < self.names.get_length():
            cur = cur.next
            count += 1
        return cur

    def get_circular_linked_list(self):
        return DiZhiCircularLinkedList

    def get_items(self):
        return DiZhiItems
