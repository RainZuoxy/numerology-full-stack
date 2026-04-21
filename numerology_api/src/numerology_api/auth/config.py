import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AuthConfig:
    jwt_secret: str = os.getenv("NUMEROLOGY_JWT_SECRET", "change-me-in-production")
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = int(os.getenv("NUMEROLOGY_JWT_EXPIRE_MIN", "1440"))

    wechat_appid: str = os.getenv("WECHAT_APPID", "")
    wechat_secret: str = os.getenv("WECHAT_SECRET", "")
    wechat_code2session_url: str = "https://api.weixin.qq.com/sns/jscode2session"


auth_config = AuthConfig()
