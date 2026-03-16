# Crypto Data Pipeline

Simple crypto data pipeline that collects cryptocurrency prices from the CoinGecko API and stores them in PostgreSQL.  
The data is visualized using a Streamlit dashboard with auto refresh.

## Technologies

- Python
- PostgreSQL
- Streamlit
- CoinGecko API

## Project Structure
pipeline.py – collects crypto prices from API and stores them in database
run_pipeline_loop.py – runs pipeline every few minutes
dashboard.py – Streamlit dashboard to visualize crypto prices

## How to Run

Install dependencies:

pip install -r requirements.txt

Run pipeline:

python run_pipeline_loop.py

Run dashboard:

streamlit run dashboard.py