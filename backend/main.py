from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    return {
        "airportId": airport_id,
        "checkpoints": [],
        "historicalData": [],
    }