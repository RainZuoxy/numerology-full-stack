import json
import logging
from datetime import date, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from numerology.core.ganzhi_calendar import GanZhiCalendar
from numerology_cli.commands.ba_zi import GenerateBaZiChartCommand
from sqlmodel import Session

from numerology_api.archives import service as archive_service
from numerology_api.archives.models import Archive, DailyPrediction
from numerology_api.auth.dependencies import get_current_user
from numerology_api.auth.models import User
from numerology_api.db.engine import get_session
from numerology_api.fortune import DeepSeekError, chat_json
from numerology_api.fortune.daily_prompts import DAILY_SYSTEM_PROMPT, build_daily_user_prompt
from numerology_api.models.archive import (
    ArchiveCreateRequest,
    ArchiveItem,
    ArchiveListResponse,
    DailyPredictionPayload,
    DailyPredictionResponse,
)

log = logging.getLogger("numerology_api.archives")
router = APIRouter(prefix="/archives", tags=["Archive 归档与预测"])


def _to_item(a: Archive) -> ArchiveItem:
    return ArchiveItem(
        archive_id=a.archive_id or 0,
        name=a.name,
        gender=a.gender,  # type: ignore[arg-type]
        dob_time=a.dob_time,
        is_primary=a.is_primary,
        created_at=a.created_at,
    )


def _record_to_response(record: DailyPrediction, archive: Archive) -> Optional[DailyPredictionResponse]:
    """把数据库记录转成响应；若是旧版 schema 则返回 None，由调用方决定是否清理。"""
    try:
        data = json.loads(record.payload_json)
        payload = DailyPredictionPayload.model_validate(data.get("payload", data))
    except Exception as e:
        log.warning(
            f"预测记录 id={record.prediction_id} schema 不兼容，将按'无记录'处理: {e}"
        )
        return None
    return DailyPredictionResponse(
        predict_date=record.predict_date,
        archive_id=record.archive_id,
        archive_name=archive.name,
        day_pillar=data.get("day_pillar"),
        payload=payload,
        created_at=record.created_at,
    )


