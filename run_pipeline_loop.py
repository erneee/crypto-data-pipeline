# run_pipeline_loop.py
import time
from pipeline import run_pipeline

INTERVAL = 10  # 10 sec

while True:
    run_pipeline()
    print(f"Palaukiam {INTERVAL} sekundžių...")
    time.sleep(INTERVAL)