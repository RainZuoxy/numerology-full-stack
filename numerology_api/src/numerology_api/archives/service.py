from datetime import date
from typing import Optional

from sqlmodel import Session, select

from numerology_api.archives.models import Archive, DailyPrediction

MAX_ARCHIVES_PER_USER = 5


def list_archives(session: Session, user_id: int) -> list[Archive]:
    stmt = select(Archive).where(Archive.user_id == user_id).order_by(Archive.created_at)
    return list(session.exec(stmt).all())


def get_archive(session: Session, user_id: int, archive_id: int) -> Optional[Archive]:
    stmt = select(Archive).where(
        Archive.archive_id == archive_id, Archive.user_id == user_id
    )
    return session.exec(stmt).first()


def get_primary_archive(session: Session, user_id: int) -> Optional[Archive]:
    stmt = select(Archive).where(
        Archive.user_id == user_id, Archive.is_primary == True  # noqa: E712
    )
    return session.exec(stmt).first()


def create_archive(
    session: Session, user_id: int, name: str, gender: str, dob_time: str
) -> Archive:
    count = len(list_archives(session, user_id))
    if count >= MAX_ARCHIVES_PER_USER:
        raise ValueError(f"每个账户最多创建 {MAX_ARCHIVES_PER_USER} 个归档")
    archive = Archive(
        user_id=user_id,
        name=name,
        gender=gender,
        dob_time=dob_time,
        is_primary=(count == 0),  # 第一个自动设为主档
    )
    session.add(archive)
    session.commit()
    session.refresh(archive)
    return archive


def delete_archive(session: Session, user_id: int, archive_id: int) -> bool:
    archive = get_archive(session, user_id, archive_id)
    if not archive:
        return False
    was_primary = archive.is_primary
    session.delete(archive)
    session.commit()
    # 如果删除的是主档且还有其它档案，选最早的一个作为主档
    if was_primary:
        remaining = list_archives(session, user_id)
        if remaining:
            remaining[0].is_primary = True
            session.add(remaining[0])
            session.commit()
    return True


def set_primary_archive(session: Session, user_id: int, archive_id: int) -> Optional[Archive]:
    target = get_archive(session, user_id, archive_id)
    if not target:
        return None
    all_items = list_archives(session, user_id)
    for a in all_items:
        a.is_primary = (a.archive_id == archive_id)
        session.add(a)
    session.commit()
    session.refresh(target)
    return target


def get_prediction_for(
    session: Session, user_id: int, on_date: date
) -> Optional[DailyPrediction]:
    stmt = select(DailyPrediction).where(
        DailyPrediction.user_id == user_id,
        DailyPrediction.predict_date == on_date,
    )
    return session.exec(stmt).first()


def save_prediction(
    session: Session,
    user_id: int,
    archive_id: int,
    on_date: date,
    score: int,
    payload_json: str,
) -> DailyPrediction:
    record = DailyPrediction(
        user_id=user_id,
        archive_id=archive_id,
        predict_date=on_date,
        score=score,
        payload_json=payload_json,
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return record
