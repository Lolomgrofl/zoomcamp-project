from fastapi import APIRouter, File, UploadFile
from fastapi.exceptions import HTTPException

from app.services.data import DataService

router = APIRouter(tags=["data_importer"])


@router.post("/import")
def import_data(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    return DataService.prepare_data(file.file)
