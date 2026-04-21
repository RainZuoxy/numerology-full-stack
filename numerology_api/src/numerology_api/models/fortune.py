from typing import Any, Optional

from pydantic import BaseModel, Field


class FortuneRequest(BaseModel):
    bazi: dict[str, Any] = Field(..., description="八字排盘完整结果")
    question: Optional[str] = Field(default=None, description="求测者想重点了解的问题")


class DimensionAnalysis(BaseModel):
    label: str
    score: int = Field(ge=0, le=100)
    overall: str
    insights: list[str]
    suggestions: list[str]
    timing: Optional[str] = None


class FortuneResponse(BaseModel):
    summary: str
    dimensions: dict[str, DimensionAnalysis]
    remarks: str
