# Authentication & Database Infrastructure Plan

This plan details the setup of PostgreSQL and InfluxDB using Docker, followed by the implementation of authentication using the `better-auth` TypeScript library.

## Objective
1. **Infrastructure**: Provision PostgreSQL (for relational data like users and assets) and InfluxDB (for time-series telemetry data) via Docker Compose.
2. **Authentication**: Replace the mock authentication in the Next.js frontend with `better-auth`, connecting it to the PostgreSQL database.
3. **Integration**: Secure both frontend routes and backend APIs using the new authentication system.

## Key Context & Files
- `docker-compose.yml` (New): To orchestrate PostgreSQL and InfluxDB.
- `frontend/package.json`: Will be updated with `better-auth` and a database driver (e.g., `pg`).
- `frontend/src/lib/auth.ts` (New): Configuration and initialization of `better-auth` server instance.
- `frontend/src/lib/auth-client.ts` (New): Initialization of `better-auth` client instance.
- `frontend/src/app/api/auth/[...all]/route.ts` (New): Next.js App Router API endpoints for handling auth requests.
- `frontend/src/middleware.ts` (New): Next.js middleware to protect dashboard routes.
- `frontend/src/app/(auth)/login/page.tsx`: Updated to use `better-auth` sign-in methods.
- `backend/precognito/api.py`: Will be updated to authenticate requests using the session token from `better-auth`.

## Implementation Steps

### Phase 1: Database Infrastructure (Docker)
1. **Create `docker-compose.yml`**:
   - Define a `postgres` service (latest version) with environment variables for user, password, and default database (`precognito`).
   - Define an `influxdb` service (v2.x) with environment variables for setup (username, password, org, bucket, admin token).
   - Configure persistent volumes for both databases.
2. **Start Services**: Run `docker compose up -d` to spin up the databases.

### Phase 2: Frontend Authentication (`better-auth`)
1. **Install Dependencies**:
   - Run `bun add better-auth pg` inside the `frontend` directory.
   - Run `bun add -D @types/pg`.
2. **Configure `better-auth`**:
   - Create `frontend/src/lib/auth.ts` to configure `better-auth` with the PostgreSQL adapter, connecting to the Dockerized Postgres instance.
   - Configure plugins if needed (e.g., username/password login, JWT plugin).
3. **Create API Routes**:
   - Add `frontend/src/app/api/auth/[...all]/route.ts` to handle better-auth API endpoints (login, logout, session check).
4. **Create Client Hooks**:
   - Create `frontend/src/lib/auth-client.ts` to export `signIn`, `signOut`, and `useSession` from `createAuthClient()`.
5. **Update UI & State**:
   - Refactor `frontend/src/app/(auth)/login/page.tsx` to use the new `signIn` method.
   - Refactor or remove `authContext.tsx`, replacing it with `better-auth`'s `useSession` hook across components (like `Sidebar.tsx`, `Header.tsx`, `DashboardPage.tsx`).
6. **Route Protection**:
   - Create `frontend/src/middleware.ts` to intercept requests to `/(dashboard)/*` and redirect to `/login` if the user is unauthenticated.

### Phase 3: Backend API Protection
Since `better-auth` handles sessions in the Next.js ecosystem, the FastAPI backend needs to verify these sessions.
1. **Database Connection**: 
   - Add a database connection in FastAPI using `asyncpg` or `SQLAlchemy` to connect to the PostgreSQL container.
2. **Session Verification**:
   - Create a dependency in FastAPI (`backend/precognito/api.py` or new `auth.py`) that extracts the session cookie/token from incoming requests and verifies it against the `session` table in PostgreSQL.
3. **Protect Endpoints**:
   - Apply this dependency to protected FastAPI routes (e.g., `/ingest`, `/alerts`).

## Verification & Testing
1. **Infrastructure**: Verify PostgreSQL (port 5432) and InfluxDB (port 8086) are running and accessible.
2. **Database Schema**: Verify `better-auth` successfully creates the required tables (`user`, `session`, `account`, etc.) in PostgreSQL upon initialization.
3. **Authentication Flow**:
   - Test user registration (if enabled) or manual user creation.
   - Test login and verify a session cookie is set.
   - Attempt to access `/dashboard` while logged out (expect redirect).
4. **Backend Security**: Send an API request to FastAPI without a valid session cookie and verify it returns `401 Unauthorized`.
