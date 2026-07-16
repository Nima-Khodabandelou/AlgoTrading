from pathlib import Path
import pandas as pd
from src.data.loader import load_data

SYMBOL = "ETHUSDT"
INTERVAL = "1h"

INFILE = Path("data/features") / f"{SYMBOL}_{INTERVAL}_features.parquet"

df = load_data(
    start="2024-01-01",
    end="2024-12-31",
)

# Previous 20-hour high/low (exclude current candle)
df["prev_hh20"] = df["high"].rolling(20).max().shift(1)
df["prev_ll20"] = df["low"].rolling(20).min().shift(1)

# Breakout signals
df["long_signal"] = df["close"] > df["prev_hh20"]
df["short_signal"] = df["close"] < df["prev_ll20"]

print(df[[
    "open_time",
    "close",
    "prev_hh20",
    "prev_ll20",
    "long_signal",
    "short_signal"
]].head(30))

print()

print("Long signals :", int(df["long_signal"].sum()))
print("Short signals:", int(df["short_signal"].sum()))

OUT = Path("data/signals")
OUT.mkdir(parents=True, exist_ok=True)

df.to_parquet(
    OUT / f"{SYMBOL}_{INTERVAL}_breakout.parquet",
    index=False,
)

print("\nSaved.")