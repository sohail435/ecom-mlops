def calculate_dynamic_pricing(
    base_cost: float,
    current_price: float,
    competitor_price: float,
    current_stock: int,
    safety_stock_threshold: int = 20
) -> dict:
    """
    Computes optimal pricing and tactical recommendations based on 
    competitor intelligence and inventory buffer constraints.
    """
    # 1. Calculate Competitor Price Ratio
    competitor_ratio = current_price / competitor_price if competitor_price > 0 else 1.0
    
    # 2. Determine Inventory Pressure Multiplier
    if current_stock <= safety_stock_threshold:
        stock_modifier = 1.05  # 5% scarcity margin protection
        strategy = "Scarcity Margin Protection (Low Stock)"
    elif current_stock > (safety_stock_threshold * 4):
        stock_modifier = 0.92  # 8% clearance discount to free capital
        strategy = "Excess Inventory Liquidation"
    else:
        stock_modifier = 1.00  
        strategy = "Optimal Market Alignment"

    # 3. Factor in Competitor Positioning
    if competitor_ratio > 1.10:
        recommended_adjustment = -0.05  # Match market downward pressure
        market_stance = "Competitive Threat: Overpriced"
    elif competitor_ratio < 0.90:
        recommended_adjustment = +0.05  # Capture margin upside
        market_stance = "Margin Expansion Opportunity: Underpriced"
    else:
        recommended_adjustment = 0.00
        market_stance = "Market Parity"

    # 4. Compute Final Optimal Price
    net_multiplier = stock_modifier + recommended_adjustment
    optimal_price = round(current_price * net_multiplier, 2)
    
    # Floor price safeguard (preventing loss-leading below base cost)
    if optimal_price < base_cost:
        optimal_price = base_cost
        strategy = "Floor Price Enforced (Cost Protection)"

    projected_margin_pct = round(((optimal_price - base_cost) / optimal_price) * 100, 2) if optimal_price > 0 else 0.0

    return {
        "current_price": current_price,
        "competitor_price": competitor_price,
        "optimal_recommended_price": optimal_price,
        "projected_margin_percentage": projected_margin_pct,
        "pricing_strategy": strategy,
        "market_stance": market_stance
    }