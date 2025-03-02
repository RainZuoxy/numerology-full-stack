from enum import Enum

from numerology.core.base import CellProperty, Singleton, BaseProperty
from numerology.core.base.tiangan import TianGanCircularLinkedList
from numerology.const.wu_xing import BaseWuXing


class TianGanItems(Enum):
    JIA = CellProperty(name='甲', yinyang=True, wuxing=BaseWuXing.WOOD)
    YI = CellProperty(name='乙', yinyang=False, wuxing=BaseWuXing.WOOD)
    BING = CellProperty(name='丙', yinyang=True, wuxing=BaseWuXing.FIRE)
    DING = CellProperty(name='丁', yinyang=False, wuxing=BaseWuXing.FIRE)
    WU = CellProperty(name='戊', yinyang=True, wuxing=BaseWuXing.EARTH)
    JI = CellProperty(name='己', yinyang=False, wuxing=BaseWuXing.EARTH)
    GENG = CellProperty(name='庚', yinyang=True, wuxing=BaseWuXing.METAL)
    XIN = CellProperty(name='辛', yinyang=False, wuxing=BaseWuXing.METAL)
    REN = CellProperty(name='壬', yinyang=True, wuxing=BaseWuXing.WATER)
    GUI = CellProperty(name='癸', yinyang=False, wuxing=BaseWuXing.WATER)


class TianGan(Singleton, BaseProperty):

    def current_node(self, name: str):
        # , yinyang: bool    and cur.data.yinyang is yinyang
        cur = self.names.head
        count = 0
        while cur.data.name != name or count < self.names.get_length():
            cur = cur.next
            count += 1
        return cur

    def get_circular_linked_list(self):
        return TianGanCircularLinkedList

    def get_items(self):
        return TianGanItems
