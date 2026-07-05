from pathlib import Path
import requests
import zipfile
from io import BytesIO

BASE_URL = "https://data.binance.vision/data/spot/monthly/klines"

SYMBOL = "ETHUSDT"
INTERVAL = "1h"

START_YEAR = 2017
END_YEAR = 2026

OUT_DIR = Path("data/raw") / SYMBOL / INTERVAL
OUT_DIR.mkdir(parents=True, exist_ok=True)

for year in range(START_YEAR, END_YEAR + 1):
    for month in range(1, 13):

        filename = f"{SYMBOL}-{INTERVAL}-{year}-{month:02d}.zip"
        url = f"{BASE_URL}/{SYMBOL}/{INTERVAL}/{filename}"

        print(f"Downloading {filename}...")

        r = requests.get(url)

        if r.status_code != 200:
            print("Not found.")
            continue

        with zipfile.ZipFile(BytesIO(r.content)) as z:
            z.extractall(OUT_DIR)

print("Done.")