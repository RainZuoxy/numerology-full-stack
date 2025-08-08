from enum import Enum


class TimeFormat(str, Enum):

    HOUR_FORMAT = "%H"
    MINUTE_FORMAT = "%M"
    SECOND_FORMAT = "%S"
    FULL_FORMAT = "%H:%M:%S"


class DateFormat(str, Enum):

    YEAR_FORMAT = "%Y"
    MONTH_FORMAT = "%m"
    DAY_FORMAT = "%d"
    FULL_FORMAT = "%Y-%m-%d"


class DateTimeFormat(str, Enum):

    ISO_FORMAT = f"{DateFormat.FULL_FORMAT.value} {TimeFormat.FULL_FORMAT.value}"
    BA_ZI_FORMAT = f"{DateFormat.FULL_FORMAT.value} {TimeFormat.HOUR_FORMAT.value}"

