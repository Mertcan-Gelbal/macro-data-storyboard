"""
Synchronous Fetching Engine for the Proxy API
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data.catalog import INDICATORS

def fetch_indicator_data(symbol: str, horizon: str = "1Y"):
    """Fetch and standardize data for the given symbol."""
    if symbol not in INDICATORS:
        return None
    
    try:
        info = INDICATORS[symbol]
        fetch_func = info['fetch_func']
        df_raw = fetch_func()
        
        # Standardize columns
        date_cols = ['日期', 'date', 'Date', '时间', 'time', '公布日期', 'Timestamp', 'last_update']
        date_col = next((col for col in date_cols if col in df_raw.columns), None)
        
        if date_col:
            df_raw = df_raw.rename(columns={date_col: 'date'})
        else:
            df_raw = df_raw.reset_index().rename(columns={df_raw.columns[0]: 'date'})
            
        val_cols = ['value', 'Value', '利率', 'rate', '今值', '数值', '价格', '指数', '收盘', 'close', 'settle', 'price', '10.0']
        val_col = next((col for col in val_cols if col in df_raw.columns), df_raw.columns[1])
        
        df_raw['value'] = pd.to_numeric(df_raw[val_col], errors='coerce')
        df_raw['date'] = pd.to_datetime(df_raw['date'], errors='coerce')
        df_raw = df_raw.dropna(subset=['date', 'value']).sort_values('date')
        
        # Apply Horizon Filter
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365) # Default 1Y
        if horizon == "3M": start_date = end_date - timedelta(days=90)
        elif horizon == "5Y": start_date = end_date - timedelta(days=1825)
        
        df_raw = df_raw[df_raw['date'] >= start_date]
        
        # Return as list of dicts for JSON serialization
        return df_raw.rename(columns={'date': 'x', 'value': 'y'}).to_dict(orient='records')
        
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def get_stats(data):
    """Calculate basic stats for the data range."""
    if not data: return {}
    y_values = [d['y'] for d in data]
    return {
        "latest": y_values[-1],
        "mean": sum(y_values) / len(y_values),
        "min": min(y_values),
        "max": max(y_values),
        "change_pct": ((y_values[-1] - y_values[0]) / y_values[0] * 100) if y_values[0] != 0 else 0
    }
