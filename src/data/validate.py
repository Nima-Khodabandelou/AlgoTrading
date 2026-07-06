from pathlib import Path
import pandas as pd

FILE = Path("data/parquet/ETHUSDT_1h.parquet")

df = pd.read_parquet(FILE)

print("=== DATASET ===")
print(f"Rows       : {len(df)}")
print(f"Duplicates : {df['open_time'].duplicated().sum()}")
print(f"Sorted     : {df['open_time'].is_monotonic_increasing}")

# Time differences
delta = df["open_time"].diff().dt.total_seconds()

print("\n=== INTERVAL COUNTS (seconds) ===")
print(delta.value_counts().sort_index())

# Missing candles (>1h)
gaps = df.loc[delta > 3600, ["open_time"]].copy()
gaps["gap_hours"] = delta[delta > 3600].values / 3600

print(f"\n=== GAPS (>1 hour): {len(gaps)} ===")
if gaps.empty:
    print("None")
else:
    print(gaps.head(20))

# Irregular timestamps
irregular = df[
    (df["open_time"].dt.minute != 0) |
    (df["open_time"].dt.second != 0) |
    (df["open_time"].dt.microsecond != 0)
]

print(f"\n=== IRREGULAR TIMESTAMPS: {len(irregular)} ===")
if irregular.empty:
    print("None")
else:
    print(irregular.head(20))

print("\n=== DATE RANGE ===")
print("Start:", df["open_time"].min())
print("End  :", df["open_time"].max())