import asyncio
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import data

app = FastAPI(title="Stock Data Intelligence Dashboard", version="1.0.0")

# CORS middleware for potential independent frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the static HTML frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Serves the main Frontend Dashboard"""
    return FileResponse('static/index.html')

@app.get("/companies")
async def get_companies():
    """Returns list of available companies"""
    return data.get_company_list()

@app.get("/data/{symbol}")
async def get_stock_data(symbol: str, days: int = Query(30, description="Number of recent days to fetch")):
    """Returns recent stock data along with processed ML analytics in JSON format"""
    try:
        # Advanced Feature: Run pandas workloads in background executor to keep concurrency high
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, data.get_recent_data, symbol, days)
        return {"symbol": symbol, "data": result}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/summary/{symbol}")
async def get_summary(symbol: str):
    """Returns 52-week high, low, and averages"""
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, data.get_stock_summary, symbol)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/compare")
async def get_comparison(symbol1: str, symbol2: str):
    """Compares the statistical performance between two stocks (Bonus Endpoint)"""
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, data.compare_stocks, symbol1, symbol2)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/top-movers")
async def get_top_movers():
    """Returns the top gainer and top loser of the day."""
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, data.get_top_movers)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
