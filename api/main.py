from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from predict import predict

app = FastAPI(title="NeuroSales API")

class SaleRequest(BaseModel):
    gender: str
    age: int
    category: str
    quantity: int
    price: float
    payment_method: str
    invoice_date: str
    shopping_mall: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "NeuroSales AI is running!"}

@app.post("/predict_revenue")
def get_prediction(sale: SaleRequest):
    try:
        prediction = predict(sale.dict())
        return {"expected_revenue": prediction}
    except Exception as e:
        return {"error": str(e)}

# Run using: uvicorn api.main:app --reload
