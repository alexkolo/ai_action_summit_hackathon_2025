from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Object store settings
    OBJECT_STORE_URL: str
    OBJECT_STORE_KEY: str

    # LLM settings
    LLM_API_KEY: str
    LLM_ENDPOINT: str

    class Config:
        env_file = ".env"

settings = Settings()
