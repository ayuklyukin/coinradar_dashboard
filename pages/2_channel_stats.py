# coinradar_dashboard/2_Channel_Stats.py
import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(page_title="Статистика каналов", layout="wide")
st.title("📢 Статистика каналов")

# Подключение к базе данных через secrets.toml
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
            SELECT source_channel, COUNT(*) as token_count
            FROM coin_sources
            GROUP BY source_channel
            ORDER BY token_count DESC
        """)
        rows = cur.fetchall()
        return pd.DataFrame(rows, columns=["Канал", "Количество монет"])

# Загрузка и отображение
df = load_channel_stats()

if df.empty:
    st.warning("Пока нет данных по каналам.")
else:
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df.set_index("Канал"))
