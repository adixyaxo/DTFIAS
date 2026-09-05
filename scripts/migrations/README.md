# DTFIAS Database Migrations

## How to run

### Option A — Supabase SQL Editor (simplest)

1. Open your [Supabase Dashboard](https://supabase.com/dashboard)
2. Navigate to your project → **SQL Editor**
3. Click **New query**
4. Paste the entire contents of `001_initial_schema.sql`
5. Click **Run**

### Option B — Supabase CLI

```bash
# Install Supabase CLI if not already done
npm install -g supabase

# Link to your project
supabase link --project-ref <YOUR-PROJECT-REF>

# Run the migration
supabase db push
# or run directly:
psql "postgresql+asyncpg://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres" -f scripts/migrations/001_initial_schema.sql
```

### Option C — psql directly

```bash
psql "postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres" \
     -f scripts/migrations/001_initial_schema.sql
```

---

## Migration files

| File | Description |
|------|-------------|
| `001_initial_schema.sql` | Full schema — enums, tables, triggers, indexes, RLS, seed data |

---

## Notes

- The migration wraps everything in a `BEGIN; ... COMMIT;` transaction — if any step fails, nothing is created.
- `pg_cron` for telemetry retention requires the [pg_cron extension](https://supabase.com/docs/guides/database/extensions/pg_cron). If unavailable, replace with a Supabase Edge Function on a `0 2 * * *` schedule.
- The `auth.users` table is managed by Supabase — do not modify it directly.
