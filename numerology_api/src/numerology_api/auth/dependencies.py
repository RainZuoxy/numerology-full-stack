from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from numerology_api.auth import service as auth_service
from numerology_api.auth.jwt_utils import decode_access_token
from numerology_api.auth.models import User
from numerology_api.db.engine import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def _resolve_user(session: Session, token: Optional[str]) -> Optional[User]:
    if not token:
        return None
    try:
        payload = decode_access_token(token)
    except jwt.PyJWTError:
        return None
    sub = payload.get("sub")
    if sub is None:
        return None
    try:
        user_id = int(sub)
    except (TypeError, ValueError):
        return None
    return auth_service.get_user(session, user_id)


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    user = _resolve_user(session, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_optional_user(
    token: Optional[str] = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> Optional[User]:
    return _resolve_user(session, token)
