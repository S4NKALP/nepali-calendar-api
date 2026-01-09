import os
import json
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Nepali Calendar API")

DATA_DIR = "./data"

@app.get("/", summary="Root Endpoint")
async def root():
    return {"message": "Welcome to the Nepali Calendar API. Use /docs for interactive API documentation."}

@app.get("/calendar/{year}", summary="Get Yearly Calendar")
async def get_year_calendar(year: int):
    file_path = f"{DATA_DIR}/{year}.json"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Calendar data for year {year} not found. Please run the scraper for this year.")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/calendar/{year}/{month}", summary="Get Monthly Calendar")
async def get_month_calendar(year: int, month: int):
    file_path = f"{DATA_DIR}/{year}/{month}.json"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Calendar data for {year}/{month} not found. Please run the scraper for this year.")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
