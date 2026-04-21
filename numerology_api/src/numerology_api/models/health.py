from typing import Literal
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: Literal["ok"] = Field(..., description="服务状态")
    lib_version: str = Field(..., description="numerology 核心库版本")
    api_version: str = Field(..., description="numerology-api 版本")
