"""
breakout.py

20-period Donchian breakout strategy.
"""

import pandas as pd

from src.strategies.base import BaseStrategy


class BreakoutStrategy(BaseStrategy):

    def __init__(
        self,
        lookback: int = 20,
        atr_period: int = 14,
        atr_multiple: float = 2.0,
        risk_per_trade: float = 0.01,
    ):
        self.lookback = lookback
        self.atr_period = atr_period
        self.atr_multiple = atr_multiple
        self.risk_per_trade = risk_per_trade

    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        # Donchian
        df["hh"] = df["high"].rolling(self.lookback).max()
        df["ll"] = df["low"].rolling(self.lookback).min()

        df["prev_hh"] = df["hh"].shift(1)
        df["prev_ll"] = df["ll"].shift(1)

        # ATR
        prev_close = df["close"].shift(1)

        tr = pd.concat(
            [
                df["high"] - df["low"],
                (df["high"] - prev_close).abs(),
                (df["low"] - prev_close).abs(),
            ],
            axis=1,
        ).max(axis=1)

        df["atr"] = tr.rolling(self.atr_period).mean()

        # Signals
        df["long_signal"] = df["close"] > df["prev_hh"]
        df["short_signal"] = df["close"] < df["prev_ll"]

        return df

    def entry_signal(self, row) -> bool:
        return bool(row["long_signal"])

    def exit_signal(self, row) -> bool:
        return bool(row["short_signal"])