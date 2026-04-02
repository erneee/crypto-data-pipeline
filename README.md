# Crypto Data Pipeline

This project collects cryptocurrency prices from the CoinGecko API and stores them in PostgreSQL.  
A Streamlit dashboard visualizes the collected data in real time.

---

## Architecture


CoinGecko API
↓
Python Data Pipeline
↓
PostgreSQL Database
↓
Streamlit Dashboard


---

## ⚙️ Technologies

- Python
- PostgreSQL
- Streamlit
- Docker
- CoinGecko API

---

## 🚀 How to Run

### Run with Docker (recommended)

```bash
docker-compose up --build

Then open:

http://localhost:8501
Run locally (without Docker)

Install dependencies:

pip install -r requirements.txt

Run pipeline:

python run_pipeline_loop.py

Run dashboard:

streamlit run dashboard.py
