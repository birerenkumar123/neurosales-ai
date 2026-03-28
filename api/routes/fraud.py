from fastapi import APIRouter
import numpy as np
from api.schemas.models import FraudInput, FraudResult

router = APIRouter()

# ─── NEUROSALES FRAUD DETECTION ENGINE (PROTOTYPE) ───
@router.post("/detect_fraud", response_model=FraudResult)
async def detect_fraud_endpoint(data: FraudInput):
    """
    Flags unusual transactions based on price-to-quantity ratio.
    """
    # Simple rule-based logic (can later be replaced by an Isolation Forest model)
    risk_score = 0.0
    
    # 1. High price for single item
    if data.price > 10000 and data.quantity < 2:
        risk_score += 0.5
    
    # 2. Suspicious combination
    if data.payment_method == "Credit Card" and data.price > 25000:
        risk_score += 0.3
    
    # 3. Random variance (Simulate Neural variance)
    risk_score += np.random.uniform(0.0, 0.1)
    
    is_fraud = True if risk_score > 0.7 else False
    
    return {
        "is_fraud": is_fraud,
        "risk_score": float(np.clip(risk_score, 0.0, 1.0))
    }
