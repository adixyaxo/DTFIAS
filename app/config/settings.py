from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Antarctic Digital Twin"
    environment: str = "dev"
    secret_key: str = "super-secret-key-change-in-prod"
    mysql_dsn: str = "mysql+asyncmy://root:password@localhost:3306/dtfias"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
