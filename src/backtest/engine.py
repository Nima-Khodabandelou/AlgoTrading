"""
engine.py

Purpose
-------
Executes an event-driven backtest.

Current assumptions
-------------------
- Long only
- One position at a time
- Enter on next bar open
- Exit on next bar open
- Invest 100% of available capital

Future improvements
-------------------
- Short selling
- Commission
- Slippage
- Position sizing
- Stop-loss
- Take-profit
"""

import pandas as pd

from .portfolio import Portfolio


class BacktestEngine:

    def __init__(self, initial_capital=10_000):

        self.portfolio = Portfolio(
            initial_capital=initial_capital,
            capital=initial_capital,
        )

    def run(self, df):

        trades = []

        p = self.portfolio

        for i in range(len(df) - 1):

            row = df.iloc[i]

            next_open = df.iloc[i + 1]["open"]
            next_time = df.iloc[i + 1]["open_time"]

            # Entry
            if (not p.position) and row["long_signal"]:

                p.entry_price = next_open
                p.entry_time = next_time
                p.units = p.capital / p.entry_price
                p.position = True

            # Exit
            elif p.position and row["short_signal"]:

                exit_price = next_open
                exit_time = next_time

                pnl = p.units * (exit_price - p.entry_price)

                p.capital += pnl

                trades.append(
                    {
                        "entry_time": p.entry_time,
                        "exit_time": exit_time,
                        "entry_price": p.entry_price,
                        "exit_price": exit_price,
                        "pnl": pnl,
                        "capital": p.capital,
                    }
                )

                p.position = False
                p.units = 0.0

        if p.position:

            exit_price = df.iloc[-1]["close"]
            exit_time = df.iloc[-1]["open_time"]

            pnl = p.units * (exit_price - p.entry_price)

            p.capital += pnl

            trades.append(
                {
                    "entry_time": p.entry_time,
                    "exit_time": exit_time,
                    "entry_price": p.entry_price,
                    "exit_price": exit_price,
                    "pnl": pnl,
                    "capital": p.capital,
                }
            )

        return pd.DataFrame(trades)