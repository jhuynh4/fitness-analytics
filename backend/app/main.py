from fastapi import FastAPI

app = FastAPI(title="Fitness Analytics API")

@app.get("/health")
def health_check():
    return {"status": "ok"}