"""
Institutional Global Financial Catalog - API Version
"""
import akshare as ak

INDICATORS = {
    "sp500": {
        "category": "Indices",
        "name": "S&P 500",
        "fetch_func": lambda: ak.index_us_stock_sina(symbol=".INX")
    },
    "nasdaq": {
        "category": "Indices",
        "name": "NASDAQ 100",
        "fetch_func": lambda: ak.index_us_stock_sina(symbol=".IXIC")
    },
    "dax": {
        "category": "Indices",
        "name": "DAX 30",
        "fetch_func": lambda: ak.index_global_hist_em(symbol="德国DAX30")
    },
    "gold": {
        "category": "Commodities",
        "name": "Spot Gold",
        "fetch_func": ak.spot_golden_benchmark_sge
    },
    "dxy": {
        "category": "Forex",
        "name": "US Dollar Index",
        "fetch_func": lambda: ak.index_us_stock_sina(symbol="DXY")
    },
    "us_10y_bond": {
        "category": "Fixed Income",
        "name": "US 10Y Yield",
        "fetch_func": ak.bond_zh_us_rate
    },
    "china_gdp": {
        "category": "Macro",
        "name": "China GDP",
        "fetch_func": ak.macro_china_gdp
    }
}
