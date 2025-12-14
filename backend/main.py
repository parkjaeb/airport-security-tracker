from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import random
from typing import Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import random

app = FastAPI()

# In-memory store (resets on deploy/restart)
REPORTS: Dict[str, Dict[str, int]] = {}
LAST_UPDATED: Dict[str, str] = {}

# Allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "Airport Security Tracker API running"}

@app.get("/test")
def test():
    return {"message": "test endpoint works"}

@app.get("/api/wait-times/{airport_id}")
def get_wait_times(airport_id: str) -> Dict[str, Any]:
    checkpoints = [
        {"name": "General Checkpoint A", "type": "General", "historicalAverage": 20},
        {"name": "PreCheck Checkpoint B", "type": "PreCheck", "historicalAverage": 10},
        {"name": "Premium Checkpoint C", "type": "Premium", "historicalAverage": 5},
    ]

    reported_for_airport = REPORTS.get(airport_id, {})

    # Fill waitTimeMinutes either from reports or random mock baseline
    for cp in checkpoints:
        cp_type = cp["type"]
        cp["waitTimeMinutes"] = reported_for_airport.get(
            cp_type,
            random.randint(max(1, cp["historicalAverage"] - 5), cp["historicalAverage"] + 10),
        )

    # Fake 24-hour historical data per checkpoint type
    historical_data = []
    now = datetime.utcnow()
    for cp in checkpoints:
        base = cp["historicalAverage"]
        for hour_offset in range(24):
            # older = bigger hour_offset
            noise = random.uniform(-5, 5)
            value = max(2, round(base + noise))
            historical_data.append(
                {
                    "hourOffset": hour_offset,   # 0–23
                    "avgWait": value,
                    "type": cp["type"],
                }
            )

    return {
        "airportId": airport_id,
        "lastUpdated" : LAST_UPDATED.get(airport_id),
        "checkpoints": checkpoints,
        "historicalData": historical_data,
    }

class WaitTimeReport(BaseModel):
    airportId: str = Field(..., min_length=1)
    checkpointType: str = Field(..., pattern="^(General|PreCheck|Premium)$")
    reportedMinutes: int = Field(..., ge=1, le=180)

@app.post("/api/report-wait-time")
def report_wait_time(payload: WaitTimeReport):
    airport_id = payload.airportId
    cp_type = payload.checkpointType
    minutes = payload.reportedMinutes

    # Initialize airport entry if missing
    if airport_id not in REPORTS:
        REPORTS[airport_id] = {}

    # Simple smoothing: blend new report with previous value if exists
    prev = REPORTS[airport_id].get(cp_type)
    if prev is None:
        updated = minutes
    else:
        updated = round((prev * 0.6) + (minutes * 0.4))

    REPORTS[airport_id][cp_type] = updated
    LAST_UPDATED[airport_id] = datetime.now(timezone.utc).isoformat()

    return {
        "status": "ok",
        "airportId": airport_id,
        "checkpointType": cp_type,
        "appliedWaitTimeMinutes": updated,
        "lastUpdated": LAST_UPDATED[airport_id],
    }