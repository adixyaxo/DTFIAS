# DTFIAS — Vercel Environment Variables Reference

Set these in: **Vercel Dashboard → Your Project → Settings → Environment Variables**

All variables should be set for **Production** (and optionally Preview/Development).

---

## Required Variables

| Variable | Where to Find | Example Value |
|----------|--------------|---------------|
| `DATABASE_URL` | Supabase Dashboard → Project Settings → Database → **Connection String (URI)** → change `postgresql://` to `postgresql+asyncpg://` and use the **pooler** URL on port **6543** | `postgresql+asyncpg://postgres.xxxx:[PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres` |
| `SUPABASE_URL` | Supabase Dashboard → Project Settings → API → Project URL | `https://xxxxxxxxxxxx.supabase.co` |
| `SUPABASE_PUBLISHABLE_KEY` | Supabase Dashboard → Project Settings → API → **anon / public** key | `sb_publishable_...` |
| `SUPABASE_SECRET_KEY` | Supabase Dashboard → Project Settings → API → **service_role** key | `sb_secret_...` |
| `SUPABASE_JWKS_URL` | Constructed from your project ref | `https://xxxxxxxxxxxx.supabase.co/auth/v1/.well-known/jwks.json` |
| `SECRET_KEY` | Generate a strong random string | `openssl rand -hex 32` output |
| `JWT_SECRET` | Generate a strong random string (different from `SECRET_KEY`) | `openssl rand -hex 32` output |
| `ENVIRONMENT` | Set to `production` on Vercel | `production` |

---

## Optional Variables (defaults apply if not set)

| Variable | Default | Notes |
|----------|---------|-------|
| `APP_NAME` | `Antarctic Digital Twin` | Shown in FastAPI docs title |
| `JWT_ALGORITHM` | `HS256` | Do not change unless you know what you're doing |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` (24h) | JWT validity window |

---

## Critical Notes

> **Do NOT use the anon/publishable key as the DB password.**
> The `DATABASE_URL` password is the Postgres database password, found at:
> Supabase Dashboard → Project Settings → Database → URI → the `[YOUR-PASSWORD]` section.
> It is NOT the `sb_publishable_*` API key.

> **Use the Supabase connection pooler URL** (port 6543, Transaction mode), not the direct
> connection (port 5432). Vercel serverless creates many short-lived connections; the pooler
> prevents exhausting Supabase's connection limit.

> **VERCEL=1** is automatically injected by Vercel into every function invocation.
> You do NOT need to set this manually — the app uses it internally to activate
> serverless-compatible behavior (NullPool, SSE snapshot mode).

---

## Vercel-Injected Variables (Do NOT set manually)

These are automatically provided by Vercel's runtime:

| Variable | Purpose |
|----------|---------|
| `VERCEL` | `"1"` — triggers serverless-safe mode in the app |
| `VERCEL_URL` | The deployment URL (e.g. `dtfias-xxx.vercel.app`) |
| `VERCEL_ENV` | `production`, `preview`, or `development` |

---

## Security Checklist Before Going Live

- [ ] `SECRET_KEY` is at least 32 random bytes (not the default from `.env.example`)
- [ ] `JWT_SECRET` is at least 32 random bytes (different from `SECRET_KEY`)
- [ ] `SUPABASE_SECRET_KEY` is stored **only** in Vercel env vars, never committed to git
- [ ] `DATABASE_URL` uses the **pooler** endpoint (port 6543), not direct Postgres (port 5432)
- [ ] `ENVIRONMENT=production` is set so cookies get `Secure` flag (C10)
- [ ] `.env` is in `.gitignore` (already is — verify before first push)
