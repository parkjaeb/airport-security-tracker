from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random

app = FastAPI()

# Allow your frontend to fetch from this backend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can restrict to your GitHub Pages domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AVAILABLE_AIRPORTS = [
    "SFO_T3",
    "LAX_T1",
    "JFK_T4",
]

def generate_mock_data(airport_id: str):
    code, terminal = airport_id.split("_")

    checkpoints = [
        {
            "name": "General Checkpoint A",
            "type": "General",
            "waitTimeMinutes": random.randint(10, 25),
            "historicalAverage": 20,
        },
        {
            "name": "PreCheck Checkpoint B",
            "type": "PreCheck",
            "waitTimeMinutes": random.randint(5, 12),
            "historicalAverage": 10,
        },
        {
            "name": "Premium Checkpoint C",
            "type": "Premium",
            "waitTimeMinutes": random.randint(2, 6),
            "historicalAverage": 5,
        },
    ]

    historical = []
    for hour in range(24):
        for cp in checkpoints:
            noise = random.randint(-5, 5)
            val = max(2, cp["historicalAverage"] + noise)
            historical.append({
                "hourOffset": hour,
                "avgWait": val,
                "type": cp["type"],
            })

    return {
        "airportId": airport_id,
        "airportCode": code,
        "terminal": terminal,
        "lastUpdated": datetime.utcnow().isoformat() + "Z",
        "checkpoints": checkpoints,
        "historicalData": historical,
    }

@app.get("/api/wait-times/{airport_id}")
def get_wait_times(airport_id: str):
    if airport_id not in AVAILABLE_AIRPORTS:
        airport_id = "SFO_T3"
    return generate_mock_data(airport_id)