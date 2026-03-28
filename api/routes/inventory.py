from fastapi import APIRouter
from api.schemas.models import InventoryInput, ReorderResult
import numpy as np

router = APIRouter()

@router.post("/optimize_inventory", response_model=ReorderResult, tags=["Inventory AI"])
async def optimize_inventory(data: InventoryInput):
    """
    AI Inventory brain predicting reorder needs based on demand trends.
    """
    days_to_out = 0
    reorder = False
    rec_qty = 0
    
    # 1. Base consumption rate logic
    consumption = 50 # items/day baseline
    if data.demand_trend == "Increasing": consumption *= 1.5
    elif data.demand_trend == "Decreasing": consumption *= 0.7
    
    # 2. Days left calculation
    days_to_out = int(data.current_stock / (consumption + 1e-5))
    
    # 3. Decision logic
    if days_to_out < 7:
        reorder = True
        rec_qty = int(consumption * 30) # 1 month stock
    
    return {
        "should_reorder": reorder,
        "recommended_quantity": rec_qty,
        "days_to_stockout": days_to_out
    }
