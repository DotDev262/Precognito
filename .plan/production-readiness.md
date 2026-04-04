# Plan: Production Readiness Refinement

Objective: Address architectural, performance, and reliability gaps to finalize the system for production deployment.

## 1. Database Migrations (Alembic)
- [ ] Install `alembic`.
- [ ] Initialize alembic in `backend/`.
- [ ] Configure `alembic.ini` and `env.py` to use the unified SQLAlchemy `Base`.
- [ ] Generate the initial migration script reflecting current schemas.

## 2. Health Check & Observability
- [ ] Add `GET /health` endpoint to `backend/precognito/api.py`.
    - [ ] Verify PostgreSQL connectivity (asyncpg and SQLAlchemy).
    - [ ] Verify InfluxDB connectivity.
- [ ] Implement structured JSON logging for standardizing logs.

## 3. Performance & Reliability
- [ ] Optimize `/assets` Flux query to use `limit` and `offset` for true pagination.
- [ ] Replace hardcoded mock metrics in `get_model_metrics` with dynamic calculations where data is available.
- [ ] Implement a simple Circuit Breaker for InfluxDB interactions to prevent cascading failures.

## 4. Documentation
- [ ] Add instructions for running migrations to `README.md`.
- [ ] Update `AUDIT_REVIEW.md` readiness score.

## Verification
- [ ] Run `alembic upgrade head` and verify schema.
- [ ] `curl http://localhost:8000/health` and verify 200 OK.
- [ ] Verify logs are in JSON format.
- [ ] Test `/assets?limit=5` and verify only 5 records are fetched from InfluxDB.
