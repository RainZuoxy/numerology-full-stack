import logging
import os
import time
import uuid
from contextlib import asynccontextmanager

from dotenv import load_dotenv

# 在其它模块加载前先读 .env（fortune_config/db_config 均在 import 期读取环境变量）
load_dotenv()

from numerology_api.logging_setup import setup_logging

setup_logging(os.getenv("NUMEROLOGY_LOG_LEVEL", "INFO"))

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

log = logging.getLogger("numerology_api.http")

from numerology import __version__ as lib_version
from numerology_api import __version__ as api_version
from numerology_api.db import init_db, engine
from numerology_api.models import HealthResponse
from numerology_api.routers import (
    archives_router,
    auth_router,
    bazi_router,
    fortune_router,
    gua_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    engine.dispose()


app = FastAPI(
    title="Numerology API",
    description="中国传统命理学计算 API：八字、十神、大运、六十四卦（含鉴权，兼容微信小程序）",
    version=api_version,
    lifespan=lifespan
)

_cors_origins = os.getenv("NUMEROLOGY_CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    rid = uuid.uuid4().hex[:8]
    method = request.method
    path = request.url.path
    client = request.client.host if request.client else "-"
    log.info(f"▶ [{rid}] {method} {path} from {client}")
    t0 = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        dt_ms = (time.perf_counter() - t0) * 1000
        log.exception(f"✗ [{rid}] {method} {path} raised after {dt_ms:.1f}ms")
        raise
    dt_ms = (time.perf_counter() - t0) * 1000
    log.info(f"◀ [{rid}] {method} {path} → {response.status_code} in {dt_ms:.1f}ms")
    return response

app.include_router(auth_router, prefix="/api/v1")
app.include_router(bazi_router, prefix="/api/v1")
app.include_router(gua_router, prefix="/api/v1")
app.include_router(fortune_router, prefix="/api/v1")
app.include_router(archives_router, prefix="/api/v1")


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", lib_version=lib_version, api_version=api_version)


def start():
    uvicorn.run("numerology_api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
