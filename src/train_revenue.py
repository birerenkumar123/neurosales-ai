import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib
import os
from skorch import NeuralNetRegressor

from preprocessing import feature_engineering, get_preprocessor
# Use our shared professional-grade PyTorch model
from models_torch import NeuroSalesNet

def main():
    print("🚀 Initializing NeuroSales Deep Learning Engine (PyTorch)...")
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'sales_data.csv')
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    df = pd.read_csv(data_path)

    print("🧠 Feature Engineering for Neural Net...")
    df = feature_engineering(df)
    X = df.drop('revenue', axis=1)
    # Target must be float32 for PyTorch
    y = df['revenue'].values.astype(np.float32).reshape(-1, 1)

    print("📊 Preprocessing Features...")
    preprocessor = get_preprocessor()
    X_transformed = preprocessor.fit_transform(X).astype(np.float32)
    X_transformed = X_transformed.toarray() if hasattr(X_transformed, 'toarray') else X_transformed
    input_size = X_transformed.shape[1]

    print(f"🤖 Training PyTorch Neural Network (Input Layers: {input_size})...")
    # Wrap PyTorch into a scikit-learn compatible net
    net = NeuralNetRegressor(
        NeuroSalesNet,
        module__input_dim=input_size,
        max_epochs=150, # More training for higher accuracy
        lr=0.005,
        optimizer=torch.optim.Adam,
        train_split=None, 
        device='cuda' if torch.cuda.is_available() else 'cpu'
    )

    # Reconnect preprocessor to the net so the predictor is simple to call
    final_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('pytorch_net', net)
    ])

    print("⚡ Optimizing Weights (Epochs: 150)...")
    final_pipeline.fit(X, y)

    print("💾 Finalizing High-Performance Neural Brain...")
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(final_pipeline, os.path.join(model_dir, "revenue_model.pkl"))

    print("✅ Optimization Successful! Brain is now running on PyTorch Deep Learning.")

if __name__ == "__main__":
    main()