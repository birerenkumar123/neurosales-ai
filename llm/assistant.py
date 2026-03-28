import os
import pandas as pd
from openai import OpenAI

# Store client globally if configured
_client = None

import time

# ── Dynamic Cache ──
_cache = {"data": None, "expiry": 0}

def load_sales_context():
    """Generates a text summary of all time raw sales data to feed the LLM. Optimized with 5-min cache."""
    global _cache
    now = time.time()
    
    if _cache["data"] and now < _cache["expiry"]:
        return _cache["data"]

    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'sales_data.csv'))
    try:
        df = pd.read_csv(data_path)
        df['revenue'] = df['quantity'] * df['price']
        total_rev = df['revenue'].sum()
        top_cat = df.groupby('category')['revenue'].sum().idxmax()
        total_qty = df['quantity'].sum()
        context = f"Lifetime Revenue: ${total_rev:,.2f}. Top Category: {top_cat}. Total items sold: {total_qty}."
        
        # update cache
        _cache["data"] = context
        _cache["expiry"] = now + 300 # 5 minutes
        return context
    except Exception as e:
        return f"Error loading context: {e}"

def chat_with_neurosales(user_query, chat_history, user_api_key):
    global _client
    if not user_api_key:
        return "No API Key provided. Please enter your OpenAI API key strictly mapped to your NeuroSales account.", chat_history

    try:
        # Route natively depending on the brand of the API key
        if user_api_key.startswith("gsk_"):
            client = OpenAI(api_key=user_api_key, base_url="https://api.groq.com/openai/v1")
            model_name = "llama-3.1-8b-instant"  # Upgraded model
        else:
            client = OpenAI(api_key=user_api_key)
            model_name = "gpt-3.5-turbo"
        
        context = load_sales_context()
        
        system_prompt = f"""You are NOVA — the intelligent AI Sales Assistant embedded inside NeuroSales AI.
NeuroSales AI is an advanced AI-powered revenue intelligence platform developed by Mrs. Biren Kumar Nayak.
It uses custom PyTorch Deep Learning Neural Networks (NeuroSalesNet architecture) and a scalable data pipeline that processes over 1TB of weekly customer interaction data.
The platform has increased conversion rates by 15% and sales efficiency by 20%.
It uses Python, PyTorch (Deep Learning), Streamlit, FastAPI, SQLite, and 120B character LLM models from Groq.

ABOUT THE DEVELOPER:
- Developer: Mrs. Biren Kumar Nayak
- If anyone asks who made this app, who built NeuroSales, or who is the developer — always say: "NeuroSales AI was developed by Mrs. Biren Kumar Nayak, an innovative AI engineer and entrepreneur."

CRITICAL INSTRUCTIONS:
- NEVER simulate a conversation or output dialogue tags like "User:" or "Assistant:".
- Only output a direct, clean response to the user's latest message.
- Reply in Hindi or English based on whichever language the user uses.
- Be concise, smart, and professional.
- You have access to real-time store context below:
real-time store context: {context}"""
        
        # Build strict message history
        messages = [{"role": "system", "content": system_prompt}]
        for msg in chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
            
        # Append latest question
        messages.append({"role": "user", "content": user_query})
        
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=250
        )
        
        reply = response.choices[0].message.content
        
        # update history
        chat_history.append({"role": "user", "content": user_query})
        chat_history.append({"role": "assistant", "content": reply})
        
        return reply, chat_history
    except Exception as e:
        chat_history.append({"role": "user", "content": user_query})
        chat_history.append({"role": "assistant", "content": f"⚠️ API Error: {str(e)}"})
        return f"Error connecting to OpenAI Brain: {str(e)}", chat_history
