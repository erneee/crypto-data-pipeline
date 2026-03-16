# run_pipeline_loop.py
import time
from pipeline import run_pipeline

INTERVAL = 10  # 5 minutes

while True:
    run_pipeline()
    print(f"Palaukiam {INTERVAL} sekundžių...")
    time.sleep(INTERVAL)