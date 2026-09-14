import os
from typing import Optional
from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application settings
    app_name: str = Field(default="Antarctic Digital Twin", validation_alias=AliasChoices("APP_NAME", "app_name"))
    environment: str = Field(default="dev", validation_alias=AliasChoices("ENVIRONMENT", "environment"))
    secret_key: str = Field(
        default="super-secret-key-change-in-prod",
        validation_alias=AliasChoices("SECRET_KEY", "secret_key"),
    )

    # Database (Supabase / PostgreSQL connection string)
    # Format: postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DBNAME
    database_url: str = Field(default="", validation_alias=AliasChoices("DATABASE_URL", "database_url"))

    # Supabase API & Auth configuration
    supabase_url: str = Field(default="", validation_alias=AliasChoices("SUPABASE_URL", "supabase_url"))
    supabase_publishable_key: str = Field(
        default="",
        validation_alias=AliasChoices(
            "SUPABASE_PUBLISHABLE_KEY",
            "supabase_publishable_key",
            "SUPABASE_KEY",
            "supabase_key",
            "SUPABASE_ANON_KEY",
            "supabase_anon_key",
        ),
    )
    supabase_secret_key: str = Field(
        default="",
        validation_alias=AliasChoices(
            "SUPABASE_SECRET_KEY",
            "supabase_secret_key",
            "SUPABASE_SERVICE_ROLE_KEY",
            "supabase_service_role_key",
        ),
    )
    supabase_jwks_url: str = Field(
        default="",
        validation_alias=AliasChoices("SUPABASE_JWKS_URL", "supabase_jwks_url"),
    )

    # JWT / RBAC security configuration
    jwt_secret: str = Field(
        default="dtfias-polar-twin-sih26060-secret-key-production",
        validation_alias=AliasChoices("JWT_SECRET", "jwt_secret"),
    )
    jwt_algorithm: str = Field(
        default="HS256",
        validation_alias=AliasChoices("JWT_ALGORITHM", "jwt_algorithm"),
    )
    access_token_expire_minutes: int = Field(
        default=60 * 24,
        validation_alias=AliasChoices("ACCESS_TOKEN_EXPIRE_MINUTES", "access_token_expire_minutes"),
    )

    # Convenience properties
    @property
    def supabase_key(self) -> str:
        return self.supabase_publishable_key

    @property
    def supabase_service_role_key(self) -> str:
        return self.supabase_secret_key

    @property
    def is_vercel(self) -> bool:
        """True when running inside a Vercel serverless function (VERCEL=1 injected automatically)."""
        import os
        return bool(os.environ.get("VERCEL"))

    @property
    def is_production(self) -> bool:
        """True when ENVIRONMENT=production."""
        return self.environment.lower() == "production"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()

# Direct Python variable exports from environment config for clean imports
APP_NAME: str = settings.app_name
ENVIRONMENT: str = settings.environment
SECRET_KEY: str = settings.secret_key
DATABASE_URL: str = settings.database_url

SUPABASE_URL: str = settings.supabase_url
SUPABASE_PUBLISHABLE_KEY: str = settings.supabase_publishable_key
SUPABASE_KEY: str = settings.supabase_publishable_key
SUPABASE_SECRET_KEY: str = settings.supabase_secret_key
SUPABASE_SERVICE_ROLE_KEY: str = settings.supabase_secret_key
SUPABASE_JWKS_URL: str = settings.supabase_jwks_url

JWT_SECRET: str = settings.jwt_secret
JWT_ALGORITHM: str = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.access_token_expire_minutes

