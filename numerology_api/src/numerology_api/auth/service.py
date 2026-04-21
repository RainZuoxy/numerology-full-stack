from typing import Optional

import bcrypt
from sqlmodel import Session, select

from numerology_api.auth.models import User


def _hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _verify_password(pw: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(pw.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


def register_password_user(
    session: Session,
    username: str,
    password: str,
    nickname: Optional[str] = None,
) -> User:
    existing = session.exec(select(User).where(User.username == username)).first()
    if existing:
        raise ValueError(f"username already exists: {username}")
    user = User(
        username=username,
        password_hash=_hash_password(password),
        nickname=nickname or username,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_password(
    session: Session,
    username: str,
    password: str,
) -> Optional[User]:
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not user.password_hash:
        return None
    if not _verify_password(password, user.password_hash):
        return None
    return user


def get_or_create_wechat_user(
    session: Session,
    openid: str,
    nickname: Optional[str] = None,
) -> User:
    user = session.exec(select(User).where(User.openid == openid)).first()
    if user:
        return user
    user = User(
        username=f"wx_{openid[:8]}",
        openid=openid,
        nickname=nickname or "微信用户",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)
