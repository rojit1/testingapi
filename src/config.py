from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    database_hostname: str = 'HOST'
    database_port: str = 'PORT'
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()