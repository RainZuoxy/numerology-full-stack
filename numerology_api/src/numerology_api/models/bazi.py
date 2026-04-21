from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

from numerology.models.base import BaseStem
from numerology.models.chart import GanZhiChart, MainDestinyChart, ShiShenChart


class BaZiRequest(BaseModel):
    name: str = Field(default="UNKNOWN", description="姓名")
    dob_time: str = Field(
        ...,
        description="阳历出生时间 (YYYY-MM-DD HH:MM:SS)",
        examples=["1990-01-01 00:00:00"],
    )
    gender: Literal["male", "female"] = Field(..., description="性别")
    dayun_number: int = Field(default=7, ge=1, le=20, description="大运数量")


class BaZiResponse(BaseModel):
    """
    字段通过 alias 映射 ChartConf.results 中的原始函数名键，
    对外输出使用更语义化的字段名。
    """

    model_config = ConfigDict(populate_by_name=True)

    standard_start_age: str = Field(
        ..., alias="standard_start_age", description="标准起运年龄"
    )
    chinese_zodiac: str = Field(
        ..., alias="get_chinese_zodiac", description="生肖"
    )
    day_master: BaseStem = Field(
        ..., alias="get_day_master", description="日主（日干）"
    )
    main_destiny: MainDestinyChart = Field(
        ..., alias="generate_main_destiny", description="大运"
    )
    ba_zi: GanZhiChart = Field(
        ..., alias="generate_ba_zi", description="八字（四柱干支）"
    )
    shi_shen: ShiShenChart = Field(
        ..., alias="generate_shi_shen", description="十神"
    )
