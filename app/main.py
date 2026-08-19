from fastapi import FastAPI
from pydantic import BaseModel
from app.model import calculate_stockout

app = FastAPI(title="E-Commerce Stock Predictor API", version="1.0")

class InventoryItem(BaseModel):
    sku: str
    current_stock: int
    avg_daily_sales: float

@app.get("/")
def read_root():
    return {"status": "online", "message": "MLOps Inventory Predictor is running."}

@app.post("/predict/")
def predict_stockout(item: InventoryItem):
    prediction = calculate_stockout(item.current_stock, item.avg_daily_sales)
    
    return {
        "sku": item.sku,
        **prediction
    }