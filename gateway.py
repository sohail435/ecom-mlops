from fastapi import FastAPI, Request, HTTPException
import httpx
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Initialize Gateway with Security Guardrails
app = FastAPI(title="Dabbubu API Gateway", version="1.0.0")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Target internal service (will map to Kubernetes service discovery later)
INVENTORY_SERVICE_URL = "http://127.0.0.1:8001"

@app.post("/predict/")
@limiter.limit("5/minute")  # Bad load management guardrail: 5 requests per minute per IP
async def gateway_predict(request: Request, payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            # Forward the payload securely to the internal inventory worker
            response = await client.post(f"{INVENTORY_SERVICE_URL}/predict/", json=payload, timeout=10.0)
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
            return response.json()
            
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Inventory microservice is currently offline.")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Inventory microservice response timed out.")