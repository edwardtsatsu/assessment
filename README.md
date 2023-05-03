# ASSESSMENT

This assessment is to test how I tackle problems, how fast I learn new technologies, and my level of knowledge right now.

This project is build with python run on the FASTAPI framework. All logs from the application are set to papertrail

## Installation

### clone
```bash
git clone https://github.com/edwardtsatsu/assessment.git
```

### change directory to the project directory
```bash
cd assessment
```

### install dependencies and libs
```bash
pip install -r requirements.txt
```

## Run Project

### Run migrations to create tables
```bash
alembic upgrade head
```

### Run test cases (OPTIONAL)
```bash
pytest
```

### Run the application with docker
```bash
docker-compose --env-file .env up -d
```

### start project using
```bash
uvicorn app.main:app --reload
```

### Start celery to process the background jobs
```bash
celery -A app.task.celery worker --loglevel=info --pool=solo
```

## API Documentation
```
http://127.0.0.1:8000/redoc
```

## Other Usage

### To create a new migration follow the following
```bash
alembic init {name of migration file}
```

### create a migration version
```bash
alembic revision --autogenerate -m '<name of migration>'
```

### To run the migration
```bash
alembic upgrade head
```

### To downgrade migration use
```bash
alembic downgrade -1

or

alembic downgrade {version_name}
```

## Contributing

Thank you for taking time to go through this!!


## License
This project is licensed under the MIT License.
