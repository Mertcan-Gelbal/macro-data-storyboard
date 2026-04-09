"""
MacroData Storyboard - Institutional Global Financial Terminal
Professional Grade Macro Intelligence System
"""
import sys
import os
from datetime import datetime, timedelta

# --- GLOBAL PLATFORM PATCH ---
if sys.platform == "darwin":
    try:
        import selectors
        if hasattr(selectors, 'KqueueSelector'):
            selectors.DefaultSelector = selectors.SelectSelector
    except: pass

import streamlit as st
import pandas as pd
from data.indicators import get_indicator_list, get_indicator_info, INDICATORS
from services.data_fetcher import fetch_data
from services.stats_analyzer import analyze_stats
from services.commentary_generator import generate_commentary
from components.charts import render_line_chart
from components.summary_cards import render_summary_cards
from utils.helpers import get_date_ranges, format_date, get_cached_indicators

# Page Configuration - Institutional Standard
st.set_page_config(
    page_title="MacroData | Institutional",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Institutional Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0B0E14; }
    
    /* Institutional Metric Cards */
    [data-testid="metric-container"] {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 4px;
        padding: 20px;
    }
    
    .section-label {
        color: #8B949E;
        font-size: 0.65rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 2px;
    }
    
    .terminal-header {
        font-size: 2.4rem;
        font-weight: 700;
        color: #F0F6FC;
        margin-bottom: 25px;
        border-bottom: 1px solid #30363D;
        padding-bottom: 10px;
    }

    /* Professional Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 4px 4px 0 0;
        color: #8B949E;
        font-weight: 500;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1F242C !important;
        color: #58A6FF !important;
        border-bottom: 2px solid #58A6FF !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Asset Registry
with st.sidebar:
    st.markdown("### ASSET REGISTRY")
    
    cats = sorted(list(set(v['category'] for v in INDICATORS.values())))
    selection = []
    for cat in cats:
        with st.expander(cat.upper(), expanded=(cat == "Indices: Americas")):
            cat_options = [k for k, v in INDICATORS.items() if v['category'] == cat]
            for opt in cat_options:
                if st.checkbox(INDICATORS[opt]['name'], key=f"sel_{opt}", value=(opt in ["sp500", "gold"])):
                    selection.append(opt)
    
    st.markdown("---")
    st.markdown("### ANALYTICS CONTROL")
    show_reg = st.toggle("Trend Regressions", False)
    norm_base = st.toggle("Normalize Series (Base 100)", True)
    
    st.markdown("---")
    st.markdown("### TIME HORIZON")
    horizon = st.selectbox("Historical Window", list(get_date_ranges().keys()) + ["Custom"], index=3)
    
    ranges = get_date_ranges()
    start_date, end_date = None, None
    if horizon == "Custom":
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
    else:
        s, e = ranges[horizon]
        start_date, end_date = format_date(s), None

    if st.button("INITIALIZE SYSTEM CACHE", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# --- MAIN INTERFACE ---
st.markdown('<p class="section-label">Institutional Analysis Environment</p>', unsafe_allow_html=True)
st.markdown('<h1 class="terminal-header">Global Data Terminal</h1>', unsafe_allow_html=True)

if not selection:
    st.info("System Ready. Please select assets from the Registry to begin.")
    st.stop()

# --- SILENT DATA SYNCHRONIZATION ---
dfs, stats_list, names = [], [], []
failed_streams = []

with st.status("Establishing Global Data Uplinks...", expanded=False) as status:
    for sym in selection:
        try:
            df = fetch_data(sym, start_date, end_date)
            if not df.empty:
                if norm_base and len(df) > 1:
                    base_val = df['value'].iloc[0]
                    if base_val != 0: df['value'] = (df['value'] / base_val) * 100
                
                dfs.append(df)
                stats_list.append(analyze_stats(df))
                names.append(INDICATORS[sym]['name'])
            else:
                failed_streams.append(INDICATORS[sym]['name'])
        except:
            failed_streams.append(INDICATORS[sym]['name'])
    
    status.update(label="System Synchronized", state="complete")

# --- INTERFACE TABS ---
tab_dashboard, tab_analysis, tab_insign, tab_export = st.tabs([
    "Market Dashboard", 
    "Trend Analytics", 
    "Intelligence Report",
    "Data Hub"
])

# Global connectivity note (if any)
if failed_streams:
    with st.expander("Connectivity Status Note"):
        st.info(f"The following data streams are currently offline or unavailable for the selected range: {', '.join(failed_streams)}")

if dfs:
    with tab_dashboard:
        st.markdown('<p class="section-label">Core Performance Metrics</p>', unsafe_allow_html=True)
        render_summary_cards(dfs, names, stats_list)
        
        st.markdown("---")
        st.markdown("#### Performance Comparison Matrix")
        matrix_data = []
        for n, s in zip(names, stats_list):
            if not s: continue
            
            latest = s.get('latest', 0)
            mean = s.get('mean', 0)
            std = s.get('std', 0)
            
            matrix_data.append({
                "Asset Identifier": n,
                "Current Value": f"{latest:.2f}",
                "Period Mean": f"{mean:.2f}",
                "Volatility (StdDev)": f"{std:.2f}",
                "Period Change (%)": f"{s.get('period_change_pct', 0):.2f}%",
                "Historical Max": f"{s.get('max', 0):.2f}"
            })
        if matrix_data:
            st.table(pd.DataFrame(matrix_data))

    with tab_analysis:
        st.markdown('<p class="section-label">Time Series Convergence</p>', unsafe_allow_html=True)
        render_line_chart(dfs, names)
        
        if show_reg:
            from components.charts import render_trend_line
            st.markdown("---")
            st.markdown("#### Linear Projections")
            for d, s, n in zip(dfs, stats_list, names):
                with st.expander(f"View Projection: {n}"):
                    render_trend_line(d, s)

    with tab_insign:
        st.markdown('<p class="section-label">Quantitative Analysis Report</p>', unsafe_allow_html=True)
        cols = st.columns(len(names))
        for i, (name, stats) in enumerate(zip(names, stats_list)):
            with cols[i % len(cols)]:
                st.markdown(f"**Asset Summary: {name}**")
                st.write(generate_commentary(stats))
                st.markdown("---")

    with tab_export:
        st.markdown('<p class="section-label">Data Extraction</p>', unsafe_allow_html=True)
        export_df = pd.DataFrame()
        for d, n in zip(dfs, names):
            t = d.copy()
            t.columns = ['Timestamp', n]
            export_df = t if export_df.empty else pd.merge(export_df, t, on='Timestamp', how='outer')
        
        st.dataframe(export_df, use_container_width=True)
        
        st.download_button(
            "Export as CSV (Professional)",
            data=export_df.to_csv(index=False).encode('utf-8'),
            file_name=f"terminal_export_{datetime.now().strftime('%Y%m%d')}.csv",
            use_container_width=True
        )

else:
    st.error("Protocol Error: No synchronized data available. Please adjust asset selection or time horizon.")

# System Footer
st.markdown('<p style="font-size: 0.6rem; color: #444; text-align: center; margin-top: 60px; letter-spacing: 0.5px;">PROPRIETARY ALGORITHMIC CORE V2.2 | INSTITUTIONAL DATA ACCESS</p>', unsafe_allow_html=True)
