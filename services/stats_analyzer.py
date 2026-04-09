"""Statistical analysis and trend detection - Professional Grade."""
import pandas as pd
import numpy as np
from typing import Dict, Any

def analyze_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute key statistics and trends with high reliability."""
    if df.empty or 'value' not in df.columns:
        return {}
    
    # Core numeric series
    vals = pd.to_numeric(df['value'], errors='coerce').dropna()
    if vals.empty:
        return {}

    # Primary Analytics
    stats = {
        'latest': float(vals.iloc[-1]),
        'mean': float(vals.mean()),
        'std': float(vals.std()),
        'min': float(vals.min()),
        'max': float(vals.max()),
        'period_change_pct': float((vals.iloc[-1] - vals.iloc[0]) / vals.iloc[0] * 100) if vals.iloc[0] != 0 else 0
    }
    
    # Legacy support (keeping 'average' for any internal dependencies)
    stats['average'] = stats['mean']
    
    # Trend slope (linear regression)
    x = np.arange(len(vals))
    slope = np.polyfit(x, vals, 1)[0]
    stats['trend_slope'] = slope
    stats['trend_direction'] = 'upward' if slope > 0 else 'downward' if slope < 0 else 'sideways'
    
    # Position relative to extremes
    full_range = stats['max'] - stats['min']
    stats['pos_high'] = (stats['latest'] - stats['min']) / full_range if full_range > 0 else 0
    stats['near_high'] = stats['pos_high'] > 0.8
    stats['near_low'] = stats['pos_high'] < 0.2
    
    # Volatility (Annualized / Rolling)
    stats['volatility'] = float(vals.pct_change().std() * np.sqrt(252) * 100) if len(vals) > 10 else 0
    
    return stats
