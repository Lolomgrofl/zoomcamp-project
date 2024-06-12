import pandas as pd
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from app.db import SessionDep, engine
from app.models.properties import Property
from app.schemas.statistics import BaseStatistics, PropertyModel

router = APIRouter(tags=["properties"], prefix="/properties")


@router.get("")
async def filter_properties(
    session: SessionDep,
    min_price: float | None = Query(None, description="Minimum price"),
    max_price: float | None = Query(None, description="Maximum price"),
    bedrooms: int | None = Query(None, description="Number of bedrooms"),
    bathrooms: int | None = Query(None, description="Number of bathrooms"),
    city: str | None = Query(None, description="City"),
):
    query = session.query(Property)

    if min_price:
        query = query.filter(Property.price >= min_price)

    if max_price:
        query = query.filter(Property.price <= max_price)

    if bedrooms:
        query = query.filter(Property.bedrooms == bedrooms)

    if bathrooms:
        query = query.filter(Property.bathrooms == bathrooms)

    if city:
        query = query.filter(Property.city == city)

    results = query.all()

    if not results:
        JSONResponse(
            "No properties found for the given filters",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return [PropertyModel.model_validate(property) for property in query.all()]


@router.get("/statistics")
async def process_data() -> BaseStatistics:
    df = pd.read_sql("select * from properties", engine)

    # Calculating statistics
    average_price = df["price"].mean()
    median_price = df["price"].median()
    average_price_per_sqft = (df["price"] / df["squarefeet"]).mean()
    total_properties = len(df)

    return BaseStatistics(
        average_price=average_price,
        median_price=median_price,
        total_properties=total_properties,
        average_price_per_sqft=average_price_per_sqft,
    )
