# Plan: Address Audit Vulnerabilities - Phase 1 & 2

Objective: Resolve critical and high-severity security vulnerabilities identified in `AUDIT_REPORT.md` to ensure industrial readiness.

## Phase 1: Immediate Security Remediation

### 1. Secrets Management
- [ ] Create `.env.example` with placeholders for all necessary environment variables.
- [ ] Update `backend/precognito/api.py`: Replace hardcoded `DATABASE_URL` default with `None` or an empty string, forcing environment configuration.
- [ ] Update `backend/precognito/work_orders/database.py`: Replace hardcoded `DATABASE_URL` default.
- [ ] Update `backend/precognito/ingestion/influx_client.py`: Replace hardcoded `INFLUX_TOKEN` default.
- [ ] Update `docker-compose.yml`: Replace hardcoded passwords and tokens with `${VARIABLE_NAME}` and ensure they are sourced from `.env`.

### 2. Authentication & Authorization
- [ ] Create `backend/precognito/auth.py` and move `get_current_user` and `RoleChecker` logic there.
- [ ] Refactor `get_current_user` to use `request.app.db_pool` to avoid circular dependencies.
- [ ] Secure `/ingest/dev` in `backend/precognito/api.py` using `admin_only` dependency.
- [ ] Secure `backend/precognito/work_orders/api.py` endpoints with `Depends(get_current_user)`.
- [ ] Secure `backend/precognito/inventory/api.py` endpoints with `Depends(get_current_user)` and specific role checks where appropriate.
- [ ] Secure `backend/precognito/financial/routes.py` endpoints with `manager_above` or `admin_only`.

### 3. Frontend Authentication Fixes
- [ ] Remove auto-registration (signup on login failure) from `frontend/src/app/(auth)/login/page.tsx`.
- [ ] Remove the Role selector from the login page.
- [ ] Implement a more robust password complexity check on the client side (minimum 8 chars + complexity).

### 4. Input Validation
- [ ] Define Pydantic models for inventory and work order requests.
- [ ] Update endpoints to use these models instead of raw `dict`.

## Phase 2: High Severity Fixes

### 5. Server-Side Role Enforcement
- [ ] Ensure all sensitive operations verify the user's role on the backend (not just UI-level hiding).

### 6. Rate Limiting
- [ ] Implement `slowapi` or similar middleware in `backend/precognito/api.py` to protect against DoS.

### 7. Secure Communication
- [ ] Add MQTT authentication and TLS configuration (optional, if broker supports it).
- [ ] Update `backend/precognito/api.py` to include basic security headers (using `fastapi.middleware.cors` and custom headers).

### 8. Timing-Safe Token Comparison
- [ ] Use `secrets.compare_digest` for session token verification in `auth.py`.

## Verification & Testing
- [ ] Verify that `/ingest/dev` now requires an admin token.
- [ ] Verify that work order and inventory endpoints return 401 without a token.
- [ ] Verify that frontend no longer allows role selection.
- [ ] Run existing tests to ensure no regressions.
- [ ] Add new tests for the secured endpoints.
