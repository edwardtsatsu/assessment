from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import attributes
from fastapi import HTTPException, status
import base64
from app.logs.logs_conf import log_levels

from app import schemas
from app.models import models
from app.task import load_data_to_db
from app.utils import save_file_to_cloudinary


def create_diagnosis(diagnosis_request, db):
    # Check if diagnosis code already exists
    existing_diagnosis = (
        db.query(models.Diagnosis).filter_by(diag_code=diagnosis_request.code).first()
    )
    if existing_diagnosis:
        log_levels().info("=========SAME RECORD FOUND=========== ERROR NO")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Diagnosis code already exists",
        )

    # Create category
    category = models.Category(
        code=diagnosis_request.code, title=diagnosis_request.title
    )
    db.add(category)

    try:
        db.commit()
    except IntegrityError as e:
        log_levels().error(f"=========ROLLBACK EXCEPTION RECORD NOT SAVED {str(e)}==========")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Internal Server Error"
        )

    # Create diagnosis
    diagnosis = models.Diagnosis(
        category_id=category.id,
        diag_code=diagnosis_request.code,
        full_code=diagnosis_request.full_code,
        abb_desc=diagnosis_request.abb_desc,
        full_desc=diagnosis_request.full_desc,
    )
    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)

    return schemas.DiagnosisResponse(
        id=diagnosis.id,
        diag_code=diagnosis.diag_code,
        abb_desc=diagnosis.abb_desc,
        full_code=diagnosis.full_code,
        code=category.code,
        title=category.title,
        full_desc=diagnosis.full_desc,
        created_at=diagnosis.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
    )


def get_diagnosis_by_id(diagnosis_id, db):
    diagnosis = (
        db.query(models.Diagnosis)
        .join(models.Category)
        .options(joinedload(models.Diagnosis.category))
        .filter(models.Diagnosis.id == diagnosis_id)
        .first()
    )

    if not diagnosis:
        log_levels().info("========= RECORD NOT FOUND=========== ERROR NON++")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Diagnosis not found"
        )

    return schemas.DiagnosisResponse(
        id=diagnosis.id,
        diag_code=diagnosis.diag_code,
        abb_desc=diagnosis.abb_desc,
        full_code=diagnosis.full_code,
        code=diagnosis.category.code,
        title=diagnosis.category.title,
        full_desc=diagnosis.full_desc,
        created_at=diagnosis.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
    )


def delete_diagnosis_by_id(diagnosis_id, db):
    diagnosis = (
        db.query(models.Diagnosis)
        .join(models.Category)
        .options(joinedload(models.Diagnosis.category))
        .filter(models.Diagnosis.id == diagnosis_id)
        .first()
    )
    if not diagnosis:
        log_levels().info("========= RECORD NOT FOUND=========== ERROR NON++")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Diagnosis code not found"
        )

    db.query(models.Category).filter(models.Category.id == diagnosis_id).delete(
        synchronize_session=False
    )

    db.delete(diagnosis)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def update_diagnosis_by_id(diagnosis_id, new_diagnosis, db):
    diagnosis = (
        db.query(models.Diagnosis).filter(models.Diagnosis.id == diagnosis_id).first()
    )
    if not diagnosis:
        log_levels().info("========= RECORD NOT FOUND=========== ERROR NON++")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Diagnosis not found"
        )

    category = diagnosis.category

    for key, value in new_diagnosis.dict(exclude_unset=True).items():
        if value:
            setattr(diagnosis, key, value)
            setattr(category, key, value)

    db.commit()
    db.refresh(diagnosis)
    db.refresh(category)

    return {
        **attributes.instance_dict(diagnosis),
        "code": category.code,
        "title": category.title,
    }


def all_diagnoses_codes(offset, limit, db):
    diagnoses = db.query(models.Diagnosis).offset(offset).limit(limit).all()
    categories = (
        db.query(models.Category)
        .filter(models.Category.id.in_([d.category_id for d in diagnoses]))
        .all()
    )

    results = []
    for diagnosis, category in zip(diagnoses, categories):
        results.append(
            schemas.DiagnosisResponse(
                id=diagnosis.id,
                diag_code=diagnosis.diag_code,
                full_code=diagnosis.full_code,
                abb_desc=diagnosis.abb_desc,
                full_desc=diagnosis.full_desc,
                code=category.code,
                title=category.title,
                created_at=diagnosis.created_at,
            )
        )

    total_diagnoses = db.query(models.Diagnosis).count()

    return schemas.DiagnosesListResponse(
        metadata={
            "total_diagnoses": total_diagnoses,
            "offset": offset,
            "limit": limit,
            "next_offset": offset + limit if offset + limit < total_diagnoses else None,
            "prev_offset": offset - limit if offset - limit >= 0 else None,
        },
        data=results,
    )


def process_file(file: schemas.UploadFileRequest):
    try:
        decoded_data = base64.b64decode(file.file_content)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid base64 encoded file content",
        )

    # call save to cloudinary method yo upload the file
    log_levels().warning(
        "========= CLOUDINARY ERROR NOT IMPLEMENTED=========== ERROR NON--"
    )
    file_data = {"file": (f"{file.file_name}.csv", decoded_data)}
    save_file_to_cloudinary(file_data)

    # Convert bytes to string
    csv_data = decoded_data.decode("utf-8")

    # Call the Celery task to load the data into the database
    task = load_data_to_db.delay(
        csv_data=csv_data, file_name=file.file_name, email_add=file.recipient_email
    )

    return {"task_id": task.id, "status": task.status}
