from pydantic import BaseModel
from datetime import datetime
from typing import Union

from numerology.models.base import Field


class SolarTermItem(BaseModel):
    name: str
    dt: datetime


class CalendarEdgeResult(BaseModel):
    left_edge: Union[SolarTermItem, None] = Field(default=None)
    right_edge: Union[SolarTermItem, None] = Field(default=None)

    def is_exist_left(self) -> bool:
        return self.left_edge is not None

    def is_exist_right(self) -> bool:
        return self.right_edge is not None

    def is_exist(self) -> bool:
        return self.is_exist_left() and self.is_exist_right()
