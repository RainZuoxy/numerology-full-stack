from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from numerology_api.auth import service as auth_service
from numerology_api.auth.config import auth_config
from numerology_api.auth.dependencies import get_current_user
from numerology_api.auth.jwt_utils import create_access_token
from numerology_api.auth.models import User
from numerology_api.auth.wechat import WeChatAuthError, code2session
from numerology_api.db.engine import get_session
from numerology_api.models.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserInfo,
    WeChatLoginRequest,
)

router = APIRouter(prefix="/auth", tags=["Auth 鉴权"])


def _to_user_info(user: User) -> UserInfo:
    return UserInfo(
        user_id=str(user.user_id),
        username=user.username,
        nickname=user.nickname,
        openid=user.openid,
    )


def _issue_token(user: User) -> TokenResponse:
    token = create_access_token(subject=str(user.user_id), extra={"username": user.username})
    return TokenResponse(
        access_token=token,
        expires_in=auth_config.jwt_expire_minutes * 60,
        user=_to_user_info(user),
    )


@router.post("/register", response_model=TokenResponse, summary="用户名/密码注册")
def register(
    req: RegisterRequest,
    session: Session = Depends(get_session),
) -> TokenResponse:
    try:
        user = auth_service.register_password_user(
            session, username=req.username, password=req.password, nickname=req.nickname
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return _issue_token(user)


@router.post("/login", response_model=TokenResponse, summary="用户名/密码登录")
def login(
    req: LoginRequest,
    session: Session = Depends(get_session),
) -> TokenResponse:
    user = auth_service.authenticate_password(session, req.username, req.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    return _issue_token(user)


@router.post("/wechat", response_model=TokenResponse, summary="微信小程序登录")
async def wechat_login(
    req: WeChatLoginRequest,
    session: Session = Depends(get_session),
) -> TokenResponse:
    try:
        wx_session = await code2session(req.code)
    except WeChatAuthError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    user = auth_service.get_or_create_wechat_user(
        session, openid=wx_session["openid"], nickname=req.nickname
    )
    return _issue_token(user)


@router.get("/me", response_model=UserInfo, summary="获取当前用户信息")
def me(user: User = Depends(get_current_user)) -> UserInfo:
    return _to_user_info(user)
