import streamlit as st
import sys
import os

# Ensure root paths are setup for the assistant module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from llm.assistant import chat_with_neurosales
except ModuleNotFoundError:
    pass

def render_chat_widget():
    """
    Renders NOVA AI as a sleek 'small tab' (Floating Bubble) on every page.
    """
    st.markdown("""
    <style>
    /* ── The Chat Bubble (Small Tab) Styling ── */
    [data-testid="stPopover"] {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        z-index: 999999;
    }
    [data-testid="stPopover"] > button {
        background: linear-gradient(135deg, #7c3aed 0%, #3b82f6 100%) !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        border-radius: 50% !important; /* Circular like a modern bubble */
        width: 60px !important;
        height: 60px !important;
        color: white !important;
        font-size: 26px !important;
        padding: 0 !important;
        box-shadow: 0 10px 40px rgba(124,58,237,0.4) !important;
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    [data-testid="stPopover"] > button:hover {
        transform: scale(1.1) rotate(5deg) !important;
        box-shadow: 0 15px 50px rgba(124,58,237,0.6) !important;
    }

    /* ── The Chat Window (Small Tab Body) ── */
    div[data-testid="stPopoverBody"] {
        background: #0b0b1e !important;
        border: 1px solid rgba(167,139,250,0.2) !important;
        border-radius: 24px !important;
        width: 360px !important;
        max-height: 500px !important;
        box-shadow: 0 30px 100px rgba(0,0,0,0.8) !important;
        overflow: hidden !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.popover("🤖"):
        # Header for the Small Tab
        st.markdown("""
        <div style="background: linear-gradient(to right, #1a0533, #06061e);
                    padding: 16px 20px; border-bottom: 1px solid rgba(255,255,255,0.05); text-align: center;">
            <div style="font-size:16px; font-weight:900; color:#a78bfa; margin-bottom:2px;">NOVA AI AGENT</div>
            <div style="font-size:10px; color:#6b7280; letter-spacing:1px; text-transform:uppercase;">Enterprise Neural Engine</div>
        </div>
        """, unsafe_allow_html=True)

        # Groq API Key
        api_key = st.secrets.get("GROQ_API_KEY", "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")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Chat Window content
        with st.container(height=300):
            if not st.session_state.chat_history:
                st.markdown("<div style='text-align:center; padding-top:40px; color:#4b5563; font-size:12px;'>Namaste! How can I help with your store today?</div>", unsafe_allow_html=True)
            
            for msg in st.session_state.chat_history:
                role = msg["role"]
                content = msg["content"]
                if role == "user":
                    st.markdown(f"<div style='margin-bottom:10px; text-align:right;'><span style='background:#7c3aed; color:white; padding:8px 12px; border-radius:15px 15px 2px 15px; display:inline-block; font-size:13px;'>{content}</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='margin-bottom:10px; text-align:left;'><span style='background:#1e1e30; color:#e2e8f0; padding:8px 12px; border-radius:15px 15px 15px 2px; display:inline-block; font-size:13px; line-height:1.5; border:1px solid rgba(255,255,255,0.05);'>{content}</span></div>", unsafe_allow_html=True)

        # Input Area
        q = st.chat_input("Ask about sales, stock, or fraud...")
        if q:
            reply, hist = chat_with_neurosales(q, st.session_state.chat_history, api_key)
            st.session_state.chat_history = hist
            st.rerun()

        if st.session_state.chat_history:
            if st.button("Reset Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
