from fastapi import APIRouter

from app.settings import settings

api_router = APIRouter(prefix=settings.API_V1_STR)
