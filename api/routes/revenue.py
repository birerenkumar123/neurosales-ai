from fastapi import APIRouter, HTTPException
import os
import sys
import pandas as pd
from datetime import datetime

# Add root and src path to find modules
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _root not in sys.path:
    sys.path.append(_root)
_src = os.path.join(_root, 'src')
if _src not in sys.path:
    sys.path.append(_src)

from api.schemas.models import SalesInput, PredictionOutput
from predict import predict as run_prediction

router = APIRouter()

@router.post("/predict_revenue", response_model=PredictionOutput)
async def predict_revenue_endpoint(data: SalesInput):
    try:
        # Prepare input for our prediction script
        input_data = {
            "gender": data.gender, "age": data.age, "category": data.category,
            "quantity": data.quantity, "price": data.price, "payment_method": data.payment_method,
            "invoice_date": datetime.now().strftime("%d/%m/%Y"),
            "shopping_mall": data.shopping_mall
        }
        
        # Call core prediction script
        val = run_prediction(input_data)
        
        # Smart Advice engine
        advice = "Healthy Day" if val > 1000 else "Consider Marketing Campaign"
        
        return {
            "predicted_revenue": float(val),
            "confidence_score": 0.95, # Mock: Replace with real model variance later
            "advice": advice
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Neural Engine Error: {str(e)}")
