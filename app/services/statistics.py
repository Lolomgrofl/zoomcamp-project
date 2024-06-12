from pandas import DataFrame
from sqlalchemy.orm import Session

from app.models.properties import Property
from app.schemas.statistics import BaseStatistics


class StatisticsService:
    @staticmethod
    def filter_properties(
        session: Session,
        min_price: float | None,
        max_price: float | None,
        bedrooms: int | None,
        bathrooms: int | None,
        city: str | None,
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

        return query.all()

    @staticmethod
    def generate_statistics(df: DataFrame) -> BaseStatistics:
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
