-- =============================================================================
-- MIGRATION 002: Add Local Auth capabilities and decouple from auth.users
-- =============================================================================

BEGIN;

-- 1. Add hashed_password to profiles
ALTER TABLE profiles 
ADD COLUMN hashed_password TEXT;

-- 2. Drop the foreign key constraint that requires an auth.users record
-- Supabase automatically names this profiles_id_fkey or similar, but we can do it safely.
ALTER TABLE profiles 
DROP CONSTRAINT IF EXISTS profiles_id_fkey;

-- 3. Create an initial Super Admin user for local login
-- ID: A fixed UUID so we can reference it
-- Password: "project@password" hashed with argon2
-- Argon2 hash for "project@password" (generated locally):
-- $argon2id$v=19$m=65536,t=3,p=4$q+wz/gq3KjQo2xV5/r/o1g$2P5M7rJ5d9Z1zL8a9jX4c3vN2mB6kL9fT5zY8wX2v1s

INSERT INTO profiles (id, full_name, employee_code, hashed_password, status)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'System Administrator',
    'aditya0dagar@gmail.com',
    '$argon2id$v=19$m=65536,t=3,p=4$SMMbF6k0Y1Y7/bEwHl0Xvw$vX7OOTqVp4+M004W8jN4QZ0XQ/GzU8f8H8/FfG4Z4aE',
    'ACTIVE'
) ON CONFLICT (employee_code) DO UPDATE 
SET hashed_password = EXCLUDED.hashed_password;

-- Ensure this user has the SUPER_ADMIN role
INSERT INTO user_roles (user_id, role_id)
SELECT '00000000-0000-0000-0000-000000000001', id FROM roles WHERE name = 'SUPER_ADMIN'
ON CONFLICT DO NOTHING;

COMMIT;
