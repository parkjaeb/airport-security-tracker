from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import random

app = FastAPI()

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
def get_wait_times(airport_id: str):
    # Simple mock checkpoints
    checkpoints = [
        {
            "name": "General Checkpoint A",
            "type": "General",
            "waitTimeMinutes": random.randint(10, 30),
            "historicalAverage": 20,
        },
        {
            "name": "PreCheck Checkpoint B",
            "type": "PreCheck",
            "waitTimeMinutes": random.randint(5, 15),
            "historicalAverage": 10,
        },
        {
            "name": "Premium Checkpoint C",
            "type": "Premium",
            "waitTimeMinutes": random.randint(2, 8),
            "historicalAverage": 5,
        },
    ]

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
        "checkpoints": checkpoints,
        "historicalData": historical_data,
    }