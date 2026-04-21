from numerology_api.routers.archives import router as archives_router
from numerology_api.routers.auth import router as auth_router
from numerology_api.routers.bazi import router as bazi_router
from numerology_api.routers.fortune import router as fortune_router
from numerology_api.routers.gua import router as gua_router

__all__ = [
    "archives_router",
    "auth_router",
    "bazi_router",
    "fortune_router",
    "gua_router",
]
