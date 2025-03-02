from dataclasses import dataclass
from numerology.const.shishen import SHI_SHEN
from numerology.core.base import CellProperty
from numerology.core.base.wuxing import WuXing


@dataclass
class ShiShen:
    rizhu: CellProperty

    def get_shishen(self, target: CellProperty):
        rizhu_wuxing, rizhu_yinyang = self.rizhu.wuxing.value, self.rizhu.yinyang
        if not isinstance(target, CellProperty):
            raise ValueError('target value is invalidate.')
        target_wuxing, target_yinyang = target.wuxing.value, target.yinyang
        _relationship = WuXing().current_node(name=rizhu_wuxing).get_relationship(target=target_wuxing)
        _diff = '同' if rizhu_yinyang is target_yinyang else '异'
        return SHI_SHEN[_relationship][_diff]
