from typing import Optional
from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=6, max_length=64)
    nickname: Optional[str] = Field(default=None, max_length=32)


class LoginRequest(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class WeChatLoginRequest(BaseModel):
    code: str = Field(..., description="wx.login() 返回的临时 code")
    nickname: Optional[str] = Field(default=None, description="用户昵称（可选）")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer")
    expires_in: int = Field(..., description="过期时间（秒）")
    user: "UserInfo"


class UserInfo(BaseModel):
    user_id: str
    username: str
    nickname: Optional[str] = None
    openid: Optional[str] = None


TokenResponse.model_rebuild()
