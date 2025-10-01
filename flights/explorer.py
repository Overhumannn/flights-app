from __future__ import annotations
import pandas as pd
from typing import Optional, Union

class FlightsExplorer:
    def __init__(self, source: Union[str, pd.DataFrame]):
        if isinstance(source, str):
            self.df = pd.read_csv(source)
        elif isinstance(source, pd.DataFrame):
            self.df = source.copy()
        else:
            raise ValueError("source must be a CSV path or a pandas DataFrame")

        self._normalize_types()

    def _normalize_types(self):
        for col in ["departure_time", "arrival_time"]:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors="coerce")

    def summarize_for_llm(self) -> str:
        if self.df.empty:
            return "No flight data available for this airport."
        
        total_flights = len(self.df)
        
        summary = f"Flight Data Summary:\n- Total flights: {total_flights}\n"
        
        # Топ стран
        if "from_country" in self.df.columns:
            top_countries = self.df["from_country"].value_counts().head(5)
            if not top_countries.empty:
                summary += "\nTop countries by flights:\n"
                for country, count in top_countries.items():
                    summary += f"- {country}: {count} flights\n"
        
        # Топ авиакомпаний
        if "airline" in self.df.columns:
            top_airlines = self.df["airline"].value_counts().head(5)
            if not top_airlines.empty:
                summary += "\nTop airlines:\n"
                for airline, count in top_airlines.items():
                    summary += f"- {airline}: {count} flights\n"
        
        return summary.strip()