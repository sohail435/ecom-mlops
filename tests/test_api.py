from fastapi.testclient import TestClient
from app.main import app
from app.model import calculate_enterprise_stockout

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "message": "Enterprise MLOps Demand-Sensing Predictor is running."}

def test_enterprise_model_logic():
    result = calculate_enterprise_stockout(
        current_stock=100,
        base_daily_sales=10,
        supplier_lead_time_days=10,
        return_rate=0.10,          # Net base sales = 9.0
        seasonality_index=2.0,     # Doubled due to holidays -> 18.0 net daily sales
        marketing_spend_delta=0.0,
        competitor_price_ratio=1.0
    )
    assert result["adjusted_projected_daily_sales"] == 18.0
    assert result["estimated_days_until_stockout"] == 5.6
    assert result["action_required"] == True

def test_predict_endpoint_enterprise():
    response = client.post("/predict/", json={
        "sku": "SKU-PROMO-99",
        "current_stock": 50,
        "base_daily_sales": 10,
        "seasonality_index": 1.5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["sku"] == "SKU-PROMO-99"
    assert "adjusted_projected_daily_sales" in data
    assert "risk_level" in data