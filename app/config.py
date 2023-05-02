from pydantic import BaseSettings

# Validate the environment variable before the  booting the app
class Settings(BaseSettings):
    database_password: str
    database_username: str
    database_name: str
    database_port: int
    database_host: str
    cloud_name: str
    api_key: str
    api_secret: str
    analyzer: str
    papertrail_host: str
    papertrail_port: str
    broker: str
    sendinblue_endpoint: str
    sender_email_add: str


    class Config:
        env_file = '.env'

settings = Settings()
