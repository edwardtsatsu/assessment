#!/bin/sh

alembic revision --autogenerate -m "test db"

alembic upgrade head

pytest

screen -d -m bash -c "uvicorn app.main:app --host 0.0.0.0 --port 8000;"

celery -A app.task.celery worker --loglevel=info --pool=solo
