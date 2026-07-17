"""
breakout.py

Breakout trading strategy.

This strategy is responsible for:
1. Computing its own indicators.
2. Generating entry/exit signals.
3. Returning an enriched DataFrame.

The backtest engine should know nothing about how the
signals are created.
"""

import pandas as pd

from src.strategies.base import BaseStrategy


class BreakoutStrategy(BaseStrategy):
    """
    20-bar breakout strategy.

    Entry:
        Close > previous 20-bar highest high.

    Exit:
        Close < previous 20-bar lowest low.
    """

    def __init__(self, lookback=20):
        self.lookback = lookback

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate indicators and trading signals.

        Parameters
        ----------
        df : pandas.DataFrame

        Returns
        -------
        pandas.DataFrame
        """

        df = df.copy()

        # -------------------------
        # Indicators
        # -------------------------

        df["hh"] = df["high"].rolling(self.lookback).max()
        df["ll"] = df["low"].rolling(self.lookback).min()

        df["prev_hh"] = df["hh"].shift(1)
        df["prev_ll"] = df["ll"].shift(1)

        # -------------------------
        # Signals
        # -------------------------

        df["long_signal"] = df["close"] > df["prev_hh"]
        df["short_signal"] = df["close"] < df["prev_ll"]

        return df