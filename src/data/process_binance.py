"""
process_binance.py

Reads raw Binance monthly CSV files, normalizes timestamps,
merges all files into a single dataset, removes duplicates,
sorts chronologically, and saves the result as a Parquet file.

Input:
    data/raw/<SYMBOL>/<TIMEFRAME>/*.csv

Output:
    data/parquet/<SYMBOL>_<TIMEFRAME>.parquet
"""

import pandas as pd

from src.config.settings import (
    SYMBOL,
    TIMEFRAME,
    RAW_DIR,
    PARQUET_DIR,
)

PARQUET_DIR.mkdir(parents=True, exist_ok=True)

COLUMNS = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_volume",
    "trades",
    "taker_buy_base",
    "taker_buy_quote",
    "ignore",
]

raw_path = RAW_DIR / SYMBOL / TIMEFRAME

dfs = []

for file in sorted(raw_path.glob("*.csv")):
    print(f"Reading {file.name}")

    df = pd.read_csv(
        file,
        header=None,
        names=COLUMNS,
    )

    # Normalize timestamps (microseconds -> milliseconds)
    df["open_time"] = df["open_time"].astype("int64")
    mask = df["open_time"] > 10_000_000_000_000
    df.loc[mask, "open_time"] //= 1000

    dfs.append(df)

df = pd.concat(dfs, ignore_index=True)

# Convert timestamps to UTC datetime
df["open_time"] = pd.to_datetime(
    df["open_time"],
    unit="ms",
    utc=True,
)

# Clean dataset
df = (
    df.drop_duplicates(subset="open_time")
      .sort_values("open_time")
      .reset_index(drop=True)
)

output_file = PARQUET_DIR / f"{SYMBOL}_{TIMEFRAME}.parquet"

df.to_parquet(
    output_file,
    index=False,
)

print("\nDone.")
print(df.head())
print(df.tail())
print(f"Rows: {len(df)}")
print(f"Saved to: {output_file}")