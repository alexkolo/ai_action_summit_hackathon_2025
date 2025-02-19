from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # api key
    BACKEND_API_KEY_NAME: str
    BACKEND_API_KEY: str

    # Object store settings
    OBJECT_STORE_URL: str
    OBJECT_STORE_KEY: str

    # LLM settings
    LLM_API_KEY: str
    LLM_ENDPOINT: str
    LLM_MISTRAL_MODEL: str

    class Config:
        env_file = ".env"
        # ignore extra environment variables
        extra = "allow"  

settings = Settings()
