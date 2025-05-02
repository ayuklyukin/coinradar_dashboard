import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(page_title="Статистика каналов", layout="wide")
st.title("📢 Статистика каналов")

# Подключение к базе
conn = psycopg2.connect(
    dbname=st.secrets["SUPABASE_DB_NAME"],
    user=st.secrets["SUPABASE_DB_USER"],
    password=st.secrets["SUPABASE_DB_PASS"],
    host=st.secrets["SUPABASE_DB_HOST"],
    port=st.secrets["SUPABASE_DB_PORT"]
)

@st.cache_data(ttl=120)
def load_channel_stats():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                source_channel,
                COUNT(*) FILTER (WHERE skip_updates IS TRUE) AS scam,
                COUNT(*) FILTER (WHERE skip_updates IS NOT TRUE) AS good
            FROM coin_info
            GROUP BY source_channel
            ORDER BY COUNT(*) DESC
        """)
        rows = cur.fetchall()
        return pd.DataFrame(rows, columns=["Канал", "Скам", "Хорошие"])

df = load_channel_stats()

if df.empty:
    st.warning("Пока нет данных по каналам.")
else:
    # 📊 Общая сводка
    df["Всего"] = df["Скам"] + df["Хорошие"]
    df["% Хороших"] = (df["Хорошие"] / df["Всего"] * 100).round(1).astype(str) + "%"

    total = df["Всего"].sum()
    good = df["Хорошие"].sum()
    scam = df["Скам"].sum()
    percent_good = (good / total * 100) if total else 0

    st.subheader("📊 Общая статистика")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Всего монет", total)
    col2.metric("Хороших монет", good)
    col3.metric("Скам-монет", scam)
    col4.metric("Процент хороших", f"{percent_good:.1f}%")

    # 📋 Таблица
    st.subheader("📋 Детализация по каналам")
    st.dataframe(df[["Канал", "Всего", "Хорошие", "Скам", "% Хороших"]], use_container_width=True)

    # 📈 График bar_chart от Streamlit
    st.subheader("📈 Монеты по каналам (хорошие vs скам)")

    # Готовим данные для красивого графика
    df_plot = df[["Канал", "Хорошие", "Скам"]].set_index("Канал")
    st.bar_chart(df_plot)
