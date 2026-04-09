"""Rule-based commentary generator."""

from typing import Dict, Any

def generate_commentary(stats: Dict[str, Any], period: str = "selected period") -> str:
    """Generate analytical commentary based on stats."""
    if not stats:
        return "No data available for analysis."
    
    comments = []
    
    # Trend
    trend_map = {
        'upward': f"showing {stats['trend_direction']} trend over the {period}",
        'downward': f"showing {stats['trend_direction']} trend over the {period}",
        'sideways': f"trading sideways over the {period}"
    }
    comments.append(trend_map.get(stats['trend_direction'], ""))
    
    # Current position
    latest = stats['latest']
    if stats.get('near_high'):
        comments.append(f"Current value {latest:.2f} near long-term high of {stats['max']:.2f}")
    elif stats.get('near_low'):
        comments.append(f"Current value {latest:.2f} near long-term low of {stats['min']:.2f}")
    else:
        comments.append(f"Current value {latest:.2f}, average {stats['average']:.2f}")
    
    # Change
    change = stats['period_change_pct']
    if abs(change) > 10:
        dir = "increased" if change > 0 else "decreased"
        comments.append(f"{dir} by {abs(change):.1f}% over the period")
    
    # Volatility
    if stats['volatility'] > 20:
        comments.append("Elevated volatility observed")
    elif stats['volatility'] < 5:
        comments.append("Low volatility environment")
    
    return " | ".join(comments) if comments else "Data stable, no significant patterns."

