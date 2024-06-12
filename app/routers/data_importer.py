import pandas as pd
from fastapi import APIRouter, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app.db import engine

router = APIRouter(tags=["data_importer"])


@router.post("/import")
async def import_data(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    try:
        # Read CSV file into DataFrame
        df = pd.read_csv(file.file)

        # Small data cleaning

        # Dropping the date datelisted because it has 400k missing values
        df.drop(columns=["datelisted"], inplace=True)

        # Dropping duplicates based on the propertyid because it is the primary key. There was 1 example
        df.drop_duplicates(subset="propertyid", keep="first", inplace=True)

        # Fill missing values with the mean
        df["price"] = df["price"].fillna(df["price"].mean())
        df["squarefeet"] = df["squarefeet"].fillna(df["squarefeet"].mean())
        df["bedrooms"] = df["bedrooms"].fillna(df["bedrooms"].mean())
        df["bathrooms"] = df["bathrooms"].fillna(df["bathrooms"].mean())

        df.to_sql(con=engine, name="properties", if_exists="append", index=False)
        return JSONResponse("Data imported successfully")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
