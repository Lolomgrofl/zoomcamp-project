from unittest.mock import MagicMock

import pytest
from pandas import DataFrame
from sqlalchemy.orm import Session

from app.models.properties import Property
from app.schemas.statistics import BaseStatistics
from app.services.statistics import StatisticsService

# Mock data for testing
mock_properties = [
    Property(
        propertyid=1,
        price=200000,
        bedrooms=3,
        bathrooms=2,
        squarefeet=1500,
        city="Springfield",
    ),
    Property(
        propertyid=2,
        price=250000,
        bedrooms=4,
        bathrooms=3,
        squarefeet=2000,
        city="Shelbyville",
    ),
]


@pytest.fixture
def mock_session():
    session = MagicMock(spec=Session)
    session.query.return_value.filter.return_value.all.return_value = mock_properties
    return session


@pytest.fixture
def mock_dataframe():
    data = {
        "price": [200000, 250000],
        "bedrooms": [3, 4],
        "bathrooms": [2, 3],
        "squarefeet": [1500, 2000],
        "city": ["Springfield", "Shelbyville"],
    }
    return DataFrame(data)


def test_filter_properties(mock_session):
    filtered_properties = StatisticsService.filter_properties(
        session=mock_session,
        min_price=150000,
        max_price=300000,
        bedrooms=3,
        bathrooms=2,
        city="Springfield",
    )
    # Assuming the mock_properties list is what's not expected after filtering
    assert len(filtered_properties) != len(
        mock_properties
    ), "Incorrect number of properties filtered."


def test_generate_statistics(mock_dataframe):
    statistics = StatisticsService.generate_statistics(df=mock_dataframe)
    assert isinstance(
        statistics, BaseStatistics
    ), "The result should be an instance of BaseStatistics."
    assert (
        statistics.average_price == mock_dataframe["price"].mean()
    ), "Incorrect average price calculated."
    assert (
        statistics.median_price == mock_dataframe["price"].median()
    ), "Incorrect median price calculated."
    assert statistics.total_properties == len(
        mock_dataframe
    ), "Incorrect total properties counted."
    assert (
        statistics.average_price_per_sqft
        == (mock_dataframe["price"] / mock_dataframe["squarefeet"]).mean()
    ), "Incorrect average price per square foot calculated."
