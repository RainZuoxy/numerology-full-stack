import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DBConfig:
    """
    数据库配置。默认使用项目根目录下的 SQLite 文件，便于本地测试。
    切换数据库只需修改 NUMEROLOGY_DB_URL，例如：
      - sqlite:///./numerology.db
      - postgresql+psycopg://user:pass@host:5432/dbname
      - mysql+pymysql://user:pass@host:3306/dbname
    """
    url: str
    echo: bool


def _load() -> DBConfig:
    return DBConfig(
        url=os.getenv("NUMEROLOGY_DB_URL", "sqlite:///./numerology.db"),
        echo=os.getenv("NUMEROLOGY_DB_ECHO", "0") == "1",
    )


db_config = _load()
