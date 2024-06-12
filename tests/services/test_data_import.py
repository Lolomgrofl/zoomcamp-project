from unittest.mock import patch

import pandas as pd
import pytest
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app.db import engine
from app.services.data import DataService

# Sample data for testing
sample_data = {
    "propertyid": [1, 2, 2, 3],  # Duplicate ID to test dropping duplicates
    "datelisted": [
        "2021-01-01",
        "2021-01-02",
        "2021-01-02",
        "2021-01-03",
    ],  # Column to be dropped
    "price": [100000, 200000, 200000, None],  # Contains None to test filling with mean
    "squarefeet": [1000, None, 2000, 1500],  # Contains None to test filling with mean
    "bedrooms": [3, 4, 4, None],  # Contains None to test filling with mean
    "bathrooms": [2, None, 3, 2],  # Contains None to test filling with mean
}

expected_data = {
    "propertyid": [1, 2, 3],
    "price": [100000, 200000, 150000],  # Mean of 100000, 200000, and 200000
    "squarefeet": [1000, 2000, 1500],
    "bedrooms": [3, 4, 3.5],  # Mean of 3, 4, and 4
    "bathrooms": [2, 3, 2],
}


@pytest.fixture
def mock_file(tmpdir):
    file = tmpdir.join("test.csv")
    file.write_text(
        "propertyid,datelisted,price,squarefeet,bedrooms,bathrooms\n"
        "1,2021-01-01,100000,1000,3,2\n"
        "2,2021-01-02,200000,,4,\n"
        "2,2021-01-02,200000,2000,4,3\n"
        "3,2021-01-03,,1500,,2\n",
        encoding="utf-8",
    )
    return str(file)


@patch("pandas.read_csv")
@patch("pandas.DataFrame.to_sql")
def test_prepare_data_success(mock_to_sql, mock_read_csv, mock_file):
    mock_read_csv.return_value = pd.DataFrame(sample_data)
    mock_to_sql.return_value = None  # Simulate successful SQL import

    response = DataService.prepare_data(mock_file)

    # Verify the response
    assert isinstance(response, JSONResponse), "Response should be a JSONResponse."
    assert (
        response.body.decode("utf-8") == '"Data imported successfully"'
    ), "Response message mismatch."

    mock_to_sql.assert_called_once_with(
        con=engine, name="properties", if_exists="append", index=False
    )


@patch("pandas.read_csv")
def test_prepare_data_failure(mock_read_csv, mock_file):
    mock_read_csv.side_effect = Exception("Error reading CSV file")

    with pytest.raises(HTTPException) as exc_info:
        DataService.prepare_data(mock_file)

    assert (
        exc_info.value.status_code == 400
    ), "Should raise HTTPException with status code 400."
    assert "Error reading CSV file" in str(
        exc_info.value.detail
    ), "Exception detail should contain the error message."
