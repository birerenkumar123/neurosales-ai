import pandas as pd
import numpy as np
import os
import joblib
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
from datetime import timedelta

def main():
    print("Loading data for forecasting...")
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'sales_data.csv')
    if not os.path.exists(data_path):
        print("Dataset not found!")
        return

    df = pd.read_csv(data_path)
    
    # Preprocess
    df['revenue'] = df['quantity'] * df['price']
    df['invoice_date'] = pd.to_datetime(df['invoice_date'], format="mixed", dayfirst=True)
    
    # Aggregate daily revenue
    daily_sales = df.groupby('invoice_date')['revenue'].sum().reset_index()
    daily_sales = daily_sales.sort_values('invoice_date')
    
    # Feature Engineering for Time Series
    daily_sales['day_of_week'] = daily_sales['invoice_date'].dt.dayofweek
    daily_sales['is_weekend'] = daily_sales['day_of_week'].isin([5, 6]).astype(int)
    daily_sales['month'] = daily_sales['invoice_date'].dt.month
    
    # Create target (Next day revenue)
    daily_sales['target_next_day'] = daily_sales['revenue'].shift(-1)
    
    # Drop NAs
    final_df = daily_sales.dropna()
    
    X = final_df[['revenue', 'day_of_week', 'is_weekend', 'month']]
    y = final_df['target_next_day']
    
    print("Training Forecasting Model...")
    model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    print("Saving Forecasting Model...")
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, 'forecast_model.pkl'))
    print("Forecasting model trained and saved!")

if __name__ == "__main__":
    main()
