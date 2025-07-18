from datetime import datetime
from functools import cached_property
from typing import Dict, Tuple, Literal, List
from pydantic import BaseModel, computed_field

from numerology.const.calendar import SOLAR_TERM_WEIGHT, D, SOLAR_TERM_CALENDAR, SOLAR_TERM_MAP_DIZHI
from numerology.models import DI_ZHI, TIAN_GAN
from numerology.models.base import Field
from numerology.models.pillar import PillarItem
from numerology.models.solar_term import CalendarEdgeResult, SolarTermItem
from numerology.utils.datetimes import convert_st_item
from numerology.utils.validator import convert_tian_gan_index, convert_di_zhi_index, convert_index


def is_leap_year(year: int) -> bool:
    return True if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else False


def get_datetime_from_solar_stem(year: int, solar_term: str) -> int:
    if solar_term not in SOLAR_TERM_WEIGHT:
        raise KeyError(f"'{solar_term}' is not found in SOLAR_TERM_WEIGHT")
    is_leap = is_leap_year(year=year)
    y = year % 100
    c = SOLAR_TERM_WEIGHT[solar_term]
    # l = (y - 1) / 4 if solar_term in ["立春", "雨水", "小寒", "大寒"] else y / 4
    l = int(y / 4)
    return (y * D + c) - l


