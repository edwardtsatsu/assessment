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

### Setting Up Credentials
```bash
Rename the .env.example file to .env
```

### Run application with Docker Compose
```bash
docker-compose up --build
```

### Stop application using Docker Compose
```bash
docker-compose down -v
```

## Additional Information [Not Compulsory]
### Building Docker Image from Dockerfile
```bash
docker build -t <tag_name>:<version> .
```

### start application using
```bash
docker run -p <host_value>:8000 --env-file=.env <tag_name>:<version>
```

## API Documentation
```bash
http://127.0.0.1:8000/redoc
```

## API SandBox
```bash
http://127.0.0.1:8000/docs
```

## Other Usage

## Contributing

Thank you for taking time to go through this!!


## License
This project is licensed under the MIT License.
