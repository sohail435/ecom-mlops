from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Dabbubu Inventory Microservice", version="1.0.0")

class PredictionInput(BaseModel):
    sku: str = Field(..., example="SKU-PROMO-01")
    current_stock: int = Field(..., ge=0, example=120)
    base_daily_sales: float = Field(..., gt=0, example=15.0)
    supplier_lead_time_days: int = Field(..., gt=0, example=10)
    return_rate: float = Field(..., ge=0.0, le=1.0, example=0.08)
    seasonality_index: float = Field(..., gt=0, example=1.4)
    marketing_spend_delta: float = Field(..., example=0.20)
    competitor_price_ratio: float = Field(..., gt=0, example=0.95)

@app.post("/predict/")
def predict_stockout(payload: PredictionInput):
    try:
        # Core demand-sensing calculation model logic
        adjusted_sales = payload.base_daily_sales * payload.seasonality_index * (1 + payload.marketing_spend_delta)
        net_daily_sales = adjusted_sales * (1 - payload.return_rate)
        
        # Avoid division by zero
        net_daily_sales = max(net_daily_sales, 0.01)
        
        days_until_stockout = round(payload.current_stock / net_daily_sales, 1)
        action_required = days_until_stockout <= payload.supplier_lead_time_days
        
        risk_level = "Critical" if action_required else "Stable"
        
        return {
            "sku": payload.sku,
            "adjusted_projected_daily_sales": round(net_daily_sales, 2),
            "estimated_days_until_stockout": days_until_stockout,
            "risk_level": risk_level,
            "action_required": action_required
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))