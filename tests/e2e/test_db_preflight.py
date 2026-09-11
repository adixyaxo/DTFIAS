import asyncio
import os
import pytest
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")

@pytest.fixture(scope="function")
async def db_connection():
    """Provides a database connection for the tests."""
    assert DATABASE_URL, "DATABASE_URL is missing in .env"
    
    # Catch the common mistake of using the anon key instead of the DB password
    assert "sb_publishable_" not in DATABASE_URL, (
        "DATABASE_URL contains the Supabase anon key ('sb_publishable_...') "
        "instead of the database password. Please check your Supabase Dashboard -> "
        "Project Settings -> Database -> URI to get the correct password."
    )
    
    assert DATABASE_URL.startswith("postgresql+asyncpg://"), (
        "DATABASE_URL must start with 'postgresql+asyncpg://'"
    )

    raw_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    
    try:
        conn = await asyncpg.connect(raw_url, timeout=10, statement_cache_size=0)
        yield conn
    except Exception as e:
        pytest.fail(f"Failed to connect to the database: {e}")
    finally:
        await conn.close()


@pytest.mark.asyncio
async def test_database_connection(db_connection):
    """Test if we can connect and fetch the postgres version."""
    version = await db_connection.fetchval("SELECT version();")
    assert "PostgreSQL" in version


@pytest.mark.asyncio
async def test_essential_tables_exist(db_connection):
    """Test if the essential tables from the initial schema are present."""
    tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """
    records = await db_connection.fetch(tables_query)
    existing_tables = {record['table_name'] for record in records}
    
    expected_tables = {
        'stations', 'station_areas', 'profiles', 'roles', 'permissions',
        'assets', 'sensors', 'energy_readings', 'environment_readings',
        'commands', 'active_alerts', 'audit_logs'
    }
    
    missing_tables = expected_tables - existing_tables
    assert not missing_tables, f"Missing tables in public schema: {missing_tables}. Run migrations."


@pytest.mark.asyncio
async def test_essential_enums_exist(db_connection):
    """Test if the essential ENUMs are created."""
    enums_query = """
        SELECT typname 
        FROM pg_type 
        JOIN pg_enum ON pg_enum.enumtypid = pg_type.oid 
        GROUP BY typname;
    """
    records = await db_connection.fetch(enums_query)
    existing_enums = {record['typname'] for record in records}
    
    expected_enums = {
        'station_status', 'station_type', 'profile_status', 
        'asset_status', 'reading_quality', 'alert_severity'
    }
    
    missing_enums = expected_enums - existing_enums
    assert not missing_enums, f"Missing ENUMs in database: {missing_enums}. Run migrations."


@pytest.mark.asyncio
async def test_seed_data_exists(db_connection):
    """Verify that seed data like Maitri and Bharati stations exists."""
    stations = await db_connection.fetch("SELECT code, name FROM stations;")
    station_codes = {s['code'] for s in stations}
    
    assert 'MAT' in station_codes, "Maitri station (MAT) is missing from seed data."
    assert 'BHA' in station_codes, "Bharati station (BHA) is missing from seed data."
