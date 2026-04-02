# run_pipeline_loop.py
import time
from pipeline import run_pipeline

INTERVAL = 300  # 120 sec

while True:
    run_pipeline()
    print(f"Palaukiam {INTERVAL} sekundžių...")
    time.sleep(INTERVAL)