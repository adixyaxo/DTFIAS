# infrastructure/database/postgres/session.py
# Thin re-export of the shared async session from app/config/database.py.
# Infrastructure-layer code should import from here to maintain the
# DDD boundary — the engine layer never reaches into app/config directly.
from app.config.database import AsyncSessionLocal, get_db

__all__ = ["AsyncSessionLocal", "get_db"]
