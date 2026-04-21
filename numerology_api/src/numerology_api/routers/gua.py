from fastapi import APIRouter, Depends, HTTPException
from numerology_cli.commands.gua import QueryTrigramCommand

from numerology_api.auth.dependencies import get_current_user
from numerology_api.auth.models import User
from numerology_api.models.gua import GuaRequest, GuaResponse

router = APIRouter(prefix="/gua", tags=["Gua 卦象"])


@router.post(
    "",
    response_model=GuaResponse,
    summary="查询卦象",
    description="根据六爻阴阳序列查询六十四卦（需登录）",
)
def query_gua(
    request: GuaRequest,
    _user: User = Depends(get_current_user),
) -> GuaResponse:
    try:
        up_trigram, down_trigram = QueryTrigramCommand.parse_trigram_series(
            trigram_series=request.trigram_series
        )
        result = QueryTrigramCommand.query_trigram(
            up_trigram=up_trigram, down_trigram=down_trigram
        )
        return GuaResponse(name=result.value.name, value=result.value)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
