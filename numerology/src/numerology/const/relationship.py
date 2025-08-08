from enum import Enum


class WuXingRelationshipType(Enum):
    """
    五行关系
    A 生 B: A -> B
    Example:
    水      木    火   土    金
    base -> a -> b -> c -> d
    0: base is supported by base
    1: base is weakened by a
    2: base is consumed by b
    3: base is destroyed by c
    4: base is produced by d
    ---------------------------
    同我者 -> 助
    我生者- > 泄
    我克者 -> 耗
    克我者 -> 克
    生我者 -> 生
    """
    SUPPORTED = 0  # 同我者 -> 助
    WEAKENED = 1  # 我生者- > 泄
    CONSUMED = 2  # 我克者 -> 耗
    DESTROYED = 3  # 克我者 -> 克
    PRODUCED = 4  # 生我者 -> 生

    @property
    def text(self) -> str:
        """

        :return:
        """
        relationship_names = {0: '助', 1: '泄', 2: '耗', 3: '克', 4: '生'}
        return relationship_names.get(self.value)

    @property
    def weight(self) -> int:
        weight_map = {0: 1, 1: -1, 2: -1, 3: -2, 4: 1}
        return weight_map.get(self.value)
