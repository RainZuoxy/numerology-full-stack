from datetime import time
from enum import Enum


class DiZhiType(Enum):
    ZI = '子'
    CHOU = '丑'
    YIN = '寅'
    MAO = '卯'
    CHEN = '辰'
    SI = '巳'
    WU = '午'
    WEI = '未'
    SHEN = '申'
    YOU = '酉'
    XU = '戌'
    HAI = '亥'

    @classmethod
    def get_list(cls):
        return [
            cls.ZI, cls.CHOU, cls.YIN, cls.MAO, cls.CHEN, cls.SI,
            cls.WU, cls.WEI, cls.SHEN, cls.YOU, cls.XU, cls.HAI
        ]

    @classmethod
    def get_time_range_list(cls):
        return {
            (time(23, 0, 0), time(23, 59, 59)): cls.ZI,
            (time(0, 0, 0), time(0, 59, 59)): cls.ZI,
            (time(1, 0, 0), time(2, 59, 59)): cls.CHOU,
            (time(3, 0, 0), time(4, 59, 59)): cls.YIN,
            (time(5, 0, 0), time(6, 59, 59)): cls.MAO,
            (time(7, 0, 0), time(8, 59, 59)): cls.CHEN,
            (time(9, 0, 0), time(10, 59, 59)): cls.SI,
            (time(11, 0, 0), time(12, 59, 59)): cls.WU,
            (time(13, 0, 0), time(14, 59, 59)): cls.WEI,
            (time(15, 0, 0), time(16, 59, 59)): cls.SHEN,
            (time(17, 0, 0), time(18, 59, 59)): cls.YOU,
            (time(19, 0, 0), time(20, 59, 59)): cls.XU,
            (time(21, 0, 0), time(22, 59, 59)): cls.HAI,
        }

    @classmethod
    def get_month_range_list(cls):
        return {
            12: cls.ZI,
            1: cls.CHOU,
            2: cls.YIN,
            3: cls.MAO,
            4: cls.CHEN,
            5: cls.SI,
            6: cls.WU,
            7: cls.WEI,
            8: cls.SHEN,
            9: cls.YOU,
            10: cls.XU,
            11: cls.HAI,
        }

    @classmethod
    def get_di_zhi_by_month(cls, m:int) -> "DiZhiType":
        try:
            return cls.get_month_range_list()[m]
        except KeyError:
            raise KeyError(f"无法查找月份为:{m}对应的地支")

    @classmethod
    def get_di_zhi_by_hour(cls, t: time) -> "DiZhiType":
        for (start_time, end_time,), dizhi in cls.get_time_range_list().items():
            if start_time <= t < end_time:
                return dizhi

        raise ValueError(f'无法查找{time}时辰的地支')
