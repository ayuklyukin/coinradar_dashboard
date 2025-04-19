# coinradar_dashboard/1_Enriched_Coins.py
import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(page_title="Enriched Coins", layout="wide")
st.title("💎 Обогащённые монеты")

# Подключение к Supabase через secrets.toml
conn = psycopg2.connect(
    dbname=st.secrets["SUPABASE_DB_NAME"],
    user=st.secrets["SUPABASE_DB_USER"],
    password=st.secrets["SUPABASE_DB_PASS"],
    host=st.secrets["SUPABASE_DB_HOST"],
    port=st.secrets["SUPABASE_DB_PORT"]
)

@st.cache_data(ttl=20)
def load_data():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT coin_name, ca_address, price, mcap, liquidity, holders,
                   telegram_link, twitter_link, website_link, source_channel, updated_at
            FROM coin_info
            ORDER BY updated_at DESC
            LIMIT 100
        """)
        rows = cur.fetchall()
        cols = [
            "coin_name", "ca_address", "price", "mcap", "liquidity", "holders",
            "telegram", "twitter", "website", "source_channel", "updated"
        ]
        return pd.DataFrame(rows, columns=cols)

# Отображаем данные
coins_df = load_data()
st.dataframe(coins_df, use_container_width=True)
