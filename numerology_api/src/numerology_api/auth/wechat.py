import httpx

from numerology_api.auth.config import auth_config


class WeChatAuthError(Exception):
    pass


async def code2session(code: str) -> dict:
    """
    调用微信 jscode2session 接口，用前端 wx.login() 返回的 code 换取 openid / session_key。
    返回 { openid, session_key, unionid? }
    """
    if not auth_config.wechat_appid or not auth_config.wechat_secret:
        raise WeChatAuthError("WeChat appid/secret not configured")

    params = {
        "appid": auth_config.wechat_appid,
        "secret": auth_config.wechat_secret,
        "js_code": code,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(auth_config.wechat_code2session_url, params=params)
        data = resp.json()

    if "errcode" in data and data["errcode"] != 0:
        raise WeChatAuthError(f"WeChat error: {data.get('errmsg')} (code={data.get('errcode')})")
    if "openid" not in data:
        raise WeChatAuthError("WeChat response missing openid")
    return data
