from enum import Enum


class ShiShenType(Enum):
    ZHENG_YIN = '正印'
    XIAO_SHEN = '枭神'
    BI_JIAN = '比肩'
    JIE_CAI = '劫财'
    SHI_SHEN = '食神'
    SHANG_GUAN = '伤官'
    ZHENG_CAI = '正财'
    PIAN_CAI = '偏财'
    ZHENG_GUAN = '正官'
    QI_SHA = '七杀'

    @classmethod
    def get_temperaments(cls):
        return {
            cls.ZHENG_YIN: "好",
            cls.XIAO_SHEN: "慢",
            cls.BI_JIAN: "犟",
            cls.JIE_CAI: "犟",
            cls.SHI_SHEN: "急",
            cls.SHANG_GUAN: "急",
            cls.ZHENG_CAI: "好",
            cls.PIAN_CAI: "倔",
            cls.ZHENG_GUAN: "好",
            cls.QI_SHA: "差"
        }

    def get_temperament(self) -> str:
        return self.get_temperaments()[self]
