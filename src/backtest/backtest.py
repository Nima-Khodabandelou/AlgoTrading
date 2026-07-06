"""
backtest.py

Purpose
-------
Simple event-driven backtester for breakout strategies.

Input
-----
data/signals/ETHUSDT_1h_breakout.parquet

Strategy
--------
- Long only
- Enter at next candle's open after a long signal.
- Exit at next candle's open after a short signal.
- One position at a time.
- Invest 100% of available capital.
- No commissions, slippage or spread (added later).

Output
------
Prints:
- Trade log
- Final capital
- Total return

Future improvements
-------------------
- Commission
- Slippage
- Spread
- Short selling
- Position sizing
- Stop-loss
- Take-profit
- Performance statistics
"""

from pathlib import Path
import pandas as pd

SYMBOL = "ETHUSDT"
INTERVAL = "1h"
INITIAL_CAPITAL = 10_000.0

DATA = (
    Path("data/signals")
    / f"{SYMBOL}_{INTERVAL}_breakout.parquet"
)

df = pd.read_parquet(DATA).reset_index(drop=True)

capital = INITIAL_CAPITAL

position = False
units = 0.0
entry_price = 0.0
entry_time = None

trades = []

for i in range(len(df) - 1):

    row = df.iloc[i]
    next_open = df.iloc[i + 1]["open"]
    next_time = df.iloc[i + 1]["open_time"]

    # -------------------------
    # Entry
    # -------------------------
    if (not position) and row["long_signal"]:

        entry_price = next_open
        entry_time = next_time

        units = capital / entry_price

        position = True

    # -------------------------
    # Exit
    # -------------------------
    elif position and row["short_signal"]:

        exit_price = next_open
        exit_time = next_time

        pnl = units * (exit_price - entry_price)

        capital += pnl

        trades.append(
            {
                "entry_time": entry_time,
                "exit_time": exit_time,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "pnl": pnl,
                "capital": capital,
            }
        )

        position = False
        units = 0.0

# Close any remaining position at the final close
if position:

    exit_price = df.iloc[-1]["close"]
    exit_time = df.iloc[-1]["open_time"]

    pnl = units * (exit_price - entry_price)

    capital += pnl

    trades.append(
        {
            "entry_time": entry_time,
            "exit_time": exit_time,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "pnl": pnl,
            "capital": capital,
        }
    )

trades = pd.DataFrame(trades)

print()
print("========== TRADE LOG ==========")
print(trades)

print()
print(f"Trades       : {len(trades)}")
print(f"Initial      : ${INITIAL_CAPITAL:,.2f}")
print(f"Final        : ${capital:,.2f}")
print(f"Return       : {(capital / INITIAL_CAPITAL - 1) * 100:.2f}%")