@router.get("", response_model=ArchiveListResponse, summary="列出当前用户归档")
def list_archives(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> ArchiveListResponse:
    items = archive_service.list_archives(session, user.user_id)  # type: ignore[arg-type]
    return ArchiveListResponse(
        items=[_to_item(a) for a in items],
        max_archives=archive_service.MAX_ARCHIVES_PER_USER,
    )


@router.post("", response_model=ArchiveItem, summary="创建归档（≤5）")
def create_archive(
    req: ArchiveCreateRequest,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> ArchiveItem:
    try:
        archive = archive_service.create_archive(
            session, user.user_id, req.name, req.gender, req.dob_time  # type: ignore[arg-type]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return _to_item(archive)


@router.delete("/{archive_id}", summary="删除归档")
def delete_archive(
    archive_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict:
    ok = archive_service.delete_archive(session, user.user_id, archive_id)  # type: ignore[arg-type]
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="归档不存在")
    return {"ok": True}


@router.post("/{archive_id}/primary", response_model=ArchiveItem, summary="设为主档")
def set_primary(
    archive_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> ArchiveItem:
    archive = archive_service.set_primary_archive(session, user.user_id, archive_id)  # type: ignore[arg-type]
    if not archive:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="归档不存在")
    return _to_item(archive)


@router.get(
    "/predictions/today",
    response_model=DailyPredictionResponse | None,
    summary="获取今日锦囊（若存在）",
)
def get_today_prediction(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    record = archive_service.get_prediction_for(session, user.user_id, date.today())  # type: ignore[arg-type]
    if not record:
        log.info(f"GET today: user={user.user_id} 尚无今日记录")
        return None
    archive = archive_service.get_archive(session, user.user_id, record.archive_id)  # type: ignore[arg-type]
    if not archive:
        log.warning(f"GET today: user={user.user_id} 记录指向的归档已被删除，删除陈旧预测")
        session.delete(record)
        session.commit()
        return None
    resp = _record_to_response(record, archive)
    if resp is None:
        # 旧 schema：删掉让用户可重新生成
        log.info(f"GET today: 删除旧 schema 的陈旧预测 id={record.prediction_id}")
        session.delete(record)
        session.commit()
        return None
    return resp


@router.post(
    "/predictions/today",
    response_model=DailyPredictionResponse,
    summary="生成今日预测（每账户每日一次，基于主档）",
)
async def create_today_prediction(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DailyPredictionResponse:
    today = date.today()
    log.info(f"POST today: user={user.user_id} 开始拆锦囊")
    existing = archive_service.get_prediction_for(session, user.user_id, today)  # type: ignore[arg-type]
    if existing:
        # 若旧 schema 不兼容 → 删除允许重新生成；否则 409
        try:
            json_data = json.loads(existing.payload_json)
            DailyPredictionPayload.model_validate(json_data.get("payload", json_data))
            log.info(f"POST today: user={user.user_id} 今日已有有效锦囊 → 409")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="今日锦囊已拆启，请明日再来"
            )
        except HTTPException:
            raise
        except Exception as e:
            log.warning(f"POST today: 清除旧 schema 记录 id={existing.prediction_id}: {e}")
            session.delete(existing)
            session.commit()

    primary = archive_service.get_primary_archive(session, user.user_id)  # type: ignore[arg-type]
    if not primary:
        log.info(f"POST today: user={user.user_id} 未设主档 → 400")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="尚未设置主档")
    log.info(f"POST today: user={user.user_id} 使用主档 {primary.name} ({primary.dob_time})")

    # 计算主档八字
    try:
        command = GenerateBaZiChartCommand(name=GenerateBaZiChartCommand.__name__)
        bazi_raw = command.get_bazi_chart(
            name=primary.name,
            dob_time=primary.dob_time,
            gender=primary.gender,
            dayun_number=7,
        )
        # 计算今日四柱（以 00:00 代表当日）
        today_str = today.strftime("%Y-%m-%d") + " 00:00:00"
        today_raw = GanZhiCalendar(dob=today_str)
        day_pillar = today_raw.model_dump(mode='json')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"命盘计算失败: {e}")

    owner_bazi = {
        "name": primary.name,
        "gender": primary.gender,
        "dob_time": primary.dob_time,
        "ba_zi": bazi_raw.get("generate_ba_zi").model_dump(mode='json'),
        "shi_shen": bazi_raw.get("generate_shi_shen").model_dump(mode='json'),
        "day_master": bazi_raw.get("get_day_master").model_dump(mode='json'),
    }
    today_bazi = {
        "date": today.isoformat(),
        "ba_zi": day_pillar
    }

    try:
        data = await chat_json(
            DAILY_SYSTEM_PROMPT,
            build_daily_user_prompt(owner_bazi, today_bazi, day_pillar, today.isoformat()),
        )
    except DeepSeekError as e:
        log.error(f"POST today: DeepSeek 失败 → 502: {e}")
        raise HTTPException(status_code=502, detail=str(e))

    try:
        payload = DailyPredictionPayload.model_validate(data)
    except Exception as e:
        log.error(f"POST today: AI 返回结构不符合预期 → 502: {e} | data={data}")
        raise HTTPException(status_code=502, detail=f"AI 返回结构不符合预期: {e}")
    log.info(f"POST today: user={user.user_id} 锦囊生成成功 sign={payload.sign} score={payload.score}")

    record = archive_service.save_prediction(
        session,
        user_id=user.user_id,  # type: ignore[arg-type]
        archive_id=primary.archive_id,  # type: ignore[arg-type]
        on_date=today,
        score=payload.score,
        payload_json=json.dumps(
            {"payload": payload.model_dump(), "day_pillar": day_pillar},
            ensure_ascii=False,
        ),
    )
    _ = datetime  # silence unused
    return _record_to_response(record, primary)
