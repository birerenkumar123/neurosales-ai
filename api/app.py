import os
import sys

# Ensure src can be found during runtime
_src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if _src_path not in sys.path:
    sys.path.append(_src_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Create the main FastAPI instance
app = FastAPI(
    title="NeuroSales AI — Enterprise ML API",
    description="Professional Machine Learning API for Revenue Prediction, Churn, and Fraud Analysis. Built by Mrs. Biren Kumar Nayak.",
    version="2.0.0"
)

# ─── MIDDLEWARE (CORS) ───
# Ensuring any app or dashboard can securely connect to this brain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ROUTE INTEGRATION ───
from api.routes import revenue, churn, fraud, inventory, customer_insights

# Attach our advanced ML routes to the main engine
app.include_router(revenue.router, prefix="/v1/ml", tags=["Revenue Intelligence"])
app.include_router(churn.router, prefix="/v1/ml", tags=["Customer CRM"])
app.include_router(fraud.router, prefix="/v1/ml", tags=["Fraud & Risk"])
app.include_router(inventory.router, prefix="/v1/ml", tags=["Inventory Optimization"])
app.include_router(customer_insights.router, prefix="/v1/ml", tags=["Customer Insights"])

# ─── HEALTH CHECK ───
@app.get("/")
def home():
    """Returns the NeuroSales Engine status."""
    return {
        "status": "online",
        "engine": "NeuroSales PyTorch v2.0",
        "developer": "Mrs. Biren Kumar Nayak",
        "features": ["Revenue Forecasting", "Fraud Detection", "Churn Prediction", "Customer Intelligence"]
    }
