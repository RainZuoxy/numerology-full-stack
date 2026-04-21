from pydantic import BaseModel, Field, field_validator

from numerology.const.gua import Trigram64Item


class GuaRequest(BaseModel):
    trigram_series: str = Field(
        ...,
        description="六爻序列，0=阴，1=阳，顺序为初爻→上爻",
        examples=["010111"],
    )

    @field_validator("trigram_series")
    @classmethod
    def validate_trigram_series(cls, v: str) -> str:
        if len(v) != 6 or not all(c in "01" for c in v):
            raise ValueError("trigram_series 必须是由 0 和 1 组成的 6 位字符串")
        return v


class GuaResponse(BaseModel):
    name: str = Field(..., description="卦象枚举名")
    value: Trigram64Item = Field(..., description="卦象详细信息")
