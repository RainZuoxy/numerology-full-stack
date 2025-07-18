from datetime import datetime
from lunardate import LunarDate
from numerology.const.datetime_format import DateTimeFormat
from numerology.models.solar_term import SolarTermItem


def convert_to_datetime(datetime_string: str, datetime_format=DateTimeFormat.ISO_FORMAT.value) -> datetime:
    return datetime.strptime(datetime_string, datetime_format)


def convert_to_lunar_datetime(dt: datetime) -> datetime:
    lunar_dt = LunarDate.fromSolarDate(dt.year, dt.month, dt.day)
    return datetime(
        year=lunar_dt.year, month=lunar_dt.month, day=lunar_dt.day, hour=dt.hour, minute=dt.minute, second=dt.second,
        microsecond=dt.microsecond
    )


def convert_st_item(year: int, st_tuple: tuple) -> SolarTermItem:
    st, (_month, _day) = st_tuple
    return SolarTermItem(name=st, dt=datetime(year=year, month=_month, day=_day))
