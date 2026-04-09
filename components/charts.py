"""Plotly chart components."""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import List
import pandas as pd

def render_line_chart(dfs: List[pd.DataFrame], symbols: List[str], chart_type: str = "Line", height: int = 500):
    """Render interactive line or area chart with multiple series."""
    fig = go.Figure()
    
    colors = px.colors.qualitative.Plotly
    
    for i, (df, symbol) in enumerate(zip(dfs, symbols)):
        if not df.empty:
            color = colors[i % len(colors)]
            
            # Main series
            fill_mode = 'toself' if chart_type == "Area" else None
            fig.add_trace(go.Scatter(
                x=df['date'], y=df['value'],
                mode='lines',
                name=symbol,
                fill=fill_mode,
                line=dict(color=color, width=2.5),
            ))
            
            # Highlight latest point
            fig.add_trace(go.Scatter(
                x=[df['date'].iloc[-1]], y=[df['value'].iloc[-1]],
                mode='markers+text',
                marker=dict(color=color, size=12, symbol='star', line=dict(width=2, color='white')),
                text=[f"Latest: {df['value'].iloc[-1]:.2f}"],
                textposition="top right",
                name=f"{symbol} (latest)",
                showlegend=False
            ))

            # Mark Period High and Low
            high_idx = df['value'].idxmax()
            low_idx = df['value'].idxmin()
            
            fig.add_trace(go.Scatter(
                x=[df['date'].iloc[high_idx]], y=[df['value'].iloc[high_idx]],
                mode='markers',
                marker=dict(color='lightgreen', size=8, symbol='triangle-up'),
                name='Period High',
                hoverinfo='text',
                text=[f"High: {df['value'].iloc[high_idx]:.2f}"],
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=[df['date'].iloc[low_idx]], y=[df['value'].iloc[low_idx]],
                mode='markers',
                marker=dict(color='coral', size=8, symbol='triangle-down'),
                name='Period Low',
                hoverinfo='text',
                text=[f"Low: {df['value'].iloc[low_idx]:.2f}"],
                showlegend=False
            ))
    
    fig.update_layout(
        title=f"Macroeconomic Indicators ({chart_type} View)",
        xaxis_title="Date",
        yaxis_title="Value",
        height=height,
        template="plotly_dark",
        hovermode='x unified',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_trend_line(df: pd.DataFrame, stats: dict):
    """Optional trend line overlay."""
    if len(df) < 2:
        return
    
    x = list(range(len(df)))
    slope = stats['trend_slope']
    intercept = df['value'].iloc[0] - slope * x[0]
    trend_y = [slope * xi + intercept for xi in x]
    
    trend_dir = "Upward" if slope > 0 else "Downward" if slope < 0 else "Flat"
    st.info(f"**{trend_dir} trend** (slope: {slope:.4f})")

