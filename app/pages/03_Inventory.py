import streamlit as st
import pandas as pd
import os
import sys
import plotly.express as px

st.set_page_config(page_title="Inventory Management", page_icon="📦", layout="wide")

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

st.markdown("<h1>📦 Shop Inventory Tracker</h1>", unsafe_allow_html=True)

@st.cache_data
def load_stock():
    # Load past sales to deduce stock
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw', 'sales_data.csv'))
    
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
    else:
        return pd.DataFrame()
    
    # Mocking starting inventory by giving every category a 15,000 baseline minus items sold
    items_sold = df.groupby('category')['quantity'].sum().reset_index()
    items_sold['starting_stock'] = 15000
    items_sold['current_stock'] = items_sold['starting_stock'] - items_sold['quantity']
    items_sold['status'] = items_sold['current_stock'].apply(lambda x: "🟢 Healthy" if x > 5000 else ("🟡 Low Warn" if x > 2000 else "🔴 CRITICAL"))
    return items_sold

stock_df = load_stock()

if stock_df.empty:
    st.warning("No sales history found. Start selling to see stock alerts!")
    st.stop()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Current Stock Levels")
    fig = px.bar(stock_df, x="current_stock", y="category", orientation='h', 
                 color="status", title="Real-time Inventory", template="plotly_dark",
                 color_discrete_map={"🟢 Healthy":"#4CAF50", "🟡 Low Warn":"#FFC107", "🔴 CRITICAL":"#FF5252"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### ⚠️ Reorder Alerts")
    critical = stock_df[stock_df['status'] == "🔴 CRITICAL"]
    if not critical.empty:
        for _, row in critical.iterrows():
            st.error(f"**{row['category']}** is dangerously low ({row['current_stock']} left)!")
    else:
        st.success("All stock is healthy. No critical reorders needed today.")


# Chat Widget is now automatically injected by inject_global_css_and_navbar()
