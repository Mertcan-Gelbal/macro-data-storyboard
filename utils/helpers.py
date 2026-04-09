"""Utility functions."""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

def get_date_ranges():
    """Get predefined date ranges."""
    end_date = datetime.now()
    ranges = {
        "1M": (end_date - timedelta(days=30), end_date),
        "3M": (end_date - timedelta(days=90), end_date),
        "6M": (end_date - timedelta(days=180), end_date),
        "1Y": (end_date - timedelta(days=365), end_date),
        "3Y": (end_date - timedelta(days=3*365), end_date),
        "5Y": (end_date - timedelta(days=5*365), end_date),
        "MAX": (None, end_date)
    }
    return ranges

def format_date(date_obj) -> str:
    """Format date for AKShare (YYYYMMDD)."""
    if date_obj is None:
        return None
    dt = pd.to_datetime(date_obj)
    return dt.strftime("%Y%m%d")

@st.cache_data
def get_cached_indicators():
    """Cached indicator list."""
    from data.indicators import get_indicator_list
    return get_indicator_list()

