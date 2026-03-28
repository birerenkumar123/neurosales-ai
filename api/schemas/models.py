from pydantic import BaseModel
from typing import List, Optional

class SalesInput(BaseModel):
    gender: str          # "Male" or "Female"
    age: int
    category: str       # e.g., "Clothing", "Food"
    quantity: int
    price: float
    payment_method: str
    shopping_mall: str

class PredictionOutput(BaseModel):
    predicted_revenue: float
    confidence_score: float
    advice: str

class FraudInput(BaseModel):
    quantity: int
    price: float
    payment_method: str

class FraudResult(BaseModel):
    is_fraud: bool
    risk_score: float # 0.0 to 1.0

class ChurnInput(BaseModel):
    last_purchase_days: int # Days since last purchase
    avg_bill: float
    total_visit_count: int

class ChurnResult(BaseModel):
    churn_probability: float
    segment: str # "Active", "At Risk", "Churned"

class InventoryInput(BaseModel):
    category: str
    current_stock: int
    demand_trend: str # "Increasing", "Decreasing", "Stable"

class ReorderResult(BaseModel):
    should_reorder: bool
    recommended_quantity: int
    days_to_stockout: int

class CLVInput(BaseModel):
    total_spend: float
    tenure_months: int
    frequency_per_month: float

class CLVResult(BaseModel):
    predicted_lifetime_value: float
    loyalty_category: str # "Platinum", "Gold", "Silver"
