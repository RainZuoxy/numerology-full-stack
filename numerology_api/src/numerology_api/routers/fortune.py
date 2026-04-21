from fastapi import APIRouter, Depends, HTTPException

from numerology_api.auth.dependencies import get_current_user
from numerology_api.auth.models import User
from numerology_api.fortune import DeepSeekError, chat_json
from numerology_api.fortune.prompts import SYSTEM_PROMPT, build_user_prompt
from numerology_api.models.fortune import FortuneRequest, FortuneResponse

router = APIRouter(prefix="/fortune", tags=["Fortune 运势详解"])


@router.post(
    "/analyze",
    response_model=FortuneResponse,
    summary="基于命盘生成六维运势详解",
    description="调用 DeepSeek，根据八字/十神/大运输出姻缘、财运、事业、学业、健康、子嗣六个维度的推断",
)
async def analyze_fortune(
    request: FortuneRequest,
    _user: User = Depends(get_current_user),
) -> FortuneResponse:
    user_prompt = build_user_prompt(request.bazi, request.question)
    try:
        data = await chat_json(SYSTEM_PROMPT, user_prompt)
    except DeepSeekError as e:
        raise HTTPException(status_code=502, detail=str(e))

    try:
        return FortuneResponse.model_validate(data)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"DeepSeek 返回结构不符合预期: {e}")
