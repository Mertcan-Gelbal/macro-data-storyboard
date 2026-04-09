"""
Global Macro Intelligence API Server - Vercel Final Edition
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .data.catalog import INDICATORS
from .services.fetcher import fetch_indicator_data, get_stats
from typing import Optional

app = FastAPI(title="MacroData API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "MacroData System Operational", "platform": "Vercel Edge"}

@app.get("/api/indicators")
async def list_indicators():
    return [{"id": k, "name": v["name"], "category": v["category"]} for k, v in INDICATORS.items()]

@app.get("/api/data/{symbol}")
async def get_data(symbol: str, horizon: Optional[str] = "1Y"):
    data = fetch_indicator_data(symbol, horizon)
    if not data:
        raise HTTPException(status_code=404, detail="Asset data unavailable")
    return {"symbol": symbol, "name": INDICATORS[symbol]["name"], "stats": get_stats(data), "series": data}
