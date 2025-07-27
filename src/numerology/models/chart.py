from datetime import datetime
from typing import Any, Optional, Tuple

from pydantic import BaseModel, ConfigDict, model_validator, field_serializer
from lunardate import LunarDate
from numerology.const import Gender, ShiShenType
from numerology.models.base import BaseStem
from numerology.utils.datetimes import (
    convert_solar_to_lunar_datetime, convert_lunar_to_solar_datetime,
    convert_to_datetime
)

DZ_TYPE = Tuple[ShiShenType, ShiShenType | None, ShiShenType | None]


class MainInfoChart(BaseModel):
    dob: Optional[datetime] = None
    lunar_dob: Optional[LunarDate] = None
    gender: Gender

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode='before')
    @classmethod
    def check_dob(cls, values: Any):
        _dob = values.get('dob')
        _lunar_dob = values.get('lunar_dob')
        if not (_dob or _lunar_dob):
            raise ValueError("dob or lunar_dob is required")
        if not _lunar_dob:
            _dob = convert_to_datetime(_dob) if isinstance(_dob, str) else _dob
            values['lunar_dob'] = convert_solar_to_lunar_datetime(_dob)
        if not _dob:
            values['dob'] = convert_lunar_to_solar_datetime(_lunar_dob)
        return values

    @field_serializer('lunar_dob')
    def serialize_lunar_dob(self, lunar_dob: LunarDate):
        return str(lunar_dob)


class GanZhiChart(BaseModel):
    tg_year: BaseStem
    dz_year: BaseStem
    tg_month: BaseStem
    dz_month: BaseStem
    tg_day: BaseStem
    dz_day: BaseStem
    tg_hour: BaseStem
    dz_hour: BaseStem


class ShiShenChart(BaseModel):
    tg_year: ShiShenType
    dz_year: DZ_TYPE
    tg_month: ShiShenType
    dz_month: DZ_TYPE
    dz_day: DZ_TYPE
    tg_hour: ShiShenType
    dz_hour: DZ_TYPE
