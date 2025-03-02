from numerology.core.base import CircularLinkedList, BaseNode, BaseRules, Singleton, BaseProperty
from numerology.const.wu_xing import WuXingRelationship, BaseWuXing


class WuXingNode(BaseNode, BaseRules):

    def produce(self):
        return self.find_by_index(index=WuXingRelationship.PRODUCE.value)

    # 克
    def restrain(self):
        return self.find_by_index(index=WuXingRelationship.RESTRAIN.value)

    # 耗
    def consume(self):
        return self.find_by_index(index=WuXingRelationship.CONSUME.value)

    # 泄
    def weaken(self):
        return self.find_by_index(index=WuXingRelationship.WEAKEN.value)

    # 助
    def support(self):
        return self.find_by_index(index=WuXingRelationship.SUPPORT.value)

    def get_relationship(self, target: str):
        while True:
            if self.produce().data == target:
                return '生'
            elif self.restrain().data == target:
                return '克'
            elif self.consume().data == target:
                return '耗'
            elif self.weaken().data == target:
                return '泄'
            else:
                return '助'


class WuXingCircularLinkedList(CircularLinkedList):

    def get_node_type(self):
        return WuXingNode


class WuXing(Singleton, BaseProperty):
    def get_circular_linked_list(self):
        return WuXingCircularLinkedList

    def get_items(self):
        return BaseWuXing
