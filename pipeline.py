# pipeline.py
import requests
import psycopg2
import datetime
import os
from dotenv import load_dotenv

load_dotenv()




def run_pipeline():
    coins = ["bitcoin", "ethereum", "solana"]

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(coins), "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    data = response.json()

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()

    for coin in coins:
        price = float(data[coin]["usd"])
        timestamp = datetime.datetime.now()
        cur.execute(
            "INSERT INTO crypto_price (coin, price_usd, timestamp) VALUES (%s, %s, %s)",
            (coin, price, timestamp)
        )
        print(f"{coin} price įrašyta:", price)

    conn.commit()
    cur.close()
    conn.close()