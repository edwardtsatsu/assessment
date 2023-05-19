import random
import string
import pytest
from app.models import models
from app.database import SessionLocal

from app.models import models


@pytest.fixture(scope="function")
def db():
    """Create a new database session for each test."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_diagnosis_creation(db):
    # Create a random diagnosis code
    code = "".join(random.choices(string.ascii_uppercase, k=4))
    category = models.Category(title="Test Diagnosis Code", code=code)
    db.add(category)
    db.commit()

    diagnosis = models.Diagnosis(
        category_id=category.id,
        diag_code=code,
        full_code="1324",
        abb_desc="great point",
        full_desc="I will be okay",
    )

    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)
    assert diagnosis.id is not None
    assert diagnosis.full_code == "1324"
    assert diagnosis.full_desc == "I will be okay"


def test_category_creation(db):
    # Create a random diagnosis code
    code = "".join(random.choices(string.ascii_uppercase, k=4))
    category = models.Category(title="Test Diagnosis Code", code=code)
    db.add(category)
    db.commit()

    db.refresh(category)

    assert category.id is not None
    assert category.title == "Test Diagnosis Code"
    assert category.code == code


def test_file_upload_creation(db):
    file_upload = models.FileUpload(
        email_add="test@email.com", file_name="test.csv", file_type="csv"
    )
    db.add(file_upload)
    db.commit()

    db.refresh(file_upload)

    assert file_upload.id is not None
    assert file_upload.email_add == "test@email.com"
    assert file_upload.file_name == "test.csv"
