"""
app.py
Streamlit interface for FastAPI backend.
"""
import os
import streamlit as st
import requests

# Backend URL (from .env or default local)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Flights by Country", page_icon="✈️", layout="wide")
st.title("Flights by Country ✈️")

# Airport selection
airports = ["DXB", "LHR", "CDG", "SIN", "HKG", "AMS"]
airport = st.selectbox("Select destination airport:", airports)

# Q&A section
st.subheader("Ask a question about flights")
question = st.text_input("For example: 'Which country has the most flights?'")

if question:
    payload = {
        "airport_code": airport,
        "question": question
    }
    try:
        response = requests.post(f"{BACKEND_URL}/query", json=payload, timeout=10)
        if response.status_code == 200:
            answer = response.json().get("answer", "No response from backend")
        else:
            answer = f"Error from backend: {response.status_code} {response.text}"
    except Exception as e:
        answer = f"Failed to connect to backend: {e}"
    
    st.info(answer)