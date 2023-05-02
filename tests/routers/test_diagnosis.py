import random
import string
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


def test_post_diagnosis(client):
    # Create a random diagnosis code
    code = "".join(random.choices(string.ascii_uppercase, k=4))
    diagnosis = schemas.DiagnosisRequest(
        diag_code=code,
        abb_desc="Comma-ind anal ret",
        full_code="A01234",
        code=code,
        title="Malignant neoplasm of anus and anal canal",
        full_desc="Comma-induced anal retention",
    )

    # Send a POST request to create the diagnosis
    response = client.post(url="/api/v1/diagnosis/", json=diagnosis.dict())

    # Assert that the response status code is 201 CREATED
    assert response.status_code == status.HTTP_201_CREATED


@pytest.fixture
def test_update_diagnosis():
    code = "".join(random.choices(string.ascii_uppercase, k=4))

    id = test_create_diagnosis.id
    # Define the update payload
    update_payload = {"code": code, "full_desc": "The journey of what exist"}

    # Send a PUT request to update the diagnosis
    response = client.put(
        url=f"/api/v1/diagnosis/{id}", json=update_payload
    )

    # Assert that the response status code is 200 OK
    assert response.status_code == status.HTTP_200_OK

@pytest.fixture
def test_get_diagnosis(client):
    id = test_create_diagnosis.id
    response = client.get(url=f"/api/v1/diagnosis/{id}")
    assert response.status_code == 200


@pytest.fixture
def test_delete_diagnosis():
    id = test_create_diagnosis.id

    response = client.delete(
        url=f"/api/v1/diagnosis/{id}"
    )

    # Assert that the response status code is 200 OK
    assert response.status_code == status.HTTP_204_NO_CONTENT
