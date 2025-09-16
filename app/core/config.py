# Application settings from environment variables or .env file
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "rebase-base-identity-service"
    PROJECT_VERSION: str = "0.1.0"
    BASE_URL: str = "http://localhost:8000"

    # JWT
    JWT_ALG: str = "RS256"
    PRIVATE_KEY_PATH: str = "keys/private.pem"
    PUBLIC_KEY_PATH: str = "keys/public.pem"

    # Database
    DATABASE_URL: str = f"postgresql+psycopg2://{os.getenv('DATA_BASE_USER')}:{os.getenv('DATA_BASE_PASSWORD')}@{os.getenv('DATA_BASE_HOST')}:{os.getenv('DATA_BASE_PORT')}/{os.getenv('DATA_BASE_NAME')}"


settings = Settings()
