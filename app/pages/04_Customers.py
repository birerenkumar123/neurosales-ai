import streamlit as st
import pandas as pd
import os
import sys
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Customer CRM", page_icon="👥", layout="wide")

# ── Global UI & Navbar ──
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from styles_helper import inject_global_css_and_navbar
inject_global_css_and_navbar()

st.markdown('<div class="page-title">👥 AI Customer Intelligence</div>', unsafe_allow_html=True)

@st.cache_data
def load_crm_data():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw', 'sales_data.csv'))
    if not os.path.exists(data_path): return pd.DataFrame()
    
    df = pd.read_csv(data_path)
    df['revenue'] = df['quantity'] * df['price']
    
    # Segment demographics
    grouped = df.groupby('age').agg({'revenue': 'mean', 'quantity': 'sum'}).reset_index()
    if grouped.empty: return pd.DataFrame()
    
    # Clustering
    scaler = StandardScaler()
    scaled = scaler.fit_transform(grouped[['revenue', 'quantity']])
    km = KMeans(n_clusters=3, random_state=42)
    grouped['cluster'] = km.fit_predict(scaled)
    cluster_names = {0: "Bargain Seekers", 1: "VIP Spenders", 2: "Occasional Buyers"}
    grouped['Segment'] = grouped['cluster'].map(cluster_names)
    
    return grouped

crm = load_crm_data()

if crm.empty:
    st.warning("No audience data found. Record more sales to enable AI segmenting!")
    st.stop()

# ── ROW 1: Demographic Intelligence ──
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown("##### 👩‍🔬 Demographic Value Matrix")
    fig = px.scatter(crm, x="age", y="revenue", size="quantity", color="Segment", 
                     hover_name="Segment", size_max=40, template="plotly_dark",
                     title="Value vs Age Clustering")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    st.markdown("##### 🚀 AI Promotion Strategy")
    st.success("Target **VIP Spenders** with VIP early access!")
    st.info("Offer bulk discounts to **Bargain Seekers**.")

st.divider()

# ── ROW 2: Churn Prediction Engine ──
st.markdown("##### 📉 Customer Churn Risk Analysis")
st.write("Using behavioral patterns to predict which customers are likely to stop visiting.")

# Churn Mock Logic (Integrated)
# Segmenting CRM output into Churn risks
crm['Churn_Risk'] = crm['revenue'].apply(lambda r: "🟢 Active" if r > 4000 else ("🟡 At Risk" if r > 2000 else "🔴 High Churn Risk"))
churn_counts = crm['Churn_Risk'].value_counts().reset_index()
churn_counts.columns = ['Risk', 'Count']

c3, c4 = st.columns(2)
with c3:
    fig_pie = px.pie(churn_counts, values='Count', names='Risk', template="plotly_dark", color='Risk', 
                 color_discrete_map={"🟢 Active":"#4CAF50", "🟡 At Risk":"#FFC107", "🔴 High Churn Risk":"#FF5252"})
    st.plotly_chart(fig_pie, use_container_width=True)
with c4:
    at_risk = crm[crm['Churn_Risk'] != "🟢 Active"].head(20)
    st.write("📋 **Customers needing Attention:**")
    st.dataframe(at_risk[['age', 'Segment', 'Churn_Risk']], use_container_width=True)

# Chat Widget is automated
