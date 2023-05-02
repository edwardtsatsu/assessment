import random
import string
import uuid
from fastapi import status
from fastapi.testclient import TestClient
import pytest

from app import schemas
from app.database import SessionLocal
from app.models import models
from app.main import app
from tests.services.test_diagnosis import test_create_diagnosis


@pytest.fixture
def mock_db():
    return SessionLocal()


@pytest.fixture
def client():
    return TestClient(app)


def test_post_diagnosis(client, mock_db):
    # Create a random diagnosis code
    code = "".join(random.choices(string.ascii_uppercase, k=4))
    diagnosis = schemas.DiagnosisRequest(
        diagnosis_code=code,
        abbreviated_desc="Comma-ind anal ret",
        full_code="A01234",
        category_code="A01",
        title="Malignant neoplasm of anus and anal canal",
        full_desc="Comma-induced anal retention",
    )

    # Send a POST request to create the diagnosis
    response = client.post(url="/api/v1/diagnosis/", json=diagnosis.dict())

    # Assert that the response status code is 201 CREATED
    assert response.status_code == status.HTTP_201_CREATED

    # Convert the response to a Pydantic model object
    response_model = schemas.DiagnosisResponse.parse_obj(response.json())

    # Assert that the response body is of type schemas.DiagnosisResponse
    assert isinstance(response_model, schemas.DiagnosisResponse)

    # Assert that the response body has the correct values
    assert response_model.full_code == diagnosis.full_code
    assert response_model.full_desc == diagnosis.full_desc

    # Check that the diagnosis has been created in the database
    created_diagnosis = (
        mock_db.query(models.Diagnosis).filter_by(diag_code=code).first()
    )
    assert created_diagnosis is not None
    assert created_diagnosis.full_desc == diagnosis.full_desc


def test_update_diagnosis(client, mock_db):
    code = "".join(random.choices(string.ascii_uppercase, k=4))
    # Create a diagnosis code in the database to update
    diagnosis_code = models.DiagnosisCode(code=code, name="Test Diagnosis")
    mock_db.add(diagnosis_code)
    mock_db.commit()

    # Create a diagnosis version for the code
    diagnosis_version = models.DiagnosisVersion(
        code_id=diagnosis_code.id, version="1.0", description="Test description"
    )
    mock_db.add(diagnosis_version)
    mock_db.commit()

    # Define the update payload
    update_payload = {"code": code, "description": "The journey of what exist"}

    # Send a PUT request to update the diagnosis
    response = client.put(
        url=f"/api/v1/diagnosis/{diagnosis_code.id}", json=update_payload
    )

    # Assert that the response status code is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Convert the response to a Pydantic model object
    response_model = schemas.DiagnosisUpdateResponse.parse_obj(response.json())

    # Assert that the response body is of type schemas.DiagnosisUpdateResponse
    assert isinstance(response_model, schemas.DiagnosisUpdateResponse)

    # Assert that the response body has the correct values
    assert response_model.id == diagnosis_code.id
    assert response_model.code == update_payload["code"]
    assert response_model.description == update_payload["description"]
    assert response_model.name == diagnosis_code.name


def test_get_diagnosis_nonexistent_id(client):
    fake_id = uuid.uuid4()
    response = client.get(url=f"/api/v1/diagnosis/{fake_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Diagnosis not found"}


@pytest.fixture
def test_get_diagnosis(client):
    id = test_create_diagnosis.id
    response = client.get(url=f"/api/v1/diagnosis/{id}")
    assert response.status_code == 200
