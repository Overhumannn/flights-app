import os
import pandas as pd
import httpx
from datetime import datetime

API_KEY = os.getenv("FLIGHTAPI_KEY")
BASE_URL = "https://api.flightapi.io/schedule"

_cache = {}
_cache_timestamps = {}
CACHE_TTL = 30

async def fetch_today_schedule(airport_iata: str) -> pd.DataFrame:
    if not API_KEY:
        raise ValueError("FLIGHTAPI_KEY environment variable not set")

    cache_key = airport_iata
    current_time = datetime.utcnow().timestamp()
    
    if cache_key in _cache:
        cached_time = _cache_timestamps.get(cache_key, 0)
        if current_time - cached_time < CACHE_TTL:
            return _cache[cache_key].copy()

    params = {
        "mode": "arrivals",
        "iata": airport_iata,
        "day": 1
    }

    url = f"{BASE_URL}/{API_KEY}"

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, read=20.0)) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
    except Exception as e:
        raise ValueError(f"Failed to fetch data from API: {str(e)}")

    # Проверяем структуру ответа
    if not isinstance(data, dict):
        return pd.DataFrame()
    
    airport_data = data.get("airport", {})
    if not airport_data:
        return pd.DataFrame()
    
    plugin_data = airport_data.get("pluginData", {})
    if not plugin_data:
        return pd.DataFrame()
    
    schedule = plugin_data.get("schedule", {})
    if not schedule:
        return pd.DataFrame()
    
    # Для arrivals используем ключ "arrivals"
    arrivals_data = schedule.get("arrivals", {})
    if not arrivals_data:
        return pd.DataFrame()
    
    arrivals = arrivals_data.get("data", [])
    
    if not arrivals:
        empty_df = pd.DataFrame()
        _cache[cache_key] = empty_df
        _cache_timestamps[cache_key] = current_time
        return empty_df

    flights_data = []
    for item in arrivals:
        if not isinstance(item, dict) or "flight" not in item:
            continue
            
        flight = item.get("flight", {})
        if not flight:
            continue
        
        # Для arrivals: origin - откуда летит, destination - куда (наш аэропорт)
        airport_info = flight.get("airport", {}) or {}
        origin = airport_info.get("origin", {}) or {}
        destination = airport_info.get("destination", {}) or {}
        
        # Origin - откуда прилетает (другие страны)
        origin_position = origin.get("position", {}) or {}
        origin_country = origin_position.get("country", {}) or {}
        origin_region = origin_position.get("region", {}) or {}
        
        # Destination - куда прилетает (наш аэропорт)
        dest_code = destination.get("code", {}) or {}
        dest_position = destination.get("position", {}) or {}
        dest_country = dest_position.get("country", {}) or {}
        
        identification = flight.get("identification", {}) or {}
        number = identification.get("number", {}) or {}
        airline = flight.get("airline", {}) or {}
        aircraft_data = flight.get("aircraft", {}) or {}
        model = aircraft_data.get("model", {}) or {}
        status = flight.get("status", {}) or {}
        time_info = flight.get("time", {}) or {}
        scheduled = time_info.get("scheduled", {}) or {}
        
        flight_record = {
            "flight_number": number.get("default", "N/A"),
            "airline": airline.get("name", "Unknown"),
            "from_airport": origin.get("name", "Unknown"),
            "from_country": origin_country.get("name", "Unknown"),
            "from_city": origin_region.get("city", "Unknown"),
            "to_airport": destination.get("name", airport_iata),
            "to_country": dest_country.get("name", "Unknown"),
            "aircraft": model.get("code", "N/A"),
            "status": status.get("text", "Unknown"),
            "departure_time": scheduled.get("departure"),
            "arrival_time": scheduled.get("arrival"),
        }
        flights_data.append(flight_record)
    
    if not flights_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(flights_data)
    
    # Приведение типов
    if "departure_time" in df.columns:
        df["departure_time"] = pd.to_datetime(df["departure_time"], unit='s', errors="coerce")
    if "arrival_time" in df.columns:
        df["arrival_time"] = pd.to_datetime(df["arrival_time"], unit='s', errors="coerce")
    
    df["date"] = datetime.utcnow().strftime("%Y-%m-%d")

    _cache[cache_key] = df.copy()
    _cache_timestamps[cache_key] = current_time

    return df