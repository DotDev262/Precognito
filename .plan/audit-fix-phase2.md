# Plan: Address Remaining Audit Review Issues

Objective: Resolve High and Medium severity issues identified in `AUDIT_REVIEW.md`.

## High Severity Fixes

### 1. Fix CORS Wildcard on Sub-APIs
- [ ] Update `backend/precognito/predictive/backend/main.py`: Restrict `allow_origins`.
- [ ] Update `backend/precognito/predictive/api/main.py`: Restrict `allow_origins`.
- [ ] Update `backend/precognito/anomaly/main_simple.py`: Restrict `allow_origins`.

### 2. Secure MQTT Communication
- [ ] Ensure `backend/precognito/ingestion/mqtt_worker.py` uses environment variables for user/password/TLS.
- [ ] (Optional) Add a sample `mosquitto.conf` with authentication enabled.

### 3. Enforce HTTPS
- [ ] Add `HTTPSRedirectMiddleware` to `backend/precognito/api.py`.

## Medium Severity & Performance Fixes

### 4. Optimize InfluxDB Writes
- [ ] Update `backend/precognito/ingestion/influx_client.py`: Change `write_options` from `SYNCHRONOUS` to batch/asynchronous mode.

### 5. Address N+1 Queries in `/assets`
- [ ] Refactor `get_assets` in `backend/precognito/api.py` to use a single Flux query for all devices instead of looping.

### 6. Implement Pagination
- [ ] Add `limit` and `offset` parameters to list endpoints:
    - [ ] `/assets`
    - [ ] `/anomalies`
    - [ ] `/audit-logs`
    - [ ] `/work-orders/`
    - [ ] `/inventory/`

### 7. Persistent Heartbeats
- [ ] (Alternative) Instead of in-memory `device_status`, query InfluxDB for last seen time per device to avoid loss on restart.

## Verification
- [ ] Verify CORS headers on sub-APIs.
- [ ] Verify HTTPS redirect.
- [ ] Verify that `/assets` performs better with many devices.
- [ ] Verify pagination works on at least one endpoint.
