# Later, when the project grows, split the feature folder into:
# features/
#     builder.py          # orchestrates everything
#     trend.py            # SMA, EMA...
#     volatility.py       # ATR, Bollinger...
#     momentum.py         # RSI, ROC...
#     volume.py           # OBV, VWAP...

from pathlib import Path
import pandas as pd
from src.data.loader import load_data

SYMBOL = "ETHUSDT"
INTERVAL = "1h"

DATA = Path("data/parquet") / f"{SYMBOL}_{INTERVAL}.parquet"

df = load_data(
    start="2024-01-01",
    end="2024-12-31",
)

# keep only 2024
df = df[
    (df["open_time"] >= "2024-01-01")
    & (df["open_time"] < "2025-01-01")
].copy()

# returns
df["ret1"] = df["close"].pct_change()

# moving averages
df["sma20"] = df["close"].rolling(20).mean()
df["sma50"] = df["close"].rolling(50).mean()

# highest high / lowest low
df["hh20"] = df["high"].rolling(20).max()
df["ll20"] = df["low"].rolling(20).min()

# volatility
df["vol20"] = df["ret1"].rolling(20).std()

print(df.head(30))
print()
print(df.tail())
print()
print(df.info())

OUT = Path("data/features")
OUT.mkdir(parents=True, exist_ok=True)

df.to_parquet(
    OUT / f"{SYMBOL}_{INTERVAL}_features.parquet",
    index=False,
)

print("\nSaved.")


