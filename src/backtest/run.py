from pathlib import Path
import pandas as pd

from .engine import BacktestEngine
from .metrics import report

from src.config.settings import (
    SIGNALS_DIR,
    SYMBOL,
    TIMEFRAME,
    INITIAL_CAPITAL,
)

DATA = SIGNALS_DIR / f"{SYMBOL}_{TIMEFRAME}_breakout.parquet"

df = pd.read_parquet(DATA)

engine = BacktestEngine(initial_capital=INITIAL_CAPITAL)

trades = engine.run(df)

report(trades, INITIAL_CAPITAL)