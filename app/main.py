from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.model import calculate_enterprise_stockout

app = FastAPI(title="Enterprise E-Commerce Stock Predictor API", version="2.0")

class EnterpriseInventoryItem(BaseModel):
    sku: str = Field(..., description="Unique Stock Keeping Unit identifier")
    current_stock: int = Field(..., ge=0, description="Units currently available in warehouse")
    base_daily_sales: float = Field(..., ge=0, description="Average baseline units sold per day")
    supplier_lead_time_days: int = Field(7, ge=1, description="Days required for supplier to restock")
    return_rate: float = Field(0.05, ge=0.0, le=1.0, description="Fraction of sales returned (0 to 1)")
    seasonality_index: float = Field(1.0, gt=0.0, description="Multiplier for demand surges/holidays")
    marketing_spend_delta: float = Field(0.0, description="Percentage change in ad budget (e.g., 0.25 for +25%)")
    competitor_price_ratio: float = Field(1.0, gt=0.0, description="Ratio of our price to market average")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Enterprise MLOps Demand-Sensing Predictor is running."}

@app.post("/predict/")
def predict_stockout(item: EnterpriseInventoryItem):
    prediction = calculate_enterprise_stockout(
        current_stock=item.current_stock,
        base_daily_sales=item.base_daily_sales,
        supplier_lead_time_days=item.supplier_lead_time_days,
        return_rate=item.return_rate,
        seasonality_index=item.seasonality_index,
        marketing_spend_delta=item.marketing_spend_delta,
        competitor_price_ratio=item.competitor_price_ratio
    )
    
    return {
        "sku": item.sku,
        **prediction
    }