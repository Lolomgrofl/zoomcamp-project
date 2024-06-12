from fastapi import APIRouter

from app.routers import data_importer, statistics
from app.settings import settings

api_router = APIRouter(prefix=settings.API_V1_STR)


api_router.include_router(data_importer.router)
api_router.include_router(statistics.router)
