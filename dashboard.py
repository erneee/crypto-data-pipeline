import os
import logging

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )


def load_data():
    conn = None
    try:
        conn = get_db_connection()
        query = """
            SELECT id, coin, price_usd, timestamp
            FROM crypto_price
            ORDER BY timestamp
        """
        df = pd.read_sql(query, conn)
        logger.info("Loaded %s rows from database", len(df))
        return df

    except Exception as e:
        logger.error("Failed to load data from database: %s", e)
        st.error(f"Nepavyko nuskaityti duomenų iš DB: {e}")
        return pd.DataFrame()

    finally:
        if conn is not None:
            conn.close()


def show_latest_metrics(df):
    st.subheader("Latest Prices")

    latest = df.sort_values("timestamp").groupby("coin").tail(1)

    for _, row in latest.iterrows():
        st.metric(
            label=row["coin"].upper(),
            value=f"${row['price_usd']:.2f}"
        )


def show_price_history(df):
    st.subheader("Price History")

    for coin in df["coin"].unique():
        st.write(f"### {coin.upper()}")
        coin_df = df[df["coin"] == coin].copy()
        coin_df = coin_df.sort_values("timestamp")
        st.line_chart(coin_df.set_index("timestamp")["price_usd"])


def main():
    st.set_page_config(page_title="Crypto Dashboard", layout="wide")
    st.title("Crypto Dashboard")

    st_autorefresh(interval=60000, key="crypto_refresh")

    df = load_data()

    if df.empty:
        st.warning("Duomenų bazėje dar nėra duomenų.")
        return

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    show_latest_metrics(df)
    show_price_history(df)


if __name__ == "__main__":
    main()
