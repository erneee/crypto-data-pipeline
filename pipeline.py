import os
import logging
from datetime import datetime

import requests
import psycopg2
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


COINS = ["bitcoin", "ethereum", "solana"]
API_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )


def create_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS crypto_price (
            id SERIAL PRIMARY KEY,
            coin VARCHAR(50) NOT NULL,
            price_usd NUMERIC(20, 8) NOT NULL,
            timestamp TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)


def fetch_crypto_prices(coins):
    params = {
        "ids": ",".join(coins),
        "vs_currencies": "usd"
    }

    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    if not isinstance(data, dict):
        raise ValueError("API response is not a valid dictionary.")

    return data


def insert_prices(cur, data, coins):
    inserted_count = 0

    for coin in coins:
        if coin not in data:
            logger.warning("Missing data for coin: %s", coin)
            continue

        if "usd" not in data[coin]:
            logger.warning("Missing USD price for coin: %s", coin)
            continue

        price = data[coin]["usd"]

        try:
            price = float(price)
        except (TypeError, ValueError):
            logger.warning("Invalid price for coin %s: %s", coin, price)
            continue

        timestamp = datetime.now()

        cur.execute(
            """
            INSERT INTO crypto_price (coin, price_usd, timestamp)
            VALUES (%s, %s, %s)
            """,
            (coin, price, timestamp)
        )

        logger.info("%s price written: %s", coin, price)
        inserted_count += 1

    return inserted_count


def run_pipeline():
    conn = None
    cur = None

    try:
        logger.info("Pipeline started")

        data = fetch_crypto_prices(COINS)

        conn = get_db_connection()
        cur = conn.cursor()

        create_table(cur)
        inserted_count = insert_prices(cur, data, COINS)

        conn.commit()
        logger.info("Pipeline finished successfully. Inserted rows: %s", inserted_count)

    except requests.RequestException as e:
        logger.error("API request failed: %s", e)

    except psycopg2.Error as e:
        logger.error("Database error: %s", e)
        if conn:
            conn.rollback()

    except Exception as e:
        logger.error("Unexpected error: %s", e)
        if conn:
            conn.rollback()

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
        logger.info("Database connection closed")