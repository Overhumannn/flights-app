# flights/llm_adapter.py
from typing import Any
import os
import httpx

OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

async def ask_llm(prompt: str, model: str = "deepseek/deepseek-chat") -> str:
    """
    Sends a prompt to an LLM via OpenRouter API and returns the answer.
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is not set in environment variables.")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Flights Q&A"
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system", 
                "content": "You are a flight data analyst. Answer questions about flights in clear, concise English using only the provided data."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 300,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data: Any = response.json()
        
        choices = data.get("choices", [])
        if not choices:
            return "Unable to generate response."
        
        answer = choices[0].get("message", {}).get("content", "")
        return answer.strip() if answer else "No response generated."