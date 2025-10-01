# flights/qa.py
"""
qa.py
Простой Q&A модуль для вопросов о рейсах.
"""
from __future__ import annotations
from flights.explorer import FlightsExplorer


class FlightsQA:
    def __init__(self, explorer: FlightsExplorer):
        self.explorer = explorer

    def answer(self, airport: str, question: str) -> str:
        """
        Простейший поиск ответа по ключевым словам.
        """
        q = question.lower()

        if "больше всего" in q or "топ страна" in q:
            top = self.explorer.top_country(airport)
            if top:
                return f"В аэропорт {airport} больше всего рейсов из {top[0]} ({top[1]} рейсов)."
            return f"Нет данных по аэропорту {airport}."

        if "сколько стран" in q:
            num = self.explorer.num_countries(airport)
            return f"Аэропорт {airport} обслуживается рейсами из {num} стран."

        if "топ" in q:
            # ищем число после слова "топ"
            try:
                n = int([w for w in q.split() if w.isdigit()][0])
            except (IndexError, ValueError):
                n = 3
            series = self.explorer.top_n_countries(airport, n)
            parts = [f"{c}: {cnt}" for c, cnt in series.items()]
            return f"Топ-{n} стран для аэропорта {airport}: " + ", ".join(parts)

        return "Извините, я пока понимаю только простые вопросы: 'больше всего', 'сколько стран', 'топ N'."
