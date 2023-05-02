# Base image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update \
    && apt-get install -y gcc postgresql libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Run migrations
RUN alembic upgrade head

# Expose port
EXPOSE 80

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
