# Plan: Final Audit Optimizations

Objective: Resolve remaining non-critical items from `AUDIT_REVIEW.md` (Post-Fixes Review).

## 1. Client-Side Route Protection (Next.js Middleware)
- [ ] Create `frontend/src/middleware.ts` to enforce role-based access at the routing level.
- [ ] Redirect unauthorized users from `/admin` or `/inventory` if they lack the required role.

## 2. In-Memory Device State (Persistence)
- [ ] Verify if `get_heartbeats` in `api.py` is fully persistent using InfluxDB queries (Done, but double check implementation).

## 3. Model Drift Detection (ML Monitoring)
- [ ] Create `backend/precognito/predictive/drift_detector.py` as a scheduled script to monitor performance over time.
- [ ] Log metrics for model accuracy degradation.

## 4. Documentation & Final Review Update
- [ ] Update `AUDIT_REVIEW.md` to reflect all fixes and the current state of the project.

## Verification
- [ ] Attempt to access `/admin-reporting` in frontend with a non-admin role (verify redirect).
- [ ] Verify that device heartbeats survive a backend restart.
- [ ] Run drift detection script to see generated reports.
