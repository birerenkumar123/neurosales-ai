import streamlit as st
import os
import sys

# ── Global Page Config ──
st.set_page_config(
    page_title="NOVA AI — Virtual Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Dynamic Path Setup ──
# Assistant.py is in app/pages/
# _root is c:/ts/Neurosales_ai
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if _root not in sys.path:
    sys.path.append(_root)
if _app_path not in sys.path:
    sys.path.append(_app_path)

# ── Styles & Navbar ──
from styles_helper import inject_global_css_and_navbar
inject_global_css_and_navbar()

# ── Custom Header ──
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(6,6,18,1));
            border: 1px solid rgba(167,139,250,0.1); border-radius: 20px; padding: 40px; text-align: center; margin-bottom: 30px;">
    <h1 style="font-size: clamp(32px, 5vw, 48px); font-weight: 900; color: #f9fafb; margin-bottom: 10px;">
        🤖 Meet <span style="color:#a78bfa;">NOVA AI Agent</span>
    </h1>
    <p style="color:#9ca3af; font-size: 14px; max-width: 600px; margin: 0 auto; line-height: 1.6;">
        Our advanced Neural Language Agent is here to help you solve store problems, 
        suggest growth ideas, and generate new marketing strategies in Hindi or English.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Chat Core ──
from llm.assistant import chat_with_neurosales
api_key = st.secrets.get("GROQ_API_KEY", "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")

if "chat_history_full" not in st.session_state:
    st.session_state.chat_history_full = []

# Desktop Column Layout for chat
c1, c2, c3 = st.columns([1, 4, 1])

with c2:
    # ── Chat history area ──
    chat_container = st.container(height=500)
    
    with chat_container:
        if not st.session_state.chat_history_full:
            st.markdown("""
            <div style="text-align:center; padding: 100px 20px; color: #4b5563;">
                <div style="font-size:62px; margin-bottom:15px; filter: drop-shadow(0 0 10px rgba(124,58,237,0.4));">🤖</div>
                <div style="font-size:18px; font-weight:700; color:#f9fafb; margin-bottom:10px;">What's on your mind?</div>
                <div style="font-size:13px; color:#6b7280; max-width: 400px; margin: 0 auto;">
                    "How to increase my clothing store sales?"<br>
                    "Mere store me fraud kaise rokein?"<br>
                    "Show me my top growth areas."
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for message in st.session_state.chat_history_full:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div style="display:flex; justify-content:flex-end; margin:10px 0;">
                        <div style="background:linear-gradient(135deg,#7c3aed,#5b21b6);color:white;border-radius:20px 20px 4px 20px;padding:12px 20px;max-width:80%;font-size:14px;box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                            {message['content']}
                        </div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="display:flex; justify-content:flex-start; margin:10px 0;">
                        <div style="background:#1e1e30;border:1px solid rgba(255,255,255,0.06);color:#f9fafb;border-radius:20px 20px 20px 4px;padding:12px 20px;max-width:85%;font-size:14px;line-height:1.6;box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                            {message['content']}
                        </div>
                    </div>""", unsafe_allow_html=True)

    # ── User Input area ──
    user_query = st.chat_input("Message NOVA AI Agent...")
    
    if user_query:
        # Trigger AI
        reply, updated_hist = chat_with_neurosales(user_query, st.session_state.chat_history_full, api_key)
        st.session_state.chat_history_full = updated_hist
        st.rerun()

    # ── Clear & Help area ──
    if st.session_state.chat_history_full:
        if st.button("🗑 Reset Assistant Memory", use_container_width=True):
            st.session_state.chat_history_full = []
            st.rerun()

st.markdown("<br><div style='text-align:center; font-size:11px; color:#4b5563; letter-spacing:1px;'>Developed by Mrs. Biren Kumar Nayak</div>", unsafe_allow_html=True)
