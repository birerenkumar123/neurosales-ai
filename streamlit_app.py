import streamlit as st
import time
import os
import sys

# ── Dynamic Path Setup ──
_root = os.path.abspath(os.path.dirname(__file__))
if _root not in sys.path:
    sys.path.append(_root)
# Also append "app" to sys.path to ensure styles_helper can be found by sub-pages
_app_path = os.path.join(_root, 'app')
if _app_path not in sys.path:
    sys.path.append(_app_path)

st.set_page_config(
    page_title="NeuroSales AI — Revenue Intelligence Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Global Styles & Navbar ──
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ── Global Styles & Navbar ──
from styles_helper import inject_global_css_and_navbar
inject_global_css_and_navbar()

# ══════════════════════════════════════════════════════
#  LOGIN PAGE
# ══════════════════════════════════════════════════════
if not st.session_state['logged_in']:
    st.markdown("""
    <style>
    .hero-wrapper { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 80vh; padding: 20px; text-align: center; }
    .hero-title { font-size: clamp(32px, 8vw, 72px); font-weight: 900; background: linear-gradient(135deg, #fff, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; line-height: 1.1; }
    .login-glass { background: rgba(255,255,255,0.03); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: clamp(20px, 4vw, 40px); width: 100%; max-width: 440px; }
    .stats-row { display: flex; gap: clamp(15px, 4vw, 40px); margin-bottom: 30px; justify-content: center; flex-wrap: wrap; }
    .stat-num { font-size: clamp(18px, 2.5vw, 24px); font-weight: 900; color: #a78bfa; }
    .stat-label { font-size: 10px; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">NeuroSales AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6b7280; margin-bottom:30px;">Professional Revenue Intelligence Powered by PyTorch Deep Learning</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stats-row">
        <div class="stat-item"><div class="stat-num">+15%</div><div class="stat-label">Conv. Rate</div></div>
        <div class="stat-item"><div class="stat-num">+20%</div><div class="stat-label">Efficiency</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-glass">', unsafe_allow_html=True)
    from src.database_ops import init_db, verify_user, register_user
    init_db()

    t1, t2 = st.tabs(["Sign In", "Create Account"])
    with t1:
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("LAUNCH ENGINE →", use_container_width=True):
                if verify_user(u, p):
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.rerun()
                else: st.error("Invalid credentials")
    with t2:
        with st.form("reg"):
            nu = st.text_input("New Username")
            np = st.text_input("New Password", type="password")
            if st.form_submit_button("REGISTER →", use_container_width=True):
                if register_user(nu, np): st.success("Account created! Sign in now.")
                else: st.error("Error creating account")
    
    st.markdown("</div><div style='margin-top:20px; font-size:10px; color:#4b5563;'>Built by Mrs. Biren Kumar Nayak</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  AUTHENTICATED HOME
# ══════════════════════════════════════════════════════
else:
    col_l, col_r = st.columns([4, 1])
    with col_l:
        st.markdown(f"<h2 style='margin:0; color:#a78bfa;'>🧠 NeuroSales Platform</h2><p style='color:#6b7280; font-size:14px;'>Welcome, <b>{st.session_state.username.title()}</b></p>", unsafe_allow_html=True)
    with col_r:
        if st.button("Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    st.divider()

    # Community Count
    try:
        from src.database_ops import DB_PATH
        import sqlite3
        with sqlite3.connect(DB_PATH) as conn:
            cnt = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        st.markdown(f"<div style='background:rgba(124,58,237,0.1); padding:10px; border-radius:10px; text-align:center; font-size:13px; color:#a78bfa;'>Join <b>{cnt} merchants</b> using AI to automate their shops.</div>", unsafe_allow_html=True)
    except: pass

    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(0,0,0,0)); 
                padding: clamp(20px, 4vw, 50px); border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);
                margin-bottom: 30px;">
        <h2 style="font-size: clamp(24px, 4vw, 36px); font-weight: 900; color: #f9fafb; margin-bottom: 12px;">📊 Project Intelligence Platform</h2>
        <p style="color: #9ca3af; font-size: 14px; line-height: 1.6; max-width: 800px;">
            <b>NeuroSales AI</b> is a high-performance MLaaS (Machine Learning as a Service) platform designed to modernize rural and urban retail commerce. 
            By integrating <b>PyTorch Neural Networks</b> for revenue forecasting and <b>FastAPI</b> for real-time risk assessment, 
            we empower merchants with deep-learning insights that were previously only available to giant corporations. 
            Our vision is to bridge the data-gap for small shopkeepers, turning raw transactions into <b>actionable growth strategies.</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🚀 AI Control Center")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="feature-card"><div class="feature-icon">📊</div><div class="feature-title">Dashboard</div><div class="feature-desc">Live Sales & AI Performance metrics.</div></div>', unsafe_allow_html=True)
        if st.button("Open Dashboard", use_container_width=True): st.switch_page("pages/01_Dashboard.py")
    with c2:
        st.markdown('<div class="feature-card"><div class="feature-icon">🔮</div><div class="feature-title">Predictor</div><div class="feature-desc">PyTorch-powered Daily Revenue Forecasts.</div></div>', unsafe_allow_html=True)
        if st.button("Run Predictions", use_container_width=True): st.switch_page("pages/02_Predictor.py")
    with c3:
        st.markdown('<div class="feature-card"><div class="feature-icon">📁</div><div class="feature-title">Intelligence</div><div class="feature-desc">Upload CSV/Excel for automated AI analysis.</div></div>', unsafe_allow_html=True)
        if st.button("Upload Data", use_container_width=True): st.switch_page("pages/07_Data_Upload.py")

    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown('<div class="feature-card"><div class="feature-icon">👥</div><div class="feature-title">Customers</div><div class="feature-desc">AI segmentation & Churn risk analysis.</div></div>', unsafe_allow_html=True)
        if st.button("View Customers", use_container_width=True): st.switch_page("pages/04_Customers.py")
    with c5:
        st.markdown('<div class="feature-card"><div class="feature-icon">📈</div><div class="feature-title">Forecasting</div><div class="feature-desc">7-Day ahead Aggregate Revenue Forecast.</div></div>', unsafe_allow_html=True)
        if st.button("See Forecast", use_container_width=True): st.switch_page("pages/05_Forecasting.py")
    with c6:
        st.markdown('<div class="feature-card"><div class="feature-icon">📦</div><div class="feature-title">Inventory</div><div class="feature-desc">Stock alerts and reorder predictions.</div></div>', unsafe_allow_html=True)
        if st.button("Manage Stock", use_container_width=True): st.switch_page("pages/03_Inventory.py")

    st.divider()
    # Big AI Agent Promo
    st.markdown('<div class="feature-card" style="text-align:center; max-width:600px; margin: 0 auto; border: 1px solid rgba(167,139,250,0.4); background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(0,0,0,0));">'
                '<div class="feature-icon">🤖</div>'
                '<div class="feature-title">NOVA Virtual Assistant</div>'
                '<div class="feature-desc">Our intelligent AI Agent is now available as a full-screen experience in the top navbar. Get expert advice in Hindi and English easily.</div>'
                '</div>', unsafe_allow_html=True)
    if st.button("Chat with NOVA AI Agent →", use_container_width=True): st.switch_page("pages/06_Assistant.py")

    st.markdown("<br><div style='text-align:center; font-size:10px; color:#4b5563;'>Developed by Mrs. Biren Kumar Nayak</div>", unsafe_allow_html=True)
