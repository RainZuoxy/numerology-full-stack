import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    """集中配置日志：ISO 时间戳 + logger 名 + 等级 + 消息。"""
    root = logging.getLogger()
    if root.handlers:  # 避免 reload 重复挂
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s.%(msecs)03d | %(levelname)-5s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    root.addHandler(handler)
    root.setLevel(level)

    # uvicorn / fastapi / httpx 也接到相同 handler
    for name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi", "httpx"):
        lg = logging.getLogger(name)
        lg.handlers = []
        lg.propagate = True
