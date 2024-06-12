import pandas as pd
from fastapi import APIRouter, Query, status
from fastapi.exceptions import HTTPException

from app.db import SessionDep, engine
from app.schemas.statistics import BaseStatistics, PropertyModel
from app.services.statistics import StatisticsService

router = APIRouter(tags=["properties"], prefix="/properties")


@router.get("", summary="Filter properties by price, bedrooms, bathrooms, and city")
def filter_properties(
    session: SessionDep,
    min_price: float | None = Query(None, description="Minimum price"),
    max_price: float | None = Query(None, description="Maximum price"),
    bedrooms: int | None = Query(None, description="Number of bedrooms"),
    bathrooms: int | None = Query(None, description="Number of bathrooms"),
    city: str | None = Query(None, description="City"),
) -> list[PropertyModel]:
    results = StatisticsService.filter_properties(
        session, min_price, max_price, bedrooms, bathrooms, city
    )

    if not results:
        raise HTTPException(
            detail="No properties found for the given filters",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return [PropertyModel.model_validate(property) for property in results]


@router.get("/statistics", summary="Get statistics about the properties")
def generate_statistics() -> BaseStatistics:
    df = pd.read_sql("select * from properties", engine)
    return StatisticsService.generate_statistics(df)
