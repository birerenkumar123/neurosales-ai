from fastapi import APIRouter
import numpy as np
from api.schemas.models import ChurnInput, ChurnResult

router = APIRouter()

# ─── NEUROSALES CHURN PREDICTION ENGINE ───
@router.post("/predict_churn", response_model=ChurnResult)
async def predict_churn_endpoint(data: ChurnInput):
    """
    Predicts the probability of a customer stopping their visits.
    """
    # Rule-based inference (to be upgraded later with a Logistic Regression model)
    prob_score = 0.0
    
    # 1. Recency penalty (The longer the gap, the more risk)
    if data.last_purchase_days > 180:
        prob_score += 0.6
    elif data.last_purchase_days > 90:
        prob_score += 0.3
    
    # 2. Loyalty bonus (The more visits, the less risk)
    if data.total_visit_count > 10:
        prob_score -= 0.2
    
    # 3. High bill (High spenders are less likely to churn)
    if data.avg_bill > 10000:
        prob_score -= 0.1
        
    # Final clamping
    prob_score = np.clip(prob_score, 0.0, 1.0)
    
    # Segment assignment
    segment = "Active"
    if prob_score > 0.7:
        segment = "Churned"
    elif prob_score > 0.3:
        segment = "At Risk"
        
    return {
        "churn_probability": float(prob_score),
        "segment": segment
    }
