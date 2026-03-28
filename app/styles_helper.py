import streamlit as st
import os

def inject_global_css_and_navbar():
    # 1. Load the CSS stylesheet (always apply global styles)
    css_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'styles.css'))
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    # 2. Condition: Only show Navbar if the user is LOGGED IN
    is_logged_in = st.session_state.get('logged_in', False)
    
    if is_logged_in:
        # ── Global Chat Widget (NOVA AI) ──
        import sys
        _root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        if _root not in sys.path:
            sys.path.append(_root)
        try:
            from llm.chat_widget import render_chat_widget
            render_chat_widget()
        except:
            pass

        # ── Modern Stable Navbar (Only for active sessions) ──
        navbar_html = """
        <div class="nav-container">
            <div class="nav-brand">🧠 NeuroSales AI</div>
            <div class="nav-links">
                <a href="/" target="_self">Home</a>
                <a href="Dashboard" target="_self">Sales</a>
                <a href="Predictor" target="_self">Predict</a>
                <a href="Inventory" target="_self">Stock</a>
                <a href="Customers" target="_self">CRM</a>
                <a href="Data_Upload" target="_self">Upload</a>
                <a href="Assistant" target="_self">AI Agent</a>
            </div>
        </div>
        """
        st.markdown(navbar_html, unsafe_allow_html=True)

        # ── Navbar Styling ──
        st.markdown("""
            <style>
            .nav-container {
                position: sticky; top: 0; left: 0; right: 0;
                background: rgba(10,10,26,0.95);
                backdrop-filter: blur(10px);
                border-bottom: 2px solid #7c3aed;
                display: flex; justify-content: space-between; align-items: center;
                padding: 1rem 1.5rem;
                z-index: 999999;
                margin-bottom: 2rem;
                width: 100%;
            }
            .nav-brand { font-size: 20px; font-weight: 900; color: #a78bfa; }
            .nav-links { display: flex; gap: 1rem; }
            .nav-links a { color: #d1d5db; text-decoration: none; font-size: 14px; font-weight: 700; transition: 0.3s; }
            .nav-links a:hover { color: #ffffff; text-decoration: underline; }
            
            div[data-testid="stHeader"] { display: none !important; }
            .block-container { padding-top: 0px !important; }
            </style>
        """, unsafe_allow_html=True)
    else:
        # If not logged in, just hide the header space to keep the login page clean
        st.markdown("""
            <style>
            div[data-testid="stHeader"] { display: none !important; }
            .block-container { padding-top: 2rem !important; }
            </style>
        """, unsafe_allow_html=True)
