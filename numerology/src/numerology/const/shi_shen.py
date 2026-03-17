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

    @classmethod
    def get_symbolic_significance(cls):
        return {
            cls.ZHENG_YIN: ("学识", "保护", "长辈", "贵人", "", "", "",),
            cls.XIAO_SHEN: ("偏门技能", "灵感", "孤独", "", "", "",),
            cls.BI_JIAN: ("同辈助力", "竞争", "独立", "", "", "",),
            cls.JIE_CAI: ("争夺", "破财", "冲动", "", "", "",),
            cls.SHI_SHEN: ("才华", "享受", "口福", "艺术", "", "",),
            cls.SHANG_GUAN: ("叛逆", "创新", "表达欲", "",),
            cls.ZHENG_CAI: ("稳定收入", "节俭", "物质保障", "", "", "",),
            cls.PIAN_CAI: ("意外之财", "投机", "慷慨", "", "", "",),
            cls.ZHENG_GUAN: ("规则", "责任", "地位", "约束", "", "",),
            cls.QI_SHA: ("竞争", "挑战", "野心", "压力", "", "",)
        }
