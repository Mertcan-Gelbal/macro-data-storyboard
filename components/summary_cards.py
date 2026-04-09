"""Summary metric cards."""

import streamlit as st
from typing import Dict, List, Any
import pandas as pd

def render_summary_cards(dfs: List[pd.DataFrame], symbols: List[str], stats_list: List[Dict[str, Any]]):
    """Render stats cards for each indicator."""
    for df, symbol, stats in zip(dfs, symbols, stats_list):
        if df.empty or not stats:
            continue
            
        st.markdown(f"#### {symbol}")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("LATEST VALUE", f"{stats['latest']:.2f}", delta=f"{stats['period_change_pct']:+.1f}%")
        with c2:
            st.metric("PERIOD AVERAGE", f"{stats['average']:.2f}")
        with c3:
            st.metric("RANGE (MIN / MAX)", f"{stats['min']:.2f} / {stats['max']:.2f}")
        st.markdown("<br>", unsafe_allow_html=True)

