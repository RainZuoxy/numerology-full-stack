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
    def get_all(cls):
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
            cls.ZI: 12,
            cls.CHOU: 1,
            cls.YIN: 2,
            cls.MAO: 3,
            cls.CHEN: 4,
            cls.SI: 5,
            cls.WU: 6,
            cls.WEI: 7,
            cls.SHEN: 8,
            cls.YOU: 9,
            cls.XU: 10,
            cls.HAI: 11,
        }

    def get_month(self):
        return self.get_month_range_list()[self]

    @classmethod
    def get_chinese_zodiacs(cls):
        return {
            cls.ZI: "鼠",
            cls.CHOU: "牛",
            cls.YIN: "虎",
            cls.MAO: "兔",
            cls.CHEN: "龙",
            cls.SI: "蛇",
            cls.WU: "马",
            cls.WEI: "羊",
            cls.SHEN: "猴",
            cls.YOU: "鸡",
            cls.XU: "狗",
            cls.HAI: "猪",
        }

    def get_chinese_zodiac(self):
        return self.get_chinese_zodiacs()[self]
