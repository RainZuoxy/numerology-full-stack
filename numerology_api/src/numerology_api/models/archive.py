from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class ArchiveCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=32)
    gender: Literal["male", "female"]
    dob_time: str = Field(..., description="YYYY-MM-DD HH:MM:SS")


class ArchiveItem(BaseModel):
    archive_id: int
    name: str
    gender: Literal["male", "female"]
    dob_time: str
    is_primary: bool
    created_at: datetime


class ArchiveListResponse(BaseModel):
    items: list[ArchiveItem]
    max_archives: int


class DailyDimensions(BaseModel):
    wealth: int = Field(ge=0, le=100)
    love: int = Field(ge=0, le=100)
    career: int = Field(ge=0, le=100)
    health: int = Field(ge=0, le=100)
    study: int = Field(ge=0, le=100)


SignLevel = Literal["上上签", "上签", "中平签", "下签", "下下签"]


class DailyPredictionPayload(BaseModel):
    sign: SignLevel
    score: int = Field(ge=0, le=100)
    dimensions: DailyDimensions
    overall: str
    highlight: str
    caution: str
    lucky_color: str
    lucky_direction: str
    advice: str


class DailyPredictionResponse(BaseModel):
    predict_date: date
    archive_id: int
    archive_name: str
    day_pillar: Optional[str] = None
    payload: DailyPredictionPayload
    created_at: datetime
