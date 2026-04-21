from fastapi import APIRouter, Depends, HTTPException
from numerology_cli.commands.ba_zi import GenerateBaZiChartCommand

from numerology_api.auth.dependencies import get_current_user
from numerology_api.auth.models import User
from numerology_api.models.bazi import BaZiRequest, BaZiResponse

router = APIRouter(prefix="/bazi", tags=["BaZi 八字"])


@router.post(
    "",
    response_model=BaZiResponse,
    response_model_by_alias=False,
    summary="生成八字命盘",
    description="根据阳历生辰八字，生成八字、十神、大运等信息（需登录）",
)
def generate_bazi(
    request: BaZiRequest,
    _user: User = Depends(get_current_user),
) -> BaZiResponse:
    command = GenerateBaZiChartCommand(name=GenerateBaZiChartCommand.__name__)
    try:
        results = command.get_bazi_chart(**request.model_dump())
        return BaZiResponse.model_validate(results)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
