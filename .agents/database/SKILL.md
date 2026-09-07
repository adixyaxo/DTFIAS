---
name: supabase-postgres-best-practices
description: "Postgres best practices maintained by Supabase, for Postgres running anywhere. Load this skill BEFORE writing or changing anything that lives in a Postgres database: creating or altering tables and columns (including choosing column types), schema design, migrations and declarative schema files, RLS policies and the tests that verify them, indexes, triggers, database functions, queues and scheduled jobs (pg_cron, pgmq), vector/semantic search (pgvector), and restoring dumps (pg_restore) or importing data. Also load it when diagnosing slow queries, high CPU, timeouts, EXPLAIN plans, connection exhaustion, locking, bloat, or rows visible to the wrong user or tenant. This is not just a performance guide — schema, migration, security, and SQL authoring tasks need these rules too, even for a one-column change or a single query."
license: MIT
metadata:
  author: supabase
  version: "1.1.1"
  organization: Supabase
  date: January 2026
  abstract: Comprehensive Postgres performance optimization guide for developers using Supabase and Postgres. Contains performance rules across 8 categories, prioritized by impact from critical (query performance, connection management) to incremental (advanced features). Each rule includes detailed explanations, incorrect vs. correct SQL examples, query plan analysis, and specific performance metrics to guide automated optimization and code generation.
---

# Supabase Postgres Best Practices

Comprehensive performance optimization guide for Postgres, maintained by Supabase. Contains rules across 8 categories, prioritized by impact to guide automated query optimization and schema design.

## When to Apply

Reference these guidelines when:
- Writing SQL queries or designing schemas
- Implementing indexes or query optimization
- Reviewing database performance issues
- Configuring connection pooling or scaling
- Optimizing for Postgres-specific features
- Working with Row-Level Security (RLS)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Connection Management | CRITICAL | `conn-` |
| 3 | Security & RLS | CRITICAL | `security-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Concurrency & Locking | MEDIUM-HIGH | `lock-` |
| 6 | Data Access Patterns | MEDIUM | `data-` |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |
| 8 | Advanced Features | LOW | `advanced-` |

## Essential Rules for DTFIAS PostgreSQL & Supabase

### 1. Connection & Driver Strategy
- **Driver Scheme**: Always use `postgresql+asyncpg://` for SQLAlchemy async engine.
- **Port Selection**:
  - Direct connection: `db.<ref>.supabase.co:5432/postgres` (default session mode for migrations and dev).
  - Transaction pooler: `aws-0-<region>.pooler.supabase.com:6543/postgres` (use when scaling serverless or multi-worker).
- **SSL / TLS**: Supabase requires SSL. In asyncpg, ensure SSL context is configured if connecting directly in production.
- **NEVER** use anon key (`sb_publishable_*`) as database password. Use the database password from Supabase Project Settings.

### 2. Query Performance & Indexing Rules
- **Foreign Key Indexing**: Postgres does NOT automatically index foreign key columns. Always index every `REFERENCES` column (e.g. `station_id`, `user_id`, `asset_id`).
  ```sql
  CREATE INDEX idx_assets_station_id ON assets(station_id);
  ```
- **Time-Series Telemetry Composite Index**: For rolling telemetry (`energy_readings`, `environment_readings`, `asset_readings`), queries filter by station and order by timestamp. Use a composite B-Tree index:
  ```sql
  CREATE INDEX idx_energy_readings_station_time ON energy_readings(station_id, recorded_at DESC);
  ```
- **Partial Indexes for Operational Status**: When querying active alerts or pending commands, use partial indexes to avoid full table scans:
  ```sql
  CREATE INDEX idx_active_alerts_unresolved ON active_alerts(station_id) WHERE resolved_at IS NULL;
  CREATE INDEX idx_commands_executing ON commands(station_id) WHERE status IN ('SENT', 'RECEIVED', 'EXECUTING');
  ```

### 3. Schema Design & Data Integrity
- **Canonical Schema Authority**: Consult [`docs/database.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/database.md) and [`scripts/migrations/001_initial_schema.sql`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/scripts/migrations/001_initial_schema.sql) before adding or changing tables.
- **IDs & Keys**:
  - Use `UUID PRIMARY KEY DEFAULT gen_random_uuid()` for all entities (stations, users, assets, logs).
  - Station references MUST be `station_id UUID REFERENCES stations(id) NOT NULL`.
- **Enums**:
  - Operational states use native Postgres enums: `station_status`, `alert_severity`, `command_status`, `telemetry_quality`.
  - Roles and Stations are normalized relational tables (`roles`, `stations`).
- **Timestamps**: Always use `TIMESTAMPTZ` (timestamp with time zone) and default to `NOW()`. Never use timezone-naive `TIMESTAMP`.

### 4. Security & Access Control
- **Backend Only (C15)**: The frontend never connects directly to Supabase Postgres. Only the FastAPI backend connects via async SQLAlchemy with backend credentials.
- **Zero f-string SQL (C8)**: Construct all queries using SQLAlchemy ORM or parameterized `text("SELECT ... WHERE col = :val")`. Never interpolate Python strings into SQL.
- **Audit Logging (C7)**: Every login, state write, command issuance, and permission denial MUST insert a record into `audit_logs`.

### 5. References & Resources
- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/current/)
- [Supabase Database Guides](https://supabase.com/docs/guides/database/overview)
- [SQLAlchemy 2.0 Async Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- DTFIAS Canonical Schema: [`docs/database.md`](file:///C:/Users/adity/Documents/Coding/Projects/DTFIAS/docs/database.md)