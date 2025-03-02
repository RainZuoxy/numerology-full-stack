import datetime
import math
from enum import Enum
from ephem import Equatorial, Ecliptic, Sun, Date, now


class SolarTerm(str, Enum):
    LICHUN = "立春"
    YUSHUI = "雨水"
    JINGZHE = "惊蛰"
    CHUNFEN = "春分"
    QINGMING = "清明"
    GUYU = "谷雨"
    LIXIA = "立夏"
    XIAOMAN = "小满"
    MANGZHONG = "芒种"
    XIAZHI = "夏至"
    XIAOSHU = "小暑"
    DASHU = "大暑"
    LIQIU = "立秋"
    CHUSHU = "处暑"
    BAILU = "白露"
    QIUFEN = "秋分"
    HANLU = "寒露"
    SHUANGJIANG = "霜降"
    LIDONG = "立冬"
    XIAOXUE = "小雪"
    DAXUE = "大雪"
    DONGZHI = "冬至"
    XIAOHAN = "小寒"
    DAHAN = "大寒"

    @classmethod
    def get_list(cls):
        return [
            cls.CHUNFEN, cls.QINGMING, cls.GUYU, cls.LIXIA, cls.XIAOMAN, cls.MANGZHONG,
            cls.XIAZHI, cls.XIAOSHU, cls.DASHU, cls.LIQIU, cls.CHUSHU, cls.BAILU,
            cls.QIUFEN, cls.HANLU, cls.SHUANGJIANG, cls.LIDONG, cls.XIAOXUE, cls.DAXUE,
            cls.DONGZHI, cls.XIAOHAN, cls.DAHAN, cls.LICHUN, cls.YUSHUI, cls.JINGZHE
        ]

    @staticmethod
    def __ecliptic_lon(jd_utc):
        s = Sun(jd_utc)  # 构造太阳
        equ = Equatorial(s.ra, s.dec, epoch=jd_utc)  # 求太阳的视赤经视赤纬（epoch设为所求时间就是视赤经视赤纬）
        e = Ecliptic(equ)  # 赤经赤纬转到黄经黄纬
        return e.lon  # 返回黄纬

    # 根据时间求太阳黄经，计算到了第几个节气，春分序号为0
    def sta(self, jd):
        e = self.__ecliptic_lon(jd)
        n = int(e * 180.0 / math.pi / 15)
        return n

    # 根据当前时间，求下个节气的发生时间
    def iteration(self, jd):  # jd：要求的开始时间，sta：不同的状态函数
        s1 = self.sta(jd)  # 初始状态(太阳处于什么位置)
        s0 = s1
        dt = 1.0  # 初始时间改变量设为1天
        while True:
            jd += dt
            s = self.sta(jd)
            if s0 != s:
                s0 = s
                dt = -dt / 2  # 使时间改变量折半减小
            if abs(dt) < 0.0000001 and s != s1:
                break
        return jd

    def get_jieqi(self, target_date, num):  # 从当前时间开始连续输出未来n个节气的时间
        jd = now()  # 获取当前时间的一个儒略日和1899/12/31 12:00:00儒略日的差值
        e = self.__ecliptic_lon(jd)
        n = int(e * 180.0 / math.pi / 15) + 1
        for i in range(num):
            if n >= 24:
                n -= 24
            jd = self.iteration(jd)
            date = Date(jd + 1 / 3).tuple()
            print(
                "{0}-{1:02d}-{2:02d} {3}：{4:02d}:{5:02d}:{6:03.1f}".format(
                    date[0], date[1], date[2], jieqi[n], date[3], date[4], date[5])
            )
            n += 1


if __name__ == '__main__':
    # import pypinyin
    #
    dic = {"春分": "", "清明": "", "谷雨": "", "立夏": "", "小满": "", "芒种": "",
           "夏至": "",
           "小暑": "", "大暑": "", "立秋": "", "处暑": "", "白露": "", "秋分": "", "寒露": "", "霜降": "", "立冬": "",
           "小雪": "",
           "大雪": "", "冬至": "", "小寒": "", "大寒": "", "立春": "", "雨水": "", "惊蛰": ""}
    jieqi = SolarTerm.get_list()


    # for k in dic.keys():
    #     print(f'{"".join(pypinyin.lazy_pinyin(k)).upper()}="{k}"')
    current_date = datetime.datetime.now()
    sep_date = datetime.timedelta(days=15)
    print(current_date)
    print(current_date + sep_date)
    print(int(current_date.timestamp()))
    print(current_date.timetuple().tm_yday)
    y = 2089
    C = 4.475
    D = 0.2422
    x = int((y * D + C)) - int((y / 4 - 15))
    start_date = datetime.datetime(2024, 2, x)
    print(start_date)
    tmp_date = start_date
    _jieqi_dates=[]
    target=datetime.datetime.strptime('1994-06-13', '%Y-%m-%d')
    for jieqi in dic.keys():
        print(f"{jieqi}: {tmp_date}")
        _jieqi_dates.append(tmp_date)
        tmp_date += sep_date
    diff_times=[abs(x-target) for x in _jieqi_dates]
    print(min(diff_times))
    # print(x)

    # def ecliptic_lon(jd_utc):
    #     s = Sun(jd_utc)  # 构造太阳
    #     equ = Equatorial(s.ra, s.dec, epoch=jd_utc)  # 求太阳的视赤经视赤纬（epoch设为所求时间就是视赤经视赤纬）
    #     e = Ecliptic(equ)  # 赤经赤纬转到黄经黄纬
    #     return e.lon  # 返回黄纬


    # # 根据时间求太阳黄经，计算到了第几个节气，春分序号为0
    # def sta(jd):
    #     e = ecliptic_lon(jd)
    #     n = int(e * 180.0 / math.pi / 15)
    #     return n
    #
    #
    # # 根据当前时间，求下个节气的发生时间
    # def iteration(jd, sta):  # jd：要求的开始时间，sta：不同的状态函数
    #     s1 = sta(jd)  # 初始状态(太阳处于什么位置)
    #     s0 = s1
    #     dt = 1.0  # 初始时间改变量设为1天
    #     while True:
    #         jd += dt
    #         s = sta(jd)
    #         if s0 != s:
    #             s0 = s
    #             dt = -dt / 2  # 使时间改变量折半减小
    #         if abs(dt) < 0.0000001 and s != s1:
    #             break
    #     return jd


    # def jq(num):  # 从当前时间开始连续输出未来n个节气的时间
    #     jd = now()  # 获取当前时间的一个儒略日和1899/12/31 12:00:00儒略日的差值
    #     e = ecliptic_lon(jd)
    #     n = int(e * 180.0 / math.pi / 15) + 1
    #     for i in range(num):
    #         if n >= 24:
    #             n -= 24
    #         jd = iteration(jd, sta)
    #         d = Date(jd + 1 / 3).tuple()
    #         print("{0}-{1:02d}-{2:02d} {3}：{4:02d}:{5:02d}:{6:03.1f}".format(d[0], d[1], d[2], jieqi[n], d[3], d[4],
    #                                                                          d[5]))
    #         n += 1
    #
    #
    # jq(36)

