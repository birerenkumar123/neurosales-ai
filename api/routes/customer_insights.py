from fastapi import APIRouter
from api.schemas.models import CLVInput, CLVResult
import numpy as np

router = APIRouter()

@router.post("/predict_clv", response_model=CLVResult, tags=["Customer Insights"])
async def predict_clv_endpoint(data: CLVInput):
    """
    Predicting Customer Lifetime Value using spend patterns and frequency.
    """
    # Predictive CLV = Avg Monthly Spend * (Tenure + 12 months)
    predicted_val = (data.total_spend / max(data.tenure_months, 1)) * (data.tenure_months + 12)
    
    # ── Category logic ──
    cat = "Silver"
    if predicted_val > 50000: cat = "Platinum"
    elif predicted_val > 20000: cat = "Gold"
    
    return {
        "predicted_lifetime_value": float(predicted_val),
        "loyalty_category": cat
    }
