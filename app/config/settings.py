from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os
load_dotenv()

class Settings(BaseSettings):
    app_name: str = "Antarctic Digital Twin"
    environment: str = "dev"
    secret_key: str = "super-secret-key-change-in-prod"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

class ENV():
    class database():
        db_user: str = os.getenv("DB_USER")
        db_password: str = os.getenv("DB_PASSWORD")
        db_host: str = os.getenv("DB_HOST")
        db_port: int = os.getenv("DB_PORT")
        db_name: str = os.getenv("DB_NAME")


settings = Settings()
env = ENV()
