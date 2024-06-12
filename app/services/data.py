import pandas as pd
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from loguru import logger

from app.db import engine


class DataService:
    @staticmethod
    def prepare_data(file):
        try:
            # Read CSV file into DataFrame
            df = pd.read_csv(file)
            logger.info(
                "Data read successfully from file...Starting with data cleaning..."
            )

            # Small data cleaning
            # NOTE: In the real world, we would need to do more data cleaning and try to understand the data better.
            # Right now I'll do the most basics steps to make the data importable. On the ETL part, we would need to do more data transformation, feature extraction/engineering etc. That's totally out of the scope of this project.

            # Dropping the date datelisted because it has 400k missing values
            df.drop(columns=["datelisted"], inplace=True)

            # Dropping duplicates based on the propertyid because it is the primary key. There was 1 example found for sure, but there might be more.
            df.drop_duplicates(subset="propertyid", keep="first", inplace=True)

            # Fill missing values with the mean
            df["price"] = df["price"].fillna(df["price"].mean())
            df["squarefeet"] = df["squarefeet"].fillna(df["squarefeet"].mean())
            df["bedrooms"] = df["bedrooms"].fillna(df["bedrooms"].mean())
            df["bathrooms"] = df["bathrooms"].fillna(df["bathrooms"].mean())
            logger.info("Data cleaning finished...Starting with data import...")

            df.to_sql(con=engine, name="properties", if_exists="append", index=False)
            logger.info("Data import finished!!!")
            return JSONResponse("Data imported successfully")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
