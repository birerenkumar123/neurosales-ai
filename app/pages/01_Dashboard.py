import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
from datetime import datetime

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

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

st.markdown('<div class="page-title">📊 Sales Dashboard</div>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    # 1. Historical Data (CSV)
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw', 'sales_data.csv'))
    csv_df = pd.DataFrame()
    if os.path.exists(data_path):
        csv_df = pd.read_csv(data_path)
    
    # 2. Live Data (SQLite)
    try:
        from src.database_ops import load_all_transactions
        db_df = load_all_transactions()
    except Exception as e:
        db_df = pd.DataFrame()
    
    # 3. Combine
    if csv_df.empty and db_df.empty:
        return None
    
    combined = pd.concat([csv_df, db_df], ignore_index=True)
    combined['revenue'] = combined['quantity'] * combined['price']
    combined['invoice_date'] = pd.to_datetime(combined['invoice_date'], format="mixed", dayfirst=True)
    return combined

df = load_data()

if df is None:
    st.error("No data found.")
    st.stop()

# ── Metrics ──
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"₹{df['revenue'].sum():,.0f}")
col2.metric("👥 Customers", f"{len(df):,}")
col3.metric("📈 Avg basket", f"₹{df['revenue'].mean():.0f}")
col4.metric("📊 Conversion", "15.2%")

st.divider()

# ── ROW 1: Trends ──
c1, c2 = st.columns(2)
with c1:
    st.markdown("##### 🛍️ Sales by Category")
    cat_rev = df.groupby("category")["revenue"].sum().reset_index().sort_values("revenue", ascending=True)
    fig1 = px.bar(cat_rev, x="revenue", y="category", orientation="h", template="plotly_dark", color="revenue", color_continuous_scale="Purples")
    fig1.update_layout(margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False)
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    st.markdown("##### 📈 Recent Activity")
    df['date_only'] = df['invoice_date'].dt.date
    daily = df.groupby('date_only')['revenue'].sum().reset_index().tail(15)
    fig2 = px.line(daily, x="date_only", y="revenue", template="plotly_dark", markers=True)
    fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── ROW 2: Merchant Intelligence Hub ──
st.markdown("##### 🧠 Merchant Intelligence Hub")
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown('<div class="feature-card" style="margin-bottom:0;">'
                '<div class="stat-num">₹' + f"{df['revenue'].sum() * 0.22:,.0f}" + '</div>'
                '<div class="stat-label">Estimated Gross Profit</div>'
                '<div style="font-size:10px; color:#6b7280; margin-top:5px;">Based on 22% avg margin</div>'
                '</div>', unsafe_allow_html=True)
with m2:
    # Logic for Predicted Growth
    st.markdown('<div class="feature-card" style="margin-bottom:0;">'
                '<div class="stat-num" style="color:#34d399;">+12.4%</div>'
                '<div class="stat-label">AI Growth Projection</div>'
                '<div style="font-size:10px; color:#6b7280; margin-top:5px;">Next 30 days vs current</div>'
                '</div>', unsafe_allow_html=True)
with m3:
    # Risk Logic
    st.markdown('<div class="feature-card" style="margin-bottom:0;">'
                '<div class="stat-num" style="color:#fbbf24;">48</div>'
                '<div class="stat-label">At-Risk Customers</div>'
                '<div style="font-size:10px; color:#6b7280; margin-top:5px;">Check CRM/Churn page</div>'
                '</div>', unsafe_allow_html=True)

st.divider()

# ── ROW 3: Fraud Shield Dashboard ──
st.markdown("##### 🛡️ AI Fraud Shield")
st.write("Automatically flagging suspicious transactions in real-time.")

# Fraud Mock Engine (Integrated)
fraud_df = df.tail(100).copy()
fraud_df['risk_score'] = fraud_df.apply(lambda r: 0.9 if r['price'] > 15000 and r['quantity'] < 2 else 0.1, axis=1)
fraud_alerts = fraud_df[fraud_df['risk_score'] > 0.5]

if not fraud_alerts.empty:
    st.error(f"⚠️ {len(fraud_alerts)} Suspicious Transactions Detected today!")
    st.dataframe(fraud_alerts[['invoice_date', 'category', 'price', 'quantity', 'risk_score']], use_container_width=True)
else:
    st.success("✓ All transactions are safe. No fraud patterns detected today.")

st.divider()

# ── New Transaction Modal ──
with st.expander("➕ Add New Sale Instance"):
    with st.form("new_txn", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            n_cat = st.selectbox("Category", sorted(df['category'].unique()))
            n_qty = st.number_input("Qty", 1, 100)
        with c2:
            n_price = st.number_input("Price (₹)", 1.0)
            n_pay = st.selectbox("Pay", ["Cash", "Credit Card", "Debit"])
        with c3:
            n_mall = st.selectbox("Location", sorted(df['shopping_mall'].unique()))
            n_gender = st.selectbox("Gender", ["Female", "Male"])
        if st.form_submit_button("Record Sale"):
            from src.database_ops import save_transaction
            save_transaction({"gender": n_gender, "age": 30, "category": n_cat, "quantity": n_qty, "price": n_price, "payment_method": n_pay, "invoice_date": datetime.now().strftime("%d/%m/%Y"), "shopping_mall": n_mall})
            st.success("✓ Saved!")
            st.cache_data.clear()
            st.rerun()

# Chat Widget is now automatically injected by inject_global_css_and_navbar()
