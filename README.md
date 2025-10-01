# Flights by Country

## Overview
This project allows users to explore flight arrivals for six major airports (DXB, LHR, CDG, SIN, HKG, AMS) and ask natural language questions about today's flights. Data is fetched from [FlightAPI.io](https://www.flightapi.io/) and interpreted using an LLM.

---

## Architecture

- **Frontend:** Streamlit app (`app.py`) providing dropdowns and question input.
- **Backend:** FastAPI app (`backend/main.py`) serving endpoints for flight data and LLM query handling.
- **Flight API Client:** `flights/api_client.py` - async HTTP client with parsing of API responses.
- **LLM Adapter:** `flights/llm_adapter.py` - wrapper for querying the LLM and generating answers.
- **Data Explorer:** `flights/explorer.py` - processes API data into Pandas DataFrame and provides utility functions.
- **Tests:** `tests/test_api_client.py`, `tests/test_explorer.py`.
- **Environment Variables:** `.env` (API keys, LLM settings).

---

## LLM Integration Architecture

The system consists of three main layers:

1. **Frontend (Streamlit)** – provides the user interface where a person can enter flight-related questions and see the results.  
2. **Backend (FastAPI)** – receives queries from the frontend, handles communication with the FlightAPI, performs preprocessing, and integrates with the LLM for reasoning.  
3. **External APIs (FlightAPI.io)** – provide real-time flight schedule data, which is then enriched and structured before being passed to the LLM.  

---

## Query Flow

1. The user types a question in the Streamlit interface (e.g., "Which country has the most arrivals to DXB today?").  
2. The query, along with parameters such as IATA code and day, is sent to the FastAPI backend.  
3. The backend makes a secure request to the FlightAPI using the API key stored in the `.env` file.  
4. The flight schedule data is fetched, cleaned, and transformed into a structured format.  
5. The backend calls the LLM with this structured data to generate a natural-language answer.  
6. The response is returned to the frontend and displayed to the user.  

---

## Why This Approach?

- **Separation of Concerns** – frontend handles UI only, backend handles logic and LLM integration.  
- **Security** – API keys are never exposed to the user or frontend.  
- **Preprocessing** – flight data can be normalized and validated before passing to the LLM, improving reliability.  
- **Scalability** – backend can be containerized with Docker and deployed on Render.com, making it easy to scale independently from the UI.  
- **Flexibility** – this architecture allows adding new data sources or swapping the LLM provider without changing the frontend.  