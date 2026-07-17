"""
run.py
======

Runs a complete backtest.

Workflow
--------
1. Load OHLCV data
2. Instantiate strategy
3. Run backtest engine
4. Print results

Future
------
Performance metrics and charts will be added later.
"""

from pathlib import Path

import pandas as pd

from src.backtest.engine import BacktestEngine
from src.config.settings import (
    FEATURE_DIR,
    SYMBOL,
    TIMEFRAME,
    INITIAL_CAPITAL,
)

from src.strategies.breakout import BreakoutStrategy


# ---------------------------------------------------------

data_file = FEATURE_DIR / f"{SYMBOL}_{TIMEFRAME}_features.parquet"

df = pd.read_parquet(data_file)

strategy = BreakoutStrategy()

engine = BacktestEngine(
    strategy=strategy,
    initial_capital=INITIAL_CAPITAL,
)

trades = engine.run(df)

# ---------------------------------------------------------

print()
print("========== TRADE LOG ==========")
print(trades)

print()

print(f"Trades       : {len(trades)}")
print(f"Initial      : ${INITIAL_CAPITAL:,.2f}")

if len(trades):

    final_capital = trades.iloc[-1]["capital"]

else:

    final_capital = INITIAL_CAPITAL

print(f"Final        : ${final_capital:,.2f}")

print(
    f"Return       : {(final_capital / INITIAL_CAPITAL - 1) * 100:.2f}%"
)