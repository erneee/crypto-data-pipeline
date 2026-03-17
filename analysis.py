import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

conn = psycopg2.connect(
    host="localhost",
    database="crypto",
    user="postgres",
    password="postgres",
    port="5432"
)

query = "SELECT * FROM crypto_price ORDER BY timestamp"

df = pd.read_sql(query, conn)

print(df)

conn.close()

coins = df["coin"].unique()

for coin in coins:

    coin_data = df[df["coin"] == coin]

    plt.plot(
        coin_data["timestamp"],
        coin_data["price_usd"],
        label=coin
    )

plt.title("Crypto Prices Over Time")
plt.xlabel("Time")
plt.ylabel("Price USD")
plt.legend()

plt.show()