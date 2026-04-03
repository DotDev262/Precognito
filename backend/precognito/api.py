from fastapi import FastAPI, Request, HTTPException, Depends
from typing import Optional
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://precognito_user:precognito_password@localhost:5432/precognito")

app = FastAPI()

async def get_db_pool():
    if not hasattr(app, "db_pool"):
        app.db_pool = await asyncpg.create_pool(DATABASE_URL)
    return app.db_pool

async def get_current_user(request: Request, pool = Depends(get_db_pool)):
    session_token = request.cookies.get("better-auth.session_token")
    if not session_token:
        # Check Authorization header too
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header.split(" ")[1]

    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    async with pool.acquire() as conn:
        # Better Auth stores sessions in 'session' table
        session = await conn.fetchrow(
            'SELECT "userId", "expiresAt" FROM "session" WHERE "token" = $1',
            session_token
        )

        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")

        # Check expiry (asyncpg returns datetime)
        from datetime import datetime, timezone
        if session["expiresAt"].replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Session expired")

        user = await conn.fetchrow(
            'SELECT * FROM "user" WHERE "id" = $1',
            session["userId"]
        )
        return user

@app.get("/")
def home():
    return {"message": "Precognito Backend Running"}

@app.post("/ingest")
async def ingest_data(data: dict, user = Depends(get_current_user)):
    from precognito.ingestion.core import process_ingestion

    device_id = data.get("device_id")
    if not device_id:
        raise HTTPException(status_code=400, detail="device_id is required")

    result = process_ingestion(device_id, data)
    
    if not result:
        raise HTTPException(status_code=500, detail="Ingestion processing failed")

    return {
        **result,
        "status": "success",
        "user": user["name"]
    }

@app.get("/assets")
async def get_assets(user = Depends(get_current_user)):
    from precognito.ingestion.influx_client import get_all_devices, query_latest_data
    
    device_ids = get_all_devices()
    assets = []
    
    for d_id in device_ids:
        # Get latest telemetry
        tel_tables = query_latest_data(d_id, "machine_telemetry")
        # Get latest prediction
        pred_tables = query_latest_data(d_id, "predictive_results")
        
        asset_info = {
            "id": d_id,
            "name": d_id.replace("_", " ").title(),
            "status": "GREEN", # Default
            "rms": 0.0,
            "rul": 0.0,
            "lastUpdated": None
        }
        
        if tel_tables:
            for table in tel_tables:
                for record in table.records:
                    if record.get_field() == "vibration_rms":
                        asset_info["rms"] = record.get_value()
                    asset_info["lastUpdated"] = record.get_time().isoformat()
        
        if pred_tables:
            for table in pred_tables:
                for record in table.records:
                    if record.get_field() == "predicted_rul_hours":
                        asset_info["rul"] = record.get_value()
                    if record.get_field() == "risk_level":
                        risk = record.get_value()
                        if risk == "High-Risk": asset_info["status"] = "RED"
                        elif risk == "Warning": asset_info["status"] = "YELLOW"
        
        assets.append(asset_info)
        
    return assets

@app.get("/assets/{device_id}/telemetry")
async def get_asset_telemetry(device_id: str, range: str = "-24h", user = Depends(get_current_user)):
    from precognito.ingestion.influx_client import query_historical_data
    
    tables = query_historical_data(device_id, "machine_telemetry", range)
    results = []
    
    for table in tables:
        for record in table.records:
            results.append(record.values)
            
    return results

@app.get("/assets/{device_id}/predictions")
async def get_asset_predictions(device_id: str, range: str = "-24h", user = Depends(get_current_user)):
    from precognito.ingestion.influx_client import query_historical_data
    
    tables = query_historical_data(device_id, "predictive_results", range)
    results = []
    
    for table in tables:
        for record in table.records:
            results.append(record.values)
            
    return results

@app.get("/alerts")
async def get_all_alerts(range: str = "-24h", user = Depends(get_current_user)):
    from precognito.ingestion.influx_client import INFLUX_BUCKET, INFLUX_ORG, query_api
    
    query = f'from(bucket: "{INFLUX_BUCKET}") |> range(start: {range}) |> filter(fn: (r) => r["_measurement"] == "anomaly_results") |> filter(fn: (r) => r["_field"] == "anomaly_detected") |> filter(fn: (r) => r["_value"] == true) |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
    
    tables = query_api.query(query, org=INFLUX_ORG)
    results = []
    
    for table in tables:
        for record in table.records:
            results.append({
                "id": f"{record.get_time().timestamp()}-{record.values.get('device_id')}",
                "deviceId": record.values.get("device_id"),
                "severity": record.values.get("severity"),
                "message": record.values.get("reason"),
                "timestamp": record.get_time().isoformat(),
                "acknowledged": False
            })
            
    # Sort by timestamp descending
    results.sort(key=lambda x: x["timestamp"], reverse=True)
    return results

@app.post("/ingest/dev")
async def ingest_data_dev(data: dict):
    """Unauthenticated ingestion for development/testing"""
    from precognito.ingestion.core import process_ingestion

    device_id = data.get("device_id")
    if not device_id:
        raise HTTPException(status_code=400, detail="device_id is required")

    result = process_ingestion(device_id, data)
    
    if not result:
        raise HTTPException(status_code=500, detail="Ingestion processing failed")

    return {
        **result,
        "status": "success",
        "user": "dev_user"
    }

@app.get("/heartbeats")
async def get_heartbeats():
    from precognito.ingestion.heartbeat import device_status
    from datetime import datetime
    
    results = []
    for device_id, last_seen in device_status.items():
        diff = (datetime.now() - last_seen).seconds
        status = "Active" if diff <= 5 else "Inactive"
        results.append({
            "deviceId": device_id,
            "lastSeen": last_seen.isoformat(),
            "status": status,
            "secondsSinceLast": diff
        })
    return results

@app.on_event("startup")
async def startup():
    await get_db_pool()

@app.on_event("shutdown")
async def shutdown():
    if hasattr(app, "db_pool"):
        await app.db_pool.close()