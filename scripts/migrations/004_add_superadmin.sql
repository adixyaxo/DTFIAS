-- =============================================================================
-- MIGRATION 004: Add second Super Admin user (superadmin@gmail.com)
-- =============================================================================

BEGIN;

INSERT INTO profiles (id, full_name, employee_code, hashed_password, status)
VALUES (
    gen_random_uuid(),
    'Global Super Admin',
    'superadmin@gmail.com',
    '$argon2id$v=19$m=65536,t=3,p=4$c38Q7JaAH3tUow0MGOqWDA$1g/GpK7tKs3DnXFVdz2yuPII86urVCFi9kalc1C97yM',
    'ACTIVE'
) ON CONFLICT (employee_code) DO UPDATE 
SET hashed_password = EXCLUDED.hashed_password;

-- Ensure this user has the SUPER_ADMIN role
INSERT INTO user_roles (user_id, role_id)
SELECT id, (SELECT id FROM roles WHERE name = 'SUPER_ADMIN')
FROM profiles WHERE employee_code = 'superadmin@gmail.com'
ON CONFLICT DO NOTHING;

COMMIT;
