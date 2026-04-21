from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=64)
    password_hash: Optional[str] = Field(default=None, max_length=128)
    openid: Optional[str] = Field(default=None, index=True, unique=True, max_length=64)
    nickname: Optional[str] = Field(default=None, max_length=64)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
