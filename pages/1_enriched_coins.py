import streamlit as st
import pandas as pd
import psycopg2
import time

st.set_page_config(page_title="Enriched Coins", layout="wide")
st.title("💎 Обогащённые монеты")

#st.markdown("**💀 Монета помечена как скам — капитализация < 10,000, больше не обновляется.**")


# Подключение к базе
conn = psycopg2.connect(
    dbname=st.secrets["SUPABASE_DB_NAME"],
    user=st.secrets["SUPABASE_DB_USER"],
    password=st.secrets["SUPABASE_DB_PASS"],
    host=st.secrets["SUPABASE_DB_HOST"],
    port=st.secrets["SUPABASE_DB_PORT"]
)

def load_data():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT coin_name, ca_address, price, mcap, liquidity, holders,
                   telegram_link, twitter_link, website_link,
                   source_channel, updated_at, skip_updates
            FROM coin_info
            ORDER BY updated_at DESC
            LIMIT 100
        """)
        rows = cur.fetchall()
        cols = [
            "coin_name", "ca_address", "price", "mcap", "liquidity", "holders",
            "telegram", "twitter", "website", "source_channel", "updated", "skip_updates"
        ]
        df = pd.DataFrame(rows, columns=cols)

        # 💀 Добавим emoji, если skip_updates = True
        df["coin_name"] = df.apply(
            lambda row: f"💀 {row['coin_name']}" if row["skip_updates"] else row["coin_name"],
            axis=1
        )

        # 🧹 Удаляем колонку skip_updates
        return df.drop(columns=["skip_updates"])

# ⏱️ Автообновление
st.markdown("⏱️ Данные обновляются автоматически каждые **15 секунд**")
if st.button("🔄 Обновить сейчас"):
    st.session_state.last_refresh = time.time()

last_refresh = st.session_state.get("last_refresh", 0)
if time.time() - last_refresh > 15:
    st.session_state.last_refresh = time.time()

# 📥 Загрузка данных
df = load_data()

# 📊 Отображение через st.dataframe
st.dataframe(df, use_container_width=True)



