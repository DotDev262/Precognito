# Plan: Finalize Security and Scalability

Objective: Complete the four requested tasks to ensure the system is production-ready.

## 1. Add HTTPS at Load Balancer
- [ ] Update `backend/precognito/api.py` to ensure it works correctly behind a proxy that terminates TLS.
- [ ] Add `ForwardedHeaderMiddleware` if necessary to handle `X-Forwarded-Proto`.

## 2. Implement Pagination on All List Endpoints
- [ ] Update `backend/precognito/api.py`:
    - [ ] Add pagination to `/safety-alerts`.
    - [ ] Add pagination to `/heartbeats`.
- [ ] Ensure consistent naming for `limit` and `offset` across all modules.

## 3. Async InfluxDB Writes with Batching
- [ ] Update `backend/precognito/ingestion/influx_client.py`:
    - [ ] Configure `WriteOptions` explicitly for batching (e.g., `batch_size=50`, `flush_interval=1000`).
    - [ ] Ensure the `write_api` is properly utilized in asynchronous mode.

## 4. Server-Side Route Middleware (Frontend)
- [ ] Enhance `frontend/src/middleware.ts`:
    - [ ] Implement a mechanism to verify the session token against the backend (or at least check the role if available in the cookie).
    - [ ] Block access to `/inventory` if the user is not `ADMIN`, `MANAGER`, or `STORE_MANAGER`.
    - [ ] Block access to `/admin-reporting` if the user is not `ADMIN` or `MANAGER`.

## Verification
- [ ] Test pagination with `?limit=1&offset=0`.
- [ ] Verify InfluxDB data is still being saved correctly under load.
- [ ] Verify that non-admin users cannot access the admin reporting route via URL manipulation.
