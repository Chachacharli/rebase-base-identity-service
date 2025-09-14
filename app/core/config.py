from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "rebase-base-identity-service"
    PROJECT_VERSION: str = "0.1.0"
    BASE_URL: str = "http://localhost:8000"

    # JWT
    JWT_ALG: str = "RS256"
    PRIVATE_KEY_PATH: str = "keys/private.pem"
    PUBLIC_KEY_PATH: str = "keys/public.pem"


settings = Settings()
