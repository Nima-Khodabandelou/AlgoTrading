from pathlib import Path
import pandas as pd

SYMBOL = "ETHUSDT"
INTERVAL = "1h"

RAW_DIR = Path("data/raw") / SYMBOL / INTERVAL
OUT_DIR = Path("data/parquet")
OUT_DIR.mkdir(parents=True, exist_ok=True)

cols = [
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_volume", "trades",
    "taker_buy_base", "taker_buy_quote", "ignore"
]

dfs = []

for f in sorted(RAW_DIR.glob("*.csv")):
    print(f"Reading {f.name}")

    df = pd.read_csv(f, header=None, names=cols)

    # Normalize timestamps (µs -> ms)
    df["open_time"] = df["open_time"].astype("int64")
    mask = df["open_time"] > 10_000_000_000_000
    df.loc[mask, "open_time"] //= 1000

    dfs.append(df)

df = pd.concat(dfs, ignore_index=True)

# Convert timestamp to datetime
df["open_time"] = pd.to_datetime(
    df["open_time"],
    unit="ms",
    utc=True
)

# Clean dataset
df = (
    df
    .drop_duplicates(subset="open_time")
    .sort_values("open_time")
    .reset_index(drop=True)
)

# Save
out_file = OUT_DIR / f"{SYMBOL}_{INTERVAL}.parquet"
df.to_parquet(out_file, index=False)

print("\nDone.")
print(df.head())
print(df.tail())
print(f"Rows: {len(df)}")
print(f"Saved to: {out_file}")