from datetime import datetime
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
    create_diagnosis,
    get_diagnosis_by_id,
    delete_diagnosis_by_id,
)


@pytest.fixture
def mock_db():
    return SessionLocal()


def test_create_diagnosis(mock_db):
    code = "".join(random.choices(string.ascii_uppercase, k=4))
    diagnosis = schemas.DiagnosisRequest(
        diag_code=code,
        abb_desc="Comma-ind anal ret",
        full_code="A01234",
        code=code,
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
        diag_code=code,
        abb_desc="Comma-ind anal ret",
        full_code="A01234",
        code=code,
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
        diag_code=response.diag_code,
        abb_desc=response.abb_desc,
        full_code=response.full_code,
        code=response.code,
        title=response.title,
        full_desc=response.full_desc,
        created_at=response.created_at,
    )


@pytest.fixture
def test_delete_diagnosis_by_id(mock_db):
    id = test_create_diagnosis.id

    # Delete the diagnosis by ID
    response = delete_diagnosis_by_id(id, mock_db)

    assert response.status_code == status.HTTP_204_NO_CONTENT
