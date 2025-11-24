# config.py

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Loads .env variables


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    JWT_SECRET: str = "mysecretkey"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }


settings = Settings()

