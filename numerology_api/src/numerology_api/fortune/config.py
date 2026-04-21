import os
from dataclasses import dataclass


@dataclass(frozen=True)
class FortuneConfig:
    api_key: str
    base_url: str
    model: str
    timeout: float


def _load() -> FortuneConfig:
    return FortuneConfig(
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/"),
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        timeout=float(os.getenv("DEEPSEEK_TIMEOUT", "60")),
    )


fortune_config = _load()
