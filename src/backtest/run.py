"""
run.py

Purpose
-------
Main entry point for running a backtest.

Responsibilities
----------------
1. Load trading signals.
2. Instantiate the selected strategy.
3. Create the backtesting engine.
4. Execute the backtest.
5. Print trade log.
6. Print performance report.

This file should remain very small. It simply orchestrates the workflow.
The trading logic belongs in strategies/.
The execution logic belongs in engine.py.
The reporting logic belongs in metrics.py.
"""

from pathlib import Path

import pandas as pd

from src.config.settings import (
    SIGNALS_DIR,
    SYMBOL,
    TIMEFRAME,
    INITIAL_CAPITAL,
)

from src.strategies.breakout import BreakoutStrategy
from src.backtest.engine import BacktestEngine
from src.backtest.metrics import report


def main():
    """
    Run the complete backtest.
    """

    signal_file = (
        SIGNALS_DIR /
        f"{SYMBOL}_{TIMEFRAME}_breakout.parquet"
    )

    df = pd.read_parquet(signal_file)

    strategy = BreakoutStrategy()

    engine = BacktestEngine(
        strategy=strategy,
        initial_capital=INITIAL_CAPITAL,
    )

    trades = engine.run(df)

    print()
    print("=" * 10, "TRADE LOG", "=" * 10)
    print(trades)

    print()

    report(
        trades=trades,
        initial_capital=INITIAL_CAPITAL,
    )


if __name__ == "__main__":
    main()