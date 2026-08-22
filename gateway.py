from fastapi import FastAPI, Request, HTTPException
import httpx
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pricing_service import calculate_dynamic_pricing

# Initialize Gateway with Security Guardrails
app = FastAPI(title="Dabbubu API Gateway", version="1.0.0")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Target internal service (will map to Kubernetes service discovery later)
INVENTORY_SERVICE_URL = "http://127.0.0.1:8001"

@app.post("/predict-price/")
@limiter.limit("5/minute")
async def gateway_pricing(request: Request, payload: dict, client_info: dict = Security(verify_api_key)):
    try:
        base_cost = payload.get("base_cost", 0.0)
        current_price = payload.get("current_price", 0.0)
        competitor_price = payload.get("competitor_price", 0.0)
        current_stock = payload.get("current_stock", 0)
        
        pricing_result = calculate_dynamic_pricing(
            base_cost=base_cost,
            current_price=current_price,
            competitor_price=competitor_price,
            current_stock=current_stock
        )
        
        return {
            "status": "success",
            "client_store": client_info.get("store_name"),
            "data": pricing_result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))