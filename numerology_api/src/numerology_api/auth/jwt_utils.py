from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

from numerology_api.auth.config import auth_config


def create_access_token(subject: str, extra: Optional[dict] = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=auth_config.jwt_expire_minutes)).timestamp()),
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, auth_config.jwt_secret, algorithm=auth_config.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, auth_config.jwt_secret, algorithms=[auth_config.jwt_algorithm])
