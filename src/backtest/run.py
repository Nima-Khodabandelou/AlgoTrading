"""
run.py

Purpose
-------
Entry point for running a backtest.

Workflow
--------
1. Load OHLCV data
2. Instantiate strategy
3. Let the strategy prepare indicators/signals
4. Run the backtest engine
5. Report performance
"""

import pandas as pd

from src.config.settings import (
    PARQUET_DIR,
    SYMBOL,
    TIMEFRAME,
    INITIAL_CAPITAL,
    TRAIN_START,
    TRAIN_END,
    COMMISSION,
    SLIPPAGE,
)

from src.backtest.engine import BacktestEngine
from src.backtest.metrics import report

from src.strategies.breakout import BreakoutStrategy


def main():

    # --------------------------------------------------
    # Load raw price data
    # --------------------------------------------------

    data_file = PARQUET_DIR / f"{SYMBOL}_{TIMEFRAME}.parquet"

    df = pd.read_parquet(data_file)

    # ------------------------------------------
    # Select backtest period
    # ------------------------------------------

    df = df[
        (df["open_time"] >= TRAIN_START)
        & (df["open_time"] <= TRAIN_END)
    ].reset_index(drop=True)

    # --------------------------------------------------
    # Strategy
    # --------------------------------------------------

    strategy = BreakoutStrategy(
        lookback=20
    )

    df = strategy.prepare_data(df)

    # --------------------------------------------------
    # Backtest
    # --------------------------------------------------

    engine = BacktestEngine(
        strategy=strategy,
        initial_capital=INITIAL_CAPITAL,
        commission=COMMISSION,
        slippage=SLIPPAGE,
    )

    trades = engine.run(df)

    # --------------------------------------------------
    # Report
    # --------------------------------------------------

    report(
        trades,
        INITIAL_CAPITAL,
    )


if __name__ == "__main__":
    main()