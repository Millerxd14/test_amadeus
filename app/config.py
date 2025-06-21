from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "a_very_secret_key"
    ALGORITHM: str = "HS256"  # Ensure the algorithm is a valid one like HS256

    class ConfigDict:
        env_file = ".env"

settings = Settings()
