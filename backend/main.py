"""
Global Macro Intelligence API Server
Powering the React Native Global Terminal
"""
import sys

# --- GLOBAL PLATFORM PATCH (macOS Support) ---
if sys.platform == "darwin":
    try:
        import selectors
        if hasattr(selectors, 'KqueueSelector'):
            selectors.DefaultSelector = selectors.SelectSelector
    except: pass

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from data.catalog import INDICATORS
from services.fetcher import fetch_indicator_data, get_stats
from typing import Optional

app = FastAPI(title="MacroData API", version="2.0.0")

# Enable CORS for React Native Development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "MacroData System Operational", "engine": "AKShare Core"}

@app.get("/api/indicators")
async def list_indicators():
    """Returns the full catalog of available assets."""
    return [
        {"id": k, "name": v["name"], "category": v["category"]} 
        for k, v in INDICATORS.items()
    ]

@app.get("/api/data/{symbol}")
async def get_data(symbol: str, horizon: Optional[str] = "1Y"):
    """Returns timeseries data and stats for a symbol."""
    data = fetch_indicator_data(symbol, horizon)
    if data is None:
        raise HTTPException(status_code=404, detail="Asset not found or source offline")
    
    return {
        "symbol": symbol,
        "name": INDICATORS[symbol]["name"],
        "stats": get_stats(data),
        "series": data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
