from datetime import datetime, timezone
import random
import string
from fastapi import status
from unittest import mock
import uuid
import pytest

from app import schemas
from app.models import models
from app.database import SessionLocal
from app.services.diagnosis import (
    # all_diagnoses_codes,
    create_diagnosis,
    get_diagnosis_by_id,
    # delete_diagnosis_by_id,
    # get_diagnosis_by_id,
    # update_diagnosis_by_id,

)


@pytest.fixture
def mock_db():
    return SessionLocal()


def test_create_diagnosis(mock_db):
    code = "".join(random.choices(string.ascii_uppercase, k=4))
    diagnosis = schemas.DiagnosisRequest(
        diagnosis_code=code,
        abbreviated_desc="Comma-ind anal ret",
        full_code="A01234",
        category_code="A01",
        title="Malignant neoplasm of anus and anal canal",
        full_desc="Comma-induced anal retention",
    )

    uuid_val = uuid.uuid4()

    with mock.patch("uuid.uuid4", return_value=uuid_val):
        with mock.patch("datetime.datetime") as mock_datetime:
            mock_now = datetime(2023, 4, 30, 21, 18, 14, 713652)
            mock_datetime.utcnow.return_value = mock_now

            response = create_diagnosis(diagnosis, mock_db)

    expected_created_at = response.created_at
    assert response == schemas.DiagnosisResponse(
        id=response.id,
        diagnosis_code=code,
        abbreviated_desc="Comma-ind anal ret",
        full_code="A01234",
        category_code="A01",
        title="Malignant neoplasm of anus and anal canal",
        full_desc="Comma-induced anal retention",
        created_at=expected_created_at,
    )


@pytest.fixture
def test_get_diagnosis_by_id():
    id = test_create_diagnosis.id
    response = get_diagnosis_by_id(id)

    assert response == schemas.DiagnosisResponse(
        id=response.id,
        diagnosis_code=response.diag_code,
        abbreviated_desc=response.abb_desc,
        full_code=response.full_code,
        category_code=response.code,
        title=response.title,
        full_desc=response.full_desc,
        created_at=response.created_at,
    )


# def test_delete_diagnosis_by_id(mock_db):
#     # Create a diagnosis code to delete
#     code = "".join(random.choices(string.ascii_uppercase, k=4))
#     diagnosis_code = models.DiagnosisCode(
#         name="test",
#         code=code,
#         created_at=datetime.utcnow(),
#     )
#     mock_db.add(diagnosis_code)
#     mock_db.commit()

#     # Delete the diagnosis by ID
#     response = delete_diagnosis_by_id(diagnosis_code.id, mock_db)

#     assert response.status_code == status.HTTP_204_NO_CONTENT

#     # Make sure the diagnosis was deleted
#     assert (
#         mock_db.query(models.DiagnosisCode)
#         .filter(models.DiagnosisCode.id == diagnosis_code.id)
#         .first()
#     ) is None


# @mock.patch("app.services.diagnosis.get_diagnosis_code")
# def test_update_diagnosis_by_id(mock_get_diagnosis_code, mock_db):
#     # Create a diagnosis code to update
#     code = "".join(random.choices(string.ascii_uppercase, k=4))
#     diagnosis_code = models.DiagnosisCode(
#         name="test",
#         code=code,
#     )
#     mock_db.add(diagnosis_code)
#     mock_db.commit()

#     # Define new values to update the diagnosis code with
#     new_diagnosis = schemas.DiagnosisRequest(
#         name="updated namer",
#         code=code,
#         version="10",
#         description="Updated description",
#     )

#     # Mock the get_diagnosis_code method to return the diagnosis_code object
#     mock_get_diagnosis_code.return_value = diagnosis_code

#     # Call the update function and get the response
#     response = update_diagnosis_by_id(diagnosis_code.id, new_diagnosis, mock_db)

#     # Check that the response matches the expected values
#     assert response.id == diagnosis_code.id
#     assert response.code == diagnosis_code.code
#     assert response.name == new_diagnosis.name
#     assert response.version == new_diagnosis.version
#     assert response.description == new_diagnosis.description
#     assert response.updated_at == diagnosis_code.updated_at


# def test_all_diagnoses_codes():
#     # Create test data if needed
#     db = SessionLocal()
#     if db.query(models.DiagnosisCode).count() == 0:
#         code = "".join(random.choices(string.ascii_uppercase, k=4))
#         diagnosis_code_one = models.DiagnosisCode(
#             name="Test Diagnosis Code one", code=code
#         )
#         db.add(diagnosis_code_one)
#         db.commit()

#         diagnosis_version_1 = models.DiagnosisVersion(
#             code_id=diagnosis_code_one.id, version="1", description="Description one"
#         )
#         db.add(diagnosis_version_1)
#         db.commit()

#     # Call the function being tested
#     response = all_diagnoses_codes(1, db)

#     # Assertions
#     expected_length = db.query(models.DiagnosisCode).count()
#     assert len(response) == min(expected_length, 20)
