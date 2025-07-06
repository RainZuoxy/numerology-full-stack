from numerology.core.base import CircularLinkedList, BaseNode, BaseRules
from numerology.core.base.wuxing import WuXing
from numerology.const.wu_xing import BaseTianGan


class TianGanNode(BaseNode, BaseRules):
    def __search_validate_wuxing(self, target_wuxing: str):
        limit = 0
        result = []
        count = 0
        cur = self
        while count < len(BaseTianGan) and limit < 2:
            if cur.data.wuxing.value == target_wuxing:
                result.append(cur)
                limit += 1
            cur = cur.next
            count += 1
        return result

    def produce(self):
        produce_wuxing = WuXing().current_node(name=self.data.wuxing.value).produce().data
        return self.__search_validate_wuxing(target_wuxing=produce_wuxing)

    # 克
    def destroy(self):
        restrain_wuxing = WuXing().current_node(name=self.data.wuxing.value).destroy().data
        return self.__search_validate_wuxing(target_wuxing=restrain_wuxing)

    # 耗
    def consume(self):
        consume_wuxing = WuXing().current_node(name=self.data.wuxing.value).consume().data
        return self.__search_validate_wuxing(target_wuxing=consume_wuxing)

    # 泄
    def weaken(self):
        weaken_wuxing = WuXing().current_node(name=self.data.wuxing.value).weaken().data
        return self.__search_validate_wuxing(target_wuxing=weaken_wuxing)

    # 助
    def support(self):
        support_wuxing = WuXing().current_node(name=self.data.wuxing.value).support().data
        return self.__search_validate_wuxing(target_wuxing=support_wuxing)


class TianGanCircularLinkedList(CircularLinkedList):

    def get_node_type(self):
        return TianGanNode
