# dashboard.py
import streamlit as st
import pandas as pd
import psycopg2
from streamlit_autorefresh import st_autorefresh

st.title("Crypto Dashboard")

# Auto-refresh kas 1 minutę
st_autorefresh(interval=60000, key="crypto_refresh")

# Prisijungimas prie DB ir duomenų skaitymas
conn = psycopg2.connect(
    host="localhost",
    database="crypto",
    user="postgres",
    password="postgres",
    port="5432"
)
query = "SELECT * FROM crypto_price ORDER BY timestamp"
df = pd.read_sql(query, conn)
conn.close()

# Paskutinės kainos
st.subheader("Latest Prices")
latest = df.sort_values("timestamp").groupby("coin").tail(1)
for _, row in latest.iterrows():
    st.metric(row["coin"].upper(), row["price_usd"])

# Grafikas visoms monetoms
st.subheader("Price History")
coins = df["coin"].unique()
for coin in coins:
    coin_df = df[df["coin"] == coin]
    st.line_chart(coin_df.set_index("timestamp")["price_usd"])