"""
portfolio.py
============

Portfolio management.

Responsibilities
----------------
- Track available capital
- Track open position
- Calculate PnL
- Store trade history

The backtest engine should not modify capital directly.
Everything goes through Portfolio.
"""

from __future__ import annotations

import pandas as pd


class Portfolio:
    """
    Represents one trading account.
    """

    def __init__(self, initial_capital: float):

        self.initial_capital = initial_capital
        self.capital = initial_capital

        self.position = False
        self.units = 0.0

        self.entry_price = None
        self.entry_time = None

        self.trades = []

    # ---------------------------------------------------------
    # Entry
    # ---------------------------------------------------------

    def buy(self, price, time):

        if self.position:
            return

        self.units = self.capital / price

        self.entry_price = price
        self.entry_time = time

        self.position = True

    # ---------------------------------------------------------
    # Exit
    # ---------------------------------------------------------

    def sell(self, price, time):

        if not self.position:
            return

        pnl = self.units * (price - self.entry_price)

        self.capital += pnl

        self.trades.append(
            {
                "entry_time": self.entry_time,
                "exit_time": time,
                "entry_price": self.entry_price,
                "exit_price": price,
                "pnl": pnl,
                "capital": self.capital,
            }
        )

        self.position = False
        self.units = 0.0
        self.entry_price = None
        self.entry_time = None

    # ---------------------------------------------------------

    def close_final(self, price, time):

        if self.position:
            self.sell(price, time)

    # ---------------------------------------------------------

    def trade_log(self):

        return pd.DataFrame(self.trades)