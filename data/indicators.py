"""
Global Financial Intelligence Catalog - Master Version
Professionally mapped global indices, commodities, and macro indicators.
"""
import akshare as ak
from typing import Dict, Any

INDICATORS: Dict[str, Dict[str, Any]] = {
    # --- GLOBAL EQUITY INDICES ---
    "sp500": {
        "category": "Indices: Americas",
        "name": "S&P 500 (USA)",
        "fetch_func": lambda: ak.index_us_stock_sina(symbol=".INX")
    },
    "nasdaq": {
        "category": "Indices: Americas",
        "name": "NASDAQ 100 (USA)",
        "fetch_func": lambda: ak.index_us_stock_sina(symbol=".IXIC")
    },
    "dax": {
        "category": "Indices: Europe",
        "name": "DAX 30 (Germany)",
        "fetch_func": lambda: ak.index_global_hist_em(symbol="德国DAX30")
    },
    "ukx": {
        "category": "Indices: Europe",
        "name": "FTSE 100 (UK)",
        "fetch_func": lambda: ak.index_global_hist_em(symbol="英国富时100")
    },
    "nikkei": {
        "category": "Indices: Asia",
        "name": "Nikkei 225 (Japan)",
        "fetch_func": lambda: ak.index_global_hist_em(symbol="日经225")
    },

    # --- FOREX & FIXED INCOME ---
    "dxy": {
        "category": "Forex: Metrics",
        "name": "US Dollar Index (DXY)",
        "fetch_func": lambda: ak.index_us_stock_sina(symbol="DXY")
    },
    "us_10y_bond": {
        "category": "Forex: Fixed Income",
        "name": "US 10-Year Bond Yield",
        "fetch_func": ak.bond_zh_us_rate
    },
    "usd_try": {
        "category": "Forex: Global",
        "name": "USD / TRY (Spot)",
        "fetch_func": ak.fx_spot_quote
    },

    # --- COMMODITIES ---
    "gold": {
        "category": "Commodities",
        "name": "Spot Gold (SGE)",
        "fetch_func": ak.spot_golden_benchmark_sge
    },
    "brent": {
        "category": "Commodities",
        "name": "Brent Crude Oil",
        "fetch_func": ak.macro_usa_eia_crude_rate
    },

    # --- CORE MACRO ---
    "usa_fed_rate": {
        "category": "Macro: Central Banks",
        "name": "US Fed Rate",
        "fetch_func": ak.macro_bank_usa_interest_rate
    },
    "china_gdp": {
        "category": "Macro: China",
        "name": "China GDP Growth",
        "fetch_func": ak.macro_china_gdp
    }
}

def get_indicator_list() -> list:
    return list(INDICATORS.keys())

def get_indicator_info(symbol: str) -> Dict[str, Any]:
    return INDICATORS.get(symbol, {})
