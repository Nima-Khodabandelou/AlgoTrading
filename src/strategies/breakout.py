"""
breakout.py

20-period Donchian breakout strategy.

Rules
-----
Entry
    Close > previous 20-bar highest high

Exit
    Close < previous 20-bar lowest low

The strategy computes all required indicators itself.
"""

import pandas as pd

from src.strategies.base import BaseStrategy


class BreakoutStrategy(BaseStrategy):

    def __init__(self, lookback: int = 20):
        self.lookback = lookback

    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute indicators and trading signals.
        """

        df = df.copy()

        # -----------------------------
        # Donchian Channel
        # -----------------------------
        df["hh"] = (
            df["high"]
            .rolling(self.lookback)
            .max()
        )

        df["ll"] = (
            df["low"]
            .rolling(self.lookback)
            .min()
        )

        # Previous values (avoid look-ahead bias)
        df["prev_hh"] = df["hh"].shift(1)
        df["prev_ll"] = df["ll"].shift(1)

        # Signals
        df["long_signal"] = (
            df["close"] > df["prev_hh"]
        )

        df["short_signal"] = (
            df["close"] < df["prev_ll"]
        )

        return df

    def entry_signal(self, row: pd.Series) -> bool:
        return bool(row["long_signal"])

    def exit_signal(self, row: pd.Series) -> bool:
        return bool(row["short_signal"])