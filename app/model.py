def calculate_stockout(current_stock: int, avg_daily_sales: float) -> dict:
    """
    Core prediction logic for inventory depletion.
    """
    if avg_daily_sales <= 0:
        days_remaining = 999  # No immediate risk if sales are zero/negative
    else:
        days_remaining = round(current_stock / avg_daily_sales, 1)
    
    risk_level = "High" if days_remaining <= 7 else "Low"
    
    return {
        "estimated_days_until_stockout": days_remaining,
        "risk_level": risk_level,
        "action_required": risk_level == "High"
    }