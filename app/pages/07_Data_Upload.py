import streamlit as st
import pandas as pd
import os
import sys
import joblib
import plotly.express as px
from datetime import datetime

# ── Global Page Config ──
st.set_page_config(
    page_title="Data Intelligence — NeuroSales AI",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Path & Navbar ──
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _root not in sys.path:
    sys.path.append(_root)
if _app_path not in sys.path:
    sys.path.append(_app_path)

from styles_helper import inject_global_css_and_navbar
inject_global_css_and_navbar()

# ── Import Prediction Modules ──
try:
    from src.preprocessing import feature_engineering
    from src.models_torch import NeuroSalesNet
except ImportError:
    pass

st.markdown("""
<div class="page-title">📁 Data Intelligence & Upload</div>
<p style="color:#6b7280; margin-bottom: 25px;">Upload your own business data — Our AI will automatically analyze it and predict its total value.</p>
""", unsafe_allow_html=True)

# ── Load Model for Predictions ──
@st.cache_resource
def load_biz_model():
    m_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'revenue_model.pkl'))
    if os.path.exists(m_path):
        return joblib.load(m_path)
    return None

biz_model = load_biz_model()

# ── File Uploader ──
uploaded_file = st.file_uploader("📂 Choose a CSV or EXCEL file for Business Analysis", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Load data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"✓ '{uploaded_file.name}' Loaded successfully!")
        
        # ── Business Value Section ──
        st.markdown("### 💎 Predicted Business Value")
        
        # Check if we can predict on this file
        required_cols = ['category', 'quantity', 'price', 'payment_method', 'shopping_mall']
        has_needed = all(c in df.columns for c in required_cols)

        if has_needed and biz_model:
            with st.spinner("🤖 Running Neural Inference on your data..."):
                # Pre-process
                input_data = df.copy()
                if 'invoice_date' not in input_data.columns:
                    input_data['invoice_date'] = datetime.today().strftime("%d/%m/%Y")
                
                trans_df = feature_engineering(input_data)
                if 'revenue' in trans_df.columns: trans_df.drop('revenue', axis=1, inplace=True)
                
                # Predict
                predictions = biz_model.predict(trans_df)
                df['predicted_revenue'] = predictions
                
                total_pred = predictions.sum()
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Predicted Total Value", f"₹{total_pred:,.0f}")
                col2.metric("Avg Transaction Value", f"₹{predictions.mean():.0f}")
                col3.metric("Highest Deal Potental", f"₹{predictions.max():.0f}")
                
                st.info("💡 **Business Insight:** Our AI projects the revenue for this entire dataset to be ₹" + f"{total_pred:,.2f}" + ".")
        else:
            st.warning("⚠️ For AI Value Prediction, your file needs columns: 'category', 'quantity', 'price', 'payment_method', 'shopping_mall'.")

        st.divider()

        # ── AUTOMATED ANALYSIS ──
        st.markdown("### 📊 Automated AI Insights")
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

        if num_cols:
            col_sel = st.selectbox("🎯 Select metric to analyze", num_cols)
            c1, c2 = st.columns(2)
            with c1:
                fig_hist = px.histogram(df, x=col_sel, template="plotly_dark", color_discrete_sequence=['#a78bfa'], title=f"Spread of {col_sel}")
                st.plotly_chart(fig_hist, use_container_width=True)
            with c2:
                if len(num_cols) > 1:
                    other_col = st.selectbox("Compare with", [c for c in num_cols if c != col_sel])
                    fig_scat = px.scatter(df, x=col_sel, y=other_col, template="plotly_dark", trendline="ols", title=f"{col_sel} vs {other_col}")
                    st.plotly_chart(fig_scat, use_container_width=True)

        if cat_cols:
            cat_sel = st.selectbox("🗂️ Analyze by Grouping", cat_cols)
            if num_cols:
                sum_col = st.selectbox("Measure total of", num_cols, key="cat_sum")
                grouped = df.groupby(cat_sel)[sum_col].sum().reset_index().sort_values(sum_col, ascending=False).head(10)
                fig_bar = px.bar(grouped, x=cat_sel, y=sum_col, template="plotly_dark", color=sum_col, color_continuous_scale="Purples", title=f"Total {sum_col} by {cat_sel}")
                st.plotly_chart(fig_bar, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error analysis file: {e}")
else:
    st.info("👆 Please upload a file (CSV/Excel) to start the Automated Business Analysis engine.")

st.markdown("<br><div style='text-align:center; font-size:11px; color:#4b5563; letter-spacing:1px;'>Developed by Mrs. Biren Kumar Nayak</div>", unsafe_allow_html=True)
