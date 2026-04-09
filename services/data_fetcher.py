"""Data fetching service with caching."""

import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from data.indicators import INDICATORS, get_indicator_info

@st.cache_data
def fetch_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch data for indicator in date range.
    Handles different AKShare output formats to standardize to date/value.
    """
    try:
        info = get_indicator_info(symbol)
        fetch_func = info['fetch_func']
        kwargs = info.get('kwargs', {})
        
        # Fetch data with potential kwargs
        df_raw = fetch_func(**kwargs) if kwargs else fetch_func()
        
        # Standardize to 'date' and 'value' columns (handle common AKShare formats)
        date_cols = ['日期', 'date', 'Date', '时间', 'time', '公布日期', 'Timestamp', 'last_update', '交易时间']
        date_col = next((col for col in date_cols if col in df_raw.columns), None)
        
        if date_col:
            df_raw = df_raw.rename(columns={date_col: 'date'})
        else:
            # Fallback for simple series or index-based data
            df_raw = df_raw.reset_index()
            df_raw = df_raw.rename(columns={df_raw.columns[0]: 'date'})
        
        # Values can have various names in Chinese or English
        val_cols = [
            'value', 'Value', '利率', 'rate', 'Rate', 'index', 'Index', 
            '失业率', '今值', '数值', '价格', '增长率', '数据', '指数', '收盘', 'close', 'Close',
            '晚盘价', '早盘价', '10.0', '10年', '收益率', 'settle', 'Settle', 'price', 'Price'
        ]
        val_col_candidates = [col for col in val_cols if col in df_raw.columns]
        val_col = val_col_candidates[0] if val_col_candidates else df_raw.columns[1]
        
        # Convert values to numeric
        df_raw['value'] = pd.to_numeric(df_raw[val_col], errors='coerce')
        
        # Filter by date range
        df_raw['date'] = pd.to_datetime(df_raw['date'], errors='coerce')
        df_raw = df_raw.dropna(subset=['date', 'value'])
        df_raw = df_raw.sort_values('date')
        
        if not df_raw.empty:
            if start_date:
                df_raw = df_raw[df_raw['date'] >= pd.to_datetime(start_date)]
            if end_date:
                df_raw = df_raw[df_raw['date'] <= pd.to_datetime(end_date)]
        
        if df_raw.empty:
            st.warning(f"No data available for {symbol} in selected range.")
            return pd.DataFrame()
            
        return df_raw[['date', 'value']].reset_index(drop=True)
        
    except Exception as e:
        st.error(f"Error fetching {symbol}: {str(e)}")
        # If it's a connection issue or API change, log more details
        print(f"DEBUG: Failed to fetch {symbol}. Error: {e}")
        return pd.DataFrame()

