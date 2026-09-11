# DTFIAS Authentication Backend Implementation Plan

## 1. Executive Summary & Context

The current state of the authentication backend (`app/routers/auth/auth.py`) is functionally incomplete. It utilizes hardcoded backdoors (e.g., `is_super_admin_backdoor`) and explicitly bypasses cryptographic password verification.

Furthermore, there is a structural divergence between the **Database Schema** and the **Architectural Constraints (C1-C17)**:
- **Schema (`001_initial_schema.sql`)**: The `profiles` table is defined as a 1:1 mapping to Supabase's managed `auth.users` table (`id UUID PRIMARY KEY REFERENCES auth.users(id)`). This implies Supabase GoTrue manages credentials.
- **Constraints (C6, C14, C15)**: The architecture explicitly forbids client-side Supabase connections, disables RLS for access control, and **mandates Argon2** for password hashing (`infrastructure/security/authentication/passwords.py`). Supabase Auth defaults to `bcrypt` and handles its own hashing.

To build a fully working authentication backend that strictly respects the project's hard constraints, we must take ownership of the credential management within the FastAPI application layer.

---

## 2. Implementation Strategy: Backend-Managed Argon2 Auth

This strategy completely isolates the application from Supabase GoTrue, ensuring 100% compliance with C6 (Argon2) and C10 (Secure Cookies).

### Step 1: Database Schema Migration
To store Argon2 password hashes locally, we need to modify the `profiles` table (or create a dedicated `user_credentials` table).
1. Create a migration script (e.g., `scripts/migrations/002_add_local_auth.sql`).
2. Add a `hashed_password` column to `profiles`:
   ```sql
   ALTER TABLE profiles ADD COLUMN hashed_password TEXT;
   ```
3. *Optional but recommended:* Drop the hard `auth.users` foreign key constraint from `profiles` if we decide to abandon Supabase GoTrue entirely to prevent insertion friction.

### Step 2: Seed Initial Users
Provide a backend CLI script or adjust the seed SQL to create the initial admin users, securely hashing their passwords using the `infrastructure/security/authentication/passwords.py` utility.

### Step 3: Rewrite `process_login` (app/routers/auth/auth.py)
Update the `POST /login` route to:
1. Accept `username` (employee_code) and `password`.
2. Fetch the `Profile` (and eagerly load `roles`).
3. Verify the password using `verify_password(password, profile.hashed_password)`.
4. Enforce **Constraint C7** by writing to `audit_logs` for both `LOGIN_SUCCESS` and `LOGIN_FAILED` events.
5. Generate the JWT payload containing `sub` (User ID), `username`, and `roles`.
6. Issue the JWT as a secure, `HttpOnly`, `samesite="lax"` session cookie (Constraint C10).

### Step 4: Implement CSRF Protection (Constraint C11)
Currently, POST requests (like login and commands) lack CSRF protection.
1. Add a CSRF middleware (`infrastructure/security/csrf/csrf_middleware.py`).
2. Inject a CSRF token into all Jinja2 template contexts.
3. Validate the `X-CSRF-Token` header or form payload on every state-changing route (`POST`, `PUT`, `DELETE`).

### Step 5: User Management API (HQ Admin)
Implement routes in `app/routers/hq/users.py` allowing `HQ_ADMIN` to:
- Create new station operators (generating Argon2 hashes upon creation).
- Reset passwords.
- Suspend accounts (updating `profile_status`).

---

## 3. Alternative Strategy: Supabase GoTrue Proxy

If the project owners strongly prefer keeping `auth.users` as the identity provider, the backend must act as an Auth Proxy.

1. **Login Request**: User submits credentials to FastAPI `POST /login`.
2. **Proxy Authentication**: FastAPI makes an HTTP POST request to `SUPABASE_URL/auth/v1/token?grant_type=password` using the `SUPABASE_KEY`.
3. **Validation**: If Supabase returns a 200 OK (with a JWT), the credentials are valid.
4. **Profile Linking**: FastAPI extracts the UUID from the Supabase JWT, looks up the local `Profile`, and retrieves the user's roles.
5. **Session Creation**: FastAPI discards the Supabase JWT and issues its **own local JWT** inside a secure `HttpOnly` cookie.

*Note: This approach technically violates the spirit of C6 (Argon2 mandate), as Supabase handles the actual hashing under the hood, but it complies with the schema's reliance on `auth.users`.*

---

## 4. Immediate Action Plan

To proceed with making the authentication backend fully functional, the following files will need to be created/edited:

1. `app/routers/auth/auth.py` - Rewrite `process_login` to implement actual validation.
2. `infrastructure/security/authentication/passwords.py` - Ensure it is wired into the user creation flow.
3. `scripts/migrations/002_add_local_auth.sql` - (If choosing Strategy 1) Add the `hashed_password` field to the database.
4. `app/middleware/csrf.py` - Implement the required CSRF verification across the app.

By executing this plan, DTFIAS will replace its backdoor implementation with a secure, production-grade identity mechanism fully compliant with the 17 hard architectural constraints.
