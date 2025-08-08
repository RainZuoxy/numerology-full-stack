from datetime import datetime
from typing import Any, Optional, Tuple, List

from pydantic import BaseModel, Field, ConfigDict, model_validator, field_serializer
from lunardate import LunarDate
from numerology.const import Gender, ShiShenType
from numerology.models.base import BaseStem
from numerology.models.main_destiny import MainDestinyItem
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

    def __str__(self):
        def _format(v,width):
            return f"{v: ^{width}}"
        return f"""
    {_format('',10)}|{_format('Tian Gan',10)}|{_format('Di Zhi',10)}
    {'-' * 30}
    {_format('Year',10)}|{_format(self.tg_year.type.value,10)}|{_format(self.dz_year.type.value,10)}
    {_format('Month',10)}|{_format(self.tg_month.type.value,10)}|{_format(self.dz_month.type.value,10)}
    {_format('Day',10)}|{_format(self.tg_day.type.value,10)}|{_format(self.dz_day.type.value,10)}
    {_format('Hour',10)}|{_format(self.tg_hour.type.value,10)}|{_format(self.dz_hour.type.value,10)}
        """


class ShiShenChart(BaseModel):
    tg_year: ShiShenType
    dz_year: DZ_TYPE
    tg_month: ShiShenType
    dz_month: DZ_TYPE
    dz_day: DZ_TYPE
    tg_hour: ShiShenType
    dz_hour: DZ_TYPE

    def __str__(self):
        def _format(v,width):
            return f"{v: ^{width}}"
        return f"""
    {_format('',10)}|{_format('Tian Gan',11)}|{_format('Di Zhi',20)}
    {'-' * 20+'主气,中气,余气'.center(20,'-')}
    {_format('Year',10)}|{_format(self.tg_year.value,10)}|{_format(','.join([i.value if i else '/' for i in self.dz_year]),13)}
    {_format('Month',10)}|{_format(self.tg_month.value,10)}|{_format(','.join([i.value if i else '/' for i in self.dz_month]),13)}
    {_format('Day',10)}|{_format('(日主)',10)}|{_format(','.join([i.value if i else '/' for i in self.dz_day]),13)}
    {_format('Hour',10)}|{_format(self.tg_hour.value,10)}|{_format(','.join([i.value if i else '/' for i in self.dz_day]),13)}
        """




class MainDestinyChart(BaseModel):
    num: int
    items: List[MainDestinyItem] = Field(default_factory=list)

    model_config = ConfigDict(arbitrary_types_allowed=True)
