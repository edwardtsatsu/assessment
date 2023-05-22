from fastapi import BackgroundTasks, Depends, Query, status, APIRouter
import uuid
from fastapi_pagination import Params, Page
from sqlalchemy.orm import Session
from app.logs.logs_conf import log_levels

from app.services.diagnosis import (
    all_diagnoses_codes,
    create_diagnosis,
    delete_diagnosis_by_id,
    get_diagnosis_by_id,
    process_file,
    update_diagnosis_by_id,
)


from .. import schemas
from ..database import get_db

router = APIRouter(prefix="/api/v1/diagnosis", tags=["Diagnosis"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.DiagnosisResponse
)
async def post_diagnosis(
    diagnosis: schemas.DiagnosisRequest, db: Session = Depends(get_db)
):
    return create_diagnosis(diagnosis, db)


@router.put("/{diagnosis_id}", response_model=schemas.DiagnosisUpdateResponse)
async def update_diagnosis(
    diagnosis_id: uuid.UUID,
    new_diagnosis: schemas.UpdateDiagnosisRequest,
    db: Session = Depends(get_db),
):
    return update_diagnosis_by_id(diagnosis_id, new_diagnosis, db)


@router.get(
    "/{diagnosis_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.DiagnosisResponse,
)
async def get_diagnosis(diagnosis_id: uuid.UUID, db: Session = Depends(get_db)):
    return get_diagnosis_by_id(diagnosis_id, db)


@router.delete("/{diagnosis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diagnosis(diagnosis_id: uuid.UUID, db: Session = Depends(get_db)):
    return delete_diagnosis_by_id(diagnosis_id, db)


@router.get("/", response_model=Page[schemas.DiagnosisResponse])
async def list_diagnosis_codes(
    params: Params = Depends(),
    db: Session = Depends(get_db),
):
    return all_diagnoses_codes(params, db)


@router.post("/upload_file", status_code=status.HTTP_200_OK)
async def upload_csv(
    file: schemas.UploadFileRequest, background_tasks: BackgroundTasks
):
    background_tasks.add_task(process_file, file)
    log_levels().info("File uploaded successfully, =====CALLING TASK SERVICE===")
    return {"detail": "File uploaded successfully and will be processed shortly."}
