from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Antarctic Digital Twin"
    environment: str = "dev"
    secret_key: str = "super-secret-key-change-in-prod"
    # Supabase / PostgreSQL connection string
    # Format: postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DBNAME
    database_url: str = ""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
