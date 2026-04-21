from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

from numerology_api.db.config import db_config

_is_sqlite = db_config.url.startswith("sqlite")
_connect_args: dict = {"check_same_thread": False} if _is_sqlite else {}

engine = create_engine(
    db_config.url,
    echo=db_config.echo,
    connect_args=_connect_args,
)


def init_db() -> None:
    """确保所有 SQLModel 表已注册到 metadata，然后在数据库中创建缺失的表。"""
    # 注册模型（import 即注册到 SQLModel.metadata）
    from numerology_api.archives import models as _arch_models  # noqa: F401
    from numerology_api.auth import models as _auth_models  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
