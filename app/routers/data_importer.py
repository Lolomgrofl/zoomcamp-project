from fastapi import APIRouter, File, UploadFile, status
from fastapi.exceptions import HTTPException

from app.services.data import DataService

router = APIRouter(tags=["data_importer"])


@router.post("/import", summary="Import data from a static/data.csv file")
def import_data(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File must be a CSV"
        )
    return DataService.prepare_data(file.file)
