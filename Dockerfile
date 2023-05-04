# Base image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /assessment

RUN apt-get update \
    && apt-get install -y gcc postgresql libpq-dev \
    && apt-get install -y screen \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy requirements file
COPY . .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

RUN chmod +x entrypoint.sh

# Run application
ENTRYPOINT ["./entrypoint.sh"]
