# ASSESSMENT

This assessment is to test how I tackle problems, how fast I learn new technologies, and my level of knowledge right now.

This project is build with python run on the FASTAPI framework

## Install and Run Project

### clone the project using:
```bash
git clone https://github.com/edwardtsatsu/assessment.git
```

```bash
cd assessment
```

```bash
pip install -r requirements.txt
```

```bash
alembic head
```

```bash
uvicorn app.main:app --reload
```

```bash
celery -A app.task.celery worker --loglevel=info --pool=solo
```

## Contributing

Thank you for taking time to go through this!!
