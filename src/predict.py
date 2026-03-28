import os
import pandas as pd
import joblib

from preprocessing import feature_engineering

# Determine correct paths based on current file location
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'revenue_model.pkl')

def predict(data_dict):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Please run train_revenue.py first.")
    
    import torch
    from models_torch import NeuroSalesNet
    model = joblib.load(model_path)
    
    df = pd.DataFrame([data_dict])
    df = feature_engineering(df)
    
    if 'revenue' in df.columns:
        df = df.drop('revenue', axis=1)
        
    prediction = model.predict(df)
    return prediction[0]

if __name__ == "__main__":
    sample = {
        "gender": "Female",
        "age": 28,
        "category": "Clothing",
        "quantity": 3,
        "price": 1000.0,
        "payment_method": "Credit Card",
        "invoice_date": "1/5/2024",
        "shopping_mall": "Kanyon"
    }
    
    print("Testing Prediction on Sample data...")
    print(sample)
    
    try:
        result = predict(sample)
        print(f"\nSuccess! Predicted Revenue: ${result:.2f}")
    except Exception as e:
        print(f"\nError during prediction: {e}")
