# Plan: 100% Test Coverage Completion

Objective: Close all remaining testing gaps identified in the audit to reach a perfect 10/10 readiness score.

## Phase 1: Backend Integration Tests
Exhaustive testing of all API modules using `auth_client`.

### 1.1 Work Orders Module (`tests/integration/test_work_orders.py`)
- [ ] `POST /work-orders/assets/`: Test asset creation.
- [ ] `POST /work-orders/audit/`: Test audit/work order creation.
- [ ] `GET /work-orders/audit/{asset_id}`: Test fetching audits by asset.
- [ ] `PATCH /work-orders/audit/{id}/complete`: Test full completion flow.

### 1.2 Inventory Module (`tests/integration/test_inventory.py`)
- [ ] `POST /inventory/reserve`: Test part reservation with Pydantic validation.
- [ ] `POST /inventory/purchase-order`: Test automated PO generation.
- [ ] `GET /inventory/jit-alerts`: Test RUL-based alert integration.

### 1.3 Financial & Admin Module (`tests/integration/test_financial.py`)
- [ ] `GET /admin-reporting/recommendations`: Test ROI engine integration.
- [ ] `GET /admin-reporting/health`: Test system health monitoring.
- [ ] `GET /admin-reporting/audit-report`: Test compliance log aggregation.

### 1.4 Main API Extensions (`tests/integration/test_main_api.py`)
- [ ] `GET /anomalies`: Test InfluxDB anomaly retrieval.
- [ ] `GET /safety-alerts`: Test thermal safety monitoring.
- [ ] `GET /heartbeats`: Test persistent device status.
- [ ] `POST /analytics/feedback`: Test human-in-the-loop feedback flow.
- [ ] `GET /analytics/metrics`: Test dynamic model accuracy calculation.

## Phase 2: Frontend E2E Tests (Playwright)
Expanding `frontend/tests/e2e/` to cover the entire user surface.

- [ ] `dashboard.spec.ts`: Verify live charts and status cards.
- [ ] `inventory.spec.ts`: Verify stock management and JIT alerts.
- [ ] `work_orders.spec.ts`: Verify QR check-in and task completion.
- [ ] `reports.spec.ts`: Verify PDF/CSV export generation.
- [ ] `analytics.spec.ts`: Verify feedback loop UI.

## Phase 3: Reliability & ML Ops Tests
- [ ] `tests/unit/test_circuit_breaker.py`: Test trip/reset logic of `CircuitBreaker`.
- [ ] `tests/integration/test_drift_detection.py`: Test MAE calculation in `drift_detector.py`.

## Verification
- [ ] Run `pytest tests/integration/` -> 100% pass.
- [ ] Run `bun run test:e2e` -> 100% pass.
- [ ] Update `AUDIT_REVIEW.md` to final state.
