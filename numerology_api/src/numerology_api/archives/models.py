from datetime import date, datetime
from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class Archive(SQLModel, table=True):
    __tablename__ = "archives"

    archive_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id", index=True, nullable=False)
    name: str = Field(max_length=64)
    gender: str = Field(max_length=8)  # "male" / "female"
    dob_time: str = Field(max_length=32)  # "YYYY-MM-DD HH:MM:SS"
    is_primary: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class DailyPrediction(SQLModel, table=True):
    __tablename__ = "daily_predictions"
    __table_args__ = (
        UniqueConstraint("user_id", "predict_date", name="uq_daily_user_date"),
    )

    prediction_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id", index=True, nullable=False)
    archive_id: int = Field(foreign_key="archives.archive_id", nullable=False)
    predict_date: date = Field(nullable=False)
    score: int = Field(nullable=False)
    payload_json: str = Field(nullable=False)  # 完整 JSON 序列化内容
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
