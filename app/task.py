import csv
from celery import Celery
from app.database import SessionLocal
from app.models import models
from contextlib import contextmanager

from app.logs.logs_conf import log_levels
from app.config import settings
from app.services.email import send_email


celery = Celery(
    "__name__",
    broker=settings.broker,
    backend=settings.broker,
)


# A context manager to create a SQLAlchemy session
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    finally:
        db.close()


@celery.task
def load_data_to_db(csv_data, file_name, email_add):
    try:
        with get_db() as db:
            csv_reader = csv.reader(csv_data.splitlines())
            headers = next(csv_reader)
            log_levels().info(
                f"==============THE HEADERS OF THE CSV FILES {headers}==========="
            )

            # Combine headers and rows into a list of dictionaries
            rows = [
                {header: value for header, value in zip(headers, row)}
                for row in csv_reader
            ]

            print(rows)
            log_levels().info(
                f"==========INFORMATION OF THE MERGE ROWS======={rows}======"
            )

            file_upload = models.FileUpload(
                file_name=file_name,
                file_type="csv",
                size=100000,
                file_path="/get the path from cloudinary",
                email_add=email_add,
            )

            db.add(file_upload)
            db.flush()

            # Create new Category and Diagnosis objects and save them to the database
            for row in rows:
                category = models.Category(code=row["code"], title=row["tittle"])
                db.add(category)
                db.flush()
                diagnosis = models.Diagnosis(
                    category_id=category.id,
                    diag_code=row["diag_code"],
                    file_upload_id=file_upload.id,
                    full_code=row["full_code"],
                    abb_desc=row["abb_desc"],
                    full_desc=row["full_desc"],
                )
                db.add(diagnosis)

        log_levels().info(
            "=====Data loaded successfully, calling the email service to send email==="
        )
        response = send_email(email_add)
        log_levels().info(
            f"=============== EMAIL RESPONSE ===== {response.status_code}====="
        )
    except Exception as e:
        log_levels().error(
            f"+++++++++EXCEPTION+++++++++++ Error processing task: {str(e)} ++++++++++EXCEPTION+++++++++++"
        )
