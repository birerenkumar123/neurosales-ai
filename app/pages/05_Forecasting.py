import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import joblib
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="AI Forecast", page_icon="📈", layout="wide")

# ── Dynamic Path Setup ──
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _root not in sys.path:
    sys.path.append(_root)
if _app_path not in sys.path:
    sys.path.append(_app_path)

# ── Global UI & Navbar ──
from styles_helper import inject_global_css_and_navbar
inject_global_css_and_navbar()

st.markdown("<h1>📈 7-Day Revenue AI Forecast</h1>", unsafe_allow_html=True)
st.write("Our Gradient Boosting Regressor projects your aggregate revenue for the next week.")

@st.cache_resource
def load_forecast_model():
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'forecast_model.pkl'))
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

model = load_forecast_model()

if model:
    st.success("Forecast Model loaded successfully!")
    
    # Generate next 7 days data
    base = datetime.today()
    dates = [base + timedelta(days=x) for x in range(1, 8)]
    
    # We need: ['revenue', 'day_of_week', 'is_weekend', 'month']
    # The 'revenue' here is actually the lag(1) baseline. 
    # For a real autoregressive model we'd predict sequentially. 
    # For demo, let's inject a baseline of $10,000 for sliding window.
    
    forecasts = []
    current_rev_est = 10000.0 
    
    for d in dates:
        row = pd.DataFrame([{
            'revenue': current_rev_est,
            'day_of_week': d.weekday(),
            'is_weekend': 1 if d.weekday() in [5, 6] else 0,
            'month': d.month
        }])
        pred = model.predict(row)[0]
        forecasts.append({'Date': d.strftime("%A, %b %d"), 'Forecasted Revenue': pred})
        current_rev_est = pred # Feed autoregressive loop
        
    f_df = pd.DataFrame(forecasts)
    
    st.markdown("### Next Week Overview")
    fig = px.area(f_df, x="Date", y="Forecasted Revenue", template="plotly_dark",
                  markers=True, color_discrete_sequence=["#00E676"])
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Forecasting Model is empty. Run `python src/train_forecast.py` to generate the brain.")


# Chat Widget is now automatically injected by inject_global_css_and_navbar()
