# coinradar_dashboard/0_Home.py
import streamlit as st

st.set_page_config(page_title="CoinRadar Dashboard", layout="wide")
st.title("📊 CoinRadar: Аналитика токенов")

st.markdown("""
Добро пожаловать в CoinRadar — платформу для анализа токенов Solana, отслеживания сигналов из Telegram-каналов и оценки монет по on-chain-данным.

**Навигация:**
- [💎 Обогащённые монеты](1_Enriched_Coins.py): список монет с ценой, капитализацией, ликвидностью и метаданными
- [📢 Статистика каналов](2_Channel_Stats.py): частота упоминаний, активность и популярность токенов в разных каналах

🚀 Мы только начинаем. В ближайших релизах появятся:
- Обзор рынка
- Рейтинги по доходности
- Анализ pump & dump

Связаться: [tg: @andyklyukin](https://t.me/andyklyukin)
""")