def get_calendar_by_manual(year: int) -> Dict[str, Tuple[int, int]]:
    _calendar_year = {}
    for index, solar_term in enumerate(SOLAR_TERM_WEIGHT.keys(), start=1):
        _day = get_datetime_from_solar_stem(year=year, solar_term=solar_term)
        if solar_term not in _calendar_year:
            _calendar_year[solar_term] = (((index - 1) // 2 + 1), int(_day),)
    return _calendar_year


def get_calendar_by_solar_term(year: int) -> Dict[str, Tuple[int, int]]:
    return (
        get_calendar_by_manual(year=year)
        if str(year) not in SOLAR_TERM_CALENDAR
        else SOLAR_TERM_CALENDAR[str(year)]
    )


class GanZhiCalendar(BaseModel):
    dob: datetime = Field()

    @computed_field
    @cached_property
    def year(self) -> PillarItem:

        tiangan_index, dizhi_index = self.get_pillar_year_index()
        return self.get_pillar(pillar_name="年柱", tiangan_index=tiangan_index, dizhi_index=dizhi_index)


    @computed_field
    @cached_property
    def month(self) -> PillarItem:

        tiangan_index, dizhi_index = self.get_pillar_month_index()
        return self.get_pillar(pillar_name="月柱", tiangan_index=tiangan_index, dizhi_index=dizhi_index)


    @computed_field
    @cached_property
    def day(self) -> PillarItem:

        tiangan_index, dizhi_index = self.get_pillar_day_index()
        return self.get_pillar(pillar_name="日柱", tiangan_index=tiangan_index, dizhi_index=dizhi_index)


    @computed_field
    @cached_property
    def hour(self) -> PillarItem:

        tiangan_index, dizhi_index = self.get_pillar_hour_index()
        return self.get_pillar(pillar_name="时柱", tiangan_index=tiangan_index, dizhi_index=dizhi_index)


    @computed_field
    @cached_property
    def lichun_dt(self) -> datetime:
        return self.get_datetime_by_year_and_solar_term(year=self.dob.year, solar_term="立春")

    def before_solar_term(self, solar_term: datetime) -> bool:
        return True if self.dob < solar_term else False

    @staticmethod
    def get_pillar(
            pillar_name: Literal["年柱", "月柱", "日柱", "时柱"],
            tiangan_index: int, dizhi_index: int
    ) -> PillarItem:
        return PillarItem(
            name=pillar_name, tian_gan=TIAN_GAN[tiangan_index],
            di_zhi=DI_ZHI[dizhi_index]
        )

    @staticmethod
    def get_datetime_by_year_and_solar_term(year: int, solar_term: str) -> datetime:
        _year = str(year)
        if _year not in SOLAR_TERM_CALENDAR:
            raise KeyError(f"'{_year}' is not in SOLAR_TERM")
        if solar_term not in SOLAR_TERM_CALENDAR[_year]:
            raise KeyError(f"'{solar_term}' is not in SOLAR_TERM['{_year}']")

        month, day = SOLAR_TERM_CALENDAR[_year][solar_term]

        return datetime(year=year, month=month, day=day)

    def adjust_year(self) -> int:
        return self.dob.year - 1 if self.before_solar_term(solar_term=self.lichun_dt) else self.dob.year

    def adjust_month(self) -> int:
        calendar_edge = self.get_solar_term_edges_centered_on_dob(only_month_term=True)
        if calendar_edge.is_exist_left():
            return calendar_edge.left_edge.dt.month
        return convert_di_zhi_index(index=self.dob.month - 1)

    @staticmethod
    def get_year_tiangan_index(year: int) -> int:
        return convert_tian_gan_index(index=(year - 3) % 10)

    @staticmethod
    def get_year_dizhi_index(year: int) -> int:
        return convert_di_zhi_index(index=(year - 3) % 12)

    def check_after_dob(self, item):
        """
        Helper function to determine if a solar term occurs after the birth date.

        The solar terms are sorted chronologically, and this function helps identify
        the position of the birth date relative to the solar terms.

        Returns False for all solar terms before the birth date and True for all
        solar terms after the birth date.

        1,2,3,4,5,6,(self.dob),7,8,9,10,11,12
        ----False------------|-------True-----

        param item:
        Returns:
            bool: True if the solar term is after the birth date, False otherwise
        """
        (_st, (_month, _day)) = item
        _dt = datetime(year=self.dob.year, month=_month, day=_day)
        return self.dob < _dt

    def get_solar_terms(
            self, solar_terms: Dict[str, Tuple[int, int]], only_month_term: bool
    ) -> List[Tuple[str, Tuple[int, int]]]:
        sorted_items = sorted(solar_terms.items(), key=lambda item: item[1])
        # Just use month terms
        if only_month_term:
            sorted_items = filter(lambda item: item[0] in [j for (j, _) in SOLAR_TERM_MAP_DIZHI.keys()], sorted_items)
        sorted_items = list(sorted_items)
        return sorted_items

    def get_solar_term_edges_centered_on_dob(
            self, only_month_term: bool = False
    ) -> CalendarEdgeResult:
        """
        Get the solar terms that are immediately before and after the date of birth.

        This method returns a tuple containing the solar terms that surround the date of birth,
        effectively creating a time window around the birth date. The solar terms are returned as
        both their names and exact dates.

        Args:
            only_month_term (bool, optional): If True, only returns month terms (节气) and
                excludes mid-month terms (中气). Default is False.

        Returns:
            Tuple[Tuple[str, datetime], Tuple[str, datetime]]:
                - First tuple: The solar term before the birth date
                    * str: Name of the solar term (e.g., "立春", "雨水")
                    * datetime: Exact date of the solar term
                - Second tuple: The solar term after the birth date
                    * str: Name of the solar term
                    * datetime: Exact date of the solar term

        Example:
            >>> gzc = GanZhiCalendar(dob=datetime(year=2025, month=9, day=2))
            >>> gzc.get_solar_term_edges_centered_on_dob()
            CalendarEdgeResult(
                left_edge=SolarTermItem(name='处暑', dt=datetime.datetime(2025, 8, 23, 0, 0))
                right_edge=SolarTermItem(name='白露', dt=datetime.datetime(2025, 9, 7, 0, 0))
            )
            >>> gzc.get_solar_term_edges_centered_on_dob(only_month_term=True)
            CalendarEdgeResult(
                left_edge=SolarTermItem(name='立秋', dt=datetime.datetime(2025, 8, 7, 0, 0))
                right_edge=SolarTermItem(name='白露', dt=datetime.datetime(2025, 9, 7, 0, 0))
            )
        """

        solar_terms: Dict[str, Tuple[int, int]] = get_calendar_by_solar_term(year=self.dob.year)
        sorted_items = self.get_solar_terms(solar_terms=solar_terms, only_month_term=only_month_term)

        left, right = 0, len(sorted_items) - 1
        left_flag, right_flag = self.check_after_dob(sorted_items[left]), self.check_after_dob(sorted_items[right])

        if (not left_flag ^ right_flag) and (left_flag and right_flag):
            _solar_term_item = convert_st_item(year=self.dob.year, st_tuple=sorted_items[left])
            return CalendarEdgeResult(right_edge=_solar_term_item)

        if not (left_flag ^ right_flag or left_flag and right_flag):
            _solar_term = "大雪" if only_month_term else "冬至"
            _solar_term_item = SolarTermItem(
                name=_solar_term,
                dt=self.get_datetime_by_year_and_solar_term(year=self.dob.year, solar_term=_solar_term)
            )
            return CalendarEdgeResult(left_edge=_solar_term_item)

        while (right - left) > 1 and left_flag ^ right_flag:
            mid = (left + right) // 2
            _flag = self.check_after_dob(sorted_items[mid])
            if not left_flag ^ _flag:
                left = mid
            else:
                right = mid
        _left_item = convert_st_item(year=self.dob.year, st_tuple=sorted_items[left])
        _right_item = convert_st_item(year=self.dob.year, st_tuple=sorted_items[right])
        return CalendarEdgeResult(left_edge=_left_item, right_edge=_right_item)

    def get_nearest_solar_term_info(self, orient: Literal["forward", "backward"] = None) -> SolarTermItem:
        """
        Get the nearest solar term to the date of birth (dob).

        This method returns the solar term that is closest to the date of birth, with options to specify
        whether to look forward or backward in time. If no orientation is specified, it returns the
        closest solar term based on absolute time difference.

        Solar terms (节气) are important in traditional Chinese calendar system, marking specific
        points in the solar year. There are 24 solar terms in a year, each approximately 15 days apart.

        Args:
            orient (Literal["forward", "backward"], optional):
                - "forward": Returns the next solar term after the dob
                - "backward": Returns the previous solar term before the dob
                - None: Returns the closest solar term regardless of direction

        Returns:
            SolarTermItem:
                - st: str, The name of the solar term (e.g., "立春", "夏至")
                - dt: datetime, The exact date of the solar term

        Example:
            >>> gzc = GanZhiCalendar(dob=datetime(year=2025, month=2, day=28))
            >>> gzc.get_nearest_solar_term_info()  # Returns closest solar term
            SolarTermItem(name='惊蛰', dt=datetime.datetime(2025, 3, 5, 0, 0))
            >>> gzc.get_nearest_solar_term_info(orient='forward')  # Returns next solar term
            SolarTermItem(name='雨水', dt=datetime.datetime(2025, 2, 18, 0, 0))
            >>> gzc.get_nearest_solar_term_info(orient='backward')  # Returns previous solar term
            SolarTermItem(name='惊蛰', dt=datetime.datetime(2025, 3, 5, 0, 0))
        """
        calendar_edges = self.get_solar_term_edges_centered_on_dob(only_month_term=False)

        # Determine which solar term to return based on orientation
        match orient:
            case "forward":
                return calendar_edges.left_edge  # Returns the next solar term after dob
            case "backward":
                return calendar_edges.right_edge  # Returns the previous solar term before dob
            case _:
                # When no orientation specified, return the closest solar term
                # if calendar_edges.is_exist():
                #     check_point = (
                #             abs((self.dob - calendar_edges.left_edge.dt)) > abs(
                #         (self.dob - calendar_edges.right_edge.dt))
                #     )
                #     return calendar_edges.right_edge if check_point else calendar_edges.left_edge
                if abs((self.dob - calendar_edges.left_edge.dt)) > abs((self.dob - calendar_edges.right_edge.dt)):
                    return calendar_edges.right_edge  # Right edge is closer
                else:
                    return calendar_edges.left_edge  # Left edge is closer

    def get_month_with_solar_term(self) -> SolarTermItem:
        calendar_edge = self.get_solar_term_edges_centered_on_dob(only_month_term=True)
        return calendar_edge.left_edge

    def get_pillar_year_index(self) -> Tuple[int, int]:
        """
            在立春前 year - 1， 否则 year
            年份干支口诀:
            天干: (阴历年份-3)/10取余
            地支: (阴历年份-3)/12取余
        """

        year = self.adjust_year()

        return self.get_year_tiangan_index(year), self.get_year_dizhi_index(year)

    def get_pillar_month_index(self) -> Tuple[int, int]:

        """
        月份干支口诀:
            天干:
            凡甲年己年, 寅月天干为丙, 卯月天干为丁, 其余顺推;
            凡乙年庚年, 寅月天干为戊, 卯月天干为己, 其余顺推;
            凡丙年辛年, 寅月天干为庚, 卯月天干为辛, 其余顺推;
            凡丁年壬年, 寅月天干为壬, 卯月天干为癸, 其余顺推;
            凡戊年癸年, 寅月天干为甲, 卯月天干为乙, 其余顺推;

            地支:
            每月的地支是固定的,
            2月立春开始寅月, 3月惊蛰开始卯月, 4月清明开始辰月, 5月立夏开始巳月, 6月芒种开始午月, 7月小暑开始未月,
            8月立秋开始申月, 9月白露开始酉月, 10月寒露开始戌月, 11月立冬开始亥月, 12月大雪开始子月, 1月小寒开始丑月.
        :return:
        """

        rule = {1: 3, 2: 5, 3: 7, 4: 9, 5: 1}
        year = self.adjust_year()
        year_tiangan_index = self.get_year_tiangan_index(year=year)
        start_tiangan_index = rule.get(convert_index(index=year_tiangan_index, divisor=5))

        month = self.adjust_month()

        diff_value = month - 2
        if diff_value < 0:
            diff_value = abs(diff_value)

        month_tiangan_index = start_tiangan_index + diff_value

        return convert_tian_gan_index(index=month_tiangan_index), convert_di_zhi_index(index=month + 1)

    def get_pillar_day_index(self) -> Tuple[int, int]:
        '''
        日柱干支口诀:
        ((公元年数 - 1) * 5 + (公元年数 - 1) / 4 + 当天是当年的第几日) / 60 取余数
        天干: 余数 % 10取余
        地支: 余数 % 12取余
        '''
        day_reminder = (self.dob.year - 1) * 5 + (self.dob.year - 1) / 4
        day_reminder += self.dob.timetuple().tm_yday
        day_reminder = day_reminder % 60
        tiangan_index = int(day_reminder % 10)

        dizhi_index = int(day_reminder % 12)

        return convert_tian_gan_index(index=tiangan_index), convert_di_zhi_index(index=dizhi_index)

    def get_pillar_hour_index(self) -> Tuple[int, int]:
        """
        时柱干支口诀:
        天干:
        甲日或己日, 子时则配甲, 即甲子, 丑时则顺排, 配乙, 即乙丑, 其余顺推;
        乙日或庚日, 子时则配丙, 即丙子, 丑时则顺排, 配丁, 即丁丑, 其余顺推;
        丙日或辛日, 子时则配戊, 即戊子, 丑时则顺排, 配己, 即己丑, 其余顺推;
        丁日或壬日, 子时则配庚, 即庚子, 其余顺排.
        戊日或癸日, 子时则配壬, 即壬子, 其余顺排.

        地支：
        子时: (凌晨0~0:59:59点，晚23~23:59:59)
        子时: 23点--凌晨1点 - 丑时: 1点--凌晨3点
        寅时: 3点--凌晨5点 - 卯时: 5点--早晨7点
        辰时: 7点--上午9点 - 巳时: 9点--中午11点
        午时: 11点--下午13点 - 未时: 13点--下午15点
        申时: 15点--下午17点 - 酉时: 17点--下午19点
        戌时: 19点--晚上21点 - 亥时: 21点--晚上23点
        """
        rule = {1: 1, 2: 3, 3: 5, 4: 7, 5: 9}
        day_tiangan_index = self.day.tian_gan.sequence
        start_tiangan_index = rule.get(convert_index(index=day_tiangan_index,divisor=5))
        hour = DI_ZHI.get_di_zhi_by_hour(t=self.dob.time())
        hour = hour.sequence
        hour_tiangan_index = start_tiangan_index + (hour - 1 )

        return convert_tian_gan_index(index=hour_tiangan_index), convert_di_zhi_index(index=hour)
