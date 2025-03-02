from datetime import datetime
from lunardate import LunarDate
from numerology.const.datetime_format import DateTimeFormat


def convert_to_datetime(datetime_string: str, datetime_format=DateTimeFormat.ISO_FORMAT.value) -> datetime:
    return datetime.strptime(datetime_string, datetime_format)


def convert_to_lunar_datetime(dt: datetime) -> datetime:
    lunar_dt = LunarDate.fromSolarDate(dt.year, dt.month, dt.day)
    return datetime(
        year=lunar_dt.year, month=lunar_dt.month, day=lunar_dt.day, hour=dt.hour, minute=dt.minute, second=dt.second,
        microsecond=dt.microsecond
    )