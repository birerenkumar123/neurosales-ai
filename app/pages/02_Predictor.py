import streamlit as st
import pandas as pd
import joblib
import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from preprocessing import feature_engineering

st.set_page_config(page_title="Sales Predictor", page_icon="🔮", layout="centered")

# ── Global UI & Navbar ──
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from styles_helper import inject_global_css_and_navbar
inject_global_css_and_navbar()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #060612; }
header { display: none !important; }
.block-container { padding-top: 2rem !important; }

.page-title {
    font-size: 28px; font-weight: 900; color: #f9fafb;
    margin-bottom: 4px;
}
.page-sub { font-size: 14px; color: #6b7280; margin-bottom: 32px; }

.result-box {
    background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(5,150,105,0.2));
    border: 1px solid rgba(167,139,250,0.4);
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    margin-top: 24px;
}
.result-label { font-size: 13px; color: #9ca3af; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px; }
.result-amount { font-size: 52px; font-weight: 900; color: #a78bfa; line-height: 1; }
.result-sub { font-size: 13px; color: #6b7280; margin-top: 8px; }

.info-row { display: flex; gap: 12px; margin-top: 20px; }
.info-card {
    flex: 1; background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 16px; text-align: center;
}
.info-card-val { font-size: 20px; font-weight: 800; color: #34d399; }
.info-card-label { font-size: 11px; color: #6b7280; margin-top: 4px; }

.stSelectbox label, .stNumberInput label, .stSlider label {
    color: #9ca3af !important; font-size: 13px !important; font-weight: 600 !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: white !important;
}
.stNumberInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: white !important;
}
.stFormSubmitButton button {
    background: linear-gradient(135deg, #7c3aed, #059669) !important;
    border: none !important; border-radius: 12px !important;
    color: white !important; font-weight: 700 !important;
    font-size: 16px !important; padding: 16px !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
}
.block-container { padding-top: 1rem !important; margin-top: -30px !important; }
.stDivider { margin: 0.5rem 0 !important; }
div[data-testid="stVerticalBlock"] { gap: 1rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">🔮 Sales Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Fill in today\'s details — AI will predict your expected sales revenue.</div>', unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'revenue_model.pkl'))
    if os.path.exists(model_path):
        import torch
        from models_torch import NeuroSalesNet # Required for joblib to reconstruct the PyTorch net
        return joblib.load(model_path)
    return None

@st.cache_data
def load_data():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw', 'sales_data.csv'))
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    return None

model = load_model()
df = load_data()

if not model:
    st.warning("⚠️ Prediction model not trained yet. Run `python src/train_revenue.py` first.")
    st.stop()

if df is None:
    st.error("No sales data found.")
    st.stop()

with st.form("prediction_form"):
    st.markdown("#### 🛒 Customer Details")
    col1, col2 = st.columns(2)
    with col1:
        customers_today = st.number_input("👥 How many customers today?", min_value=1, max_value=10000, value=50, step=1)
        cat = st.selectbox("🛍️ Main Product Category", sorted(df['category'].unique()))
        gender = st.selectbox("👤 Most customers are", ["Female", "Male"])
    with col2:
        age = st.number_input("🎂 Average Customer Age", min_value=10, max_value=90, value=35)
        pay_method = st.selectbox("💳 Main Payment Method", sorted(df['payment_method'].unique()))
        mall = st.selectbox("🏬 Your Shop Location", sorted(df['shopping_mall'].unique()))

    st.markdown("#### 📦 Product Details")
    col3, col4 = st.columns(2)
    with col3:
        price = st.number_input("💰 Average Item Price (₹)", min_value=1, max_value=100000, value=500)
    with col4:
        quantity = st.number_input("📦 Avg Items per Customer", min_value=1, max_value=50, value=2)

    predict_btn = st.form_submit_button("🔮 Predict Today's Sales →", use_container_width=True)

if predict_btn:
    # Build input for ONE customer, then multiply by number of customers
    data = {
        "gender": gender, "age": age, "category": cat, "quantity": quantity,
        "price": price, "payment_method": pay_method, "shopping_mall": mall,
        "invoice_date": datetime.today().strftime("%d/%m/%Y")
    }
    input_df = pd.DataFrame([data])
    trans_input = feature_engineering(input_df)
    if 'revenue' in trans_input.columns:
        trans_input.drop('revenue', axis=1, inplace=True)

    single_pred = model.predict(trans_input)[0]
    total_pred = single_pred * customers_today
    avg_basket = single_pred

    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">Predicted Total Revenue Today</div>
        <div class="result-amount">₹{total_pred:,.0f}</div>
        <div class="result-sub">Based on {customers_today} customers · Avg basket ₹{avg_basket:,.0f}</div>
    </div>
    <div class="info-row">
        <div class="info-card">
            <div class="info-card-val">{customers_today}</div>
            <div class="info-card-label">Customers Expected</div>
        </div>
        <div class="info-card">
            <div class="info-card-val">₹{avg_basket:,.0f}</div>
            <div class="info-card-label">Avg Per Customer</div>
        </div>
        <div class="info-card">
            <div class="info-card-val">₹{total_pred:,.0f}</div>
            <div class="info-card-label">Total Revenue</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Simple advice
    if total_pred > 50000:
        st.success("🎉 Great day ahead! Stock up on popular items and have extra staff ready.")
    elif total_pred > 20000:
        st.info("👍 Good day expected. Normal operations should be fine.")
    else:
        st.warning("📢 Slow day expected. Consider running a small discount offer to attract more customers.")

# Chat Widget is automated
