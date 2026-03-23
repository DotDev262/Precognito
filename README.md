# Precognito

AI-powered predictive maintenance platform designed to eliminate unplanned downtime. By analyzing real-time IoT sensor telemetry and historical patterns, it identifies anomalies and predicts Remaining Useful Life (RUL) before failures occur.

## Project Structure

```
precognito/
├── frontend/              # Next.js PWA
│   ├── src/
│   │   ├── app/          # Pages (Next.js App Router)
│   │   ├── components/   # React components
│   │   └── lib/          # Types, mock data, auth
│   └── public/            # Static assets
│
├── backend/               # FastAPI Python package
│   ├── precognito/       # Main package
│   │   ├── __init__.py
│   │   ├── anomaly/     # Anomaly detection
│   │   ├── dashboard/    # Dashboard API
│   │   ├── financial/    # Financial analytics
│   │   ├── ingestion/    # IoT data ingestion
│   │   ├── predictive/   # RUL prediction
│   │   └── work_orders/  # Work order management
│   ├── tests/            # Unit tests
│   ├── pyproject.toml    # Python dependencies
│   └── uv.lock           # Locked dependencies
│
├── BRD.md                 # Business Requirements Document
└── README.md
```

## Getting Started

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| [Bun](https://bun.sh) | Latest | Frontend runtime |
| [uv](https://github.com/astral-sh/uv) | Latest | Python package manager |
| Python | 3.12+ | Backend runtime |

### Frontend Setup

```bash
cd frontend
bun install
bun run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate

# Run development server
uv run uvicorn precognito.api:app --reload
```

Open API docs at [http://localhost:8000/docs](http://localhost:8000/docs)

## Backend Modules

| Module | Description | Status |
|--------|-------------|--------|
| `anomaly` | Anomaly detection engine | Planned |
| `dashboard` | Dashboard API endpoints | Planned |
| `financial` | Financial analytics | Planned |
| `ingestion` | IoT data ingestion (MQTT) | Planned |
| `predictive` | RUL prediction models | Planned |
| `work_orders` | Work order management | Planned |

## Frontend Pages

| Route | Description | Access |
|-------|-------------|--------|
| `/` | Landing page | Public |
| `/login` | Login (role selection) | Public |
| `/dashboard` | Role-based dashboard | All roles |
| `/assets` | Asset health monitoring | Admin, Manager, OT, Tech |
| `/assets/[id]` | Asset detail + FFT | Admin, Manager, OT, Tech |
| `/alerts` | Alert feed | Admin, OT, Tech |
| `/edge` | Sensor connectivity | Admin, OT |
| `/reports` | Report generation | Admin, Manager |
| `/inventory` | Spare parts management | Admin, Store |
| `/work-orders` | Field check-in & docs | Admin, Tech |
| `/executive` | Financial analytics | Admin, Manager |
| `/analytics` | Model performance | Admin, Manager |
| `/ehs` | Thermal safety alerts | Admin, OT |
| `/admin` | User management | Admin |

## User Roles

| Role | Description |
|------|-------------|
| **Admin** | Full access + user management |
| **Plant Manager** | Executive dashboards, reports |
| **OT Specialist** | Monitoring, alerts, sensors |
| **Technician** | Work orders, field operations |
| **Store Manager** | Inventory management |

**Demo Login:** Any credentials work. Select a role to test different permission levels.

## Testing

```bash
# Frontend build
cd frontend && bun run build

# Backend tests
cd backend && uv run pytest tests/
```

## Tech Stack

### Frontend
- Next.js 16 (App Router)
- React 19
- TypeScript
- Tailwind CSS v4
- Recharts
- Bun runtime

### Backend
- FastAPI
- SQLAlchemy + AsyncPG
- InfluxDB
- Paho-MQTT
- scikit-learn
- Python 3.12+

## Documentation

- [BRD.md](./BRD.md) - Business Requirements Document

## License

MIT License - see [LICENSE](./LICENSE) for details.
